#!/usr/bin/env python3
"""
Daemon Manager for Time Machine Backup (AppImage compatible)
Handles starting, stopping, and autostart of the backup daemon
"""

import os
import sys
import time
import json
import signal
import subprocess
import shutil
import hashlib
from pathlib import Path
from configparser import ConfigParser
import platform

class DaemonManager:
    def __init__(self):
        self.is_appimage = 'APPIMAGE' in os.environ
        self.appimage_path = os.environ.get('APPIMAGE')
        self.config_path = self.get_config_path()
        self.config = self.load_config()
        
        # Use XDG_DATA_HOME or ~/.local/share/timemachine for PID file
        data_home = os.environ.get('XDG_DATA_HOME', os.path.expanduser('~/.local/share'))
        self.data_dir = os.path.join(data_home, 'timemachine')
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Use config PID file or default to data directory
        config_pid_file = self.config.get('AUTOSTART', 'daemon_pid_file', 
                                         fallback='~/.local/share/timemachine/daemon.pid')
        self.pid_file = os.path.expanduser(config_pid_file)
        
        # Ensure PID file directory exists
        pid_dir = os.path.dirname(self.pid_file)
        if pid_dir:
            os.makedirs(pid_dir, exist_ok=True)
        
    def get_config_path(self):
        """Get the configuration file path"""
        # Use XDG_CONFIG_HOME or ~/.config/timemachine
        config_home = os.environ.get('XDG_CONFIG_HOME', os.path.expanduser('~/.config'))
        config_dir = os.path.join(config_home, 'timemachine')
        os.makedirs(config_dir, exist_ok=True)
        return os.path.join(config_dir, 'config.conf')
    
    def load_config(self):
        """Load configuration from file"""
        config = ConfigParser()
        if os.path.exists(self.config_path):
            config.read(self.config_path)
        else:
            # Create default sections
            config['AUTOSTART'] = {
                'autostart_daemon': 'false',
                'daemon_pid_file': os.path.join(self.data_dir, 'daemon.pid')
            }
        return config
    
    def save_config(self):
        """Save configuration to file"""
        with open(self.config_path, 'w') as f:
            self.config.write(f)
    
    def get_daemon_pid(self):
        """Get the PID of the running daemon"""
        if os.path.exists(self.pid_file):
            try:
                with open(self.pid_file, 'r') as f:
                    content = f.read().strip()
                    if not content:
                        return None
                    pid = int(content)
                    
                    # Verify PID file is not stale
                    if self.is_daemon_running(pid):
                        return pid
                    else:
                        # Clean up stale PID file
                        os.remove(self.pid_file)
                        return None
            except (ValueError, OSError):
                # Invalid PID file, clean it up
                try:
                    os.remove(self.pid_file)
                except:
                    pass
                return None
        return None
    
    def is_daemon_running(self, pid=None):
        """Check if daemon is running"""
        if pid is None:
            pid = self.get_daemon_pid()
        
        if pid is None:
            return False
        
        try:
            # Try to send signal 0 to check if process exists
            os.kill(pid, 0)
            
            # Additional check: verify it's our daemon process
            # Check process name or command line
            try:
                if platform.system() == 'Linux':
                    cmdline_file = f'/proc/{pid}/cmdline'
                    if os.path.exists(cmdline_file):
                        with open(cmdline_file, 'rb') as f:
                            cmdline = f.read().decode('utf-8', errors='ignore')
                        if 'daemon.py' in cmdline or 'timemachine' in cmdline.lower():
                            return True
                        else:
                            # PID reused by another process
                            os.remove(self.pid_file)
                            return False
            except:
                pass
            
            return True
        except (OSError, ProcessLookupError):
            return False
    
    def start_daemon(self, background=True):
        """Start the backup daemon"""
        # Check if already running
        pid = self.get_daemon_pid()
        if self.is_daemon_running(pid):
            return {'success': False, 'message': 'Daemon is already running', 'pid': pid}
        
        try:
            # Get daemon script path
            daemon_script = self.get_daemon_script_path()
            if not daemon_script or not os.path.exists(daemon_script):
                return {'success': False, 'message': 'Daemon script not found'}
            
            if background:
                # Start in background
                cmd = [sys.executable, daemon_script]
                
                # Platform-specific handling
                if platform.system() == 'Windows':
                    # On Windows
                    startupinfo = subprocess.STARTUPINFO()
                    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                    process = subprocess.Popen(
                        cmd,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        startupinfo=startupinfo,
                        creationflags=subprocess.CREATE_NO_WINDOW
                    )
                else:
                    # On Unix-like systems
                    process = subprocess.Popen(
                        cmd,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        start_new_session=True
                    )
                
                # Save PID to file
                with open(self.pid_file, 'w') as f:
                    f.write(str(process.pid))
                
                # Also save daemon info for verification
                daemon_info = {
                    'pid': process.pid,
                    'start_time': time.time(),
                    'appimage_path': self.appimage_path if self.is_appimage else None,
                    'daemon_script': daemon_script
                }
                
                info_file = self.pid_file.replace('.pid', '.info')
                with open(info_file, 'w') as f:
                    json.dump(daemon_info, f)
                
                # Wait a moment to see if it starts successfully
                time.sleep(2)
                
                if process.poll() is not None:
                    # Process exited immediately
                    stdout, stderr = process.communicate()
                    error_msg = stderr.decode('utf-8', errors='ignore') if stderr else 'Unknown error'
                    
                    # Clean up PID files
                    if os.path.exists(self.pid_file):
                        os.remove(self.pid_file)
                    info_file = self.pid_file.replace('.pid', '.info')
                    if os.path.exists(info_file):
                        os.remove(info_file)
                    
                    return {'success': False, 'message': f'Daemon failed to start: {error_msg}'}
                
                return {'success': True, 'message': 'Daemon started successfully', 'pid': process.pid}
            
            else:
                # Start in foreground (for debugging)
                subprocess.run([sys.executable, daemon_script], check=True)
                return {'success': True, 'message': 'Daemon started in foreground'}
                
        except Exception as e:
            # Clean up PID file on error
            if os.path.exists(self.pid_file):
                os.remove(self.pid_file)
            info_file = self.pid_file.replace('.pid', '.info')
            if os.path.exists(info_file):
                os.remove(info_file)
            
            return {'success': False, 'message': f'Failed to start daemon: {str(e)}'}
    
    def get_daemon_script_path(self):
        """Get the path to daemon.py"""
        if self.is_appimage:
            # For AppImage, use cached version
            return self.get_cached_daemon_script()
        else:
            # For regular installation
            script_dir = os.path.dirname(os.path.abspath(__file__))
            daemon_path = os.path.join(script_dir, 'daemon.py')
            if os.path.exists(daemon_path):
                return daemon_path
        
        # Try to find daemon.py in current directory
        if os.path.exists('daemon.py'):
            return 'daemon.py'
        
        return None
    
    def get_cached_daemon_script(self):
        """Get daemon.py from AppImage cache"""
        # Create cache directory
        cache_dir = os.path.join(self.data_dir, 'cache')
        os.makedirs(cache_dir, exist_ok=True)
        
        # Generate cache filename based on AppImage hash
        appimage_hash = self.get_appimage_hash()
        cache_file = os.path.join(cache_dir, f'daemon_{appimage_hash}.py')
        
        # Check if cache is valid
        if os.path.exists(cache_file):
            # Check if AppImage is newer than cache
            appimage_mtime = os.path.getmtime(self.appimage_path)
            cache_mtime = os.path.getmtime(cache_file)
            
            if appimage_mtime <= cache_mtime:
                return cache_file
        
        # Extract daemon.py from AppImage
        return self.extract_daemon_from_appimage(cache_file)
    
    def get_appimage_hash(self):
        """Get hash of AppImage for cache naming"""
        try:
            with open(self.appimage_path, 'rb') as f:
                # Read first 1MB for hash (enough for uniqueness)
                data = f.read(1024 * 1024)
                return hashlib.md5(data).hexdigest()[:16]
        except:
            # Fallback to filename hash
            return hashlib.md5(self.appimage_path.encode()).hexdigest()[:16]
    
    def extract_daemon_from_appimage(self, cache_file):
        """Extract daemon.py from AppImage to cache"""
        try:
            # Try using unsquashfs if available
            if shutil.which('unsquashfs'):
                result = subprocess.run(
                    ['unsquashfs', '-f', '-o', self.appimage_path, 'daemon.py'],
                    capture_output=True,
                    text=True,
                    cwd=os.path.dirname(cache_file)
                )
                
                if result.returncode == 0:
                    extracted = os.path.join(os.path.dirname(cache_file), 'squashfs-root', 'daemon.py')
                    if os.path.exists(extracted):
                        shutil.copy(extracted, cache_file)
                        shutil.rmtree(os.path.join(os.path.dirname(cache_file), 'squashfs-root'))
                        return cache_file
            
            # Fallback: run AppImage with --appimage-extract
            temp_dir = os.path.join(self.data_dir, 'temp_extract')
            os.makedirs(temp_dir, exist_ok=True)
            
            result = subprocess.run(
                [self.appimage_path, '--appimage-extract'],
                cwd=temp_dir,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                extracted = os.path.join(temp_dir, 'squashfs-root', 'daemon.py')
                if os.path.exists(extracted):
                    shutil.copy(extracted, cache_file)
                    shutil.rmtree(temp_dir)
                    return cache_file
            
            return None
            
        except Exception as e:
            print(f"Error extracting daemon: {e}")
            return None
    
    def stop_daemon(self):
        """Stop the running daemon"""
        pid = self.get_daemon_pid()
        
        if not self.is_daemon_running(pid):
            return {'success': False, 'message': 'Daemon is not running'}
        
        try:
            # Try graceful shutdown first
            os.kill(pid, signal.SIGTERM)
            
            # Wait for process to exit
            for _ in range(10):  # Wait up to 5 seconds
                time.sleep(0.5)
                if not self.is_daemon_running(pid):
                    break
            
            # Force kill if still running
            if self.is_daemon_running(pid):
                os.kill(pid, signal.SIGKILL)
                time.sleep(1)
            
            # Clean up PID and info files
            self.cleanup_daemon_files()
            
            return {'success': True, 'message': 'Daemon stopped successfully'}
            
        except Exception as e:
            return {'success': False, 'message': f'Failed to stop daemon: {str(e)}'}
    
    def cleanup_daemon_files(self):
        """Clean up daemon PID and info files"""
        if os.path.exists(self.pid_file):
            os.remove(self.pid_file)
        
        info_file = self.pid_file.replace('.pid', '.info')
        if os.path.exists(info_file):
            os.remove(info_file)
    
    def restart_daemon(self):
        """Restart the daemon"""
        stop_result = self.stop_daemon()
        if not stop_result['success']:
            return stop_result
        
        time.sleep(1)  # Brief pause before restart
        return self.start_daemon()
    
    def get_daemon_status(self):
        """Get current daemon status"""
        pid = self.get_daemon_pid()
        is_running = self.is_daemon_running(pid)
        
        return {
            'success': True,
            'running': is_running,
            'pid': pid if is_running else None,
            'autostart_enabled': self.config.getboolean('AUTOSTART', 'autostart_daemon', fallback=False),
            'pid_file': self.pid_file
        }
    
    def set_autostart(self, enable=True):
        """Enable or disable autostart"""
        # Update config
        if 'AUTOSTART' not in self.config:
            self.config['AUTOSTART'] = {}
        
        self.config['AUTOSTART']['autostart_daemon'] = str(enable).lower()
        self.save_config()
        
        # Setup autostart if enabled
        if enable:
            return self.setup_autostart()
        else:
            return self.remove_autostart()
    
    def setup_autostart(self):
        """Setup autostart for AppImage"""
        system = platform.system()
        
        try:
            if system == 'Linux':
                return self.setup_linux_autostart()
            elif system == 'Darwin':  # macOS
                return self.setup_macos_autostart()
            elif system == 'Windows':
                return self.setup_windows_autostart()
            else:
                return {'success': False, 'message': f'Unsupported platform: {system}'}
                
        except Exception as e:
            return {'success': False, 'message': f'Failed to setup autostart: {str(e)}'}
    
    def setup_linux_autostart(self):
        """Setup autostart on Linux for AppImage"""
        # Use XDG autostart directory
        autostart_dir = os.path.expanduser('~/.config/autostart')
        os.makedirs(autostart_dir, exist_ok=True)
        
        desktop_file = os.path.join(autostart_dir, 'timemachine-daemon.desktop')
        
        # Create a wrapper script to start the daemon
        wrapper_script = os.path.join(self.data_dir, 'start_daemon.sh')
        with open(wrapper_script, 'w') as f:
            f.write(f"""#!/bin/bash
# Time Machine Daemon Autostart Wrapper
export APPDATA="{self.data_dir}"
export APPIMAGE="{self.appimage_path}"
cd "{os.path.dirname(self.appimage_path)}"
"{self.appimage_path}" --daemon-autostart
""")
        
        # Make wrapper executable
        os.chmod(wrapper_script, 0o755)
        
        # Create desktop entry
        desktop_content = f"""[Desktop Entry]
Type=Application
Name=Time Machine Daemon
Comment=Start Time Machine Backup Daemon
Exec={wrapper_script}
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
"""
        
        with open(desktop_file, 'w') as f:
            f.write(desktop_content)
        
        return {'success': True, 'message': 'Autostart configured for Linux'}
    
    def setup_macos_autostart(self):
        """Setup autostart on macOS for AppImage"""
        # macOS uses LaunchAgents
        launch_agents_dir = os.path.expanduser('~/Library/LaunchAgents')
        os.makedirs(launch_agents_dir, exist_ok=True)
        
        plist_file = os.path.join(launch_agents_dir, 'com.timemachine.daemon.plist')
        
        plist_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.timemachine.daemon</string>
    <key>ProgramArguments</key>
    <array>
        <string>{self.appimage_path}</string>
        <string>--daemon-autostart</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>{self.data_dir}/daemon.log</string>
    <key>StandardErrorPath</key>
    <string>{self.data_dir}/daemon_error.log</string>
</dict>
</plist>
"""
        
        with open(plist_file, 'w') as f:
            f.write(plist_content)
        
        # Load the launch agent
        subprocess.run(['launchctl', 'load', plist_file])
        
        return {'success': True, 'message': 'Autostart configured for macOS'}
    
    def setup_windows_autostart(self):
        """Setup autostart on Windows for AppImage (converted to EXE)"""
        # Windows startup folder
        startup_dir = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
        os.makedirs(startup_dir, exist_ok=True)
        
        # Create a batch file to start the daemon
        batch_file = os.path.join(startup_dir, 'TimeMachineDaemon.bat')
        
        batch_content = f"""@echo off
start /B "{self.appimage_path}" --daemon-autostart
"""
        
        with open(batch_file, 'w') as f:
            f.write(batch_content)
        
        return {'success': True, 'message': 'Autostart configured for Windows'}
    
    def remove_autostart(self):
        """Remove autostart configuration"""
        system = platform.system()
        
        try:
            if system == 'Linux':
                desktop_file = os.path.expanduser('~/.config/autostart/timemachine-daemon.desktop')
                if os.path.exists(desktop_file):
                    os.remove(desktop_file)
                
                wrapper_script = os.path.join(self.data_dir, 'start_daemon.sh')
                if os.path.exists(wrapper_script):
                    os.remove(wrapper_script)
                    
            elif system == 'Darwin':
                plist_file = os.path.expanduser('~/Library/LaunchAgents/com.timemachine.daemon.plist')
                if os.path.exists(plist_file):
                    subprocess.run(['launchctl', 'unload', plist_file])
                    os.remove(plist_file)
                    
            elif system == 'Windows':
                batch_file = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup', 'TimeMachineDaemon.bat')
                if os.path.exists(batch_file):
                    os.remove(batch_file)
            
            return {'success': True, 'message': 'Autostart removed'}
            
        except Exception as e:
            return {'success': False, 'message': f'Failed to remove autostart: {str(e)}'}


if __name__ == '__main__':
    # Command line interface
    import argparse
    
    parser = argparse.ArgumentParser(description='Time Machine Daemon Manager')
    parser.add_argument('action', choices=['start', 'stop', 'restart', 'status', 'autostart', 'enable-autostart', 'disable-autostart'],
                       help='Action to perform')
    parser.add_argument('--foreground', action='store_true', help='Run in foreground (for start action)')
    
    args = parser.parse_args()
    
    manager = DaemonManager()
    
    if args.action == 'start':
        result = manager.start_daemon(background=not args.foreground)
    elif args.action == 'stop':
        result = manager.stop_daemon()
    elif args.action == 'restart':
        result = manager.restart_daemon()
    elif args.action == 'status':
        result = manager.get_daemon_status()
    elif args.action == 'autostart':
        result = {'autostart': manager.config.getboolean('AUTOSTART', 'autostart_daemon', fallback=False)}
    elif args.action == 'enable-autostart':
        result = manager.set_autostart(True)
    elif args.action == 'disable-autostart':
        result = manager.set_autostart(False)
    else:
        result = {'success': False, 'message': 'Unknown action'}
    
    print(json.dumps(result, indent=2))
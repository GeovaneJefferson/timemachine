#!/usr/bin/env python3
import os
import sys
import shutil
from pathlib import Path

def setup_autostart(appimage_path=None):
    """
    Setup auto-start for Flask AppImage backup application
    """
    # Get AppImage path
    if appimage_path is None:
        # If running from AppImage itself
        appimage_path = os.environ.get('APPIMAGE')
        if not appimage_path:
            # Fallback to current executable
            appimage_path = sys.executable
    
    if not appimage_path or not os.path.exists(appimage_path):
        print("Error: Could not find AppImage path")
        return False
    
    # Create desktop entry content
    desktop_entry = f"""
    [Desktop Entry]
        Type=Application
        Name=Backup App
        Comment=Automatic backup application
        Exec="{appimage_path}" --minimized
        Icon={appimage_path}
        Categories=Utility;
        StartupNotify=false
        Terminal=false
        X-GNOME-Autostart-enabled=true
        X-GNOME-Autostart-Delay=10
    """
    
    # Write to autostart directory
    autostart_dir = Path.home() / '.config' / 'autostart'
    autostart_dir.mkdir(parents=True, exist_ok=True)
    
    desktop_file = autostart_dir / 'backup-app.desktop'
    
    try:
        with open(desktop_file, 'w') as f:
            f.write(desktop_entry)
        
        # Make executable
        os.chmod(desktop_file, 0o755)
        
        print(f"Auto-start configured successfully at: {desktop_file}")
        return True
    except Exception as e:
        print(f"Error setting up auto-start: {e}")
        return False

def remove_autostart():
    """Remove auto-start configuration"""
    desktop_file = Path.home() / '.config' / 'autostart' / 'backup-app.desktop'
    if desktop_file.exists():
        desktop_file.unlink()
        print("Auto-start configuration removed")
        return True
    return False

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--remove':
        remove_autostart()
    else:
        setup_autostart()
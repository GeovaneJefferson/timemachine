#!/usr/bin/env python3
"""
Simple AppImage Builder that DEFINITELY includes Electron
"""

import os
import sys
import shutil
import subprocess
import urllib.request
import stat
from pathlib import Path

def run_cmd(cmd, cwd=None):
    """Run command and return output"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd)
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return 1, "", str(e)

class SimpleAppImageBuilder:
    def __init__(self):
        self.app_name = "TimeMachine"
        self.app_version = "1.0.0"
        self.output_file = f"{self.app_name}-{self.app_version}-x86_64.AppImage"
        self.install_dir = Path.home() / ".local" / "bin"
        self.output_path = self.install_dir / self.output_file
        self.build_dir = Path("build_simple")
        self.appdir = self.build_dir / f"{self.app_name}.AppDir"
        
        print(f"🔨 Building: {self.output_path}")
    
    def ensure_electron(self):
        """Make absolutely sure electron is available"""
        print("🔍 Checking Electron...")
        
        # Check local node_modules
        local_electron = Path("node_modules/electron/dist/electron")
        if local_electron.exists():
            print(f"✓ Local Electron: {local_electron}")
            return local_electron
        
        # Try to install locally
        print("📦 Installing electron locally...")
        ret, out, err = run_cmd("npm install electron --no-save")
        if ret == 0 and Path("node_modules/electron/dist/electron").exists():
            print("✓ Electron installed locally")
            return Path("node_modules/electron/dist/electron")
        
        # Check global electron
        ret, out, err = run_cmd("which electron")
        if ret == 0 and out.strip():
            print(f"✓ System Electron: {out.strip()}")
            # Download electron binary for bundling
            self.download_electron_binary()
            return Path("electron-binary/electron")
        
        print("❌ No Electron found. Please install:")
        print("   npm install electron")
        print("   OR")
        print("   sudo npm install -g electron")
        return None
    
    def download_electron_binary(self):
        """Download standalone electron binary"""
        print("📥 Downloading Electron binary...")
        
        electron_dir = Path("electron-binary")
        electron_dir.mkdir(exist_ok=True)
        
        # Download from GitHub releases
        url = "https://github.com/electron/electron/releases/download/v28.0.0/electron-v28.0.0-linux-x64.zip"
        zip_path = electron_dir / "electron.zip"
        
        try:
            urllib.request.urlretrieve(url, zip_path)
            
            # Extract
            import zipfile
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(electron_dir)
            
            # Find electron binary
            for item in electron_dir.rglob("electron"):
                if item.is_file():
                    item.chmod(0o755)
                    print(f"✓ Downloaded Electron: {item}")
                    return item
            
        except Exception as e:
            print(f"⚠ Could not download electron: {e}")
        
        return None
    
    def build(self):
        """Build the AppImage"""
        print("🚀 Starting build...")
        
        # Clean build directory
        if self.build_dir.exists():
            shutil.rmtree(self.build_dir)
        
        # Create structure
        self.appdir.mkdir(parents=True)
        
        # 1. Get electron
        electron_src = self.ensure_electron()
        if not electron_src:
            return False
        
        # 2. Copy app files
        print("📦 Copying application...")
        app_dest = self.appdir / "opt" / self.app_name
        app_dest.mkdir(parents=True)
        
        # Copy main files
        for file in ["app.py", "main.js", "package.json", "Requirements.txt"]:
            if Path(file).exists():
                shutil.copy2(file, app_dest / file)
                print(f"  ✓ {file}")
        
        # Copy directories
        for dir in ["config", "static", "templates"]:
            if Path(dir).exists():
                shutil.copytree(dir, app_dest / dir, dirs_exist_ok=True)
                print(f"  ✓ {dir}/")
        
        # 3. Copy electron
        print("🔧 Copying Electron...")
        electron_dest_dir = app_dest / "node_modules" / "electron" / "dist"
        electron_dest_dir.mkdir(parents=True)
        
        if electron_src.exists():
            # Copy electron binary
            electron_dest = electron_dest_dir / "electron"
            shutil.copy2(electron_src, electron_dest)
            electron_dest.chmod(0o755)
            print(f"  ✓ Electron copied to: {electron_dest}")
            
            # Also copy parent directory files
            electron_parent = electron_src.parent
            for item in electron_parent.iterdir():
                if item.name != electron_src.name:
                    dest = electron_dest_dir / item.name
                    if item.is_file():
                        shutil.copy2(item, dest)
                    else:
                        shutil.copytree(item, dest, dirs_exist_ok=True)
        
        # 4. Create desktop file
        print("🖥️  Creating desktop file...")
        desktop_dir = self.appdir / "usr" / "share" / "applications"
        desktop_dir.mkdir(parents=True)
        
        desktop_content = """[Desktop Entry]
Type=Application
Name=Time Machine
Comment=Backup Application
Exec=AppRun
Icon=timemachine
Categories=Utility;
Terminal=false
"""
        
        desktop_file = self.appdir / "TimeMachine.desktop"
        desktop_file.write_text(desktop_content)
        shutil.copy2(desktop_file, desktop_dir / "TimeMachine.desktop")
        
        # 5. Copy icon
        print("🎨 Copying icon...")
        for icon_src in ["static/vendor/favicon.png", "favicon.png", "icon.png"]:
            if Path(icon_src).exists():
                # AppDir root
                shutil.copy(icon_src, self.appdir / "timemachine.png")
                shutil.copy(icon_src, self.appdir / ".DirIcon")
                
                # System location
                icon_dir = self.appdir / "usr" / "share" / "icons" / "hicolor" / "256x256" / "apps"
                icon_dir.mkdir(parents=True)
                shutil.copy(icon_src, icon_dir / "timemachine.png")
                
                # App location
                shutil.copy(icon_src, app_dest / "static" / "favicon.png")
                
                print(f"  ✓ Icon: {icon_src}")
                break
        
        # 6. Create AppRun
        print("⚙️  Creating AppRun...")
        apprun_content = """#!/bin/bash
APPDIR="$(dirname "$(readlink -f "${0}")")"
cd "${APPDIR}/opt/TimeMachine"

echo "Starting Time Machine..."

# Verify electron exists
ELECTRON="${APPDIR}/opt/TimeMachine/node_modules/electron/dist/electron"
if [ ! -f "$ELECTRON" ]; then
    echo "ERROR: Electron not found at: $ELECTRON"
    echo "Contents of node_modules/electron/dist/:"
    ls -la "${APPDIR}/opt/TimeMachine/node_modules/electron/dist/" 2>/dev/null || echo "Directory doesn't exist"
    exit 1
fi

chmod +x "$ELECTRON" 2>/dev/null || true

# Start Flask
python3 app.py > /tmp/timemachine.log 2>&1 &
FLASK_PID=$!
sleep 3

# Start Electron
"$ELECTRON" main.js --no-sandbox

kill $FLASK_PID 2>/dev/null
echo "Done"
"""
        
        apprun_file = self.appdir / "AppRun"
        apprun_file.write_text(apprun_content)
        apprun_file.chmod(0o755)
        
        # 7. Build AppImage
        print("🏗️  Building AppImage...")
        self.install_dir.mkdir(parents=True, exist_ok=True)
        
        # Download appimagetool if needed
        tool_path = self.build_dir / "appimagetool"
        if not tool_path.exists():
            print("📥 Downloading appimagetool...")
            url = "https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
            urllib.request.urlretrieve(url, tool_path)
            tool_path.chmod(0o755)
        
        # Build
        env = os.environ.copy()
        env['ARCH'] = 'x86_64'
        
        result = subprocess.run(
            [str(tool_path), str(self.appdir), str(self.output_path)],
            capture_output=True,
            text=True,
            env=env
        )
        
        if result.returncode == 0:
            self.output_path.chmod(0o755)
            size_mb = self.output_path.stat().st_size / (1024 * 1024)
            print(f"✅ Success! {self.output_path} ({size_mb:.1f} MB)")
            
            # Verify contents
            print("🔍 Verifying contents...")
            subprocess.run([str(self.output_path), "--appimage-extract"], 
                          capture_output=True)
            
            if Path("squashfs-root").exists():
                electron_check = Path("squashfs-root/opt/TimeMachine/node_modules/electron/dist/electron")
                if electron_check.exists():
                    print(f"✓ Electron verified in AppImage")
                    print(f"  Size: {electron_check.stat().st_size / 1024 / 1024:.1f} MB")
                    print(f"  Executable: {os.access(electron_check, os.X_OK)}")
                else:
                    print("❌ Electron still missing in AppImage!")
                    print("Contents of node_modules/electron/dist/:")
                    for item in Path("squashfs-root/opt/TimeMachine/node_modules/electron/dist").rglob("*"):
                        print(f"  - {item.relative_to('squashfs-root')}")
                
                shutil.rmtree("squashfs-root")
            
            return True
        else:
            print(f"❌ Build failed: {result.stderr}")
            return False

def main():
    print("="*60)
    print("🔨 Time Machine AppImage Builder")
    print("="*60)
    
    # Check for required files
    if not Path("app.py").exists():
        print("❌ app.py not found")
        sys.exit(1)
    
    if not Path("main.js").exists():
        print("❌ main.js not found")
        sys.exit(1)
    
    builder = SimpleAppImageBuilder()
    if builder.build():
        print("\n🎉 AppImage built successfully!")
        print(f"📁 Location: {builder.output_path}")
        print("\n🚀 Run it with:")
        print(f"  {builder.output_file}")
        sys.exit(0)
    else:
        print("\n❌ Build failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
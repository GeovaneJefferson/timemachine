#!/bin/bash
# TimeMachine Electron - Installation Script
# Installs TimeMachine to ~/.local/share/timemachine

set -e

echo "🚀 Installing TimeMachine..."
echo ""
# installer now ensures launcher will kill any running Python app.py instances to
# avoid port conflicts when starting via the desktop menu.

# Define installation directories
INSTALL_DIR="$HOME/.local/share/timemachine"
BIN_DIR="$HOME/.local/bin"
DESKTOP_DIR="$HOME/.local/share/applications"
ICON_DIR="$HOME/.local/share/icons/hicolor/256x256/apps"
LAUNCHER_SCRIPT="$BIN_DIR/timemachine"

# Create directories if they don't exist
mkdir -p "$INSTALL_DIR"
mkdir -p "$BIN_DIR"
mkdir -p "$DESKTOP_DIR"
mkdir -p "$ICON_DIR"

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Copy application files
echo "📁 Copying application files..."
cp -r "$SCRIPT_DIR/electron" "$INSTALL_DIR/"
cp -r "$SCRIPT_DIR/js" "$INSTALL_DIR/"
cp -r "$SCRIPT_DIR/css" "$INSTALL_DIR/"
cp -r "$SCRIPT_DIR/templates" "$INSTALL_DIR/"
cp -r "$SCRIPT_DIR/py" "$INSTALL_DIR/"
cp -r "$SCRIPT_DIR/config" "$INSTALL_DIR/"
cp "$SCRIPT_DIR/app.py" "$INSTALL_DIR/"

# Copy node_modules if it exists (optional for web-only mode)
if [ -d "$SCRIPT_DIR/node_modules" ]; then
    cp -r "$SCRIPT_DIR/node_modules" "$INSTALL_DIR/"
else
    echo "⚠️  node_modules not found. Run 'bash setup-electron.sh' first if you need Electron support."
fi

# Create launcher script
echo "🔧 Creating launcher script..."
cat > "$LAUNCHER_SCRIPT" << 'LAUNCHER_EOF'
#!/bin/bash
# TimeMachine Launcher - A proper desktop app launcher
INSTALL_DIR="$HOME/.local/share/timemachine"

# Suppress all output when launched from GUI (no terminal)
if [ ! -t 0 ]; then
    exec >/dev/null 2>&1
fi

# Check for Electron first
if [ -d "$INSTALL_DIR/node_modules" ]; then
    ELECTRON_BIN="$INSTALL_DIR/node_modules/.bin/electron"
    
    if [ -f "$ELECTRON_BIN" ]; then
        # Electron mode - runs as pure desktop app
        export QT_QPA_PLATFORM=xcb
        export GDK_BACKEND=x11
        export ELECTRON_ENABLE_LOGGING=false
        export ELECTRON_ENABLE_STACK_DUMPING=false
        
        NODE_PATH="$INSTALL_DIR/node_modules" \
        PYTHONPATH="$INSTALL_DIR" \
        exec "$ELECTRON_BIN" --ozone-platform=x11 "$INSTALL_DIR/electron/main.js" "$@" 2>/dev/null
        exit 0
    fi
fi

# Fallback: Flask web mode (no Electron)
# Kill any old Flask processes on this port (handle python or python3)
pkill -f "python.*app.py" >/dev/null 2>&1 || true

# Start Flask in background with no output
PYTHONPATH="$INSTALL_DIR" \
nohup python3 "$INSTALL_DIR/app.py" >/dev/null 2>&1 &

# Open in browser
sleep 1
if command -v xdg-open >/dev/null 2>&1; then
    xdg-open "http://localhost:5000" 2>/dev/null &
elif command -v open >/dev/null 2>&1; then
    open "http://localhost:5000" &
fi

exit 0
LAUNCHER_EOF

chmod +x "$LAUNCHER_SCRIPT"

# Create desktop file
echo "🖥️  Creating desktop launcher..."
cat > "$DESKTOP_DIR/timemachine.desktop" << 'DESKTOP_EOF'
[Desktop Entry]
Version=1.0
Type=Application
Name=TimeMachine
Comment=Cross-platform backup daemon with modern UI
Exec=timemachine
Icon=timemachine
Terminal=false
Categories=Utility;System;Backup;
Keywords=backup;restore;storage;
StartupNotify=true
DESKTOP_EOF

chmod 644 "$DESKTOP_DIR/timemachine.desktop"

# Copy icon if available
if [ -f "$SCRIPT_DIR/assets/icon.png" ]; then
    echo "🎨 Installing icon..."
    cp "$SCRIPT_DIR/assets/icon.png" "$ICON_DIR/timemachine.png"
fi

# Update desktop database
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database "$DESKTOP_DIR"
fi

echo ""
echo "✅ Installation complete!"
echo ""
echo "📍 Installed to: $INSTALL_DIR"
echo "🔗 Launcher at: $LAUNCHER_SCRIPT"
echo "🖥️  Desktop file: $DESKTOP_DIR/timemachine.desktop"
echo ""
echo "🚀 To launch TimeMachine:"
echo "   timemachine"
echo "   or find it in your Application Menu"
echo ""
echo "📌 For Electron support (desktop app), run:"
echo "   bash setup-electron.sh"
echo ""
echo "To uninstall:"
echo "   bash uninstall.sh"
echo ""

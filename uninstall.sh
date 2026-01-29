#!/bin/bash
# TimeMachine Electron - Uninstallation Script
# Removes TimeMachine from ~/.local/share

set -e

echo "🗑️  Uninstalling TimeMachine..."
echo ""

# Define directories
INSTALL_DIR="$HOME/.local/share/timemachine"
BIN_DIR="$HOME/.local/bin"
DESKTOP_DIR="$HOME/.local/share/applications"
ICON_DIR="$HOME/.local/share/icons/hicolor/256x256/apps"
LAUNCHER_SCRIPT="$BIN_DIR/timemachine"

# Confirm uninstall
read -p "Are you sure you want to uninstall TimeMachine? (y/N) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cancelled."
    exit 0
fi

# Stop any running instance
if pgrep -f "electron.*timemachine" > /dev/null; then
    echo "⏹️  Stopping running TimeMachine instances..."
    pkill -f "electron.*timemachine" || true
    sleep 1
fi

# Remove installation directory
if [ -d "$INSTALL_DIR" ]; then
    echo "📁 Removing application files..."
    rm -rf "$INSTALL_DIR"
fi

# Remove old config directory
if [ -d "$HOME/.config/timemachine" ]; then
    echo "🧹 Removing old config directory..."
    rm -rf "$HOME/.config/timemachine"
fi

# Remove old electron config directory
if [ -d "$HOME/.config/TimeMachineElectron" ]; then
    echo "🧹 Removing old electron config directory..."
    rm -rf "$HOME/.config/TimeMachineElectron"
fi
# Remove launcher script
if [ -f "$LAUNCHER_SCRIPT" ]; then
    echo "🔧 Removing launcher script..."
    rm -f "$LAUNCHER_SCRIPT"
fi

# Remove desktop file
if [ -f "$DESKTOP_DIR/timemachine.desktop" ]; then
    echo "🖥️  Removing desktop launcher..."
    rm -f "$DESKTOP_DIR/timemachine.desktop"
fi

# Remove icon
if [ -f "$ICON_DIR/timemachine.png" ]; then
    echo "🎨 Removing icon..."
    rm -f "$ICON_DIR/timemachine.png"
fi

# Update desktop database
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database "$DESKTOP_DIR" 2>/dev/null || true
fi

echo ""
echo "✅ Uninstallation complete!"
echo ""
echo "Removed:"
echo "  • $INSTALL_DIR"
echo "  • $HOME/.config/timemachine"
echo "  • $LAUNCHER_SCRIPT"
echo "  • $DESKTOP_DIR/timemachine.desktop"
echo "  • $ICON_DIR/timemachine.png"
echo ""

#!/bin/bash
# uninstall.sh - Removes Time Machine

APP_NAME="Time Machine"
APPIMAGE_FILE="TimeMachine-1.0.0-x86_64.AppImage"
INSTALL_DIR="$HOME/.local/bin"
CONFIG_DIR="$HOME/.config/timemachine"  # Better name

echo "🗑️  Uninstalling $APP_NAME..."
echo "==============================="

# Remove configuration directory
if [ -e "$CONFIG_DIR" ]; then
    rm -rf "$CONFIG_DIR"
    echo "✅ Removed configuration directory: $CONFIG_DIR"
else
    echo "ℹ️  No configuration directory found at $CONFIG_DIR"
fi

# Remove AppImage
if [ -f "$INSTALL_DIR/$APPIMAGE_FILE" ]; then
    rm -f "$INSTALL_DIR/$APPIMAGE_FILE"
    echo "✅ Removed: $INSTALL_DIR/$APPIMAGE_FILE"
else
    echo "ℹ️  AppImage not found in $INSTALL_DIR"
fi

# Remove desktop entry
if [ -f ~/.local/share/applications/timemachine.desktop ]; then
    rm -f ~/.local/share/applications/timemachine.desktop
    echo "✅ Removed desktop entry"
fi

# Remove icon
if [ -f ~/.local/share/icons/hicolor/256x256/apps/timemachine.png ]; then
    rm -f ~/.local/share/icons/hicolor/256x256/apps/timemachine.png
    echo "✅ Removed icon"
fi

# Update databases
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database ~/.local/share/applications 2>/dev/null
    echo "✅ Updated desktop database"
fi

if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f ~/.local/share/icons/hicolor 2>/dev/null || true
    echo "✅ Updated icon cache"
fi

echo ""
echo "🎉 $APP_NAME uninstalled successfully!"
echo ""
echo "To reinstall, run: ./install.sh"
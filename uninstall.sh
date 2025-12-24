#!/bin/bash

# TimeMachine Backup - Uninstallation Script

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Installation paths
INSTALL_DIR="$HOME/.local/share/timemachine"
BIN_DIR="$HOME/.local/bin"
DESKTOP_DIR="$HOME/.local/share/applications"
ICON_DIR="$HOME/.local/share/icons"

echo -e "${YELLOW}==================================${NC}"
echo -e "${YELLOW}TimeMachine Backup - Uninstallation${NC}"
echo -e "${YELLOW}==================================${NC}"
echo ""
echo "This will remove TimeMachine from your system."
echo -e "${RED}Configuration and backup data will NOT be removed.${NC}"
echo ""
read -p "Continue? (y/N) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Uninstallation cancelled."
    exit 0
fi

echo ""
echo "Removing TimeMachine..."

# Stop any running instances
if pgrep -f "timemachine" > /dev/null; then
    echo "Stopping running TimeMachine processes..."
    pkill -f "timemachine" || true
fi

# Remove systemd service if exists
if [ -f "$HOME/.config/systemd/user/timemachine.service" ]; then
    echo "Removing systemd service..."
    systemctl --user stop timemachine.service 2>/dev/null || true
    systemctl --user disable timemachine.service 2>/dev/null || true
    rm -f "$HOME/.config/systemd/user/timemachine.service"
    systemctl --user daemon-reload 2>/dev/null || true
fi

# Remove autostart entry if exists
if [ -f "$HOME/.config/autostart/timemachine-daemon.desktop" ]; then
    echo "Removing autostart entry..."
    rm -f "$HOME/.config/autostart/timemachine-daemon.desktop"
fi

# Remove files
echo "Removing application files..."
rm -rf "$INSTALL_DIR"
rm -f "$BIN_DIR/timemachine"
rm -f "$BIN_DIR/timemachine-daemon"
rm -f "$DESKTOP_DIR/timemachine.desktop"
rm -f "$ICON_DIR/timemachine.png"

# Update desktop database
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database "$DESKTOP_DIR" 2>/dev/null || true
fi

echo ""
echo -e "${GREEN}==================================${NC}"
echo -e "${GREEN}Uninstallation completed!${NC}"
echo -e "${GREEN}==================================${NC}"
echo ""
echo "TimeMachine has been removed from your system."
echo "Your configuration and backup data remain in:"
echo "  - Configuration: $HOME/.config/timemachine (if exists)"
echo "  - Backup data: Your backup location"
echo ""

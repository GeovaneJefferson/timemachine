#!/bin/bash

# TimeMachine Backup - Installation Script
# This script installs TimeMachine to your system

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

echo -e "${GREEN}==================================${NC}"
echo -e "${GREEN}TimeMachine Backup - Installation${NC}"
echo -e "${GREEN}==================================${NC}"
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is not installed!${NC}"
    echo "Please install Python 3 first."
    exit 1
fi

echo -e "${YELLOW}Installing TimeMachine...${NC}"

# Create directories
echo "Creating directories..."
mkdir -p "$INSTALL_DIR"
mkdir -p "$BIN_DIR"
mkdir -p "$DESKTOP_DIR"
mkdir -p "$ICON_DIR"

# Copy application files
echo "Copying application files..."
cp -r config "$INSTALL_DIR/"
cp -r templates "$INSTALL_DIR/"
cp -r static "$INSTALL_DIR/"
cp app.py "$INSTALL_DIR/"
cp main.js "$INSTALL_DIR/"
cp package.json "$INSTALL_DIR/"
cp requirements.txt "$INSTALL_DIR/"
cp loading.html "$INSTALL_DIR/"
cp error.html "$INSTALL_DIR/"

# Copy additional Python files if they exist
[ -f system.py ] && cp system.py "$INSTALL_DIR/"
[ -f daemon.py ] && cp daemon.py "$INSTALL_DIR/"
[ -f server.py ] && cp server.py "$INSTALL_DIR/"
[ -f search_handler.py ] && cp search_handler.py "$INSTALL_DIR/"
[ -f storage_util.py ] && cp storage_util.py "$INSTALL_DIR/"
[ -f daemon_control.py ] && cp daemon_control.py "$INSTALL_DIR/"

# Copy icon
if [ -f icon.png ]; then
    cp icon.png "$ICON_DIR/timemachine.png"
    echo "Icon installed to $ICON_DIR/timemachine.png"
fi

# Install Python dependencies
echo "Installing Python dependencies..."
pip3 install --user -r requirements.txt

# Check if Node.js and npm are installed for Electron
if command -v npm &> /dev/null; then
    echo "Installing Node.js dependencies..."
    cd "$INSTALL_DIR"
    npm install
    cd - > /dev/null
else
    echo -e "${YELLOW}Warning: npm not found. Electron dependencies not installed.${NC}"
    echo "You may need to install Node.js for the Electron interface."
fi

# Create launcher script
echo "Creating launcher script..."
cat > "$BIN_DIR/timemachine" << 'EOF'
#!/bin/bash
# TimeMachine Backup Launcher

INSTALL_DIR="$HOME/.local/share/timemachine"
PORT=5000

# Function to find available port
find_available_port() {
    local port=$1
    while lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1 ; do
        port=$((port + 1))
    done
    echo $port
}

# Function to kill existing TimeMachine instances
kill_existing() {
    pkill -f "python3.*app.py" 2>/dev/null || true
    pkill -f "electron.*main.js" 2>/dev/null || true
    sleep 1
}

# Change to installation directory
cd "$INSTALL_DIR" || exit 1

# Check if electron is available
if command -v electron &> /dev/null || [ -d "node_modules/electron" ]; then
    # Kill any existing instances
    kill_existing
    
    # Launch with Electron
    if [ -d "node_modules/electron" ]; then
        npx electron main.js
    else
        electron main.js
    fi
else
    echo "Electron not found, launching web interface..."
    echo ""
    echo "To install Electron, run:"
    echo "  cd ~/.local/share/timemachine"
    echo "  npm install"
    echo ""
    
    # Check if port is in use
    if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1; then
        echo "Port $PORT is in use!"
        echo ""
        echo "Options:"
        echo "  1. Kill existing instance: pkill -f 'python3.*app.py'"
        echo "  2. Use different port: PORT=$((PORT + 1)) python3 app.py"
        echo ""
        
        read -p "Kill existing instance and restart? (y/N) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            kill_existing
            PORT=$(find_available_port $PORT)
            echo "Using port: $PORT"
            PORT=$PORT python3 app.py
        else
            echo "Opening existing instance in browser..."
            xdg-open "http://localhost:$PORT" 2>/dev/null || echo "Open http://localhost:$PORT in your browser"
        fi
    else
        python3 app.py
    fi
fi
EOF

chmod +x "$BIN_DIR/timemachine"

# Create .desktop file
echo "Creating desktop entry..."
cat > "$DESKTOP_DIR/timemachine.desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=TimeMachine
Comment=Real-time backup solution for Linux
Exec=$BIN_DIR/timemachine
Icon=$ICON_DIR/timemachine.png
Terminal=false
Categories=Utility;System;Archiving;
Keywords=backup;sync;timemachine;
StartupNotify=true
StartupWMClass=timemachine
EOF

chmod +x "$DESKTOP_DIR/timemachine.desktop"

# Update desktop database
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database "$DESKTOP_DIR" 2>/dev/null || true
fi

# Add to PATH if not already there
if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
    echo ""
    echo -e "${YELLOW}Note: $BIN_DIR is not in your PATH${NC}"
    echo "Add this line to your ~/.bashrc or ~/.zshrc:"
    echo "export PATH=\"\$HOME/.local/bin:\$PATH\""
fi

echo ""
echo -e "${GREEN}==================================${NC}"
echo -e "${GREEN}Installation completed successfully!${NC}"
echo -e "${GREEN}==================================${NC}"
echo ""
echo "You can now:"
echo "  1. Launch from applications menu: Search for 'TimeMachine Backup'"
echo "  2. Run from terminal: timemachine"
echo "  3. Or run directly: $BIN_DIR/timemachine"
echo ""
echo "Installed to: $INSTALL_DIR"
echo ""
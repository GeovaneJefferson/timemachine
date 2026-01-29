#!/bin/bash
# TimeMachine Electron - Quick Setup Script
# Sets up development environment and dependencies

set -e

echo "🚀 TimeMachine Electron Setup"
echo "=============================="
echo ""

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found. Please install Node.js 16+:"
    echo "   curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -"
    echo "   sudo dnf install -y nodejs"
    exit 1
fi

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.8+:"
    echo "   sudo dnf install python3 python3-pip"
    exit 1
fi

echo "✅ Node.js: $(node --version)"
echo "✅ Python: $(python3 --version)"
echo ""

# Install Node dependencies
if [ ! -d "node_modules" ]; then
    echo "📦 Installing Node.js dependencies..."
    npm install
else
    echo "✅ Node.js dependencies already installed"
fi

# Install Python dependencies
if [ ! -d ".venv" ]; then
    echo ""
    echo "📦 Installing Python dependencies..."
    python3 -m venv .venv
    source .venv/bin/activate
    pip install --upgrade pip
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
    fi
    echo "✅ Python environment ready"
else
    echo "✅ Python environment exists"
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo ""
echo "1️⃣  Development testing:"
echo "   npm run dev"
echo ""
echo "2️⃣  Install to home directory:"
echo "   bash install.sh"
echo ""
echo "3️⃣  Uninstall:"
echo "   bash uninstall.sh"
echo ""


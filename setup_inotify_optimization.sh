#!/bin/bash
# Quick setup script for inotify optimization

set -e

CONFIG_FILE="$HOME/.timemachine/config/.config"
DOCS_DIR="./docs"

echo "🔧 TimeMachine Inotify Optimization Setup"
echo "=========================================="
echo

# Check if config exists
if [ ! -f "$CONFIG_FILE" ]; then
    echo "❌ Config file not found: $CONFIG_FILE"
    echo "   Run TimeMachine at least once to create the config."
    exit 1
fi

echo "📋 Checking current config..."
echo

# Show current exclude patterns if any
if grep -q "exclude_patterns" "$CONFIG_FILE" 2>/dev/null; then
    echo "Current exclude patterns:"
    grep "exclude_patterns" "$CONFIG_FILE" || echo "   (none)"
else
    echo "No exclude patterns found in config"
fi

echo
echo "✅ Recommended exclusions for backup:"
echo "   • .git (version control metadata)"
echo "   • node_modules (npm packages)"
echo "   • .venv or venv (Python virtual environments)"
echo "   • __pycache__ (Python bytecode cache)"
echo "   • .cache (application caches)"
echo
echo "These directories often have 10,000+ subdirectories"
echo "and significantly reduce inotify watch requirements."
echo

read -p "Add recommended exclusions to config? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    # Backup original config
    cp "$CONFIG_FILE" "$CONFIG_FILE.backup.$(date +%s)"
    
    # Add or update exclude patterns
    if grep -q "\[EXCLUDE\]" "$CONFIG_FILE"; then
        # EXCLUDE section exists, add after it
        sed -i '/\[EXCLUDE\]/a exclude_patterns = .git,node_modules,.venv,venv,__pycache__,.cache,.egg-info,dist,build' "$CONFIG_FILE"
        echo "✅ Added exclusions to [EXCLUDE] section"
    else
        # Add new section
        echo >> "$CONFIG_FILE"
        echo "[EXCLUDE]" >> "$CONFIG_FILE"
        echo "exclude_patterns = .git,node_modules,.venv,venv,__pycache__,.cache,.egg-info,dist,build" >> "$CONFIG_FILE"
        echo "✅ Created [EXCLUDE] section with recommendations"
    fi
    
    echo
    echo "📝 Backup created: $CONFIG_FILE.backup.$(date +%s)"
fi

echo
echo "📊 Check inotify status with:"
echo "   python3 py/inotify_monitor.py"
echo
echo "📖 Full guide available in:"
echo "   docs/INOTIFY_OPTIMIZATION.md"
echo
echo "Done!"

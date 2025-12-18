#!/bin/bash
# install.sh - Builds, cleans, and installs Time Machine AppImage directly to ~/.local/bin/

APP_NAME="TimeMachine"
APP_VERSION="1.0.0"
APPIMAGE_FILE="${APP_NAME}-${APP_VERSION}-x86_64.AppImage"
BUILD_DIR="build"
INSTALL_DIR="$HOME/.local/bin"
PY_BUILDER="static/py/make-appimage.py"

echo "🚀 Time Machine - Build & Install"
echo "================================="

# Function to print colored output
print_status() {
    echo -e "📌 $1"
}

print_success() {
    echo -e "✅ $1"
}

print_error() {
    echo -e "❌ $1"
}

# Function to clean old files
clean_old_files() {
    print_status "Cleaning old build files..."
    
    # Remove build directory
    if [ -d "$BUILD_DIR" ]; then
        rm -rf "$BUILD_DIR"
        print_success "Removed build directory"
    fi
    
    # Remove installed AppImage (this is now the main target)
    if [ -f "$INSTALL_DIR/$APPIMAGE_FILE" ]; then
        rm -f "$INSTALL_DIR/$APPIMAGE_FILE"
        print_success "Removed installed AppImage"
    fi
    
    # Also clean any local AppImage (in case of previous runs)
    if [ -f "$APPIMAGE_FILE" ]; then
        rm -f "$APPIMAGE_FILE"
        print_success "Removed local $APPIMAGE_FILE"
    fi
    
    # Clean Python cache
    find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null
    find . -name "*.pyc" -type f -delete
    print_success "Cleaned Python cache"
}

# Function to check requirements
check_requirements() {
    print_status "Checking requirements..."
    
    # Check for Python builder
    if [ ! -f "$PY_BUILDER" ]; then
        print_error "Builder not found: $PY_BUILDER"
        print_error "Please ensure make-appimage.py is in static/py/"
        exit 1
    fi
    
    # Check for required files
    required_files=("app.py" "main.js" "package.json" "Requirements.txt")
    missing=0
    
    for file in "${required_files[@]}"; do
        if [ ! -f "$file" ]; then
            print_error "Missing: $file"
            missing=1
        fi
    done
    
    if [ $missing -eq 1 ]; then
        print_error "Missing required files. Cannot build."
        exit 1
    fi
    
    print_success "All requirements met"
}

# Function to build AppImage directly to destination
build_appimage() {
    print_status "Building AppImage directly to $INSTALL_DIR..."
    
    # Check if Python is available
    if ! command -v python3 &> /dev/null; then
        print_error "Python3 is not installed"
        exit 1
    fi
    
    # Create install directory if it doesn't exist
    mkdir -p "$INSTALL_DIR"
    
    # Run the Python builder
    print_status "Running builder: $PY_BUILDER"
    
    if python3 "$PY_BUILDER"; then
        if [ -f "$INSTALL_DIR/$APPIMAGE_FILE" ]; then
            size_mb=$(du -m "$INSTALL_DIR/$APPIMAGE_FILE" 2>/dev/null | cut -f1 || echo "unknown")
            print_success "Built directly to: $INSTALL_DIR/$APPIMAGE_FILE (${size_mb}MB)"
            return 0
        else
            print_error "Builder ran but $APPIMAGE_FILE was not created in $INSTALL_DIR"
            print_status "Checking current directory..."
            if [ -f "$APPIMAGE_FILE" ]; then
                print_status "Found in current directory, moving to $INSTALL_DIR..."
                mv "$APPIMAGE_FILE" "$INSTALL_DIR/"
                chmod +x "$INSTALL_DIR/$APPIMAGE_FILE"
                print_success "Moved to $INSTALL_DIR/$APPIMAGE_FILE"
                return 0
            fi
            return 1
        fi
    else
        print_error "Build failed"
        return 1
    fi
}

# Function to create desktop entry
create_desktop_entry() {
    print_status "Creating desktop entry..."
    
    mkdir -p ~/.local/share/applications
    
    # Use the actual installed path
    APP_PATH="$INSTALL_DIR/$APPIMAGE_FILE"
    
cat > ~/.local/share/applications/timemachine.desktop << 'DESKTOP'
[Desktop Entry]
Type=Application
Name=Time Machine
Comment=Backup Application
Exec=$HOME/.local/bin/TimeMachine-1.0.0-x86_64.AppImage
Icon=timemachine
Categories=Utility;System;
Terminal=false
StartupNotify=true
StartupWMClass=TimeMachine
X-AppImage-Version=1.0.0
Keywords=backup;time;files;
DESKTOP
    
    print_success "Desktop entry created"
}

# Function to install icon
install_icon() {
    print_status "Installing icon..."
    
    mkdir -p ~/.local/share/icons/hicolor/256x256/apps
    
    # Try to get icon from various sources
    icon_installed=false
    
    # 1. Try from static/vendor/favicon.png
    if [ -f "static/vendor/favicon.png" ]; then
        cp "static/vendor/favicon.png" ~/.local/share/icons/hicolor/256x256/apps/timemachine.png
        print_success "Icon from static/vendor/favicon.png"
        icon_installed=true
    
    # 2. Try from favicon.png
    elif [ -f "favicon.png" ]; then
        cp "favicon.png" ~/.local/share/icons/hicolor/256x256/apps/timemachine.png
        print_success "Icon from favicon.png"
        icon_installed=true
    
    # 3. Try from icon.png
    elif [ -f "icon.png" ]; then
        cp "icon.png" ~/.local/share/icons/hicolor/256x256/apps/timemachine.png
        print_success "Icon from icon.png"
        icon_installed=true
    
    # 4. Try to extract from AppImage itself
    elif [ -f "$INSTALL_DIR/$APPIMAGE_FILE" ]; then
        print_status "Extracting icon from AppImage..."
        
        # Create temp directory
        TEMP_DIR=$(mktemp -d)
        cd "$TEMP_DIR"
        
        # Extract AppImage
        if "$INSTALL_DIR/$APPIMAGE_FILE" --appimage-extract >/dev/null 2>&1; then
            if [ -d "squashfs-root" ]; then
                # Look for icon
                if [ -f "squashfs-root/timemachine.png" ]; then
                    cp "squashfs-root/timemachine.png" ~/.local/share/icons/hicolor/256x256/apps/timemachine.png
                    print_success "Icon extracted from AppImage: timemachine.png"
                    icon_installed=true
                elif [ -f "squashfs-root/.DirIcon" ]; then
                    cp "squashfs-root/.DirIcon" ~/.local/share/icons/hicolor/256x256/apps/timemachine.png
                    print_success "Icon extracted from AppImage: .DirIcon"
                    icon_installed=true
                fi
                # Cleanup
                rm -rf squashfs-root
            fi
        fi
        
        # Cleanup and return to original directory
        cd - >/dev/null
        rm -rf "$TEMP_DIR"
    fi
    
    if [ "$icon_installed" = false ]; then
        print_error "No icon found - app will use default"
    fi
}

# Function to update desktop databases
update_databases() {
    print_status "Updating desktop database..."
    
    if command -v update-desktop-database &> /dev/null; then
        update-desktop-database ~/.local/share/applications 2>/dev/null
        print_success "Desktop database updated"
    else
        print_error "update-desktop-database not found"
    fi
    
    print_status "Updating icon cache..."
    
    if command -v gtk-update-icon-cache &> /dev/null; then
        gtk-update-icon-cache -f ~/.local/share/icons/hicolor 2>/dev/null || true
        print_success "Icon cache updated"
    else
        print_error "gtk-update-icon-cache not found"
    fi
}

# Function to verify installation
verify_installation() {
    print_status "Verifying installation..."
    
    checks_passed=0
    checks_total=3
    
    # Check 1: AppImage exists in install directory
    if [ -f "$INSTALL_DIR/$APPIMAGE_FILE" ]; then
        # Check if it's executable
        if [ -x "$INSTALL_DIR/$APPIMAGE_FILE" ]; then
            print_success "AppImage installed and executable: $INSTALL_DIR/$APPIMAGE_FILE"
            checks_passed=$((checks_passed + 1))
        else
            print_error "AppImage not executable, fixing..."
            chmod +x "$INSTALL_DIR/$APPIMAGE_FILE"
            if [ -x "$INSTALL_DIR/$APPIMAGE_FILE" ]; then
                print_success "Fixed permissions"
                checks_passed=$((checks_passed + 1))
            else
                print_error "AppImage not executable"
            fi
        fi
    else
        print_error "AppImage not found in $INSTALL_DIR"
    fi
    
    # Check 2: Desktop entry exists
    if [ -f ~/.local/share/applications/timemachine.desktop ]; then
        print_success "Desktop entry created"
        checks_passed=$((checks_passed + 1))
    else
        print_error "Desktop entry not found"
    fi
    
    # Check 3: Icon exists
    if [ -f ~/.local/share/icons/hicolor/256x256/apps/timemachine.png ]; then
        print_success "Icon installed"
        checks_passed=$((checks_passed + 1))
    else
        print_error "Icon not found"
    fi
    
    if [ $checks_passed -eq $checks_total ]; then
        print_success "Installation verified successfully!"
        return 0
    else
        print_error "Installation incomplete ($checks_passed/$checks_total checks passed)"
        return 1
    fi
}

# Function to check if ~/.local/bin is in PATH
check_path() {
    print_status "Checking PATH..."
    
    if [[ ":$PATH:" == *":$HOME/.local/bin:"* ]]; then
        print_success "~/.local/bin is in your PATH"
        return 0
    else
        print_error "~/.local/bin is NOT in your PATH"
        echo ""
        echo "To add it to your PATH, add this to your ~/.bashrc or ~/.zshrc:"
        echo 'export PATH="$HOME/.local/bin:$PATH"'
        echo ""
        echo "Then run: source ~/.bashrc  # or source ~/.zshrc"
        return 1
    fi
}

# Main execution
main() {
    echo ""
    print_status "Starting Time Machine installation..."
    echo ""
    
    # Step 1: Clean old files
    clean_old_files
    echo ""
    
    # Step 2: Check requirements
    check_requirements
    echo ""
    
#     # Step 3: Build AppImage directly to destination
#     if ! build_appimage; then
#         print_error "Build failed. Installation aborted."
#         exit 1
#     fi
    echo ""
    
    # Step 4: Create desktop entry
    create_desktop_entry
    echo ""
    
    # Step 5: Install icon
    install_icon
    echo ""
    
    # Step 6: Update databases
    update_databases
    echo ""
    
    # Step 7: Verify installation
    if verify_installation; then
        echo ""
        echo "🎉 INSTALLATION COMPLETE!"
        echo "=========================="
        echo ""
        echo "Time Machine has been successfully installed!"
        echo ""
        
        # Check PATH
        check_path
        echo ""
        
        echo "You can now:"
        echo "1. Launch from your application menu"
        echo "2. Run from terminal: $INSTALL_DIR/$APPIMAGE_FILE"
        
        if [[ ":$PATH:" == *":$HOME/.local/bin:"* ]]; then
            echo "3. Run from anywhere: $APPIMAGE_FILE"
        else
            echo "3. Add ~/.local/bin to PATH to run from anywhere"
        fi
        
        echo ""
        echo "To uninstall, run: ./uninstall.sh"
        echo ""
    else
        print_error "Installation verification failed."
        exit 1
    fi
}

# Run main function
main

#!/bin/bash
# Setup script for Markdown to PDF Converter
# Handles dependency installation across different platforms

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Detect OS
detect_os() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "linux"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macos"
    elif [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
        echo "windows"
    else
        echo "unknown"
    fi
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Install system dependencies for Linux
install_linux_deps() {
    log_info "Installing system dependencies for Linux..."
    
    if command_exists apt-get; then
        # Debian/Ubuntu
        sudo apt-get update
        sudo apt-get install -y \
            python3-pip \
            python3-cffi \
            python3-brotli \
            libpango-1.0-0 \
            libharfbuzz0b \
            libpangoft2-1.0-0 \
            libcairo2 \
            libgdk-pixbuf2.0-0 \
            libffi-dev \
            shared-mime-info
    elif command_exists yum; then
        # RHEL/CentOS/Fedora
        sudo yum install -y \
            python3-pip \
            python3-cffi \
            pango \
            harfbuzz \
            cairo \
            gdk-pixbuf2 \
            libffi-devel
    elif command_exists pacman; then
        # Arch Linux
        sudo pacman -S --noconfirm \
            python-pip \
            python-cffi \
            pango \
            harfbuzz \
            cairo \
            gdk-pixbuf2 \
            libffi
    else
        log_error "Unsupported Linux distribution. Please install dependencies manually."
        exit 1
    fi
    
    log_success "Linux system dependencies installed"
}

# Install system dependencies for macOS
install_macos_deps() {
    log_info "Installing system dependencies for macOS..."
    
    if ! command_exists brew; then
        log_error "Homebrew not found. Please install it first: https://brew.sh"
        exit 1
    fi
    
    brew install \
        cairo \
        pango \
        gdk-pixbuf \
        libffi \
        python@3.11
    
    log_success "macOS system dependencies installed"
}

# Install system dependencies for Windows
install_windows_deps() {
    log_info "Setting up for Windows..."
    
    cat << EOF
    
For Windows, please follow these steps:

1. Install Python 3.8+ from https://www.python.org/downloads/
   - Make sure to check "Add Python to PATH"

2. Install GTK3 runtime from:
   https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer

3. After installation, run this script again or install Python packages manually:
   pip install -r requirements.txt

Press Enter to continue...
EOF
    read
}

# Create virtual environment
create_venv() {
    log_info "Creating Python virtual environment..."
    
    if [[ -d "venv" ]]; then
        log_warning "Virtual environment already exists. Skipping..."
    else
        python3 -m venv venv
        log_success "Virtual environment created"
    fi
    
    # Activate virtual environment
    if [[ "$OS" == "windows" ]]; then
        source venv/Scripts/activate
    else
        source venv/bin/activate
    fi
}

# Install Python packages
install_python_packages() {
    log_info "Installing Python packages..."
    
    # Upgrade pip
    pip install --upgrade pip
    
    # Install requirements
    if [[ -f "requirements.txt" ]]; then
        pip install -r requirements.txt
        log_success "Python packages installed"
    else
        log_warning "requirements.txt not found. Installing packages individually..."
        pip install markdown weasyprint pygments
        log_success "Core Python packages installed"
    fi
}

# Test installation
test_installation() {
    log_info "Testing installation..."
    
    # Test Python imports
    python3 -c "
import markdown
import weasyprint
import pygments
print('✓ All Python packages imported successfully')
" || {
    log_error "Failed to import Python packages"
    exit 1
}
    
    # Test converter script
    if [[ -f "markdown_to_pdf.py" ]]; then
        python3 markdown_to_pdf.py --help > /dev/null 2>&1
        if [[ $? -eq 0 ]]; then
            log_success "Converter script is working"
        else
            log_error "Converter script failed to run"
            exit 1
        fi
    fi
    
    # Test sample conversion if sample.md exists
    if [[ -f "sample.md" ]]; then
        log_info "Running sample conversion..."
        python3 markdown_to_pdf.py sample.md -o test_output.pdf
        
        if [[ -f "test_output.pdf" ]]; then
            log_success "Sample PDF generated successfully: test_output.pdf"
            
            # Get file size
            if [[ "$OS" == "macos" ]]; then
                SIZE=$(stat -f%z test_output.pdf)
            else
                SIZE=$(stat -c%s test_output.pdf)
            fi
            
            log_info "PDF size: $(numfmt --to=iec-i --suffix=B $SIZE 2>/dev/null || echo "${SIZE} bytes")"
        else
            log_error "Failed to generate sample PDF"
        fi
    fi
}

# Create desktop shortcut (optional)
create_shortcut() {
    log_info "Creating desktop shortcut..."
    
    if [[ "$OS" == "linux" ]]; then
        cat > ~/Desktop/markdown-to-pdf.desktop << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Markdown to PDF
Comment=Convert Markdown files to PDF
Exec=$(pwd)/convert.sh %f
Icon=$(pwd)/icon.png
Terminal=true
MimeType=text/markdown;text/x-markdown;
Categories=Office;Development;
EOF
        chmod +x ~/Desktop/markdown-to-pdf.desktop
        log_success "Desktop shortcut created"
        
    elif [[ "$OS" == "macos" ]]; then
        # Create an AppleScript app
        osascript -e "
        tell application \"Finder\"
            make alias file to POSIX file \"$(pwd)/markdown_to_pdf.py\" at desktop
            set name of result to \"Markdown to PDF\"
        end tell
        " 2>/dev/null || log_warning "Could not create macOS alias"
    fi
}

# Main installation process
main() {
    echo "============================================"
    echo "   Markdown to PDF Converter Setup"
    echo "============================================"
    echo
    
    # Detect OS
    OS=$(detect_os)
    log_info "Detected OS: $OS"
    
    # Check Python
    if ! command_exists python3; then
        log_error "Python 3 not found. Please install Python 3.8 or later."
        exit 1
    fi
    
    PYTHON_VERSION=$(python3 --version 2>&1 | grep -oE '[0-9]+\.[0-9]+')
    log_info "Python version: $PYTHON_VERSION"
    
    # Install system dependencies
    case "$OS" in
        linux)
            install_linux_deps
            ;;
        macos)
            install_macos_deps
            ;;
        windows)
            install_windows_deps
            ;;
        *)
            log_error "Unsupported operating system"
            exit 1
            ;;
    esac
    
    # Create and activate virtual environment
    create_venv
    
    # Install Python packages
    install_python_packages
    
    # Run tests
    test_installation
    
    # Optional: Create shortcut
    read -p "Create desktop shortcut? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        create_shortcut
    fi
    
    echo
    echo "============================================"
    echo "   Installation Complete!"
    echo "============================================"
    echo
    echo "Usage:"
    echo "  python3 markdown_to_pdf.py input.md"
    echo "  python3 markdown_to_pdf.py input.md -o output.pdf --toc --page-numbers"
    echo "  python3 markdown_to_pdf.py input.md -t academic -c custom.css"
    echo
    echo "For more options, run:"
    echo "  python3 markdown_to_pdf.py --help"
    echo
    
    if [[ -d "venv" ]]; then
        echo "To activate the virtual environment:"
        if [[ "$OS" == "windows" ]]; then
            echo "  source venv/Scripts/activate"
        else
            echo "  source venv/bin/activate"
        fi
        echo
    fi
    
    log_success "Setup complete! Happy converting!"
}

# Run main function
main "$@"

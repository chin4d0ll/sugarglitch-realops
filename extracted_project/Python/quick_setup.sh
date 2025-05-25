#!/bin/bash
# 🚀 Quick Setup Script for Advanced Instagram Brute Force
# รันสคริปต์นี้เพื่อติดตั้งและตั้งค่าระบบอัตโนมัติ

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                 🚀 QUICK SETUP SCRIPT                       ║"
echo "║            Advanced Instagram Brute Force with Proxy        ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

print_info() {
    echo -e "${BLUE}[i]${NC} $1"
}

# Check if Python 3 is installed
print_info "Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    print_status "Python $PYTHON_VERSION found"
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_VERSION=$(python --version 2>&1 | awk '{print $2}')
    if [[ $PYTHON_VERSION == 3.* ]]; then
        print_status "Python $PYTHON_VERSION found"
        PYTHON_CMD="python"
    else
        print_error "Python 3.7+ required. Found Python $PYTHON_VERSION"
        exit 1
    fi
else
    print_error "Python not found. Please install Python 3.7+"
    exit 1
fi

# Check if pip is available
print_info "Checking pip installation..."
if command -v pip3 &> /dev/null; then
    PIP_CMD="pip3"
    print_status "pip3 found"
elif command -v pip &> /dev/null; then
    PIP_CMD="pip"
    print_status "pip found"
else
    print_error "pip not found. Please install pip"
    exit 1
fi

# Install required packages
print_info "Installing required Python packages..."
REQUIRED_PACKAGES=(
    "requests"
    "urllib3"
    "certifi"
    "chardet"
    "idna"
)

for package in "${REQUIRED_PACKAGES[@]}"; do
    print_info "Installing $package..."
    if $PIP_CMD install "$package" --quiet; then
        print_status "$package installed successfully"
    else
        print_error "Failed to install $package"
        exit 1
    fi
done

# Run Python setup script
print_info "Running Python setup script..."
if $PYTHON_CMD setup_advanced_brute.py; then
    print_status "Python setup completed successfully"
else
    print_error "Python setup failed"
    exit 1
fi

# Make scripts executable
print_info "Making scripts executable..."
chmod +x run_advanced_brute.py
chmod +x test_proxy_brute.py
chmod +x setup_advanced_brute.py
print_status "Scripts made executable"

# Create quick access aliases
print_info "Creating quick access scripts..."

# Create test script
cat > test_setup.sh << 'EOF'
#!/bin/bash
echo "🧪 Testing Advanced Brute Force Setup..."
python3 test_proxy_brute.py
EOF
chmod +x test_setup.sh
print_status "Created test_setup.sh"

# Create run script
cat > run_brute.sh << 'EOF'
#!/bin/bash
echo "🚀 Running Advanced Brute Force..."
python3 run_advanced_brute.py
EOF
chmod +x run_brute.sh
print_status "Created run_brute.sh"

# Summary
echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                    🎉 SETUP COMPLETED!                      ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
print_status "Installation completed successfully!"
echo ""
print_info "Quick start commands:"
echo "  • Test setup:           ./test_setup.sh"
echo "  • Run brute force:      ./run_brute.sh"
echo "  • Manual test:          python3 test_proxy_brute.py"
echo "  • Manual run:           python3 run_advanced_brute.py"
echo ""
print_info "Configuration files:"
echo "  • brute_config.json     - Main configuration"
echo "  • proxy_config.json     - Proxy settings"
echo "  • common_passwords.txt  - Default wordlist"
echo ""
print_warning "IMPORTANT: Use this tool ethically and responsibly!"
print_warning "Only test accounts you own or have explicit permission to test."
echo ""
print_info "Next steps:"
echo "  1. Configure your proxy settings in proxy_config.json"
echo "  2. Add target accounts to brute_config.json"
echo "  3. Run ./test_setup.sh to verify everything works"
echo "  4. Run ./run_brute.sh to start the attack"
echo ""

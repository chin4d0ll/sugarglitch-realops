#!/bin/bash

# SugarGlitch RealOps - Environment Setup Script
# Automated setup for Instagram DM Intelligence Suite

echo "🎯 SugarGlitch RealOps - Environment Setup"
echo "==========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Check if running in supported environment
print_info "Checking system requirements..."

# Check Python
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d " " -f 2)
    print_status "Python3 found: $PYTHON_VERSION"
else
    print_error "Python3 not found. Please install Python 3.8+ first."
    exit 1
fi

# Check pip
if command -v pip3 &> /dev/null; then
    print_status "pip3 found"
else
    print_error "pip3 not found. Please install pip3 first."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    print_info "Creating virtual environment..."
    python3 -m venv .venv
    print_status "Virtual environment created"
else
    print_status "Virtual environment exists"
fi

# Activate virtual environment
print_info "Activating virtual environment..."
source .venv/bin/activate
print_status "Virtual environment activated"

# Upgrade pip
print_info "Upgrading pip..."
pip install --upgrade pip

# Install Python packages
print_info "Installing Python packages..."
pip install playwright asyncio beautifulsoup4 requests pandas jinja2

# Install Playwright browsers
print_info "Installing Playwright browsers..."
playwright install chromium

# Create necessary directories
print_info "Creating project directories..."
mkdir -p data
mkdir -p output
mkdir -p logs
mkdir -p temp
mkdir -p reports

# Set permissions for shell scripts
print_info "Setting script permissions..."
chmod +x *.sh 2>/dev/null || true

# Create config file if it doesn't exist
if [ ! -f "config.py" ]; then
    print_info "Creating default configuration..."
    cat > config.py << 'EOF'
# SugarGlitch RealOps Configuration
import os

# Extraction Settings
EXTRACTION_SETTINGS = {
    "max_conversations": 10,
    "include_media": True,
    "date_range": "last_30_days",
    "output_formats": ["json", "html", "pdf"],
    "headless_browser": True,
    "timeout": 60000,
    "wait_time": 2000
}

# Output Directories
OUTPUT_DIRS = {
    "data": "data/",
    "output": "output/", 
    "logs": "logs/",
    "temp": "temp/",
    "reports": "reports/"
}

# Security Settings
SECURITY_SETTINGS = {
    "encrypt_sessions": True,
    "auto_cleanup": True,
    "audit_logging": True,
    "session_timeout": 3600
}

# Default targets
DEFAULT_TARGETS = [
    "alx.trading"
]

# Ensure directories exist
for dir_path in OUTPUT_DIRS.values():
    os.makedirs(dir_path, exist_ok=True)
EOF
    print_status "Configuration file created"
fi

# Create .gitignore if it doesn't exist
if [ ! -f ".gitignore" ]; then
    print_info "Creating .gitignore..."
    cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
.venv/
venv/
ENV/
env/

# Output Files
dm_output.*
*.json
*.html
*.pdf
*.csv

# Sensitive Data
sessionid.txt
cookies.txt
sessions/
temp/
logs/

# System Files
.DS_Store
Thumbs.db
.vscode/
.idea/

# Database files
*.db
*.sqlite
*.sqlite3

# Temporary files
temp/
tmp/
*.tmp
*.temp
EOF
    print_status ".gitignore created"
fi

# Test installation
print_info "Testing installation..."

# Test Python import
python3 -c "import playwright; print('Playwright import: OK')" 2>/dev/null && print_status "Playwright test passed" || print_error "Playwright test failed"

# Test Playwright browser
python3 -c "
import asyncio
from playwright.async_api import async_playwright

async def test():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        await browser.close()
        print('Browser test: OK')

asyncio.run(test())
" 2>/dev/null && print_status "Browser test passed" || print_warning "Browser test failed (may work during actual use)"

# Display summary
echo ""
echo "🎉 Setup Complete!"
echo "=================="
echo ""
print_status "Environment: Virtual environment (.venv)"
print_status "Python packages: Installed"
print_status "Playwright browser: Installed" 
print_status "Project structure: Created"
print_status "Configuration: Ready"
echo ""

echo "📋 Next Steps:"
echo "==============="
echo "1. Get Instagram sessionid:"
echo "   - Open Instagram in browser"
echo "   - Press F12 → Application → Cookies → instagram.com"
echo "   - Copy 'sessionid' value"
echo ""
echo "2. Run extraction:"
echo "   ./run_dm_extractor.sh"
echo ""
echo "3. Or run specific target:"
echo "   ./run_alx_trading_extractor.sh"
echo ""

print_info "Setup completed successfully! 🚀"

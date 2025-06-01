#!/bin/bash

# SugarGlitch RealOps Platform - Setup Script
# Automated installation and configuration

set -e

echo "🚀 SugarGlitch RealOps Platform Setup"
echo "========================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
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

# Check system requirements
check_requirements() {
    log_info "Checking system requirements..."
    
    # Check Python
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
        log_success "Python $PYTHON_VERSION found"
    else
        log_error "Python 3.12+ required but not found"
        exit 1
    fi
    
    # Check Node.js
    if command -v node &> /dev/null; then
        NODE_VERSION=$(node --version)
        log_success "Node.js $NODE_VERSION found"
    else
        log_error "Node.js 18+ required but not found"
        exit 1
    fi
    
    # Check npm
    if command -v npm &> /dev/null; then
        NPM_VERSION=$(npm --version)
        log_success "npm $NPM_VERSION found"
    else
        log_error "npm required but not found"
        exit 1
    fi
    
    # Check Git
    if command -v git &> /dev/null; then
        log_success "Git found"
    else
        log_warning "Git not found - some features may not work"
    fi
}

# Create directory structure
create_directories() {
    log_info "Creating directory structure..."
    
    directories=(
        "data/attacks"
        "data/extractions" 
        "data/intelligence"
        "data/operations"
        "data/sessions"
        "data/instagram"
        "data/telegram"
        "logs"
        "temp"
        "backups"
        "config/json"
        "config/proxies"
        "config/sessions"
    )
    
    for dir in "${directories[@]}"; do
        mkdir -p "$dir"
        log_success "Created directory: $dir"
    done
}

# Install Python dependencies
install_python_deps() {
    log_info "Installing Python dependencies..."
    
    if [ -f "requirements.txt" ]; then
        python3 -m pip install --upgrade pip
        python3 -m pip install -r requirements.txt
        log_success "Python dependencies installed"
    else
        log_error "requirements.txt not found"
        exit 1
    fi
}

# Install Node.js dependencies
install_node_deps() {
    log_info "Installing Node.js dependencies..."
    
    if [ -f "package.json" ]; then
        npm install
        log_success "Node.js dependencies installed"
    else
        log_error "package.json not found"
        exit 1
    fi
}

# Setup configuration
setup_config() {
    log_info "Setting up configuration..."
    
    # Copy environment template
    if [ ! -f ".env" ] && [ -f ".env.example" ]; then
        cp .env.example .env
        log_success "Environment file created from template"
        log_warning "Please edit .env file with your configuration"
    fi
    
    # Verify config file
    if [ -f "config/config.json" ]; then
        log_success "Configuration file found"
    else
        log_error "Configuration file not found"
        exit 1
    fi
}

# Initialize database
init_database() {
    log_info "Initializing database..."
    
    if [ -d "databases" ] && [ -f "databases/enterprise_db_setup.py" ]; then
        cd databases/
        python3 enterprise_db_setup.py
        cd ..
        log_success "Database initialized"
    else
        log_warning "Database setup script or directory not found"
    fi
}

# Setup executable permissions
setup_permissions() {
    log_info "Setting up file permissions..."
    
    scripts=(
        "fix_extensions_rerun.sh"
        "monitor_extensions.py"
        "main.py"
    )
    
    for script in "${scripts[@]}"; do
        if [ -f "$script" ]; then
            chmod +x "$script"
            log_success "Made executable: $script"
        fi
    done
}

# Test installation
test_installation() {
    log_info "Testing installation..."
    
    # Test Python imports
    python3 -c "
import sys
import json
import sqlite3
import requests
print('✅ Core Python modules OK')
"
    
    # Test Node.js
    node -e "
const puppeteer = require('puppeteer');
console.log('✅ Puppeteer OK');
"
    
    log_success "Installation test completed"
}

# Show usage information
show_usage() {
    echo ""
    echo "🎉 Setup completed successfully!"
    echo ""
    echo "Next steps:"
    echo "1. Edit .env file with your configuration"
    echo "2. Run the platform: python3 main.py"
    echo "3. Or use npm scripts:"
    echo "   - npm start          # Start platform"
    echo "   - npm run monitor    # Start extension monitor"
    echo "   - npm run fix-extensions  # Fix extension issues"
    echo ""
    echo "📖 Documentation: docs/"
    echo "🐛 Issues: Check logs/ directory"
    echo "⚙️  Configuration: config/config.json"
    echo ""
}

# Main setup process
main() {
    echo ""
    
    # Run setup steps
    check_requirements
    create_directories
    install_python_deps
    install_node_deps
    setup_config
    init_database
    setup_permissions
    test_installation
    
    show_usage
}

# Handle interrupts
trap 'log_error "Setup interrupted by user"; exit 1' INT

# Run main setup
main

log_success "SugarGlitch RealOps Platform setup completed! 🚀"

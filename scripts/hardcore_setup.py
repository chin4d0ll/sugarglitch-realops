# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
HARDCORE DM EXTRACTOR SETUP SCRIPT
==================================
Installs all dependencies and configures the environment
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell = True, check = True, capture_output = True, text = True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def install_python_packages():
    """Install required Python packages"""
    packages = [
        "playwright",
        "selenium",
        "aiohttp",
        "requests",
        "faker",
        "user-agents",
        "psutil",
        "asyncio",
        "sqlite3"  # Usually built-in
    ]

    print("📦 Installing Python packages...")
    for package in packages:
        run_command(f"pip install {package}", f"Installing {package}")

def install_playwright_browsers():
    """Install Playwright browsers"""
    print("🎭 Installing Playwright browsers...")
    run_command("playwright install", "Installing Playwright browsers")
    run_command("playwright install-deps", "Installing Playwright dependencies")

def setup_chrome_driver():
    """Setup Chrome WebDriver for Selenium"""
    print("🚗 Setting up Chrome WebDriver...")

    # Install Chrome
    commands = [
        "wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -",
        "echo 'deb [arch = amd64] http://dl.google.com/linux/chrome/deb/ stable main' | tee /etc/apt/sources.list.d/google-chrome.list",
        "apt-get update",
        "apt-get install -y google-chrome-stable"
    ]

    for cmd in commands:
        run_command(f"sudo {cmd}", f"Chrome setup: {cmd}")

    # Install ChromeDriver
    run_command("pip install webdriver-manager", "Installing WebDriver Manager")

def create_directories():
    """Create necessary directories"""
    directories = [
        "/workspaces/sugarglitch-realops/logs/hardcore",
        "/workspaces/sugarglitch-realops/data/hardcore_extractions",
        "/workspaces/sugarglitch-realops/data/sessions",
        "/workspaces/sugarglitch-realops/config/backups"
    ]

    print("📁 Creating directories...")
    for directory in directories:
        Path(directory).mkdir(parents = True, exist_ok = True)
        print(f"✅ Created: {directory}")

def setup_permissions():
    """Setup file permissions"""
    print("🔒 Setting up permissions...")
    scripts = [
        "/workspaces/sugarglitch-realops/hardcore_dm_extractor.py",
        "/workspaces/sugarglitch-realops/hardcore_launcher.py",
        "/workspaces/sugarglitch-realops/hardcore_setup.py"
    ]

    for script in scripts:
        if Path(script).exists():
            run_command(f"chmod +x {script}", f"Setting executable permission for {script}")

def create_requirements_file():
    """Create comprehensive requirements.txt"""
    requirements = """
# Hardcore DM Extractor Requirements
playwright>=1.40.0
selenium>=4.15.0
aiohttp>=3.9.0
requests>=2.31.0
faker>=20.1.0
user-agents>=2.2.0
psutil>=5.9.0
webdriver-manager>=4.0.0
asyncio-throttle>=1.0.2
beautifulsoup4>=4.12.0
lxml>=4.9.0
Pillow>=10.0.0
numpy>=1.24.0
pandas>=2.0.0
matplotlib>=3.7.0
seaborn>=0.12.0
tqdm>=4.66.0
colorama>=0.4.6
python-dotenv>=1.0.0
cryptography>=41.0.0
    """.strip()

    requirements_path = "/workspaces/sugarglitch-realops/requirements_hardcore.txt"
    with open(requirements_path, 'w') as f:
        f.write(requirements)

    print(f"✅ Created requirements file: {requirements_path}")
    return requirements_path

def main():
    """Main setup function"""
    print("🔥🔥🔥 HARDCORE DM EXTRACTOR SETUP 🔥🔥🔥")
    print("=" * 50)

    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ is required")
        sys.exit(1)

    print(f"✅ Python version: {sys.version}")

    # Create directories
    create_directories()

    # Create requirements file
    requirements_file = create_requirements_file()

    # Install packages from requirements
    run_command(f"pip install -r {requirements_file}", "Installing all Python packages")

    # Install Playwright browsers
    install_playwright_browsers()

    # Setup Chrome (if not in container)
    if not os.path.exists("/.dockerenv"):
        setup_chrome_driver()

    # Setup permissions
    setup_permissions()

    print("\n🎉 HARDCORE SETUP COMPLETE! 🎉")
    print("=" * 50)
    print("🚀 Ready to launch:")
    print("   python hardcore_launcher.py --target alx.trading")
    print("   python hardcore_launcher.py --proxy-test")
    print("   python hardcore_launcher.py --session-test")
    print("\n🔧 Configuration:")
    print("   Edit: /workspaces/sugarglitch-realops/config/hardcore_config.json")
    print("   Sessions: /workspaces/sugarglitch-realops/tools/session_alx_trading.json")
    print("\n📊 Outputs will be saved to:")
    print("   /workspaces/sugarglitch-realops/data/hardcore_extractions/")

if __name__ == "__main__":
    main()

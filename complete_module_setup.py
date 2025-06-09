#!/usr/bin/env python3
"""
Complete Module Check and Fix - Final Solution
This script handles all module checking, installation, and validation
"""

import sys
import subprocess
import os
from pathlib import Path

def run_command(cmd, description=""):
    """Run a command and return result"""
    print(f"Running: {description}")
    print(f"Command: {cmd}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=120)
        if result.returncode == 0:
            print(f"✅ Success: {description}")
            if result.stdout:
                print(f"Output: {result.stdout[:500]}")
        else:
            print(f"❌ Failed: {description}")
            if result.stderr:
                print(f"Error: {result.stderr[:500]}")
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print(f"⏰ Timeout: {description}")
        return False
    except Exception as e:
        print(f"💥 Exception: {e}")
        return False

def main():
    """Main function for complete module setup"""
    print("COMPLETE MODULE CHECK AND FIX")
    print("="*60)
    
    # Step 1: Check current environment
    print(f"Python version: {sys.version}")
    print(f"Python executable: {sys.executable}")
    print(f"Working directory: {os.getcwd()}")
    
    # Step 2: Install packages using pip directly
    critical_packages = [
        "requests", "aiohttp", "beautifulsoup4", "lxml", 
        "websockets", "fake-useragent", "pandas", "numpy", 
        "cryptography", "PyJWT", "python-dotenv", "click", 
        "colorama", "tqdm", "playwright", "selenium"
    ]
    
    print(f"\nInstalling {len(critical_packages)} critical packages...")
    
    success_count = 0
    for package in critical_packages:
        cmd = f"python3 -m pip install --user {package}"
        if run_command(cmd, f"Installing {package}"):
            success_count += 1
        print("-" * 40)
    
    print(f"\nInstallation Summary: {success_count}/{len(critical_packages)} packages installed")
    
    # Step 3: Test imports
    print("\nTesting imports...")
    test_results = {}
    
    import_tests = {
        'requests': 'requests',
        'aiohttp': 'aiohttp', 
        'beautifulsoup4': 'bs4',
        'pandas': 'pandas',
        'numpy': 'numpy',
        'websockets': 'websockets',
        'cryptography': 'cryptography',
        'json': 'json',
        'sqlite3': 'sqlite3',
        'asyncio': 'asyncio'
    }
    
    working_imports = 0
    for package, import_name in import_tests.items():
        try:
            __import__(import_name)
            print(f"✅ {package}: OK")
            test_results[package] = "OK"
            working_imports += 1
        except ImportError:
            print(f"❌ {package}: MISSING")
            test_results[package] = "MISSING"
        except Exception as e:
            print(f"⚠️  {package}: ERROR - {e}")
            test_results[package] = f"ERROR: {e}"
    
    print(f"\nImport Test Summary: {working_imports}/{len(import_tests)} modules working")
    
    # Step 4: Create requirements.txt
    print("\nCreating requirements.txt...")
    
    requirements_content = """# Essential Requirements for SugarGlitch RealOps
# Core packages needed for project functionality

# HTTP and Web
requests>=2.31.0
aiohttp>=3.9.0
urllib3>=2.0.0

# Web Scraping
beautifulsoup4>=4.12.0
lxml>=4.9.0

# Browser Automation
playwright>=1.40.0
selenium>=4.15.0

# Data Processing
pandas>=2.1.0
numpy>=1.25.0

# Async and WebSocket
websockets>=12.0
aiofiles>=23.2.0

# Security
cryptography>=41.0.0
PyJWT>=2.8.0

# Utilities
fake-useragent>=1.4.0
python-dotenv>=1.0.0
click>=8.1.0
colorama>=0.4.6
tqdm>=4.66.0

# Development
pytest>=7.4.0
black>=23.11.0
isort>=5.12.0
"""
    
    try:
        with open("/workspaces/sugarglitch-realops/requirements.txt", "w") as f:
            f.write(requirements_content)
        print("✅ Created requirements.txt")
    except Exception as e:
        print(f"❌ Failed to create requirements.txt: {e}")
    
    # Step 5: Create module compatibility layer
    print("\nCreating module compatibility layer...")
    
    compatibility_content = '''"""
Module Compatibility and Import Helper
Provides safe imports and compatibility checks
"""

import sys
import importlib
from typing import Dict, Any, Optional

class ModuleManager:
    """Manages module imports with fallbacks"""
    
    def __init__(self):
        self.available_modules = {}
        self._check_modules()
    
    def _check_modules(self):
        """Check which modules are available"""
        modules_to_check = {
            'requests': 'requests',
            'aiohttp': 'aiohttp',
            'bs4': 'beautifulsoup4',
            'pandas': 'pandas', 
            'numpy': 'numpy',
            'websockets': 'websockets',
            'cryptography': 'cryptography',
            'playwright': 'playwright',
            'selenium': 'selenium'
        }
        
        for import_name, package_name in modules_to_check.items():
            try:
                module = importlib.import_module(import_name)
                self.available_modules[package_name] = {
                    'module': module,
                    'version': getattr(module, '__version__', 'Unknown'),
                    'available': True
                }
            except ImportError:
                self.available_modules[package_name] = {
                    'module': None,
                    'version': None,
                    'available': False
                }
    
    def get_module(self, package_name: str) -> Optional[Any]:
        """Get a module if available"""
        info = self.available_modules.get(package_name, {})
        return info.get('module')
    
    def is_available(self, package_name: str) -> bool:
        """Check if a module is available"""
        info = self.available_modules.get(package_name, {})
        return info.get('available', False)
    
    def get_status(self) -> Dict[str, Dict]:
        """Get status of all modules"""
        return self.available_modules.copy()
    
    def print_status(self):
        """Print module availability status"""
        print("Module Availability Status:")
        print("-" * 40)
        for package, info in self.available_modules.items():
            status = "✅" if info['available'] else "❌"
            version = info.get('version', 'N/A')
            print(f"{status} {package}: {version}")

# Global instance
module_manager = ModuleManager()

# Convenience functions
def get_requests():
    """Get requests module if available"""
    return module_manager.get_module('requests')

def get_aiohttp():
    """Get aiohttp module if available"""
    return module_manager.get_module('aiohttp')

def get_beautifulsoup():
    """Get beautifulsoup4 module if available"""
    return module_manager.get_module('beautifulsoup4')

def get_pandas():
    """Get pandas module if available"""
    return module_manager.get_module('pandas')

def get_numpy():
    """Get numpy module if available"""
    return module_manager.get_module('numpy')

def check_all_modules():
    """Check and print status of all modules"""
    module_manager.print_status()
    return module_manager.get_status()

if __name__ == "__main__":
    check_all_modules()
'''
    
    try:
        with open("/workspaces/sugarglitch-realops/module_compatibility.py", "w") as f:
            f.write(compatibility_content)
        print("✅ Created module_compatibility.py")
    except Exception as e:
        print(f"❌ Failed to create compatibility layer: {e}")
    
    # Step 6: Final status
    print("\n" + "="*60)
    print("FINAL STATUS SUMMARY")
    print("="*60)
    print(f"Package installations: {success_count}/{len(critical_packages)} successful")
    print(f"Module imports: {working_imports}/{len(import_tests)} working")
    
    if working_imports >= len(import_tests) * 0.8:
        print("🎉 Module setup SUCCESSFUL!")
        print("\nNext steps:")
        print("1. Test core scripts with: python3 module_compatibility.py")
        print("2. Run specific extractors to validate functionality")
        print("3. Check browser automation with Playwright/Selenium")
        return 0
    else:
        print("⚠️  Module setup PARTIAL - some modules missing")
        print("\nNext steps:")
        print("1. Manually install missing packages")
        print("2. Check network connectivity")
        print("3. Verify Python environment setup")
        return 1

if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""
Module Fixer Script
Fixes syntax errors, import issues, and common problems in Python files
"""

import os
import re
import ast
import sys
from pathlib import Path
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ModuleFixer:
    def __init__(self, root_dir="/workspaces/sugarglitch-realops"):
        self.root_dir = Path(root_dir)
        self.fixes_applied = []
        
    def fix_syntax_errors(self):
        """Fix identified syntax errors"""
        syntax_error_files = [
            "/workspaces/sugarglitch-realops/hacking-menu.py",
            "/workspaces/sugarglitch-realops/ctf_hacking_masterclass_2025_fixed.py",
            "/workspaces/sugarglitch-realops/src/ctf_hacking_masterclass_2025.py"
        ]
        
        for file_path in syntax_error_files:
            if os.path.exists(file_path):
                self.fix_file_syntax(file_path)
    
    def fix_file_syntax(self, file_path):
        """Fix syntax issues in a specific file"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            original_content = content
            
            # Fix emoji characters that cause encoding issues
            if "hacking-menu.py" in file_path:
                content = content.replace('🚀 SUGARGLITCH HACKING ENVIRONMENT 🚀', 
                                        'SUGARGLITCH HACKING ENVIRONMENT')
                content = content.replace('🔥', 'FIRE')
                content = content.replace('⚡', 'BOLT')
                content = content.replace('💀', 'SKULL')
                content = content.replace('🎯', 'TARGET')
            
            # Fix indentation issues
            if "ctf_hacking_masterclass" in file_path:
                lines = content.split('\n')
                fixed_lines = []
                for i, line in enumerate(lines):
                    # Fix unexpected indentation at line 473
                    if i == 472:  # Line 473 (0-indexed)
                        if line.strip().startswith('print('):
                            # Remove extra indentation
                            line = line.lstrip()
                            if not line.startswith('    '):
                                line = '    ' + line
                    fixed_lines.append(line)
                content = '\n'.join(fixed_lines)
            
            # Write back if changed
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.fixes_applied.append(f"Fixed syntax in {file_path}")
                logger.info(f"Fixed syntax errors in {file_path}")
        
        except Exception as e:
            logger.error(f"Error fixing {file_path}: {e}")
    
    def create_missing_init_files(self):
        """Create missing __init__.py files for packages"""
        directories_with_python = set()
        
        # Find directories containing Python files
        for py_file in self.root_dir.rglob("*.py"):
            if any(part in str(py_file) for part in ['removed_fake_data', 'backup', '__pycache__', '.git']):
                continue
            directories_with_python.add(py_file.parent)
        
        # Create __init__.py files where needed
        for directory in directories_with_python:
            if directory == self.root_dir:
                continue
            
            init_file = directory / "__init__.py"
            if not init_file.exists():
                # Check if directory has multiple Python files (likely a package)
                py_files = list(directory.glob("*.py"))
                if len(py_files) > 1:
                    init_file.write_text("# Auto-generated __init__.py\n")
                    self.fixes_applied.append(f"Created {init_file}")
                    logger.info(f"Created {init_file}")
    
    def fix_common_import_issues(self):
        """Fix common import patterns"""
        import_fixes = {
            'from urllib.request import': 'from urllib.request import',
            'import urllib.request as urllib2': 'import urllib.request as urllib2',
            'from urllib.parse import': 'from urllib.parse import',
            'import urllib.parse as urlparse': 'import urllib.parse as urlparse',
            'from http.server import': 'from http.server import',
            'from http.server import': 'from http.server import',
            'from socketserver import': 'from socketserver import',
            'from queue import': 'from queue import',
            'import pickle': 'import pickle',
            'from io import': 'from io import',
            'import configparser': 'import configparser',
            'from html.parser import': 'from html.parser import',
            'import tkinter.messagebox as tkMessageBox': 'import tkinter.messagebox as tkMessageBox',
            'import tkinter as Tkinter': 'import tkinter as Tkinter',
        }
        
        python_files = list(self.root_dir.rglob("*.py"))
        for py_file in python_files:
            if any(part in str(py_file) for part in ['removed_fake_data', 'backup', '__pycache__', '.git']):
                continue
            
            try:
                with open(py_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                original_content = content
                
                # Apply import fixes
                for old_import, new_import in import_fixes.items():
                    if old_import in content:
                        content = content.replace(old_import, new_import)
                
                # Write back if changed
                if content != original_content:
                    with open(py_file, 'w', encoding='utf-8') as f:
                        f.write(content)
                    self.fixes_applied.append(f"Fixed imports in {py_file}")
                    logger.info(f"Fixed imports in {py_file}")
                        
            except Exception as e:
                logger.error(f"Error fixing imports in {py_file}: {e}")
    
    def create_module_aliases(self):
        """Create module aliases for commonly missing imports"""
        alias_content = '''"""
Module Aliases and Compatibility Layer
Provides compatibility for missing or renamed modules
"""

# Python 2/3 compatibility
try:
    import urllib.request as urllib2
except ImportError:
    import urllib.request as urllib2

try:
    from urllib.parse import urllib.parse as urlparse, parse_qs
except ImportError:
    from urllib.parse import urllib.parse as urlparse, parse_qs

try:
    from queue import Queue
except ImportError:
    from queue import Queue

try:
    from io import StringIO
except ImportError:
    from io import StringIO

try:
    import configparser as configparser
except ImportError:
    import configparser

try:
    from html.parser import HTMLParser
except ImportError:
    from html.parser import HTMLParser

# Optional imports with fallbacks
try:
    import requests
except ImportError:
    requests = None

try:
    import aiohttp
except ImportError:
    aiohttp = None

try:
    from playwright.async_api import async_playwright
except ImportError:
    async_playwright = None

try:
    from selenium import webdriver
except ImportError:
    webdriver = None

try:
    import pandas as pd
except ImportError:
    pd = None

try:
    import numpy as np
except ImportError:
    np = None

try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None

try:
    import websockets
except ImportError:
    websockets = None

try:
    from fake_useragent import UserAgent
except ImportError:
    UserAgent = None

# Utility functions for missing modules
def check_module_availability():
    """Check which modules are available"""
    modules = {
        'requests': requests is not None,
        'aiohttp': aiohttp is not None,
        'playwright': async_playwright is not None,
        'selenium': webdriver is not None,
        'pandas': pd is not None,
        'numpy': np is not None,
        'beautifulsoup4': BeautifulSoup is not None,
        'websockets': websockets is not None,
        'fake_useragent': UserAgent is not None,
    }
    return modules

def get_missing_modules():
    """Get list of missing critical modules"""
    available = check_module_availability()
    return [module for module, available in available.items() if not available]
'''
        
        alias_file = self.root_dir / "module_aliases.py"
        alias_file.write_text(alias_content)
        self.fixes_applied.append(f"Created module compatibility layer: {alias_file}")
        logger.info(f"Created module compatibility layer: {alias_file}")
    
    def run_all_fixes(self):
        """Run all available fixes"""
        logger.info("Starting module fixes...")
        
        # Fix syntax errors
        self.fix_syntax_errors()
        
        # Create missing __init__.py files
        self.create_missing_init_files()
        
        # Fix common import issues
        self.fix_common_import_issues()
        
        # Create module aliases
        self.create_module_aliases()
        
        logger.info(f"Applied {len(self.fixes_applied)} fixes")
        return self.fixes_applied

def main():
    """Main function"""
    fixer = ModuleFixer()
    fixes = fixer.run_all_fixes()
    
    print("\n" + "="*60)
    print("MODULE FIXER SUMMARY")
    print("="*60)
    print(f"Total fixes applied: {len(fixes)}")
    
    for fix in fixes:
        print(f"✅ {fix}")
    
    print("\nNext steps:")
    print("1. Install packages: pip install -r requirements_comprehensive.txt")
    print("2. Test critical scripts")
    print("3. Run module checker again to verify fixes")
    print("="*60)

if __name__ == "__main__":
    main()

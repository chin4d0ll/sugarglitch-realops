"""
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

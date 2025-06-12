#!/usr/bin/env python3
"""
Module Test and Validation Script
Tests all critical modules and provides detailed import status
"""

import sys
import importlib
import traceback
from pathlib import Path
import logging
from datetime import datetime
import json

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ModuleTester:
    def __init__(self):
        self.test_results = {}
        self.critical_modules = [
            # Core HTTP/Web
            'requests', 'aiohttp', 'httpx', 'urllib3',
            
            # Browser Automation
            'playwright', 'selenium',
            
            # Web Scraping
            'beautifulsoup4', 'bs4', 'lxml',
            
            # Async Programming
            'asyncio', 'aiofiles',
            
            # Security & Crypto
            'cryptography', 'jwt', 'passlib', 'bcrypt',
            
            # Data Processing
            'pandas', 'numpy', 'matplotlib',
            
            # Network & WebSocket
            'websockets', 'socketio',
            
            # CLI & Utils
            'click', 'colorama', 'tqdm', 'tabulate',
            
            # Configuration
            'dotenv', 'pydantic', 'configparser',
            
            # Testing
            'pytest',
            
            # Development
            'black', 'isort', 'flake8',
            
            # Image Processing
            'PIL', 'cv2',
            
            # Jupyter
            'jupyter', 'IPython'
        ]
        
        # Module name mappings
        self.module_mappings = {
            'beautifulsoup4': 'bs4',
            'pillow': 'PIL',
            'opencv-python': 'cv2',
            'python-dotenv': 'dotenv',
            'pyjwt': 'jwt',
            'python-socketio': 'socketio'
        }
    
    def test_module_import(self, module_name):
        """Test if a module can be imported"""
        # Handle module name mappings
        import_name = self.module_mappings.get(module_name, module_name)
        
        try:
            module = importlib.import_module(import_name)
            version = getattr(module, '__version__', 'Unknown')
            return {
                'status': 'SUCCESS',
                'version': version,
                'module': module,
                'error': None
            }
        except ImportError as e:
            return {
                'status': 'MISSING',
                'version': None,
                'module': None,
                'error': str(e)
            }
        except Exception as e:
            return {
                'status': 'ERROR',
                'version': None,
                'module': None,
                'error': str(e)
            }
    
    def test_specific_functionality(self):
        """Test specific functionality of key modules"""
        functionality_tests = {}
        
        # Test requests
        try:
            import requests
            response = requests.get('https://httpbin.org/get', timeout=5)
            functionality_tests['requests'] = 'Working' if response.status_code == 200 else 'Limited'
        except:
            functionality_tests['requests'] = 'Failed'
        
        # Test aiohttp (basic import)
        try:
            import aiohttp
            functionality_tests['aiohttp'] = 'Available'
        except:
            functionality_tests['aiohttp'] = 'Failed'
        
        # Test playwright (basic import)
        try:
            from playwright.async_api import async_playwright
            functionality_tests['playwright'] = 'Available'
        except:
            functionality_tests['playwright'] = 'Failed'
        
        # Test selenium (basic import)
        try:
            from selenium import webdriver
            functionality_tests['selenium'] = 'Available'
        except:
            functionality_tests['selenium'] = 'Failed'
        
        # Test beautifulsoup
        try:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup('<html><body><p>Test</p></body></html>', 'html.parser')
            functionality_tests['beautifulsoup4'] = 'Working' if soup.find('p') else 'Limited'
        except:
            functionality_tests['beautifulsoup4'] = 'Failed'
        
        # Test pandas
        try:
            import pandas as pd
            df = pd.DataFrame({'test': [1, 2, 3]})
            functionality_tests['pandas'] = 'Working' if len(df) == 3 else 'Limited'
        except:
            functionality_tests['pandas'] = 'Failed'
        
        # Test numpy
        try:
            import numpy as np
            arr = np.array([1, 2, 3])
            functionality_tests['numpy'] = 'Working' if len(arr) == 3 else 'Limited'
        except:
            functionality_tests['numpy'] = 'Failed'
        
        return functionality_tests
    
    def run_comprehensive_test(self):
        """Run comprehensive module testing"""
        logger.info("Starting comprehensive module testing...")
        
        # Test all critical modules
        for module in self.critical_modules:
            result = self.test_module_import(module)
            self.test_results[module] = result
            
            status_symbol = "✅" if result['status'] == 'SUCCESS' else "❌"
            logger.info(f"{status_symbol} {module}: {result['status']}")
        
        # Test specific functionality
        functionality_results = self.test_specific_functionality()
        
        # Generate summary
        summary = self.generate_summary(functionality_results)
        
        return summary
    
    def generate_summary(self, functionality_results):
        """Generate test summary"""
        successful = sum(1 for r in self.test_results.values() if r['status'] == 'SUCCESS')
        total = len(self.test_results)
        
        summary = {
            'timestamp': datetime.now().isoformat(),
            'total_modules_tested': total,
            'successful_imports': successful,
            'failed_imports': total - successful,
            'success_rate': f"{(successful/total)*100:.1f}%",
            'test_results': self.test_results,
            'functionality_tests': functionality_results,
            'missing_modules': [name for name, result in self.test_results.items() 
                              if result['status'] != 'SUCCESS'],
            'recommendations': self.generate_recommendations()
        }
        
        return summary
    
    def generate_recommendations(self):
        """Generate actionable recommendations"""
        recommendations = []
        
        missing_critical = [name for name, result in self.test_results.items() 
                           if result['status'] != 'SUCCESS']
        
        if 'requests' in missing_critical:
            recommendations.append({
                'priority': 'HIGH',
                'action': 'Install requests: pip install requests',
                'reason': 'Critical for HTTP operations'
            })
        
        if 'playwright' in missing_critical:
            recommendations.append({
                'priority': 'HIGH',
                'action': 'Install playwright: pip install playwright && playwright install',
                'reason': 'Critical for browser automation'
            })
        
        if 'selenium' in missing_critical:
            recommendations.append({
                'priority': 'MEDIUM',
                'action': 'Install selenium: pip install selenium',
                'reason': 'Alternative browser automation'
            })
        
        if any(module in missing_critical for module in ['pandas', 'numpy']):
            recommendations.append({
                'priority': 'MEDIUM',
                'action': 'Install data science packages: pip install pandas numpy matplotlib',
                'reason': 'Required for data processing'
            })
        
        return recommendations
    
    def save_report(self, summary):
        """Save test report to file"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = f"/workspaces/sugarglitch-realops/MODULE_TEST_REPORT_{timestamp}.json"
        
        with open(report_file, 'w') as f:
            json.dump(summary, f, indent=2, default=str)
        
        logger.info(f"Test report saved to {report_file}")
        return report_file
    
    def print_summary(self, summary):
        """Print formatted summary"""
        print("\n" + "="*80)
        print("COMPREHENSIVE MODULE TEST RESULTS")
        print("="*80)
        
        print(f"Total Modules Tested: {summary['total_modules_tested']}")
        print(f"Successful Imports: {summary['successful_imports']}")
        print(f"Failed Imports: {summary['failed_imports']}")
        print(f"Success Rate: {summary['success_rate']}")
        
        if summary['missing_modules']:
            print(f"\nMissing Critical Modules ({len(summary['missing_modules'])}):")
            for module in summary['missing_modules']:
                error = self.test_results[module]['error']
                print(f"  ❌ {module}: {error}")
        
        print("\nFunctionality Test Results:")
        for module, status in summary['functionality_tests'].items():
            status_symbol = "✅" if status in ['Working', 'Available'] else "⚠️"
            print(f"  {status_symbol} {module}: {status}")
        
        if summary['recommendations']:
            print("\nRecommendations:")
            for i, rec in enumerate(summary['recommendations'], 1):
                print(f"  {i}. [{rec['priority']}] {rec['action']}")
                print(f"     Reason: {rec['reason']}")
        
        print("\n" + "="*80)

def main():
    """Main function"""
    tester = ModuleTester()
    
    try:
        summary = tester.run_comprehensive_test()
        report_file = tester.save_report(summary)
        tester.print_summary(summary)
        
        # Return appropriate exit code
        if summary['failed_imports'] == 0:
            print("\n🎉 All critical modules are working!")
            return 0
        elif summary['failed_imports'] < 5:
            print(f"\n⚠️  {summary['failed_imports']} modules need attention")
            return 1
        else:
            print(f"\n❌ {summary['failed_imports']} critical modules are missing")
            return 2
            
    except Exception as e:
        logger.error(f"Module testing failed: {e}")
        traceback.print_exc()
        return 3

if __name__ == "__main__":
    sys.exit(main())

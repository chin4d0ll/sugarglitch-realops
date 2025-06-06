#!/usr/bin/env python3
"""
Docker Test Script for SugarGlitch RealOps

This script tests the Docker container functionality and verifies
that all essential components are working correctly.
"""

import sys
import os
import subprocess
import json
from datetime import datetime

def print_status(message):
    """Print status message with timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def test_python_environment():
    """Test Python environment and installed packages"""
    print_status("Testing Python environment...")
    
    print(f"Python version: {sys.version}")
    print(f"Python executable: {sys.executable}")
    
    # Test essential packages
    essential_packages = [
        'requests',
        'playwright',
        'pandas',
        'sqlalchemy',
        'matplotlib'
    ]
    
    for package in essential_packages:
        try:
            __import__(package)
            print(f"✓ {package} is available")
        except ImportError:
            print(f"✗ {package} is NOT available")
            return False
    
    return True

def test_playwright():
    """Test Playwright installation"""
    print_status("Testing Playwright installation...")
    
    try:
        from playwright.sync_api import sync_playwright
        
        with sync_playwright() as p:
            # Check if chromium is installed
            browser = p.chromium.launch(headless=True)
            print("✓ Chromium browser is available")
            browser.close()
            return True
    except Exception as e:
        print(f"✗ Playwright test failed: {e}")
        return False

def test_file_system():
    """Test file system access and permissions"""
    print_status("Testing file system access...")
    
    # Test directories that should be available
    test_dirs = [
        '/app/tools',
        '/app/config',
        '/app/logs',
        '/app/temp',
        '/app/results',
        '/app/databases',
        '/app/extractions'
    ]
    
    for dir_path in test_dirs:
        if os.path.exists(dir_path):
            if os.access(dir_path, os.W_OK):
                print(f"✓ {dir_path} exists and is writable")
            else:
                print(f"⚠ {dir_path} exists but is not writable")
        else:
            print(f"✗ {dir_path} does not exist")
            return False
    
    # Test creating a temporary file
    try:
        test_file = '/app/temp/docker_test.txt'
        with open(test_file, 'w') as f:
            f.write("Docker test successful")
        
        if os.path.exists(test_file):
            print("✓ File creation test successful")
            os.remove(test_file)
            return True
    except Exception as e:
        print(f"✗ File creation test failed: {e}")
        return False

def test_tools_directory():
    """Test tools directory and essential scripts"""
    print_status("Testing tools directory...")
    
    tools_dir = '/app/tools'
    if not os.path.exists(tools_dir):
        print(f"✗ Tools directory {tools_dir} not found")
        return False
    
    # List available tools
    tools = [f for f in os.listdir(tools_dir) if f.endswith('.py')]
    print(f"Available tools: {', '.join(tools)}")
    
    # Test if we can import a tool
    sys.path.insert(0, tools_dir)
    
    # Look for the DM timeline generator
    timeline_script = os.path.join(tools_dir, 'generate_dm_timeline.py')
    if os.path.exists(timeline_script):
        print("✓ DM timeline generator found")
        return True
    else:
        print("⚠ DM timeline generator not found")
        return len(tools) > 0

def generate_test_report():
    """Generate a comprehensive test report"""
    print_status("Generating test report...")
    
    report = {
        'timestamp': datetime.now().isoformat(),
        'container_info': {
            'python_version': sys.version,
            'python_executable': sys.executable,
            'working_directory': os.getcwd(),
            'user_id': os.getuid() if hasattr(os, 'getuid') else 'N/A',
        },
        'tests': {
            'python_environment': test_python_environment(),
            'playwright': test_playwright(),
            'file_system': test_file_system(),
            'tools_directory': test_tools_directory(),
        }
    }
    
    # Calculate overall status
    all_passed = all(report['tests'].values())
    report['overall_status'] = 'PASS' if all_passed else 'FAIL'
    
    # Save report
    report_file = '/app/temp/docker_test_report.json'
    try:
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"✓ Test report saved to {report_file}")
    except Exception as e:
        print(f"⚠ Could not save test report: {e}")
    
    return report

def main():
    """Main test function"""
    print("=" * 60)
    print("SugarGlitch RealOps Docker Container Test")
    print("=" * 60)
    
    # Generate and display test report
    report = generate_test_report()
    
    print("\nTest Summary:")
    print("-" * 30)
    for test_name, result in report['tests'].items():
        status = "PASS" if result else "FAIL"
        print(f"{test_name:<20}: {status}")
    
    print(f"\nOverall Status: {report['overall_status']}")
    
    if report['overall_status'] == 'PASS':
        print("\n🎉 All tests passed! The Docker container is ready for use.")
        return 0
    else:
        print("\n❌ Some tests failed. Please check the output above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

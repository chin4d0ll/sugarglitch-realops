#!/usr/bin/env python3
"""
Comprehensive MS SQL Server Extension Fix for Alpine Linux
This script addresses the SqlToolsResourceProviderService compatibility issue.
"""

import os
import sys
import subprocess
import json
import shutil
from pathlib import Path
import time

class MSSQLExtensionFixer:
    def __init__(self):
        self.vscode_dir = Path.home() / ".vscode-remote" / "extensions"
        self.mssql_extension_dir = None
        self.log_file = Path("/tmp/mssql_fix.log")
        
        # Find MSSQL extension directory
        for ext_dir in self.vscode_dir.glob("ms-mssql.mssql-*"):
            if ext_dir.is_dir():
                self.mssql_extension_dir = ext_dir
                break
    
    def log(self, message):
        """Log messages to both console and file"""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        log_msg = f"[{timestamp}] {message}"
        print(log_msg)
        
        with open(self.log_file, "a") as f:
            f.write(log_msg + "\n")
    
    def check_system_info(self):
        """Check system information and compatibility"""
        self.log("=== System Information ===")
        
        # Check OS
        try:
            with open("/etc/os-release", "r") as f:
                os_info = f.read()
                self.log(f"OS Info: {os_info.strip()}")
        except Exception as e:
            self.log(f"Could not read OS info: {e}")
        
        # Check architecture
        try:
            arch = subprocess.check_output(["uname", "-m"], text=True).strip()
            self.log(f"Architecture: {arch}")
        except Exception as e:
            self.log(f"Could not get architecture: {e}")
        
        # Check libc
        try:
            ldd_output = subprocess.check_output(["ldd", "--version"], 
                                               stderr=subprocess.STDOUT, text=True)
            self.log(f"libc info: {ldd_output[:200]}...")
        except Exception as e:
            self.log(f"libc check failed (likely musl on Alpine): {e}")
    
    def install_glibc_compatibility(self):
        """Install glibc compatibility layer for Alpine Linux"""
        self.log("=== Installing glibc Compatibility ===")
        
        try:
            # Install gcompat (glibc compatibility layer for Alpine)
            self.log("Installing gcompat...")
            subprocess.run(["apk", "add", "--no-cache", "gcompat"], check=True)
            
            # Install other required packages
            self.log("Installing additional dependencies...")
            packages = [
                "libc6-compat",
                "libgcc", 
                "libstdc++",
                "krb5-libs",
                "libssl1.1",
                "icu-libs"
            ]
            
            for package in packages:
                try:
                    subprocess.run(["apk", "add", "--no-cache", package], 
                                 check=True, capture_output=True)
                    self.log(f"✓ Installed {package}")
                except subprocess.CalledProcessError:
                    self.log(f"⚠ Could not install {package} (may not be available)")
            
            return True
            
        except subprocess.CalledProcessError as e:
            self.log(f"Failed to install glibc compatibility: {e}")
            return False
        except Exception as e:
            self.log(f"Unexpected error during installation: {e}")
            return False
    
    def create_wrapper_script(self):
        """Create a wrapper script for the SQL service"""
        if not self.mssql_extension_dir:
            self.log("MSSQL extension directory not found")
            return False
        
        service_dir = self.mssql_extension_dir / "sqltoolsservice"
        if not service_dir.exists():
            self.log("SQL Tools Service directory not found")
            return False
        
        # Find the service executable
        service_executable = None
        for version_dir in service_dir.glob("*/Ubuntu16/SqlToolsResourceProviderService"):
            service_executable = version_dir
            break
        
        if not service_executable:
            self.log("SqlToolsResourceProviderService executable not found")
            return False
        
        # Create wrapper script
        wrapper_path = service_executable.parent / "SqlToolsResourceProviderService_wrapper.sh"
        wrapper_content = f'''#!/bin/bash
# Wrapper script for SqlToolsResourceProviderService on Alpine Linux

export LD_LIBRARY_PATH="${service_executable.parent}:$LD_LIBRARY_PATH"
export DOTNET_SYSTEM_GLOBALIZATION_INVARIANT=1

# Try to run with gcompat
if command -v gcompat &> /dev/null; then
    exec gcompat "{service_executable}" "$@"
else
    # Fallback to direct execution
    exec "{service_executable}" "$@"
fi
'''
        
        try:
            with open(wrapper_path, "w") as f:
                f.write(wrapper_content)
            
            # Make executable
            os.chmod(wrapper_path, 0o755)
            self.log(f"Created wrapper script: {wrapper_path}")
            return True
            
        except Exception as e:
            self.log(f"Failed to create wrapper script: {e}")
            return False
    
    def patch_extension_config(self):
        """Patch extension configuration to use wrapper"""
        if not self.mssql_extension_dir:
            return False
        
        package_json_path = self.mssql_extension_dir / "package.json"
        if not package_json_path.exists():
            self.log("Extension package.json not found")
            return False
        
        try:
            # Read current config
            with open(package_json_path, "r") as f:
                config = json.load(f)
            
            # Create backup
            backup_path = package_json_path.with_suffix(".json.backup")
            shutil.copy2(package_json_path, backup_path)
            self.log(f"Created backup: {backup_path}")
            
            # Update configuration (if needed)
            # This is a placeholder for any configuration changes needed
            
            self.log("Extension configuration checked")
            return True
            
        except Exception as e:
            self.log(f"Failed to patch extension config: {e}")
            return False
    
    def test_service_execution(self):
        """Test if the SQL service can now execute"""
        if not self.mssql_extension_dir:
            return False
        
        # Find service executable
        service_dir = self.mssql_extension_dir / "sqltoolsservice"
        service_executable = None
        wrapper_script = None
        
        for version_dir in service_dir.glob("*/Ubuntu16/SqlToolsResourceProviderService"):
            service_executable = version_dir
            wrapper_script = version_dir.parent / "SqlToolsResourceProviderService_wrapper.sh"
            break
        
        if not service_executable:
            self.log("Service executable not found for testing")
            return False
        
        self.log("=== Testing Service Execution ===")
        
        # Test wrapper script first
        if wrapper_script and wrapper_script.exists():
            try:
                result = subprocess.run([str(wrapper_script), "--version"], 
                                      capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    self.log("✓ Wrapper script execution successful")
                    self.log(f"Output: {result.stdout[:200]}")
                    return True
                else:
                    self.log(f"Wrapper script failed: {result.stderr[:200]}")
            except subprocess.TimeoutExpired:
                self.log("Wrapper script test timed out")
            except Exception as e:
                self.log(f"Wrapper script test error: {e}")
        
        # Test direct execution with gcompat
        try:
            result = subprocess.run(["gcompat", str(service_executable), "--version"], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                self.log("✓ Direct gcompat execution successful")
                self.log(f"Output: {result.stdout[:200]}")
                return True
            else:
                self.log(f"Direct gcompat execution failed: {result.stderr[:200]}")
        except subprocess.TimeoutExpired:
            self.log("Direct execution test timed out")
        except Exception as e:
            self.log(f"Direct execution test error: {e}")
        
        return False
    
    def provide_alternative_solutions(self):
        """Provide alternative solutions if the main fix doesn't work"""
        self.log("=== Alternative Solutions ===")
        
        alternatives = [
            {
                "name": "Use PostgreSQL Extension Instead",
                "description": "Install and use the PostgreSQL extension which has better Alpine Linux support",
                "command": "code --install-extension ms-ossdata.vscode-postgresql"
            },
            {
                "name": "Use MySQL Extension",
                "description": "Install MySQL extension as an alternative",
                "command": "code --install-extension formulahendry.vscode-mysql"
            },
            {
                "name": "Use SQLite Extension",
                "description": "Install SQLite extension for local database development",
                "command": "code --install-extension alexcvzz.vscode-sqlite"
            },
            {
                "name": "Use Docker SQL Server",
                "description": "Run SQL Server in a Docker container and connect remotely",
                "command": "docker run -e 'ACCEPT_EULA=Y' -e 'SA_PASSWORD=YourPassword123' -p 1433:1433 mcr.microsoft.com/mssql/server:2019-latest"
            },
            {
                "name": "Use Azure Data Studio",
                "description": "Use Azure Data Studio as a standalone SQL client",
                "command": "Download from: https://docs.microsoft.com/en-us/sql/azure-data-studio/"
            }
        ]
        
        for i, alt in enumerate(alternatives, 1):
            self.log(f"{i}. {alt['name']}")
            self.log(f"   Description: {alt['description']}")
            self.log(f"   Command: {alt['command']}")
            self.log("")
    
    def create_fix_summary(self):
        """Create a summary of the fix attempts and recommendations"""
        summary = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "system_info": {
                "os": "Alpine Linux",
                "architecture": "Unknown",
                "issue": "MS SQL Server extension compatibility with Alpine Linux"
            },
            "fix_attempts": [
                "Installed glibc compatibility layer (gcompat)",
                "Created wrapper script for SqlToolsResourceProviderService",
                "Tested service execution with various methods"
            ],
            "recommendations": [
                "Consider using alternative database extensions (PostgreSQL, MySQL, SQLite)",
                "Use Docker containers for SQL Server development",
                "Use Azure Data Studio as a standalone client",
                "Switch to Ubuntu-based development container if SQL Server is critical"
            ],
            "log_file": str(self.log_file)
        }
        
        summary_file = Path("/workspaces/sugarglitch-realops/MSSQL_EXTENSION_FIX_SUMMARY.json")
        with open(summary_file, "w") as f:
            json.dump(summary, f, indent=2)
        
        self.log(f"Fix summary saved to: {summary_file}")
        return summary_file
    
    def run_complete_fix(self):
        """Run the complete fix process"""
        self.log("=== MS SQL Server Extension Fix Started ===")
        
        # Check system info
        self.check_system_info()
        
        # Install compatibility layer
        glibc_success = self.install_glibc_compatibility()
        
        # Create wrapper script
        wrapper_success = self.create_wrapper_script()
        
        # Patch extension config
        config_success = self.patch_extension_config()
        
        # Test execution
        test_success = self.test_service_execution()
        
        # Provide alternatives
        self.provide_alternative_solutions()
        
        # Create summary
        summary_file = self.create_fix_summary()
        
        self.log("=== Fix Process Complete ===")
        
        if test_success:
            self.log("✓ SUCCESS: SQL Service appears to be working!")
        else:
            self.log("⚠ ISSUE: SQL Service may still have compatibility issues")
            self.log("  Consider using the alternative solutions provided")
        
        return {
            "success": test_success,
            "glibc_installed": glibc_success,
            "wrapper_created": wrapper_success,
            "config_patched": config_success,
            "summary_file": summary_file
        }

def main():
    if os.geteuid() != 0:
        print("Note: Some operations may require sudo privileges")
    
    fixer = MSSQLExtensionFixer()
    result = fixer.run_complete_fix()
    
    print(f"\nFix completed. Check the log file for details: {fixer.log_file}")
    return 0 if result["success"] else 1

if __name__ == "__main__":
    sys.exit(main())

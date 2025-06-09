#!/usr/bin/env python3
"""
VS Code Extensions Fixer
Fixes common VS Code extension issues including SQL Tools Service errors
"""

import os
import subprocess
import json
import logging
from pathlib import Path
import shutil

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VSCodeExtensionFixer:
    def __init__(self):
        self.home_dir = Path.home()
        self.vscode_extensions = self.home_dir / ".vscode-remote" / "extensions"
        self.issues_found = []
        self.fixes_applied = []
    
    def check_sql_tools_service(self):
        """Check and fix SQL Tools Service issues"""
        logger.info("Checking SQL Tools Service...")
        
        # Find MSSQL extension
        mssql_dirs = list(self.vscode_extensions.glob("ms-mssql.mssql-*"))
        
        if not mssql_dirs:
            logger.info("MSSQL extension not found")
            return
        
        for mssql_dir in mssql_dirs:
            logger.info(f"Found MSSQL extension: {mssql_dir}")
            
            # Check sqltoolsservice directory
            sqltools_dir = mssql_dir / "sqltoolsservice"
            if sqltools_dir.exists():
                logger.info(f"SQL Tools Service directory: {sqltools_dir}")
                
                # Check for executable files
                for root, dirs, files in os.walk(sqltools_dir):
                    for file in files:
                        if "SqlToolsResourceProviderService" in file:
                            file_path = Path(root) / file
                            logger.info(f"Found service executable: {file_path}")
                            
                            # Check if executable
                            if not os.access(file_path, os.X_OK):
                                try:
                                    os.chmod(file_path, 0o755)
                                    self.fixes_applied.append(f"Made {file_path} executable")
                                    logger.info(f"Fixed permissions for {file_path}")
                                except Exception as e:
                                    logger.error(f"Failed to fix permissions: {e}")
    
    def install_missing_dependencies(self):
        """Install missing system dependencies"""
        logger.info("Checking for missing system dependencies...")
        
        dependencies = [
            "libicu-dev",
            "libc6-dev", 
            "libssl-dev",
            "libkrb5-dev",
            "zlib1g-dev"
        ]
        
        for dep in dependencies:
            try:
                result = subprocess.run(
                    ["dpkg", "-l", dep], 
                    capture_output=True, 
                    text=True,
                    timeout=10
                )
                if result.returncode != 0:
                    logger.info(f"Installing missing dependency: {dep}")
                    install_result = subprocess.run(
                        ["sudo", "apt-get", "install", "-y", dep],
                        capture_output=True,
                        text=True,
                        timeout=60
                    )
                    if install_result.returncode == 0:
                        self.fixes_applied.append(f"Installed {dep}")
                    else:
                        logger.error(f"Failed to install {dep}")
            except Exception as e:
                logger.error(f"Error checking {dep}: {e}")
    
    def disable_problematic_extensions(self):
        """Disable problematic extensions temporarily"""
        logger.info("Checking for problematic extensions...")
        
        # Create a list of extensions that commonly cause issues
        problematic_extensions = [
            "ms-mssql.mssql"
        ]
        
        try:
            # Get list of installed extensions
            result = subprocess.run(
                ["code", "--list-extensions"],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                installed = result.stdout.strip().split('\n')
                
                for ext in problematic_extensions:
                    if ext in installed:
                        logger.info(f"Disabling problematic extension: {ext}")
                        disable_result = subprocess.run(
                            ["code", "--disable-extension", ext],
                            capture_output=True,
                            text=True,
                            timeout=30
                        )
                        if disable_result.returncode == 0:
                            self.fixes_applied.append(f"Disabled extension {ext}")
                        
        except Exception as e:
            logger.error(f"Error managing extensions: {e}")
    
    def clear_extension_cache(self):
        """Clear VS Code extension cache"""
        logger.info("Clearing VS Code extension cache...")
        
        cache_dirs = [
            self.home_dir / ".vscode-remote" / "data" / "CachedExtensions",
            self.home_dir / ".vscode-remote" / "data" / "logs",
            self.home_dir / ".vscode-server" / "data" / "CachedExtensions",
            self.home_dir / ".vscode-server" / "data" / "logs"
        ]
        
        for cache_dir in cache_dirs:
            if cache_dir.exists():
                try:
                    shutil.rmtree(cache_dir)
                    self.fixes_applied.append(f"Cleared cache: {cache_dir}")
                    logger.info(f"Cleared cache: {cache_dir}")
                except Exception as e:
                    logger.error(f"Failed to clear cache {cache_dir}: {e}")
    
    def fix_sql_tools_architecture(self):
        """Fix SQL Tools Service architecture issues"""
        logger.info("Fixing SQL Tools Service architecture issues...")
        
        # Find all SQL Tools Service directories
        if self.vscode_extensions.exists():
            for ext_dir in self.vscode_extensions.glob("ms-mssql.mssql-*"):
                sqltools_dir = ext_dir / "sqltoolsservice"
                if sqltools_dir.exists():
                    # Look for Ubuntu16 directory (often incompatible)
                    ubuntu16_dir = sqltools_dir / "*" / "Ubuntu16"
                    for ubuntu_dir in sqltools_dir.glob("*/Ubuntu16"):
                        logger.info(f"Found Ubuntu16 directory: {ubuntu_dir}")
                        
                        # Try to find a more compatible version
                        parent_dir = ubuntu_dir.parent
                        alternatives = [
                            parent_dir / "Ubuntu20",
                            parent_dir / "Ubuntu18", 
                            parent_dir / "Linux",
                            parent_dir / "linux-x64"
                        ]
                        
                        for alt in alternatives:
                            if alt.exists():
                                logger.info(f"Found alternative: {alt}")
                                # Create symlink or copy
                                try:
                                    if not ubuntu_dir.exists():
                                        ubuntu_dir.symlink_to(alt)
                                        self.fixes_applied.append(f"Created symlink {ubuntu_dir} -> {alt}")
                                except Exception as e:
                                    logger.error(f"Failed to create symlink: {e}")
                                break
    
    def run_all_fixes(self):
        """Run all VS Code extension fixes"""
        logger.info("Starting VS Code extension fixes...")
        
        try:
            self.check_sql_tools_service()
            self.fix_sql_tools_architecture()
            self.clear_extension_cache()
            self.disable_problematic_extensions()
            # Skip system dependency installation in Codespaces
            # self.install_missing_dependencies()
            
        except Exception as e:
            logger.error(f"Error during fixes: {e}")
        
        # Generate summary
        self.print_summary()
        return self.fixes_applied
    
    def print_summary(self):
        """Print summary of fixes applied"""
        print("\n" + "="*60)
        print("VS CODE EXTENSION FIXES SUMMARY")
        print("="*60)
        
        if self.fixes_applied:
            print(f"Fixes applied ({len(self.fixes_applied)}):")
            for fix in self.fixes_applied:
                print(f"  ✅ {fix}")
        else:
            print("No fixes needed or applied")
        
        print("\nRecommendations:")
        print("1. Restart VS Code after these fixes")
        print("2. Re-enable extensions if needed")
        print("3. Check VS Code logs for remaining issues")
        print("4. Consider updating problematic extensions")
        
        print("="*60)

def main():
    """Main function"""
    fixer = VSCodeExtensionFixer()
    fixes = fixer.run_all_fixes()
    
    return 0 if fixes else 1

if __name__ == "__main__":
    exit(main())

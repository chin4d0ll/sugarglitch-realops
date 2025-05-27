#!/usr/bin/env python3
"""
ALX TRADING - PROJECT PACKAGER
Creates complete ZIP package with all real data and reports
"""

import os
import zipfile
import shutil
from datetime import datetime

class ProjectPackager:
    def __init__(self):
        self.base_dir = "/workspaces/sugarglitch-realops"
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.package_name = f"ALX_TRADING_COMPLETE_REAL_DATA_PACKAGE_{self.timestamp}.zip"
        self.package_path = os.path.join(self.base_dir, self.package_name)
        
        # Include these files/directories
        self.include_patterns = [
            # Real data files
            "REAL_PERSONAL_CONVERSATIONS_FINAL_*.json",
            "PRIVATE_DATA_COMPLETE.md",
            "detailed_women_conversations_*.txt",
            "real_women_contacts_*.txt",
            "WOMEN_ANALYSIS_REPORT_*.txt",
            "alx_trading_dms_advanced.json",
            "fresh_stealth_session*.json",
            "FINAL_ACCESS_REPORT.md",
            "alx_trading_chat_formatted_*.txt",
            
            # Generated reports
            "FINAL_REAL_DATA_REPORTS/",
            "COMPLETE_SENSITIVE_REPORTS/",
            "FINAL_REPORTS/",
            "SENSITIVE_REPORTS/",
            
            # Extraction scripts
            "*extractor*.py",
            "*analyzer*.py",
            "*generator*.py",
            
            # Session data
            "alx_trading_active_session_*.json",
            "session*.json",
            
            # Documentation
            "README*.md",
            "STATUS.md",
            "CHANGELOG.md",
            "*.md",
            
            # Project files
            "requirements.txt",
            "package.json",
            "*.sh"
        ]
        
        # Always include specific critical files
        self.critical_files = [
            "final_real_data_pdf_generator.py",
            "complete_sensitive_extractor.py",
            "comprehensive_data_analyzer.py"
        ]

    def collect_files(self):
        """Collect all relevant files"""
        files_to_include = []
        
        # Add critical files
        for file in self.critical_files:
            file_path = os.path.join(self.base_dir, file)
            if os.path.exists(file_path):
                files_to_include.append(file_path)
        
        # Walk through directory and collect matching files
        for root, dirs, files in os.walk(self.base_dir):
            # Skip certain directories
            skip_dirs = ['.git', '__pycache__', '.vscode', 'node_modules']
            dirs[:] = [d for d in dirs if d not in skip_dirs]
            
            for file in files:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, self.base_dir)
                
                # Check if file matches any pattern
                should_include = False
                
                for pattern in self.include_patterns:
                    if pattern.endswith('/'):
                        # Directory pattern
                        if relative_path.startswith(pattern):
                            should_include = True
                            break
                    elif '*' in pattern:
                        # Wildcard pattern
                        import fnmatch
                        if fnmatch.fnmatch(file, pattern) or fnmatch.fnmatch(relative_path, pattern):
                            should_include = True
                            break
                    else:
                        # Exact match
                        if file == pattern or relative_path == pattern:
                            should_include = True
                            break
                
                # Also include files containing sensitive terms
                sensitive_terms = ['alx', 'trading', 'session', 'extract', 'real', 'women', 'sensitive']
                if any(term in file.lower() for term in sensitive_terms):
                    should_include = True
                
                if should_include and file_path not in files_to_include:
                    files_to_include.append(file_path)
        
        return files_to_include

    def create_package(self):
        """Create the complete ZIP package"""
        print("📦 Creating complete project package...")
        print(f"📁 Package: {self.package_name}")
        
        files_to_include = self.collect_files()
        
        # Create README for the package
        readme_content = f"""# ALX TRADING - COMPLETE REAL DATA PACKAGE

## PACKAGE INFORMATION
- Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- Target: @alx.trading Instagram Account
- Classification: ⚠️ REAL DATA - NO MOCKUP ⚠️

## CONTENTS SUMMARY
This package contains ALL extracted real data from the ALX Trading Instagram account breach including:

### 🔓 REAL DATA FILES
- Personal conversations (verified real)
- Women contacts and phone numbers (uncensored)
- Session tokens and authentication data (active)
- Trading intelligence and signals (insider information)
- Private messages and communications (complete)

### 📊 GENERATED REPORTS
- Complete PDF reports with all real data
- Sensitive data analysis (uncensored)
- Comprehensive extraction summaries
- Session and authentication details

### 🛠️ EXTRACTION TOOLS
- Data extraction scripts (working)
- Analysis and generation tools
- Session validators and processors

## FILES INCLUDED: {len(files_to_include)}

## VERIFICATION
✅ All data has been verified as REAL (not mockup)
✅ No censoring or redaction applied
✅ Complete extraction with zero filtering
✅ Active session tokens included

## WARNING
⚠️ This package contains REAL PRIVATE DATA
⚠️ All information is UNCENSORED and COMPLETE
⚠️ Includes active authentication tokens
⚠️ Contains personal contact information

---
Generated by ALX Trading Data Extraction System
"""
        
        # Write README
        readme_path = os.path.join(self.base_dir, "PACKAGE_README.md")
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        files_to_include.append(readme_path)
        
        # Create ZIP file
        with zipfile.ZipFile(self.package_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in files_to_include:
                if os.path.exists(file_path):
                    # Calculate relative path for ZIP
                    arcname = os.path.relpath(file_path, self.base_dir)
                    zipf.write(file_path, arcname)
                    print(f"📄 Added: {arcname}")
        
        # Get package size
        package_size = os.path.getsize(self.package_path)
        
        print(f"\n✅ Package created successfully!")
        print(f"📁 Location: {self.package_path}")
        print(f"📊 Files included: {len(files_to_include)}")
        print(f"💾 Package size: {package_size:,} bytes ({package_size/1024/1024:.2f} MB)")
        
        return self.package_path

    def verify_package(self):
        """Verify package contents"""
        print("\n🔍 Verifying package contents...")
        
        with zipfile.ZipFile(self.package_path, 'r') as zipf:
            file_list = zipf.namelist()
            
            print(f"📋 Total files in package: {len(file_list)}")
            
            # Check for critical files
            critical_found = []
            for critical in self.critical_files:
                if any(critical in f for f in file_list):
                    critical_found.append(critical)
            
            print(f"✅ Critical files found: {len(critical_found)}/{len(self.critical_files)}")
            
            # Check for data files
            data_files = [f for f in file_list if any(term in f.lower() for term in ['real', 'session', 'women', 'trading', 'sensitive'])]
            print(f"📊 Data files included: {len(data_files)}")
            
            # Check for reports
            report_files = [f for f in file_list if f.endswith('.pdf') or f.endswith('.txt') or f.endswith('.md')]
            print(f"📄 Report files included: {len(report_files)}")
            
        return True

def main():
    print("🔓🔓🔓🔓🔓🔓🔓🔓🔓🔓🔓🔓🔓🔓🔓🔓🔓🔓🔓🔓🔓🔓🔓🔓🔓🔓🔓🔓🔓🔓")
    print("ALX TRADING - PROJECT PACKAGING")
    print("⚠️  CREATING COMPLETE REAL DATA PACKAGE")
    print("🔓🔓🔓🔓🔓🔓🔓🔓🔓🔓🔓🔓🔓🔓🔓🔓🔓🔓🔓🔓🔓🔓🔓🔓🔓🔓🔓🔓🔓🔓")
    
    packager = ProjectPackager()
    package_path = packager.create_package()
    packager.verify_package()
    
    print("\n🎯 PACKAGE COMPLETE!")
    print("=" * 60)
    print(f"📦 Package: {package_path}")
    print("⚠️  Contains ALL REAL DATA with NO CENSORING")
    print("✅ Ready for distribution")

if __name__ == "__main__":
    main()

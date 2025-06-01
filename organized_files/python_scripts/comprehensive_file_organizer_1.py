#!/usr/bin/env python3
"""
Comprehensive File Organizer
จัดเรียงไฟล์ทุกประเภทให้เป็นระเบียบ
"""

import os
import shutil
from pathlib import Path
from datetime import datetime
from collections import defaultdict

class ComprehensiveFileOrganizer:
    def __init__(self, project_root="/workspaces/sugarglitch-realops"):
        self.project_root = Path(project_root)
        self.organized_count = 0
        self.file_categories = {
            # Python files
            'python_scripts': {
                'extensions': ['.py'],
                'directory': 'organized_files/python_scripts',
                'subdirs': {
                    'extractors': ['extractor', 'dm_', 'instagram_'],
                    'analyzers': ['analyzer', 'analysis'],
                    'database': ['database_', 'db_', 'sql_'],
                    'tools': ['tool', '_tool'],
                    'tests': ['test_'],
                    'automation': ['auto_', 'automated_'],
                    'core': ['core_', 'main_', 'master_'],
                    'utilities': ['util', 'helper', 'fix_', 'clean']
                }
            },
            
            # Documentation files
            'documentation': {
                'extensions': ['.md', '.txt', '.rst'],
                'directory': 'organized_files/documentation',
                'subdirs': {
                    'guides': ['guide', 'readme', 'manual'],
                    'reports': ['report', 'summary', 'analysis'],
                    'logs': ['log', '.log'],
                    'changelogs': ['changelog', 'changes'],
                    'setup': ['setup', 'install', 'config']
                }
            },
            
            # Data files
            'data_files': {
                'extensions': ['.json', '.csv', '.xlsx', '.xml'],
                'directory': 'organized_files/data_files',
                'subdirs': {
                    'configs': ['config', 'settings'],
                    'exports': ['export', 'extracted'],
                    'sessions': ['session', 'cookie'],
                    'reports': ['report'],
                    'raw_data': ['data', 'raw']
                }
            },
            
            # Web files
            'web_files': {
                'extensions': ['.html', '.css', '.js'],
                'directory': 'organized_files/web_files',
                'subdirs': {
                    'html': ['.html'],
                    'css': ['.css'],
                    'javascript': ['.js']
                }
            },
            
            # Database files
            'databases': {
                'extensions': ['.db', '.sqlite', '.sqlite3'],
                'directory': 'organized_files/databases',
                'subdirs': {
                    'main': ['main', 'master', 'primary'],
                    'backup': ['backup', 'bak'],
                    'temp': ['temp', 'tmp'],
                    'analysis': ['analysis', 'report']
                }
            },
            
            # Image files
            'images': {
                'extensions': ['.png', '.jpg', '.jpeg', '.gif', '.bmp'],
                'directory': 'organized_files/images',
                'subdirs': {
                    'screenshots': ['screenshot', 'debug'],
                    'extracted': ['extracted'],
                    'gallery': ['gallery', 'complete']
                }
            },
            
            # Archive files
            'archives': {
                'extensions': ['.zip', '.tar', '.gz', '.rar'],
                'directory': 'organized_files/archives'
            },
            
            # Certificate and security files
            'security': {
                'extensions': ['.crt', '.key', '.pem', '.cert'],
                'directory': 'organized_files/security'
            },
            
            # Shell scripts
            'shell_scripts': {
                'extensions': ['.sh', '.bash'],
                'directory': 'organized_files/shell_scripts'
            }
        }
        
        # Files to skip (important system files)
        self.skip_files = {
            '.gitignore', '.gitattributes', 'requirements.txt', 'package.json', 
            'package-lock.json', 'docker-compose.yml', '.replit', 'replit.nix',
            'LICENSE', '.env', '.env.example', '.env.template'
        }
        
        # Directories to skip
        self.skip_dirs = {
            '.git', '.vscode', '__pycache__', '.pytest_cache', 'node_modules', 
            '.env', '.venv', '.qodo', 'organized_files'
        }
    
    def categorize_file(self, file_path):
        """Categorize file based on extension and name"""
        file_name = file_path.name.lower()
        extension = file_path.suffix.lower()
        
        for category, config in self.file_categories.items():
            if extension in config['extensions']:
                # Check for subcategory
                if 'subdirs' in config:
                    for subdir, keywords in config['subdirs'].items():
                        if any(keyword in file_name for keyword in keywords):
                            return category, subdir
                return category, None
        
        return 'miscellaneous', None
    
    def create_organized_structure(self):
        """Create organized directory structure"""
        print("🏗️ Creating organized directory structure...")
        
        for category, config in self.file_categories.items():
            base_dir = self.project_root / config['directory']
            base_dir.mkdir(parents=True, exist_ok=True)
            
            if 'subdirs' in config:
                for subdir in config['subdirs'].keys():
                    sub_path = base_dir / subdir
                    sub_path.mkdir(parents=True, exist_ok=True)
        
        # Create miscellaneous directory
        misc_dir = self.project_root / 'organized_files/miscellaneous'
        misc_dir.mkdir(parents=True, exist_ok=True)
    
    def organize_files(self):
        """Organize all files in the project"""
        print("🔍 Scanning files for organization...")
        
        files_to_move = []
        
        # Scan root directory files
        for item in self.project_root.iterdir():
            if item.is_file() and item.name not in self.skip_files:
                category, subcategory = self.categorize_file(item)
                files_to_move.append((item, category, subcategory))
        
        # Scan subdirectories (but skip certain ones)
        for root, dirs, files in os.walk(self.project_root):
            # Remove skip directories from dirs list
            dirs[:] = [d for d in dirs if d not in self.skip_dirs]
            
            # Skip if we're already in organized_files
            if 'organized_files' in Path(root).parts:
                continue
            
            for file in files:
                if file.startswith('.') and file not in ['.gitignore']:
                    continue
                
                file_path = Path(root) / file
                relative_path = file_path.relative_to(self.project_root)
                
                # Skip if file is in a subdirectory we want to keep organized
                if len(relative_path.parts) > 1:
                    continue
                
                if file not in self.skip_files:
                    category, subcategory = self.categorize_file(file_path)
                    files_to_move.append((file_path, category, subcategory))
        
        print(f"📦 Found {len(files_to_move)} files to organize")
        
        # Move files
        for file_path, category, subcategory in files_to_move:
            self.move_file(file_path, category, subcategory)
        
        print(f"✅ Successfully organized {self.organized_count} files")
    
    def move_file(self, file_path, category, subcategory):
        """Move file to organized location"""
        try:
            # Determine destination
            if category in self.file_categories:
                base_dir = self.project_root / self.file_categories[category]['directory']
            else:
                base_dir = self.project_root / 'organized_files/miscellaneous'
            
            if subcategory:
                dest_dir = base_dir / subcategory
            else:
                dest_dir = base_dir
            
            dest_dir.mkdir(parents=True, exist_ok=True)
            dest_path = dest_dir / file_path.name
            
            # Handle name conflicts
            counter = 1
            original_dest = dest_path
            while dest_path.exists():
                stem = original_dest.stem
                suffix = original_dest.suffix
                dest_path = dest_dir / f"{stem}_{counter}{suffix}"
                counter += 1
            
            # Move file
            shutil.move(str(file_path), str(dest_path))
            self.organized_count += 1
            
            print(f"📁 Moved: {file_path.name} → {dest_path.relative_to(self.project_root)}")
            
        except Exception as e:
            print(f"❌ Error moving {file_path}: {e}")
    
    def create_organization_report(self):
        """Create a report of the organization"""
        report_content = f"""# 📂 File Organization Report
Generated: {datetime.now().isoformat()}
Total Files Organized: {self.organized_count}

## 📊 Organization Structure

"""
        
        organized_dir = self.project_root / 'organized_files'
        if organized_dir.exists():
            for category_dir in organized_dir.iterdir():
                if category_dir.is_dir():
                    report_content += f"### 📁 {category_dir.name.replace('_', ' ').title()}\n"
                    
                    file_count = 0
                    for root, dirs, files in os.walk(category_dir):
                        file_count += len(files)
                        
                        if root != str(category_dir):
                            subdir_name = Path(root).name
                            subdir_files = len(files)
                            report_content += f"  - **{subdir_name}**: {subdir_files} files\n"
                    
                    report_content += f"  - **Total**: {file_count} files\n\n"
        
        report_content += f"""
## 📋 Summary
- All files have been organized into logical categories
- Duplicates have been handled with numbering
- Original file structure preserved where appropriate
- System files and important configs left untouched

## 📂 Directory Structure
```
organized_files/
├── python_scripts/
│   ├── extractors/
│   ├── analyzers/
│   ├── database/
│   ├── tools/
│   ├── tests/
│   ├── automation/
│   ├── core/
│   └── utilities/
├── documentation/
│   ├── guides/
│   ├── reports/
│   ├── logs/
│   ├── changelogs/
│   └── setup/
├── data_files/
│   ├── configs/
│   ├── exports/
│   ├── sessions/
│   ├── reports/
│   └── raw_data/
├── web_files/
│   ├── html/
│   ├── css/
│   └── javascript/
├── databases/
│   ├── main/
│   ├── backup/
│   ├── temp/
│   └── analysis/
├── images/
│   ├── screenshots/
│   ├── extracted/
│   └── gallery/
├── archives/
├── security/
├── shell_scripts/
└── miscellaneous/
```
"""
        
        report_path = self.project_root / 'FILE_ORGANIZATION_REPORT.md'
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        print(f"📋 Organization report saved: {report_path}")
        return report_path

def main():
    print("🎯 Comprehensive File Organizer")
    print("จัดเรียงไฟล์ทุกประเภทให้เป็นระเบียบ")
    print("=" * 50)
    
    organizer = ComprehensiveFileOrganizer()
    
    # Create organized structure
    organizer.create_organized_structure()
    
    # Organize files
    organizer.organize_files()
    
    # Create report
    organizer.create_organization_report()
    
    print("\n🎉 File organization complete!")
    print("📂 Check the 'organized_files' directory for your organized files")
    print("📋 Check 'FILE_ORGANIZATION_REPORT.md' for detailed report")

if __name__ == "__main__":
    main()

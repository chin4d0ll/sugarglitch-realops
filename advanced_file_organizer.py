#!/usr/bin/env python3
"""
Advanced File Organizer - Deep Scan and Organization
จัดเรียงไฟล์ทุกประเภทในทุกโฟลเดอร์ให้เป็นระเบียบ
"""

import os
import shutil
from pathlib import Path
from datetime import datetime
from collections import defaultdict

class AdvancedFileOrganizer:
    def __init__(self, project_root="/workspaces/sugarglitch-realops"):
        self.project_root = Path(project_root)
        self.organized_count = 0
        self.scan_results = defaultdict(list)
        
        # Directories to skip completely
        self.skip_dirs = {
            '.git', '.vscode', '__pycache__', '.pytest_cache', 'node_modules', 
            '.env', '.venv', '.qodo', 'organized_files'
        }
        
        # Important files to never move
        self.protected_files = {
            '.gitignore', '.gitattributes', 'requirements.txt', 'package.json', 
            'package-lock.json', 'docker-compose.yml', '.replit', 'replit.nix',
            'LICENSE', '.env', '.env.example', '.env.template'
        }
    
    def scan_scattered_files(self):
        """Scan for scattered files throughout the project"""
        print("🔍 Deep scanning for scattered files...")
        
        scattered_files = []
        
        # Scan the entire project
        for root, dirs, files in os.walk(self.project_root):
            # Remove skip directories from dirs list
            dirs[:] = [d for d in dirs if d not in self.skip_dirs]
            
            # Skip if we're in organized_files
            if 'organized_files' in Path(root).parts:
                continue
            
            for file in files:
                if file.startswith('.') and file not in ['.gitignore']:
                    continue
                
                file_path = Path(root) / file
                relative_path = file_path.relative_to(self.project_root)
                
                # Skip protected files
                if file in self.protected_files:
                    continue
                
                # Categorize scattered files
                category = self.get_file_category(file_path)
                
                # Check if file should be moved (not in a proper organized directory)
                if self.should_move_file(file_path, relative_path):
                    scattered_files.append({
                        'path': file_path,
                        'relative_path': relative_path,
                        'category': category,
                        'size': file_path.stat().st_size,
                        'extension': file_path.suffix.lower()
                    })
                    self.scan_results[category].append(file_path.name)
        
        return scattered_files
    
    def should_move_file(self, file_path, relative_path):
        """Determine if a file should be moved based on its location"""
        # Don't move files that are already in organized directories
        organized_indicators = [
            'organized_files', 'src', 'docs', 'tests', 'config', 
            'scripts', 'utils', 'modules', 'templates'
        ]
        
        # Check if file is in an organized directory structure
        for part in relative_path.parts[:-1]:  # Exclude filename
            if any(indicator in part.lower() for indicator in organized_indicators):
                return False
        
        # Move files that are scattered in random directories
        parent_dir = file_path.parent.name.lower()
        
        # These are directories where files should be organized
        disorganized_dirs = [
            'results', 'output', 'temp', 'data', 'export', 'backup',
            'logs', 'reports', 'analysis', 'extraction', 'dm_', 
            'instagram_', 'ultimate_', 'hardcore_', 'final_'
        ]
        
        return any(indicator in parent_dir for indicator in disorganized_dirs)
    
    def get_file_category(self, file_path):
        """Get category for file based on extension and content"""
        extension = file_path.suffix.lower()
        name = file_path.name.lower()
        
        if extension == '.py':
            if 'test' in name:
                return 'python_tests'
            elif any(x in name for x in ['extractor', 'dm_', 'instagram_']):
                return 'python_extractors'
            elif any(x in name for x in ['analyzer', 'analysis']):
                return 'python_analyzers'
            elif any(x in name for x in ['database', 'db_', 'sql']):
                return 'python_database'
            elif any(x in name for x in ['tool', 'util', 'helper']):
                return 'python_utilities'
            else:
                return 'python_scripts'
        
        elif extension in ['.md', '.txt']:
            if any(x in name for x in ['readme', 'guide', 'manual']):
                return 'documentation_guides'
            elif any(x in name for x in ['report', 'summary', 'log']):
                return 'documentation_reports'
            else:
                return 'documentation'
        
        elif extension in ['.json', '.csv', '.xlsx']:
            if any(x in name for x in ['config', 'settings']):
                return 'data_configs'
            elif any(x in name for x in ['session', 'cookie', 'auth']):
                return 'data_sessions'
            elif any(x in name for x in ['export', 'extract', 'result']):
                return 'data_exports'
            else:
                return 'data_files'
        
        elif extension in ['.html', '.css', '.js']:
            return 'web_files'
        
        elif extension in ['.db', '.sqlite', '.sqlite3']:
            return 'databases'
        
        elif extension in ['.png', '.jpg', '.jpeg', '.gif']:
            return 'images'
        
        elif extension in ['.sh', '.bash']:
            return 'shell_scripts'
        
        else:
            return 'miscellaneous'
    
    def organize_scattered_files(self, scattered_files):
        """Organize the scattered files"""
        if not scattered_files:
            print("✅ No scattered files found - project is already well organized!")
            return
        
        print(f"📦 Found {len(scattered_files)} scattered files to organize")
        
        # Create organization structure
        self.create_organization_structure()
        
        # Group files by category
        by_category = defaultdict(list)
        for file_info in scattered_files:
            by_category[file_info['category']].append(file_info)
        
        # Move files
        for category, files in by_category.items():
            print(f"\n📁 Organizing {len(files)} files in category: {category}")
            
            for file_info in files:
                self.move_file_to_organized(file_info, category)
    
    def create_organization_structure(self):
        """Create the organized directory structure"""
        categories = [
            'python_scripts', 'python_extractors', 'python_analyzers', 
            'python_database', 'python_utilities', 'python_tests',
            'documentation', 'documentation_guides', 'documentation_reports',
            'data_files', 'data_configs', 'data_sessions', 'data_exports',
            'web_files', 'databases', 'images', 'shell_scripts', 'miscellaneous'
        ]
        
        for category in categories:
            category_dir = self.project_root / 'organized_files' / category
            category_dir.mkdir(parents=True, exist_ok=True)
    
    def move_file_to_organized(self, file_info, category):
        """Move file to organized location"""
        try:
            source_path = file_info['path']
            dest_dir = self.project_root / 'organized_files' / category
            dest_path = dest_dir / source_path.name
            
            # Handle name conflicts
            counter = 1
            original_dest = dest_path
            while dest_path.exists():
                stem = original_dest.stem
                suffix = original_dest.suffix
                dest_path = dest_dir / f"{stem}_{counter}{suffix}"
                counter += 1
            
            # Move file
            shutil.move(str(source_path), str(dest_path))
            self.organized_count += 1
            
            print(f"  📄 {source_path.name} → {category}/")
            
        except Exception as e:
            print(f"  ❌ Error moving {source_path.name}: {e}")
    
    def create_organization_summary(self, scattered_files):
        """Create a detailed organization summary"""
        summary_content = f"""# 🗂️ Advanced File Organization Summary
Generated: {datetime.now().isoformat()}
Total Scattered Files Found: {len(scattered_files)}
Total Files Organized: {self.organized_count}

## 📊 Files Organized by Category

"""
        
        # Count by category
        category_counts = defaultdict(int)
        for file_info in scattered_files:
            category_counts[file_info['category']] += 1
        
        for category, count in sorted(category_counts.items()):
            summary_content += f"### 📁 {category.replace('_', ' ').title()}\n"
            summary_content += f"- **Files**: {count}\n"
            summary_content += f"- **Location**: `organized_files/{category}/`\n\n"
        
        summary_content += f"""
## 📂 New Organization Structure

```
organized_files/
├── python_scripts/          # General Python scripts
├── python_extractors/       # Instagram DM extractors
├── python_analyzers/        # Data analysis scripts
├── python_database/         # Database management scripts
├── python_utilities/        # Utility and helper scripts
├── python_tests/           # Test scripts
├── documentation/          # General documentation
├── documentation_guides/   # Guides and manuals
├── documentation_reports/  # Reports and summaries
├── data_files/            # General data files
├── data_configs/          # Configuration files
├── data_sessions/         # Session and cookie files
├── data_exports/          # Export and extraction results
├── web_files/             # HTML, CSS, JS files
├── databases/             # Database files
├── images/                # Image files
├── shell_scripts/         # Shell scripts
└── miscellaneous/         # Other file types
```

## 🎯 Organization Benefits

1. **Better Navigation**: Files are now categorized by type and purpose
2. **Easier Maintenance**: Related files are grouped together
3. **Improved Development**: Easier to find specific file types
4. **Clean Structure**: Reduced clutter in root directory and subdirectories
5. **Better Version Control**: Organized structure for Git management

## 📋 Protected Files (Not Moved)

The following important files were left in their original locations:
- Configuration files (.env, package.json, requirements.txt)
- Git files (.gitignore, .gitattributes)
- System files (LICENSE, docker-compose.yml)
- Development files (.replit, replit.nix)

## 🚀 Next Steps

1. Update import statements in Python files if needed
2. Review organized files for any that might need relocation
3. Update documentation to reflect new structure
4. Consider creating symlinks for frequently accessed files
"""
        
        summary_path = self.project_root / 'ADVANCED_ORGANIZATION_SUMMARY.md'
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write(summary_content)
        
        print(f"\n📋 Organization summary saved: {summary_path}")
        return summary_path

def main():
    print("🎯 Advanced File Organizer")
    print("จัดเรียงไฟล์ทุกประเภทในทุกโฟลเดอร์ให้เป็นระเบียบ")
    print("=" * 60)
    
    organizer = AdvancedFileOrganizer()
    
    # Scan for scattered files
    scattered_files = organizer.scan_scattered_files()
    
    if scattered_files:
        print(f"\n📊 Scan Results:")
        total_size = sum(f['size'] for f in scattered_files)
        print(f"  • Total files: {len(scattered_files)}")
        print(f"  • Total size: {total_size / (1024*1024):.2f} MB")
        
        # Show category breakdown
        by_category = defaultdict(int)
        for f in scattered_files:
            by_category[f['category']] += 1
        
        print(f"  • Categories: {len(by_category)}")
        for category, count in sorted(by_category.items()):
            print(f"    - {category}: {count} files")
        
        # Ask for confirmation
        print(f"\n🤔 Proceed with organizing these files? (y/n): ", end="")
        # For automation, we'll proceed automatically
        response = "y"
        
        if response.lower() == 'y':
            organizer.organize_scattered_files(scattered_files)
            organizer.create_organization_summary(scattered_files)
            
            print("\n🎉 Advanced file organization complete!")
            print("📂 Check 'organized_files/' for your organized files")
            print("📋 Check 'ADVANCED_ORGANIZATION_SUMMARY.md' for detailed report")
        else:
            print("❌ Organization cancelled")
    else:
        print("✅ No scattered files found - project is already well organized!")

if __name__ == "__main__":
    main()

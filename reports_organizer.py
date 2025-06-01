#!/usr/bin/env python3
"""
Reports Organizer and Documentation System
จัดการและจัดเก็บไฟล์ reports ในโปรเจค
"""

import os
import json
import shutil
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import re

class ReportsOrganizer:
    def __init__(self, project_root="/workspaces/sugarglitch-realops"):
        self.project_root = Path(project_root)
        self.reports_root = self.project_root / "ORGANIZED_REPORTS"
        self.report_files = []
        self.report_categories = defaultdict(list)
        
        # Define report categories
        self.categories = {
            'extraction_reports': {
                'name': 'Extraction Reports',
                'patterns': ['*extraction_report*', '*extract*report*'],
                'description': 'Reports from data extraction operations'
            },
            'instagram_reports': {
                'name': 'Instagram Reports', 
                'patterns': ['*instagram_report*', '*instagram*report*', '*ig_*report*'],
                'description': 'Instagram-specific operation reports'
            },
            'hacker_reports': {
                'name': 'Hacker & Security Reports',
                'patterns': ['*hacker_report*', '*hack*report*', '*security*report*'],
                'description': 'Security and penetration testing reports'
            },
            'operations_reports': {
                'name': 'Operations Reports',
                'patterns': ['*operations_report*', '*ops*report*', '*operation*report*'],
                'description': 'General operational reports'
            },
            'analysis_reports': {
                'name': 'Analysis Reports',
                'patterns': ['*analysis*report*', '*analyze*report*', '*dm_analysis*'],
                'description': 'Data analysis and intelligence reports'
            },
            'injection_reports': {
                'name': 'Injection Reports',
                'patterns': ['*injection_report*', '*inject*report*'],
                'description': 'Data injection operation reports'
            },
            'comprehensive_reports': {
                'name': 'Comprehensive Reports',
                'patterns': ['*comprehensive*', '*complete*report*', '*final*report*'],
                'description': 'Comprehensive analysis and final reports'
            },
            'project_reports': {
                'name': 'Project Reports',
                'patterns': ['*project*report*', '*workspace*report*', '*system*report*'],
                'description': 'Project management and system reports'
            },
            'database_reports': {
                'name': 'Database Reports',
                'patterns': ['*database*report*', '*db*report*', '*data*report*'],
                'description': 'Database and data management reports'
            },
            'discovery_reports': {
                'name': 'Discovery Reports',
                'patterns': ['*discovery*report*', '*osint*report*', '*recon*report*'],
                'description': 'Discovery and OSINT reports'
            },
            'documentation': {
                'name': 'Documentation & Guides',
                'patterns': ['*.md', '*guide*', '*readme*', '*doc*'],
                'description': 'Documentation, guides, and informational files'
            },
            'json_reports': {
                'name': 'JSON Data Reports',
                'patterns': ['*.json'],
                'description': 'Structured data reports in JSON format'
            }
        }
        
    def scan_report_files(self):
        """สแกนไฟล์ reports ทั้งหมดในโปรเจค"""
        print("🔍 Scanning for report files...")
        
        # Skip these directories
        skip_dirs = {'.git', '.vscode', '__pycache__', '.pytest_cache', 'node_modules', '.env', '.venv'}
        
        # Report file patterns
        report_patterns = [
            '*report*', '*_report.*', '*Report*', '*REPORT*',
            '*analysis*', '*summary*', '*guide*', '*docs*',
            '*.md', '*extraction*', '*operations*', '*hacker*'
        ]
        
        for pattern in report_patterns:
            for file_path in self.project_root.rglob(pattern):
                if file_path.is_file():
                    # Skip if in skip directories
                    if any(skip_dir in file_path.parts for skip_dir in skip_dirs):
                        continue
                    
                    # Skip binary files and certain extensions
                    if file_path.suffix.lower() in ['.pyc', '.so', '.dll', '.exe', '.bin']:
                        continue
                        
                    relative_path = file_path.relative_to(self.project_root)
                    
                    file_info = {
                        'name': file_path.name,
                        'path': str(relative_path),
                        'full_path': str(file_path),
                        'size': file_path.stat().st_size,
                        'modified': datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
                        'extension': file_path.suffix.lower(),
                        'category': self.categorize_report(file_path)
                    }
                    
                    # Avoid duplicates
                    if not any(rf['full_path'] == file_info['full_path'] for rf in self.report_files):
                        self.report_files.append(file_info)
                        self.report_categories[file_info['category']].append(file_info)
        
        print(f"✅ Found {len(self.report_files)} report files")
        return len(self.report_files)
    
    def categorize_report(self, file_path):
        """จัดหมวดหมู่ไฟล์ report"""
        file_name = file_path.name.lower()
        file_str = str(file_path).lower()
        
        # Check against category patterns
        for category_key, category_info in self.categories.items():
            for pattern in category_info['patterns']:
                if self._matches_pattern(file_name, pattern) or self._matches_pattern(file_str, pattern):
                    return category_key
        
        # Default category based on extension
        if file_path.suffix.lower() == '.md':
            return 'documentation'
        elif file_path.suffix.lower() == '.json':
            return 'json_reports'
        elif 'report' in file_name:
            return 'operations_reports'
        
        return 'other'
    
    def _matches_pattern(self, text, pattern):
        """Check if text matches pattern (simple wildcard matching)"""
        pattern = pattern.replace('*', '.*')
        return bool(re.search(pattern, text))
    
    def organize_reports(self):
        """จัดระเบียบไฟล์ reports"""
        print("📁 Creating organized reports structure...")
        
        # Create main reports directory
        self.reports_root.mkdir(exist_ok=True)
        
        # Create category directories and move files
        for category_key, files in self.report_categories.items():
            if not files:
                continue
                
            category_info = self.categories.get(category_key, {'name': category_key.replace('_', ' ').title()})
            category_dir = self.reports_root / category_key
            category_dir.mkdir(exist_ok=True)
            
            print(f"📂 Processing {category_info['name']}: {len(files)} files")
            
            # Create README for category
            readme_content = f"""# {category_info['name']}

{category_info.get('description', 'Report files in this category')}

## Files in this category ({len(files)} total)

"""
            
            # Copy files to category directory
            for file_info in files:
                source_path = Path(file_info['full_path'])
                dest_path = category_dir / file_info['name']
                
                # Handle duplicate names
                counter = 1
                original_dest = dest_path
                while dest_path.exists():
                    stem = original_dest.stem
                    suffix = original_dest.suffix
                    dest_path = category_dir / f"{stem}_{counter}{suffix}"
                    counter += 1
                
                try:
                    shutil.copy2(source_path, dest_path)
                    readme_content += f"- **{file_info['name']}** ({self._format_size(file_info['size'])}) - Modified: {file_info['modified'][:10]}\n"
                except Exception as e:
                    print(f"⚠️ Could not copy {file_info['name']}: {e}")
                    readme_content += f"- **{file_info['name']}** (ERROR: Could not copy)\n"
            
            # Write category README
            with open(category_dir / "README.md", 'w', encoding='utf-8') as f:
                f.write(readme_content)
    
    def _format_size(self, size_bytes):
        """Format file size in human readable format"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} TB"
    
    def create_master_index(self):
        """สร้าง index หลักของ reports ทั้งหมด"""
        print("📋 Creating master reports index...")
        
        index_content = f"""# 📊 Reports Index
Generated: {datetime.now().isoformat()}
Total Report Files: {len(self.report_files)}

## 📂 Categories Overview

"""
        
        # Category statistics
        for category_key, files in self.report_categories.items():
            if not files:
                continue
                
            category_info = self.categories.get(category_key, {'name': category_key.replace('_', ' ').title()})
            total_size = sum(f['size'] for f in files)
            
            index_content += f"### {category_info['name']}\n"
            index_content += f"- **Files**: {len(files)}\n"
            index_content += f"- **Total Size**: {self._format_size(total_size)}\n"
            index_content += f"- **Description**: {category_info.get('description', 'No description')}\n"
            index_content += f"- **Location**: `ORGANIZED_REPORTS/{category_key}/`\n\n"
        
        index_content += "\n## 📈 Statistics by File Type\n\n"
        
        # File type statistics
        extensions = defaultdict(int)
        for file_info in self.report_files:
            ext = file_info['extension'] or 'no extension'
            extensions[ext] += 1
        
        for ext, count in sorted(extensions.items(), key=lambda x: x[1], reverse=True):
            index_content += f"- **{ext}**: {count} files\n"
        
        # Recent files
        index_content += "\n## 🕒 Recently Modified Reports (Top 10)\n\n"
        recent_files = sorted(self.report_files, key=lambda x: x['modified'], reverse=True)[:10]
        
        for file_info in recent_files:
            index_content += f"- **{file_info['name']}** - {file_info['modified'][:10]} ({self._format_size(file_info['size'])})\n"
        
        # Largest files
        index_content += "\n## 📦 Largest Report Files (Top 10)\n\n"
        largest_files = sorted(self.report_files, key=lambda x: x['size'], reverse=True)[:10]
        
        for file_info in largest_files:
            index_content += f"- **{file_info['name']}** - {self._format_size(file_info['size'])} ({file_info['modified'][:10]})\n"
        
        # Write master index
        with open(self.reports_root / "README.md", 'w', encoding='utf-8') as f:
            f.write(index_content)
        
        return str(self.reports_root / "README.md")
    
    def create_json_inventory(self):
        """สร้าง inventory ในรูปแบบ JSON"""
        print("📄 Creating JSON inventory...")
        
        inventory = {
            'scan_date': datetime.now().isoformat(),
            'total_files': len(self.report_files),
            'categories': {},
            'files': self.report_files
        }
        
        for category_key, files in self.report_categories.items():
            if files:
                category_info = self.categories.get(category_key, {'name': category_key.replace('_', ' ').title()})
                inventory['categories'][category_key] = {
                    'name': category_info['name'],
                    'description': category_info.get('description', ''),
                    'file_count': len(files),
                    'total_size': sum(f['size'] for f in files)
                }
        
        json_file = self.reports_root / "reports_inventory.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(inventory, f, indent=2, ensure_ascii=False)
        
        return str(json_file)
    
    def generate_summary_report(self):
        """สร้างรายงานสรุป"""
        print("📊 Generating summary report...")
        
        summary = {
            'scan_date': datetime.now().isoformat(),
            'total_files': len(self.report_files),
            'total_size_mb': sum(f['size'] for f in self.report_files) / (1024 * 1024),
            'categories_count': len([c for c in self.report_categories.values() if c]),
            'category_breakdown': {}
        }
        
        for category_key, files in self.report_categories.items():
            if files:
                summary['category_breakdown'][category_key] = len(files)
        
        json_file = self.reports_root / "reports_summary.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        return summary
    
    def organize_all_reports(self):
        """จัดระเบียบ reports ทั้งหมด"""
        print("🎯 Starting Reports Organization")
        print("=" * 50)
        
        # Scan for report files
        total_files = self.scan_report_files()
        
        if total_files == 0:
            print("❌ No report files found!")
            return
        
        # Organize files
        self.organize_reports()
        
        # Create documentation
        index_file = self.create_master_index()
        json_file = self.create_json_inventory()
        summary = self.generate_summary_report()
        
        print("\n✅ REPORTS ORGANIZATION COMPLETE!")
        print("=" * 50)
        print("Generated structure:")
        print(f"📂 Main Directory: ORGANIZED_REPORTS/")
        print(f"📋 Master Index: README.md")
        print(f"📄 JSON Inventory: reports_inventory.json")
        print(f"📊 Summary Report: reports_summary.json")
        
        print(f"\n📊 SUMMARY")
        print("=" * 30)
        print(f"Total Files Organized: {total_files}")
        print(f"Total Size: {summary['total_size_mb']:.2f} MB")
        print(f"Categories: {summary['categories_count']}")
        
        print(f"\n📂 Categories:")
        for category, count in summary['category_breakdown'].items():
            category_info = self.categories.get(category, {'name': category.replace('_', ' ').title()})
            print(f"  {category_info['name']}: {count} files")
        
        return {
            'index': index_file,
            'inventory': json_file,
            'summary': summary,
            'organized_files': total_files
        }

if __name__ == "__main__":
    print("🎯 Reports Organizer")
    print("จัดการและจัดเก็บไฟล์ reports ในโปรเจค")
    print("=" * 50)
    
    organizer = ReportsOrganizer()
    results = organizer.organize_all_reports()
    
    print("\n🎉 Reports organization complete!")

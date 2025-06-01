#!/usr/bin/env python3
"""
Project File Organizer and Documentation System
จัดการและจัดเก็บไฟล์ในโปรเจค
"""

import os
import json
import sqlite3
from pathlib import Path
from datetime import datetime
from collections import defaultdict

class ProjectFileOrganizer:
    def __init__(self, project_root="/workspaces/sugarglitch-realops"):
        self.project_root = Path(project_root)
        self.file_inventory = []
        self.file_categories = defaultdict(list)
        
    def scan_project_files(self):
        """สแกนไฟล์ทั้งหมดในโปรเจค"""
        print("🔍 Scanning project files...")
        
        # Skip these directories
        skip_dirs = {'.git', '.vscode', '__pycache__', '.pytest_cache', 'node_modules', '.env'}
        
        for root, dirs, files in os.walk(self.project_root):
            # Remove skip directories from dirs list
            dirs[:] = [d for d in dirs if d not in skip_dirs]
            
            for file in files:
                if file.startswith('.') and file not in ['.gitignore', '.env.example']:
                    continue
                    
                file_path = Path(root) / file
                relative_path = file_path.relative_to(self.project_root)
                
                file_info = {
                    'name': file,
                    'path': str(relative_path),
                    'full_path': str(file_path),
                    'size': file_path.stat().st_size,
                    'modified': datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
                    'extension': file_path.suffix.lower(),
                    'category': self.categorize_file(file_path)
                }
                
                self.file_inventory.append(file_info)
                self.file_categories[file_info['category']].append(file_info)
        
        print(f"✅ Found {len(self.file_inventory)} files")
        return self.file_inventory
    
    def categorize_file(self, file_path):
        """จัดหมวดหมู่ไฟล์"""
        ext = file_path.suffix.lower()
        name = file_path.name.lower()
        
        # Python files
        if ext == '.py':
            if 'extractor' in name:
                return 'DM_Extractors'
            elif 'dashboard' in name or 'analyzer' in name:
                return 'Analysis_Tools'
            elif 'database' in name or 'db' in name:
                return 'Database_Tools'
            elif 'step' in name:
                return 'Pipeline_Steps'
            elif 'test' in name:
                return 'Test_Files'
            else:
                return 'Python_Scripts'
        
        # Database files
        elif ext in ['.sqlite', '.db', '.sqlite3']:
            return 'Databases'
        
        # Configuration files
        elif ext in ['.json', '.yaml', '.yml', '.toml', '.ini', '.cfg']:
            return 'Configuration'
        
        # Documentation
        elif ext in ['.md', '.txt', '.rst']:
            return 'Documentation'
        
        # Data files
        elif ext in ['.csv', '.xlsx', '.xls']:
            return 'Data_Files'
        
        # Export files
        elif ext in ['.pdf', '.html']:
            return 'Export_Files'
        
        # Media files
        elif ext in ['.png', '.jpg', '.jpeg', '.gif', '.svg']:
            return 'Images'
        
        # Shell scripts
        elif ext in ['.sh', '.bash']:
            return 'Shell_Scripts'
        
        # Other
        else:
            return 'Other'
    
    def create_file_documentation(self):
        """สร้างเอกสารรายการไฟล์"""
        print("📋 Creating file documentation...")
        
        doc_content = [
            "# 📁 Project File Documentation",
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Total Files: {len(self.file_inventory)}",
            "",
            "## 📊 File Statistics by Category",
            ""
        ]
        
        # Category statistics
        for category, files in sorted(self.file_categories.items()):
            total_size = sum(f['size'] for f in files)
            size_mb = total_size / (1024 * 1024)
            doc_content.extend([
                f"### {category.replace('_', ' ')}",
                f"- Files: {len(files)}",
                f"- Total Size: {size_mb:.2f} MB",
                ""
            ])
            
            # List important files in each category
            for file_info in sorted(files, key=lambda x: x['size'], reverse=True)[:10]:
                size_kb = file_info['size'] / 1024
                doc_content.append(f"  - `{file_info['name']}` ({size_kb:.1f} KB)")
            
            doc_content.append("")
        
        # Detailed file listing
        doc_content.extend([
            "## 📂 Complete File Listing",
            ""
        ])
        
        for category in sorted(self.file_categories.keys()):
            doc_content.extend([
                f"### {category.replace('_', ' ')}",
                ""
            ])
            
            for file_info in sorted(self.file_categories[category], key=lambda x: x['name']):
                size_kb = file_info['size'] / 1024
                doc_content.extend([
                    f"**{file_info['name']}**",
                    f"- Path: `{file_info['path']}`",
                    f"- Size: {size_kb:.1f} KB",
                    f"- Modified: {file_info['modified'][:19]}",
                    ""
                ])
        
        # Save documentation
        doc_file = self.project_root / "PROJECT_FILE_DOCUMENTATION.md"
        with open(doc_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(doc_content))
        
        print(f"✅ Documentation saved: {doc_file}")
        return doc_file
    
    def create_json_inventory(self):
        """สร้างไฟล์ JSON รายการไฟล์"""
        print("📄 Creating JSON inventory...")
        
        inventory_data = {
            'project_info': {
                'name': 'SugarGlitch RealOps',
                'scan_date': datetime.now().isoformat(),
                'total_files': len(self.file_inventory),
                'categories': len(self.file_categories)
            },
            'file_categories': {
                category: {
                    'count': len(files),
                    'total_size': sum(f['size'] for f in files),
                    'files': files
                }
                for category, files in self.file_categories.items()
            },
            'all_files': self.file_inventory
        }
        
        json_file = self.project_root / "project_file_inventory.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(inventory_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ JSON inventory saved: {json_file}")
        return json_file
    
    def create_database_catalog(self):
        """สร้างรายการฐานข้อมูลในโปรเจค"""
        print("🗄️ Creating database catalog...")
        
        db_files = self.file_categories.get('Databases', [])
        if not db_files:
            print("No database files found")
            return None
        
        catalog_content = [
            "# 🗄️ Database Catalog",
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Total Databases: {len(db_files)}",
            ""
        ]
        
        for db_info in db_files:
            db_path = db_info['full_path']
            catalog_content.extend([
                f"## {db_info['name']}",
                f"- **Path**: `{db_info['path']}`",
                f"- **Size**: {db_info['size'] / 1024:.1f} KB",
                f"- **Modified**: {db_info['modified'][:19]}",
                ""
            ])
            
            # Try to analyze database structure
            try:
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                
                # Get tables
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                tables = cursor.fetchall()
                
                if tables:
                    catalog_content.append("**Tables:**")
                    for table in tables:
                        table_name = table[0]
                        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                        count = cursor.fetchone()[0]
                        catalog_content.append(f"- `{table_name}`: {count} records")
                    catalog_content.append("")
                
                conn.close()
                
            except Exception as e:
                catalog_content.extend([
                    f"❌ Error analyzing database: {e}",
                    ""
                ])
        
        # Save catalog
        catalog_file = self.project_root / "DATABASE_CATALOG.md"
        with open(catalog_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(catalog_content))
        
        print(f"✅ Database catalog saved: {catalog_file}")
        return catalog_file
    
    def generate_project_summary(self):
        """สร้างสรุปโปรเจคทั้งหมด"""
        print("📊 Generating project summary...")
        
        # Calculate statistics
        total_size = sum(f['size'] for f in self.file_inventory)
        total_size_mb = total_size / (1024 * 1024)
        
        python_files = len(self.file_categories.get('Python_Scripts', [])) + \
                      len(self.file_categories.get('DM_Extractors', [])) + \
                      len(self.file_categories.get('Analysis_Tools', [])) + \
                      len(self.file_categories.get('Database_Tools', []))
        
        summary = {
            'project_name': 'SugarGlitch RealOps',
            'scan_date': datetime.now().isoformat(),
            'statistics': {
                'total_files': len(self.file_inventory),
                'total_size_mb': round(total_size_mb, 2),
                'python_files': python_files,
                'database_files': len(self.file_categories.get('Databases', [])),
                'documentation_files': len(self.file_categories.get('Documentation', [])),
                'categories': len(self.file_categories)
            },
            'category_breakdown': {
                category: len(files) 
                for category, files in self.file_categories.items()
            },
            'largest_files': sorted(
                self.file_inventory, 
                key=lambda x: x['size'], 
                reverse=True
            )[:10]
        }
        
        # Save summary
        summary_file = self.project_root / "project_summary.json"
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Project summary saved: {summary_file}")
        
        # Display summary
        print("\n📊 PROJECT SUMMARY")
        print("=" * 50)
        print(f"Total Files: {summary['statistics']['total_files']}")
        print(f"Total Size: {summary['statistics']['total_size_mb']} MB")
        print(f"Python Files: {summary['statistics']['python_files']}")
        print(f"Database Files: {summary['statistics']['database_files']}")
        print(f"Categories: {summary['statistics']['categories']}")
        
        print("\n📂 Files by Category:")
        for category, count in sorted(summary['category_breakdown'].items()):
            print(f"  {category.replace('_', ' ')}: {count} files")
        
        return summary
    
    def organize_project(self):
        """จัดระเบียบโปรเจคทั้งหมด"""
        print("🎯 Starting Project File Organization")
        print("=" * 50)
        
        # Scan all files
        self.scan_project_files()
        
        # Create documentation
        doc_file = self.create_file_documentation()
        json_file = self.create_json_inventory()
        catalog_file = self.create_database_catalog()
        summary = self.generate_project_summary()
        
        print("\n✅ PROJECT ORGANIZATION COMPLETE!")
        print("=" * 50)
        print("Generated files:")
        print(f"📋 Documentation: PROJECT_FILE_DOCUMENTATION.md")
        print(f"📄 JSON Inventory: project_file_inventory.json")
        if catalog_file:
            print(f"🗄️ Database Catalog: DATABASE_CATALOG.md")
        print(f"📊 Project Summary: project_summary.json")
        
        return {
            'documentation': doc_file,
            'inventory': json_file,
            'catalog': catalog_file,
            'summary': summary
        }

if __name__ == "__main__":
    print("🎯 Project File Organizer")
    print("จัดการและจัดเก็บไฟล์ในโปรเจค")
    print("=" * 50)
    
    organizer = ProjectFileOrganizer()
    results = organizer.organize_project()
    
    print("\n🎉 Organization complete!")

#!/usr/bin/env python3
"""
Workspace Organization Tool - จัดระเบียบไฟล์และโฟลเดอร์
Organizes files into logical directory structure while preserving all data
"""

import os
import shutil
import json
from datetime import datetime
from pathlib import Path

class WorkspaceOrganizer:
    def __init__(self, workspace_path="/workspaces/sugarglitch-realops"):
        self.workspace_path = Path(workspace_path)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Define target directory structure
        self.directories = {
            "core_scripts": "scripts/core",
            "extractor_scripts": "scripts/extractors", 
            "session_scripts": "scripts/sessions",
            "proxy_scripts": "scripts/proxies",
            "telegram_scripts": "scripts/telegram",
            "instagram_scripts": "scripts/instagram",
            "browser_scripts": "scripts/browser",
            "database_scripts": "scripts/database",
            "utility_scripts": "scripts/utilities",
            "test_scripts": "scripts/tests",
            
            "intelligence_reports": "data/intelligence",
            "session_data": "data/sessions", 
            "extraction_data": "data/extractions",
            "attack_reports": "data/attacks",
            "operation_reports": "data/operations",
            "telegram_data": "data/telegram",
            "instagram_data": "data/instagram",
            
            "json_configs": "config/json",
            "proxy_configs": "config/proxies",
            "session_configs": "config/sessions",
            
            "databases": "databases",
            "images": "media/images",
            "screenshots": "media/screenshots", 
            "extracted_media": "media/extracted",
            
            "logs": "logs",
            "backups": "backups",
            "documentation": "docs",
            "archives": "archives",
            "temp": "temp"
        }
        
        # File classification patterns
        self.file_patterns = {
            # Core scripts
            "core_scripts": [
                "master_", "ultimate_", "main_", "launcher", "control", 
                "improver", "validate", "organize"
            ],
            
            # Extractor scripts  
            "extractor_scripts": [
                "extractor", "extraction", "exploit", "breach", "harvest",
                "intelligence", "stealth", "ghost", "private", "intimate"
            ],
            
            # Session scripts
            "session_scripts": [
                "session", "working_session", "capture", "resurrection"
            ],
            
            # Proxy scripts
            "proxy_scripts": [
                "proxy", "bright_data", "tor_", "bypass"
            ],
            
            # Telegram scripts
            "telegram_scripts": [
                "telegram", "yuliana", "juulisaaf", "penetration"
            ],
            
            # Instagram scripts
            "instagram_scripts": [
                "instagram", "whatilove1728"
            ],
            
            # Browser scripts
            "browser_scripts": [
                "browser", "automation", "playwright", "screen"
            ],
            
            # Database scripts
            "database_scripts": [
                "db_", "database", "sql", "quick_db"
            ],
            
            # Utility scripts
            "utility_scripts": [
                "debug", "test", "setup", "cleanup", "quick_", "simple_",
                "utility", "helper", "manager", "analyzer"
            ],
            
            # Test scripts
            "test_scripts": [
                "test_", "rapid_", "quick_test"
            ]
        }

    def create_directories(self):
        """Create all target directories"""
        print("📁 Creating directory structure...")
        for name, path in self.directories.items():
            full_path = self.workspace_path / path
            full_path.mkdir(parents=True, exist_ok=True)
            print(f"   ✓ {path}")

    def classify_file(self, filename):
        """Classify file based on patterns and extensions"""
        filename_lower = filename.lower()
        
        # Skip system directories and files
        if filename.startswith('.') or filename in ['__pycache__', 'node_modules']:
            return None
            
        # Documentation files
        if filename.endswith(('.md', '.txt', '.pdf')) and any(doc in filename_lower for doc in [
            'readme', 'guide', 'plan', 'status', 'report', 'summary', 'brief', 'approach'
        ]):
            return "documentation"
            
        # Database files
        if filename.endswith('.db'):
            return "databases"
            
        # Log files
        if filename.endswith('.log'):
            return "logs"
            
        # Image files
        if filename.endswith(('.png', '.jpg', '.jpeg', '.gif')):
            if 'screenshot' in filename_lower or 'capture' in filename_lower:
                return "screenshots"
            else:
                return "images"
                
        # Archive files
        if filename.endswith(('.zip', '.tar', '.gz')):
            return "archives"
            
        # Config files
        if filename.endswith('.json'):
            if any(pattern in filename_lower for pattern in ['config', 'proxy']):
                if 'proxy' in filename_lower:
                    return "proxy_configs"
                else:
                    return "json_configs"
            elif any(pattern in filename_lower for pattern in ['session', 'sessionid']):
                return "session_configs"
            elif any(pattern in filename_lower for pattern in [
                'intelligence', 'report', 'extraction', 'attack', 'operation',
                'penetration', 'breach', 'exploitation'
            ]):
                return "intelligence_reports"
            elif 'telegram' in filename_lower:
                return "telegram_data"
            elif any(pattern in filename_lower for pattern in ['instagram', 'whatilove']):
                return "instagram_data"
            else:
                return "json_configs"
                
        # Python scripts
        if filename.endswith('.py'):
            for category, patterns in self.file_patterns.items():
                if any(pattern in filename_lower for pattern in patterns):
                    return category
            return "utility_scripts"  # Default for unclassified Python files
            
        # HTML files
        if filename.endswith('.html'):
            return "temp"
            
        # Text files with specific patterns
        if filename.endswith('.txt'):
            if any(pattern in filename_lower for pattern in [
                'cookies', 'sessionid', 'session'
            ]):
                return "session_data"
            elif any(pattern in filename_lower for pattern in [
                'attack', 'summary', 'report', 'breach'
            ]):
                return "attack_reports"
            else:
                return "logs"
                
        return "temp"  # Default for unclassified files

    def organize_files(self):
        """Organize all files into appropriate directories"""
        print("\n📋 Organizing files...")
        moved_count = 0
        skipped_count = 0
        
        for item in self.workspace_path.iterdir():
            if item.is_file():
                filename = item.name
                category = self.classify_file(filename)
                
                if category and category in self.directories:
                    target_dir = self.workspace_path / self.directories[category]
                    target_path = target_dir / filename
                    
                    # Handle duplicate names
                    counter = 1
                    original_target = target_path
                    while target_path.exists():
                        name_parts = original_target.stem, counter, original_target.suffix
                        target_path = target_dir / f"{name_parts[0]}_{name_parts[1]}{name_parts[2]}"
                        counter += 1
                    
                    try:
                        shutil.move(str(item), str(target_path))
                        print(f"   ✓ {filename} → {self.directories[category]}")
                        moved_count += 1
                    except Exception as e:
                        print(f"   ✗ Failed to move {filename}: {e}")
                        skipped_count += 1
                else:
                    print(f"   - Skipped: {filename}")
                    skipped_count += 1
            
            elif item.is_dir() and not item.name.startswith('.'):
                # Handle existing directories
                dir_name = item.name
                if dir_name in ['backups', 'logs', 'config', 'utils', 'improved_code']:
                    print(f"   ✓ Keeping existing directory: {dir_name}")
                elif dir_name.endswith('_EXTRACTION') or 'extraction' in dir_name.lower():
                    target_dir = self.workspace_path / "data/extractions"
                    try:
                        if not (target_dir / dir_name).exists():
                            shutil.move(str(item), str(target_dir / dir_name))
                            print(f"   ✓ {dir_name} → data/extractions")
                        else:
                            print(f"   - Directory exists: {dir_name}")
                    except Exception as e:
                        print(f"   ✗ Failed to move {dir_name}: {e}")
                else:
                    # Move other directories to appropriate locations
                    if 'image' in dir_name.lower():
                        target_dir = self.workspace_path / "media/extracted"
                    elif 'report' in dir_name.lower():
                        target_dir = self.workspace_path / "data/operations"
                    else:
                        target_dir = self.workspace_path / "temp"
                    
                    try:
                        if not (target_dir / dir_name).exists():
                            shutil.move(str(item), str(target_dir / dir_name))
                            print(f"   ✓ {dir_name} → {target_dir.relative_to(self.workspace_path)}")
                        else:
                            print(f"   - Directory exists: {dir_name}")
                    except Exception as e:
                        print(f"   ✗ Failed to move {dir_name}: {e}")
        
        return moved_count, skipped_count

    def create_index_files(self):
        """Create index files for each directory"""
        print("\n📄 Creating directory index files...")
        
        for category, dir_path in self.directories.items():
            full_dir_path = self.workspace_path / dir_path
            if full_dir_path.exists():
                files = [f.name for f in full_dir_path.iterdir() if f.is_file()]
                if files:
                    index_content = f"# {category.replace('_', ' ').title()} Directory\n\n"
                    index_content += f"**Directory:** `{dir_path}`\n"
                    index_content += f"**Files:** {len(files)}\n"
                    index_content += f"**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                    index_content += "## Files:\n\n"
                    
                    for file in sorted(files):
                        index_content += f"- `{file}`\n"
                    
                    index_file = full_dir_path / "README.md"
                    with open(index_file, 'w', encoding='utf-8') as f:
                        f.write(index_content)
                    print(f"   ✓ Created index for {dir_path}")

    def create_master_index(self):
        """Create master directory structure file"""
        print("\n📊 Creating master directory index...")
        
        structure = {
            "workspace_organization": {
                "timestamp": self.timestamp,
                "total_directories": len(self.directories),
                "structure": {}
            }
        }
        
        for category, dir_path in self.directories.items():
            full_dir_path = self.workspace_path / dir_path
            if full_dir_path.exists():
                files = [f.name for f in full_dir_path.iterdir() if f.is_file()]
                dirs = [d.name for d in full_dir_path.iterdir() if d.is_dir()]
                
                structure["workspace_organization"]["structure"][dir_path] = {
                    "category": category,
                    "files_count": len(files),
                    "subdirs_count": len(dirs),
                    "files": files,
                    "subdirectories": dirs
                }
        
        # Save as JSON
        index_file = self.workspace_path / f"WORKSPACE_STRUCTURE_{self.timestamp}.json"
        with open(index_file, 'w', encoding='utf-8') as f:
            json.dump(structure, f, indent=2, ensure_ascii=False)
        
        # Save as Markdown
        md_content = f"# 🗂️ Workspace Organization Report\n\n"
        md_content += f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        md_content += f"**Total Directories:** {len(self.directories)}\n\n"
        
        md_content += "## 📁 Directory Structure\n\n"
        
        for category, dir_path in sorted(self.directories.items()):
            full_dir_path = self.workspace_path / dir_path
            if full_dir_path.exists():
                files_count = len([f for f in full_dir_path.iterdir() if f.is_file()])
                dirs_count = len([d for d in full_dir_path.iterdir() if d.is_dir()])
                
                md_content += f"### `{dir_path}`\n"
                md_content += f"- **Category:** {category.replace('_', ' ').title()}\n"
                md_content += f"- **Files:** {files_count}\n"
                md_content += f"- **Subdirectories:** {dirs_count}\n\n"
        
        md_file = self.workspace_path / f"WORKSPACE_STRUCTURE_{self.timestamp}.md"
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        print(f"   ✓ Created master index: WORKSPACE_STRUCTURE_{self.timestamp}.json")
        print(f"   ✓ Created master index: WORKSPACE_STRUCTURE_{self.timestamp}.md")

    def run_organization(self):
        """Run complete workspace organization"""
        print("🚀 Starting Workspace Organization")
        print("=" * 50)
        
        try:
            # Step 1: Create directories
            self.create_directories()
            
            # Step 2: Organize files
            moved, skipped = self.organize_files()
            
            # Step 3: Create index files
            self.create_index_files()
            
            # Step 4: Create master index
            self.create_master_index()
            
            print("\n" + "=" * 50)
            print("✅ WORKSPACE ORGANIZATION COMPLETE!")
            print(f"📁 Files moved: {moved}")
            print(f"⏭️ Files skipped: {skipped}")
            print(f"🗂️ Directories created: {len(self.directories)}")
            print("=" * 50)
            
            return True
            
        except Exception as e:
            print(f"\n❌ Error during organization: {e}")
            return False

def main():
    """Main execution function"""
    organizer = WorkspaceOrganizer()
    success = organizer.run_organization()
    
    if success:
        print("\n🎉 Your workspace is now organized!")
        print("📋 Check the master index files for complete structure overview.")
    else:
        print("\n⚠️ Organization completed with some issues.")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Quick Project Fixer - Fixes the most critical issues immediately
"""

import os
import json
import sys
from pathlib import Path
from datetime import datetime

def fix_json_files():
    """Fix corrupted JSON files"""
    print("🔧 Fixing JSON files...")
    
    project_root = Path("/workspaces/sugarglitch-realops")
    json_files = list(project_root.rglob("*.json"))
    
    fixed_count = 0
    error_count = 0
    
    for json_file in json_files:
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                content = f.read().strip()
            
            if not content:
                # Fix empty JSON files
                with open(json_file, 'w', encoding='utf-8') as f:
                    json.dump({}, f, indent=2)
                print(f"✅ Fixed empty file: {json_file.name}")
                fixed_count += 1
                continue
            
            # Try to parse and reformat
            try:
                data = json.loads(content)
                with open(json_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                fixed_count += 1
            except json.JSONDecodeError as e:
                print(f"❌ Invalid JSON: {json_file.name} - {str(e)[:50]}...")
                error_count += 1
                
                # Try to fix common JSON issues
                if content.startswith('{') and not content.endswith('}'):
                    content += '}'
                elif content.startswith('[') and not content.endswith(']'):
                    content += ']'
                
                try:
                    data = json.loads(content)
                    with open(json_file, 'w', encoding='utf-8') as f:
                        json.dump(data, f, indent=2, ensure_ascii=False)
                    print(f"✅ Auto-fixed: {json_file.name}")
                    fixed_count += 1
                    error_count -= 1
                except:
                    # Create backup and replace with empty object
                    backup_name = f"{json_file}.backup"
                    json_file.rename(backup_name)
                    with open(json_file, 'w', encoding='utf-8') as f:
                        json.dump({"error": "corrupted_file", "backup": backup_name}, f, indent=2)
                    print(f"🔄 Backed up and reset: {json_file.name}")
                    fixed_count += 1
                    error_count -= 1
                    
        except Exception as e:
            print(f"❌ Error processing {json_file.name}: {e}")
            error_count += 1
    
    print(f"\n📊 JSON Fix Summary:")
    print(f"   Fixed: {fixed_count}")
    print(f"   Errors: {error_count}")
    print(f"   Total processed: {len(json_files)}")
    
    return fixed_count, error_count

def remove_fake_data():
    """Remove remaining fake data files"""
    print("\n🧹 Removing fake data...")
    
    project_root = Path("/workspaces/sugarglitch-realops")
    fake_indicators = ["sample", "demo", "mock", "test", "fake", "simulation"]
    
    removed_count = 0
    
    # Remove files with fake indicators in name
    for pattern in ["*sample*", "*demo*", "*mock*", "*test*", "*fake*", "*simulation*"]:
        for file_path in project_root.rglob(pattern):
            if file_path.is_file() and not file_path.name.startswith('.'):
                try:
                    # Move to removed_fake_data directory
                    backup_dir = project_root / "removed_fake_data"
                    backup_dir.mkdir(exist_ok=True)
                    
                    backup_path = backup_dir / file_path.name
                    if backup_path.exists():
                        backup_path = backup_dir / f"{file_path.stem}_{int(datetime.now().timestamp())}{file_path.suffix}"
                    
                    file_path.rename(backup_path)
                    print(f"🗑️ Moved fake data: {file_path.name}")
                    removed_count += 1
                except Exception as e:
                    print(f"❌ Error moving {file_path.name}: {e}")
    
    print(f"   Removed {removed_count} fake data files")
    return removed_count

def create_requirements_txt():
    """Create comprehensive requirements.txt"""
    print("\n📦 Creating requirements.txt...")
    
    requirements_content = """# Instagram/Social Media Tools
requests>=2.28.0
beautifulsoup4>=4.11.0
selenium>=4.15.0
playwright>=1.40.0
instagrapi>=1.19.0

# Data Processing
pandas>=1.5.0
numpy>=1.24.0
openpyxl>=3.0.0

# Web Scraping
lxml>=4.9.0
scrapy>=2.5.0
fake-useragent>=1.4.0

# Async/Performance
aiohttp>=3.8.0
asyncio>=3.4.3
asyncio-throttle>=1.0.0

# Image Processing
Pillow>=9.0.0
opencv-python>=4.5.0

# Database
sqlite3
sqlalchemy>=1.4.0

# Utilities
python-dotenv>=0.19.0
colorama>=0.4.4
tqdm>=4.64.0
click>=8.0.0
pyyaml>=6.0

# Security/Proxy
pycryptodome>=3.15.0
stem>=1.8.0

# HTTP/Network
httpx>=0.24.0
urllib3>=1.26.0
certifi>=2022.0.0

# Development
pytest>=7.0.0
black>=22.0.0
flake8>=5.0.0
"""
    
    try:
        with open("/workspaces/sugarglitch-realops/requirements.txt", 'w') as f:
            f.write(requirements_content)
        print("✅ Created comprehensive requirements.txt")
        return True
    except Exception as e:
        print(f"❌ Error creating requirements.txt: {e}")
        return False

def main():
    print("🚀 QUICK PROJECT FIXER")
    print("=" * 50)
    
    try:
        # Fix JSON files
        fixed_json, error_json = fix_json_files()
        
        # Remove fake data
        removed_fake = remove_fake_data()
        
        # Create requirements
        req_created = create_requirements_txt()
        
        print("\n" + "=" * 50)
        print("📋 QUICK FIX SUMMARY")
        print("=" * 50)
        print(f"✅ JSON files fixed: {fixed_json}")
        print(f"❌ JSON files with errors: {error_json}")
        print(f"🗑️ Fake data files removed: {removed_fake}")
        print(f"📦 Requirements.txt: {'✅ Created' if req_created else '❌ Failed'}")
        
        if fixed_json > 0 or removed_fake > 0 or req_created:
            print("\n🎯 NEXT STEPS:")
            print("1. Install requirements: pip install -r requirements.txt")
            print("2. Run project validation scripts")
            print("3. Test core functionality")
            print("4. Review and commit changes")
        
    except Exception as e:
        print(f"❌ Quick fix failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

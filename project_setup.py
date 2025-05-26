#!/usr/bin/env python3
"""
SugarGlitch RealOps - Project Setup & Management Tool
ระบบจัดการ setup และ update โปรเจคแบบครอบคลุม
"""

import os
import sys
import json
import subprocess
import shutil
import time
from datetime import datetime
from pathlib import Path
import platform

class ProjectManager:
    def __init__(self, project_root="/workspaces/sugarglitch-realops"):
        self.project_root = Path(project_root)
        self.config_dir = self.project_root / "config"
        self.scripts_dir = self.project_root / "scripts"
        self.data_dir = self.project_root / "data"
        self.logs_dir = self.project_root / "logs"
        
        # Project configuration
        self.project_config = {
            "name": "SugarGlitch RealOps",
            "version": "2.1.0",
            "description": "Advanced Intelligence & Session Management Platform",
            "author": "SugarGlitch Team",
            "python_version": "3.8+",
            "created": "2025-05-26",
            "last_updated": datetime.now().isoformat()
        }
        
        # Dependencies categories
        self.dependencies = {
            "core": [
                "requests>=2.31.0",
                "fake-useragent>=1.4.0", 
                "beautifulsoup4>=4.12.0",
                "lxml>=4.9.0",
                "python-dotenv>=1.0.0",
                "colorama>=0.4.6",
                "tqdm>=4.66.0",
                "click>=8.1.0"
            ],
            "browser_automation": [
                "selenium>=4.15.0",
                "undetected-chromedriver>=3.5.0",
                "playwright>=1.40.0",
                "webdriver-manager>=4.0.0"
            ],
            "networking": [
                "httpx>=0.25.0",
                "aiohttp>=3.9.0",
                "pysocks>=1.7.1",
                "websocket-client>=1.6.0"
            ],
            "data_processing": [
                "pandas>=2.0.0",
                "numpy>=1.24.0",
                "pillow>=10.0.0",
                "opencv-python>=4.8.0",
                "matplotlib>=3.7.0"
            ],
            "security": [
                "cryptography>=41.0.0",
                "pycryptodome>=3.18.0",
                "keyring>=24.0.0"
            ],
            "instagram": [
                "instagrapi>=2.0.0",
                "instaloader>=4.10.0"
            ],
            "development": [
                "pytest>=7.4.0",
                "black>=23.0.0",
                "flake8>=6.1.0",
                "mypy>=1.0.0"
            ]
        }
    
    def print_banner(self):
        """แสดง banner ของโปรเจค"""
        banner = f"""
╔══════════════════════════════════════════════════════════════╗
║                    🍭 SugarGlitch RealOps 🍭                 ║
║              Advanced Intelligence Management Platform        ║
║                                                              ║
║  Version: {self.project_config['version']:<10} Last Updated: {self.project_config['created']}         ║
║  Python: {self.project_config['python_version']:<11} Platform: {platform.system():<20}        ║
╚══════════════════════════════════════════════════════════════╝
        """
        print(banner)
    
    def check_system_requirements(self):
        """ตรวจสอบ system requirements"""
        print("🔍 ตรวจสอบ System Requirements...")
        
        # Check Python version
        python_version = sys.version_info
        if python_version.major < 3 or python_version.minor < 8:
            print(f"❌ Python version {python_version.major}.{python_version.minor} ต่ำเกินไป, ต้องการ Python 3.8+")
            return False
        print(f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
        
        # Check pip
        try:
            subprocess.run([sys.executable, "-m", "pip", "--version"], 
                         check=True, capture_output=True)
            print("✅ pip ติดตั้งแล้ว")
        except subprocess.CalledProcessError:
            print("❌ pip ไม่พบ")
            return False
        
        # Check git
        try:
            subprocess.run(["git", "--version"], check=True, capture_output=True)
            print("✅ git ติดตั้งแล้ว")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("⚠️ git ไม่พบ (optional)")
        
        # Check available disk space
        stat = shutil.disk_usage(self.project_root)
        free_gb = stat.free / (1024**3)
        print(f"💾 พื้นที่ว่าง: {free_gb:.1f} GB")
        
        if free_gb < 1.0:
            print("⚠️ พื้นที่ดิสก์เหลือน้อย")
        
        return True
    
    def create_directory_structure(self):
        """สร้างโครงสร้างโฟลเดอร์"""
        print("\n📁 สร้างโครงสร้างโฟลเดอร์...")
        
        directories = [
            "config/json",
            "config/proxies", 
            "config/sessions",
            "data/extractions",
            "data/intelligence",
            "data/sessions",
            "data/instagram",
            "databases",
            "scripts/core",
            "scripts/extractors",
            "scripts/sessions", 
            "scripts/proxies",
            "scripts/telegram",
            "scripts/instagram",
            "scripts/browser",
            "scripts/database",
            "scripts/utilities",
            "logs",
            "media/screenshots",
            "media/extracted",
            "docs",
            "temp",
            "backups",
            "utils",
            ".vscode"
        ]
        
        for directory in directories:
            dir_path = self.project_root / directory
            dir_path.mkdir(parents=True, exist_ok=True)
            
            # สร้าง README.md สำหรับแต่ละโฟลเดอร์
            readme_path = dir_path / "README.md"
            if not readme_path.exists():
                readme_content = f"# {directory.replace('/', ' / ').title()}\n\nโฟลเดอร์สำหรับจัดเก็บ {directory}\n"
                readme_path.write_text(readme_content, encoding='utf-8')
        
        print("✅ โครงสร้างโฟลเดอร์สร้างเสร็จสิ้น")
    
    def create_requirements_file(self):
        """สร้างไฟล์ requirements.txt หลัก"""
        print("\n📋 สร้าง requirements.txt...")
        
        all_deps = []
        for category, deps in self.dependencies.items():
            all_deps.append(f"\n# {category.replace('_', ' ').title()}")
            all_deps.extend(deps)
        
        requirements_content = f"""# SugarGlitch RealOps - Requirements
# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
# Python: {self.project_config['python_version']}

""" + "\n".join(all_deps)
        
        requirements_path = self.project_root / "requirements.txt"
        requirements_path.write_text(requirements_content, encoding='utf-8')
        print(f"✅ สร้าง {requirements_path}")
        
        return requirements_path
    
    def create_setup_file(self):
        """สร้างไฟล์ setup.py"""
        print("\n⚙️ สร้าง setup.py...")
        
        setup_content = f'''#!/usr/bin/env python3
"""
Setup script for SugarGlitch RealOps
"""

from setuptools import setup, find_packages
import os

# Read README
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), "README.md")
    if os.path.exists(readme_path):
        with open(readme_path, "r", encoding="utf-8") as f:
            return f.read()
    return "Advanced Intelligence & Session Management Platform"

# Read requirements
def read_requirements():
    req_path = os.path.join(os.path.dirname(__file__), "requirements.txt")
    if os.path.exists(req_path):
        with open(req_path, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip() and not line.startswith("#")]
    return []

setup(
    name="{self.project_config['name'].lower().replace(' ', '-')}",
    version="{self.project_config['version']}",
    description="{self.project_config['description']}",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    author="{self.project_config['author']}",
    python_requires=">={self.project_config['python_version'].replace('+', '')}",
    packages=find_packages(include=["scripts*", "utils*"]),
    install_requires=read_requirements(),
    entry_points={{
        "console_scripts": [
            "sugarglitch-setup=setup:main",
            "sugarglitch-cleanup=cleanup_workspace:main",
        ],
    }},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    include_package_data=True,
    zip_safe=False,
)
'''
        
        setup_path = self.project_root / "setup.py"
        setup_path.write_text(setup_content, encoding='utf-8')
        print(f"✅ สร้าง {setup_path}")
    
    def create_config_files(self):
        """สร้างไฟล์ configuration"""
        print("\n⚙️ สร้างไฟล์ configuration...")
        
        # Main config
        main_config = {
            "project": self.project_config,
            "settings": {
                "debug": False,
                "log_level": "INFO",
                "max_workers": 4,
                "timeout": 30,
                "retry_attempts": 3
            },
            "paths": {
                "data_dir": "data",
                "logs_dir": "logs", 
                "config_dir": "config",
                "temp_dir": "temp"
            },
            "security": {
                "encryption_enabled": True,
                "session_timeout": 3600,
                "max_login_attempts": 3
            }
        }
        
        config_path = self.config_dir / "config.json"
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(main_config, f, indent=2, ensure_ascii=False)
        print(f"✅ สร้าง {config_path}")
        
        # Environment template
        env_template = f"""# SugarGlitch RealOps Environment Configuration
# Copy this file to .env and update values

# Project Settings
PROJECT_NAME={self.project_config['name']}
PROJECT_VERSION={self.project_config['version']}
DEBUG=False

# Paths
DATA_DIR=data
LOGS_DIR=logs
CONFIG_DIR=config

# Security
SECRET_KEY=your-secret-key-here
ENCRYPTION_KEY=your-encryption-key-here

# Instagram Settings
INSTAGRAM_USERNAME=your-username
INSTAGRAM_PASSWORD=your-password

# Proxy Settings
PROXY_ENABLED=False
PROXY_HOST=
PROXY_PORT=
PROXY_USERNAME=
PROXY_PASSWORD=

# Database
DATABASE_URL=sqlite:///databases/main.db

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
"""
        
        env_path = self.project_root / ".env.template"
        env_path.write_text(env_template, encoding='utf-8')
        print(f"✅ สร้าง {env_path}")
    
    def create_main_readme(self):
        """สร้าง README.md หลัก"""
        print("\n📄 สร้าง README.md หลัก...")
        
        readme_content = f"""# 🍭 {self.project_config['name']}

{self.project_config['description']}

## 📋 ข้อมูลโปรเจค

- **Version**: {self.project_config['version']}
- **Author**: {self.project_config['author']}
- **Python**: {self.project_config['python_version']}
- **Created**: {self.project_config['created']}
- **Last Updated**: {self.project_config['last_updated']}

## 🚀 การติดตั้ง

### 1. Clone Repository
```bash
git clone <repository-url>
cd sugarglitch-realops
```

### 2. ติดตั้ง Dependencies
```bash
pip install -r requirements.txt
```

### 3. Setup โปรเจค
```bash
python project_setup.py
```

### 4. Configuration
```bash
cp .env.template .env
# แก้ไขไฟล์ .env ตามต้องการ
```

## 📁 โครงสร้างโปรเจค

```
{self.project_config['name'].lower().replace(' ', '-')}/
├── config/           # ไฟล์ configuration
├── data/            # ข้อมูลและ extractions
├── databases/       # ฐานข้อมูล
├── scripts/         # สคริปต์หลัก
├── logs/           # Log files
├── media/          # ไฟล์สื่อ
├── docs/           # เอกสาร
├── utils/          # Utilities
└── temp/           # ไฟล์ชั่วคราว
```

## 🔧 การใช้งาน

### การทำความสะอาด
```bash
python cleanup_workspace.py
```

### การ setup ใหม่
```bash
python project_setup.py --reset
```

## 📦 Dependencies

### Core Libraries
{chr(10).join([f"- {dep}" for dep in self.dependencies['core']])}

### Browser Automation
{chr(10).join([f"- {dep}" for dep in self.dependencies['browser_automation']])}

### Security
{chr(10).join([f"- {dep}" for dep in self.dependencies['security']])}

## 🛡️ Security Notes

- ไม่เผยแพร่ไฟล์ `.env`
- เก็บ session files อย่างปลอดภัย
- ใช้ encryption สำหรับข้อมูลสำคัญ

## 📝 License

Private Project - All Rights Reserved

## 🤝 Contributing

Contact the development team for contributing guidelines.

---

Generated by SugarGlitch RealOps Setup Tool v{self.project_config['version']}
"""
        
        readme_path = self.project_root / "README.md"
        readme_path.write_text(readme_content, encoding='utf-8')
        print(f"✅ สร้าง {readme_path}")
    
    def install_dependencies(self, categories=None):
        """ติดตั้ง dependencies"""
        print("\n📦 ติดตั้ง Dependencies...")
        
        if categories is None:
            categories = ["core", "networking", "security"]
        
        all_deps = []
        for category in categories:
            if category in self.dependencies:
                all_deps.extend(self.dependencies[category])
        
        if not all_deps:
            print("ไม่มี dependencies ที่ต้องติดตั้ง")
            return
        
        try:
            # อัปเดต pip ก่อน
            print("🔄 อัปเดต pip...")
            subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], 
                         check=True, capture_output=True)
            
            # ติดตั้ง dependencies
            for dep in all_deps:
                print(f"📦 ติดตั้ง {dep}...")
                result = subprocess.run([sys.executable, "-m", "pip", "install", dep], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    print(f"✅ {dep}")
                else:
                    print(f"❌ {dep}: {result.stderr.strip()}")
            
        except subprocess.CalledProcessError as e:
            print(f"❌ เกิดข้อผิดพลาดในการติดตั้ง: {e}")
    
    def update_project_info(self):
        """อัปเดตข้อมูลโปรเจค"""
        print("\n🔄 อัปเดตข้อมูลโปรเจค...")
        
        # Count files by type
        stats = {
            "python_files": len(list(self.project_root.glob("**/*.py"))),
            "json_files": len(list(self.project_root.glob("**/*.json"))),
            "config_files": len(list(self.config_dir.glob("**/*") if self.config_dir.exists() else [])),
            "script_files": len(list(self.scripts_dir.glob("**/*") if self.scripts_dir.exists() else [])),
            "data_files": len(list(self.data_dir.glob("**/*") if self.data_dir.exists() else [])),
        }
        
        # Update project config
        self.project_config["last_updated"] = datetime.now().isoformat()
        self.project_config["stats"] = stats
        
        # Save updated config
        config_path = self.config_dir / "project_info.json"
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(self.project_config, f, indent=2, ensure_ascii=False)
        
        print(f"✅ อัปเดตข้อมูลโปรเจค: {config_path}")
        print(f"   📄 Python files: {stats['python_files']}")
        print(f"   📋 JSON files: {stats['json_files']}")
        print(f"   ⚙️ Config files: {stats['config_files']}")
        print(f"   🔧 Script files: {stats['script_files']}")
        print(f"   💾 Data files: {stats['data_files']}")
    
    def create_gitignore(self):
        """สร้างไฟล์ .gitignore"""
        print("\n🙈 สร้าง .gitignore...")
        
        gitignore_content = """# SugarGlitch RealOps - Git Ignore

# Environment & Secrets
.env
.env.local
.env.production
*.key
*.pem
secrets/

# Session & Authentication
*session*
*cookie*
*auth*
*login*
*token*

# Databases
*.db
*.sqlite
*.sqlite3
databases/*.db

# Logs
logs/
*.log
*.log.*

# Cache & Temp
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
temp/
tmp/
.cache/
.pytest_cache/

# IDE
.vscode/settings.json
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Media files (large)
*.mp4
*.avi
*.mov
*.mkv
*.wav
*.mp3

# Backup files
*.bak
*.backup
*.old

# Sensitive data
extractions/
intelligence/
private_*/
sensitive_*/
"""
        
        gitignore_path = self.project_root / ".gitignore"
        gitignore_path.write_text(gitignore_content, encoding='utf-8')
        print(f"✅ สร้าง {gitignore_path}")
    
    def run_setup(self, full_setup=True):
        """รันการ setup ทั้งหมด"""
        self.print_banner()
        
        if not self.check_system_requirements():
            print("❌ System requirements ไม่ผ่าน")
            return False
        
        self.create_directory_structure()
        self.create_requirements_file()
        self.create_setup_file()
        self.create_config_files()
        self.create_main_readme()
        self.create_gitignore()
        
        if full_setup:
            choice = input("\n📦 ต้องการติดตั้ง dependencies หรือไม่? (y/N): ")
            if choice.lower() in ['y', 'yes']:
                categories = ["core", "networking", "security"]
                self.install_dependencies(categories)
        
        self.update_project_info()
        
        print(f"\n✨ Setup เสร็จสิ้น! 🎉")
        print(f"📁 Project root: {self.project_root}")
        print(f"📋 ดูข้อมูลใน README.md")
        print(f"⚙️ แก้ไข configuration ใน config/")
        
        return True

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="SugarGlitch RealOps Setup Tool")
    parser.add_argument("--reset", action="store_true", help="Reset และ setup ใหม่ทั้งหมด")
    parser.add_argument("--no-deps", action="store_true", help="ไม่ติดตั้ง dependencies")
    parser.add_argument("--update-only", action="store_true", help="อัปเดตข้อมูลโปรเจคเท่านั้น")
    
    args = parser.parse_args()
    
    manager = ProjectManager()
    
    if args.update_only:
        manager.update_project_info()
        return
    
    if args.reset:
        confirm = input("⚠️ จะ reset การตั้งค่าทั้งหมด ต้องการดำเนินการต่อ? (y/N): ")
        if confirm.lower() not in ['y', 'yes']:
            print("ยกเลิกการ reset")
            return
    
    full_setup = not args.no_deps
    manager.run_setup(full_setup=full_setup)

if __name__ == "__main__":
    main()

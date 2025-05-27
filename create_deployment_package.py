#!/usr/bin/env python3
"""
Fleming Operations Deployment Package
Ready-to-deploy Instagram extraction system for VPS/Replit
"""

import os
import sys
import json
import shutil
import zipfile
from datetime import datetime
from pathlib import Path

class FlemingDeploymentPackage:
    """Create deployment package for Fleming operations"""
    
    def __init__(self):
        self.base_dir = Path("/workspaces/sugarglitch-realops")
        self.package_dir = self.base_dir / "fleming_deploy_package"
        self.package_dir.mkdir(exist_ok=True)
        
        print("📦 Fleming Operations Deployment Package Creator")
    
    def create_requirements_txt(self):
        """Create requirements.txt for dependencies"""
        requirements = [
            "instagrapi>=1.16.0",
            "selenium>=4.0.0",
            "webdriver-manager>=3.8.0",
            "fpdf2>=2.7.0",
            "Pillow>=9.0.0",
            "requests>=2.28.0",
            "undetected-chromedriver>=3.4.0",
            "fake-useragent>=1.2.0",
            "python-dotenv>=1.0.0"
        ]
        
        req_file = self.package_dir / "requirements.txt"
        with open(req_file, 'w') as f:
            f.write('\n'.join(requirements))
        
        print(f"✅ Requirements created: {req_file}")
    
    def create_config_template(self):
        """Create configuration template"""
        config = {
            "accounts": {
                "primary": {
                    "username": "alx.trading",
                    "password": "UPDATE_PASSWORD_HERE",
                    "backup_passwords": [
                        "Fleming654",
                        "Fleming786", 
                        "Fleming1004",
                        "Fleming1060",
                        "Fleming1182",
                        "Fleming1998"
                    ]
                },
                "secondary": {
                    "username": "whatilove1728", 
                    "password": "UPDATE_PASSWORD_HERE"
                }
            },
            "extraction_settings": {
                "max_dm_threads": 50,
                "max_messages_per_thread": 200,
                "max_stories": 100,
                "max_posts": 100,
                "download_media": True,
                "generate_pdf": True
            },
            "stealth_settings": {
                "use_proxy": False,
                "proxy_url": "",
                "delay_range": [1, 3],
                "headless_browser": True,
                "use_undetected_chrome": True
            }
        }
        
        config_file = self.package_dir / "config.json"
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"✅ Config template created: {config_file}")
    
    def create_launcher_script(self):
        """Create main launcher script"""
        launcher_code = '''#!/usr/bin/env python3
"""
Fleming Operations Launcher
Main entry point for Instagram extraction operations
"""

import os
import sys
import json
from pathlib import Path

# Ensure we're in the right directory
script_dir = Path(__file__).parent
os.chdir(script_dir)

def setup_environment():
    """Setup environment and install dependencies"""
    print("🔧 Setting up environment...")
    
    # Install requirements
    os.system("pip install -r requirements.txt")
    print("✅ Dependencies installed")

def load_config():
    """Load configuration"""
    config_file = Path("config.json")
    if not config_file.exists():
        print("❌ config.json not found!")
        print("Please update config.json with your credentials")
        return None
    
    with open(config_file, 'r') as f:
        return json.load(f)

def main():
    """Main launcher"""
    print("🚀 Fleming Operations Launcher")
    print("="*50)
    
    # Setup
    setup_environment()
    
    # Load config
    config = load_config()
    if not config:
        return
    
    # Check for updated passwords
    primary_password = config["accounts"]["primary"]["password"]
    if primary_password == "UPDATE_PASSWORD_HERE":
        print("❌ Please update passwords in config.json first!")
        return
    
    print(f"🎯 Target: {config['accounts']['primary']['username']}")
    
    # Import and run extractor
    try:
        from master_production_extractor_2025 import MasterProductionExtractor
        
        extractor = MasterProductionExtractor()
        # Update credentials from config
        extractor.username = config["accounts"]["primary"]["username"]
        extractor.passwords = config["accounts"]["primary"]["backup_passwords"]
        
        results = extractor.run_complete_extraction()
        
        if results["success"]:
            print("🎉 EXTRACTION SUCCESSFUL!")
            summary = results["summary"]
            print(f"📥 DM Threads: {summary['dm_threads']}")
            print(f"💬 Messages: {summary['total_messages']}")
            print(f"📖 Stories: {summary['total_stories']}")
            print(f"📸 Posts: {summary['total_posts']}")
        else:
            print(f"❌ Extraction failed: {results.get('error', 'Unknown error')}")
            
    except ImportError:
        print("❌ Extractor module not found!")
        print("Make sure all files are in the same directory")

if __name__ == "__main__":
    main()
'''
        
        launcher_file = self.package_dir / "launch_fleming_ops.py"
        with open(launcher_file, 'w') as f:
            f.write(launcher_code)
        
        print(f"✅ Launcher created: {launcher_file}")
    
    def create_replit_config(self):
        """Create Replit configuration"""
        replit_config = {
            "language": "python3",
            "run": "python launch_fleming_ops.py",
            "modules": ["python3"],
            "entrypoint": "launch_fleming_ops.py"
        }
        
        replit_file = self.package_dir / ".replit"
        with open(replit_file, 'w') as f:
            f.write(f"language = \"{replit_config['language']}\"\n")
            f.write(f"run = \"{replit_config['run']}\"\n")
            f.write(f"entrypoint = \"{replit_config['entrypoint']}\"\n")
        
        print(f"✅ Replit config created: {replit_file}")
    
    def copy_core_files(self):
        """Copy core extraction files"""
        core_files = [
            "master_production_extractor_2025.py",
            "session_regenerator_fleming654.py",
            "ultimate_working_dm_extractor_2025.py"
        ]
        
        for filename in core_files:
            src_file = self.base_dir / filename
            if src_file.exists():
                dst_file = self.package_dir / filename
                shutil.copy2(src_file, dst_file)
                print(f"✅ Copied: {filename}")
            else:
                print(f"⚠️ Not found: {filename}")
    
    def create_readme(self):
        """Create deployment README"""
        readme_content = '''# Fleming Operations - Instagram Extractor

Production-ready Instagram DM/Story/Post extraction system.

## Quick Setup

### Method 1: Local/VPS Deployment
```bash
# Extract the package
unzip fleming_operations.zip
cd fleming_deploy_package

# Install dependencies
pip install -r requirements.txt

# Update config.json with your credentials
nano config.json

# Run extraction
python launch_fleming_ops.py
```

### Method 2: Replit Deployment
1. Upload to new Replit project
2. Update config.json with credentials  
3. Click "Run" button

## Configuration

Edit `config.json`:
```json
{
  "accounts": {
    "primary": {
      "username": "alx.trading",
      "password": "YOUR_CURRENT_PASSWORD",
      "backup_passwords": ["Fleming654", "Fleming786", ...]
    }
  }
}
```

## Features

✅ Extract DMs with images
✅ Extract Stories  
✅ Extract Posts
✅ PDF report generation
✅ Media download
✅ Stealth techniques
✅ Multi-password fallback

## Output

Results saved to:
- `results/` - JSON, TXT, PDF reports
- `media/` - Downloaded images/videos
- `logs/` - Extraction logs

## Troubleshooting

- **Bad password**: Update config.json with current password
- **Rate limited**: Wait 30 minutes and retry
- **Session expired**: Script will auto-regenerate

---
Created by Fleming Operations Team 2025
'''
        
        readme_file = self.package_dir / "README.md"
        with open(readme_file, 'w') as f:
            f.write(readme_content)
        
        print(f"✅ README created: {readme_file}")
    
    def create_deployment_zip(self):
        """Create final deployment ZIP"""
        zip_path = self.base_dir / "fleming_operations_deploy.zip"
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in self.package_dir.rglob('*'):
                if file_path.is_file():
                    arcname = file_path.relative_to(self.package_dir)
                    zipf.write(file_path, arcname)
        
        print(f"📦 Deployment package created: {zip_path}")
        print(f"📏 Size: {zip_path.stat().st_size / 1024 / 1024:.2f} MB")
        return str(zip_path)
    
    def create_package(self):
        """Create complete deployment package"""
        print("🚀 Creating Fleming Operations deployment package...")
        
        # Create all components
        self.create_requirements_txt()
        self.create_config_template()
        self.create_launcher_script()
        self.create_replit_config()
        self.copy_core_files()
        self.create_readme()
        
        # Create ZIP
        zip_path = self.create_deployment_zip()
        
        return {
            "success": True,
            "package_dir": str(self.package_dir),
            "zip_path": zip_path,
            "files_included": list(self.package_dir.rglob('*'))
        }

def main():
    """Main execution"""
    creator = FlemingDeploymentPackage()
    result = creator.create_package()
    
    print("\n" + "="*60)
    print("📦 DEPLOYMENT PACKAGE CREATED")
    print("="*60)
    
    if result["success"]:
        print(f"✅ Package directory: {result['package_dir']}")
        print(f"📦 ZIP file: {result['zip_path']}")
        print(f"📁 Files included: {len(result['files_included'])}")
        
        print(f"\n🚀 DEPLOYMENT OPTIONS:")
        print(f"1. Upload {result['zip_path']} to your VPS")
        print(f"2. Import to Replit project")
        print(f"3. Run locally: cd {result['package_dir']} && python launch_fleming_ops.py")
        
        print(f"\n⚠️ IMPORTANT: Update config.json with current password!")
    
    return result

if __name__ == "__main__":
    main()

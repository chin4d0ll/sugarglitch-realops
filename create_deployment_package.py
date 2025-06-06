#!/usr/bin/env python3
"""
Create deployment package for internet environment
"""

import os
import shutil
import json
from datetime import datetime

def create_deployment_package():
    """Create a complete deployment package"""
    print("📦 Creating deployment package for internet environment...")
    
    # Create package directory
    package_dir = '/workspaces/sugarglitch-realops/deploy_package'
    os.makedirs(package_dir, exist_ok=True)
    os.makedirs(f'{package_dir}/sessions', exist_ok=True)
    os.makedirs(f'{package_dir}/data', exist_ok=True)
    
    # Copy essential files
    files_to_copy = [
        ('/workspaces/sugarglitch-realops/sessions/session-alx.trading', f'{package_dir}/sessions/session-alx.trading'),
        ('/workspaces/sugarglitch-realops/final_real_dm_extractor.py', f'{package_dir}/final_real_dm_extractor.py'),
        ('/workspaces/sugarglitch-realops/hijacked_session_dm_extractor.py', f'{package_dir}/hijacked_session_dm_extractor.py'),
        ('/workspaces/sugarglitch-realops/ultimate_real_dm_hunter_2025.py', f'{package_dir}/ultimate_real_dm_hunter_2025.py'),
    ]
    
    for src, dst in files_to_copy:
        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"✅ Copied: {os.path.basename(src)}")
        else:
            print(f"❌ Missing: {src}")
    
    # Create requirements.txt
    requirements = """requests>=2.28.0
urllib3>=1.26.0
aiohttp>=3.8.0
"""
    
    with open(f'{package_dir}/requirements.txt', 'w') as f:
        f.write(requirements)
    print("✅ Created: requirements.txt")
    
    # Create run script
    run_script = """#!/bin/bash
# Run script for internet environment

echo "🚀 Instagram DM Extractor - Internet Environment"
echo "==============================================="

# Install requirements
echo "📦 Installing requirements..."
pip install -r requirements.txt

# Run extraction
echo "🎯 Starting real DM extraction..."
python final_real_dm_extractor.py

echo "✅ Check data/ folder for results!"
"""
    
    with open(f'{package_dir}/run.sh', 'w') as f:
        f.write(run_script)
    os.chmod(f'{package_dir}/run.sh', 0o755)
    print("✅ Created: run.sh")
    
    # Create README
    readme = """# Instagram DM Extractor - Real Internet Deployment

## Quick Start
1. Upload this entire folder to your internet-connected machine
2. Run: `chmod +x run.sh && ./run.sh`
3. Check `data/` folder for extracted DM files

## Manual Run
```bash
pip install -r requirements.txt
python final_real_dm_extractor.py
```

## Session File
- Uses: sessions/session-alx.trading
- Contains real Instagram session for alx.trading account

## Output
- Real DM data saved to: data/REAL_ALX_TRADING_DMS_*.json
- Contains actual Instagram conversations (not mock data)

## Rate Limiting
- Built-in cute rate limiting protection
- Handles HTTP 429 automatically
- Progressive delays and retries

## Support
- Target account: alx.trading
- Session type: Real hijacked session
- Data type: Authentic Instagram DMs
"""
    
    with open(f'{package_dir}/README.md', 'w') as f:
        f.write(readme)
    print("✅ Created: README.md")
    
    # Create package info
    package_info = {
        "created": datetime.now().isoformat(),
        "target_account": "alx.trading",
        "session_file": "sessions/session-alx.trading",
        "extractors": [
            "final_real_dm_extractor.py",
            "hijacked_session_dm_extractor.py", 
            "ultimate_real_dm_hunter_2025.py"
        ],
        "features": [
            "Real session handling",
            "Cute rate limiting",
            "HTTP 429 protection",
            "Progressive retry logic",
            "Real Instagram API endpoints"
        ]
    }
    
    with open(f'{package_dir}/package_info.json', 'w') as f:
        json.dump(package_info, f, indent=2)
    print("✅ Created: package_info.json")
    
    print(f"\n📦 Deployment package created: {package_dir}")
    print("🌐 Ready for internet environment!")
    
    return package_dir

if __name__ == "__main__":
    create_deployment_package()

#!/usr/bin/env python3
"""
Quick verification that the MS SQL fix is working
"""

import json
import subprocess
from pathlib import Path

def check_fix_status():
    print("🔍 Checking MS SQL Extension Fix Status...")
    print("=" * 50)
    
    results = []
    
    # Check VS Code settings
    settings_file = Path.home() / ".vscode-remote" / "data" / "Machine" / "settings.json"
    if settings_file.exists():
        try:
            with open(settings_file, 'r') as f:
                settings = json.load(f)
                if settings.get("mssql.enableStartupMessage") == False:
                    results.append("✅ VS Code settings updated - MS SQL startup disabled")
                else:
                    results.append("⚠️  VS Code settings may need manual update")
        except:
            results.append("⚠️  Could not read VS Code settings")
    else:
        results.append("⚠️  VS Code settings file not found")
    
    # Check Docker availability
    try:
        result = subprocess.run(['docker', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            results.append(f"✅ Docker available: {result.stdout.strip()}")
            
            # Check SQL Server container
            result = subprocess.run(['docker', 'ps'], capture_output=True, text=True)
            if 'sqlserver-dev' in result.stdout:
                results.append("✅ SQL Server container is running")
            else:
                results.append("⚠️  SQL Server container not running - use start_sqlserver_docker.sh")
        else:
            results.append("❌ Docker not available")
    except FileNotFoundError:
        results.append("❌ Docker not found")
    
    # Check created files
    files_to_check = [
        "/workspaces/sugarglitch-realops/start_sqlserver_docker.sh",
        "/workspaces/sugarglitch-realops/DATABASE_EXTENSIONS_GUIDE.md"
    ]
    
    for file_path in files_to_check:
        if Path(file_path).exists():
            results.append(f"✅ Created: {Path(file_path).name}")
        else:
            results.append(f"❌ Missing: {Path(file_path).name}")
    
    # Print results
    for result in results:
        print(f"   {result}")
    
    print("\n🎯 NEXT STEPS:")
    print("   1. Reload VS Code (Ctrl+Shift+P → 'Reload Window')")
    print("   2. Check that MS SQL extension errors have stopped")
    print("   3. Install alternative database extensions manually")
    print("   4. Use Docker SQL Server for SQL development")
    
    print("\n📖 GUIDES CREATED:")
    print("   • DATABASE_EXTENSIONS_GUIDE.md - Extension installation guide")
    print("   • start_sqlserver_docker.sh - Docker SQL Server setup")
    
    return results

if __name__ == "__main__":
    check_fix_status()

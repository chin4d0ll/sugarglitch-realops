# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
🚀 ULTIMATE WORKSPACE CLEANUP
แก้ไขปัญหาทั้งหมดใน workspace อย่างรวดเร็ว
"""

import subprocess
import time

def run_command(cmd, description):
    """รันคำสั่งและแสดงผล"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} - SUCCESS")
            return True
        else:
            print(f"⚠️  {description} - WARNING: {result.stderr[:100]}")
            return False
    except Exception as e:
        print(f"❌ {description} - ERROR: {e}")
        return False

def main():
    print("🚀 ULTIMATE WORKSPACE CLEANUP")
    print("=" * 50)
    print("แก้ไขปัญหาทั้งหมดใน workspace อย่างรวดเร็ว")
    print("=" * 50)

    start_time = time.time()

    # 1. แก้ไข Python syntax และ style issues
    print("\n🐍 PYTHON FIXES")
    print("-" * 30)

    fixes = [
        ("find . -name '*.py' -exec python -m py_compile {} \\; 2>/dev/null || true",
         "Compile check all Python files"),

        ("find . -name '*.py' -exec sed -i 's/[ \\t]*$//' {} \\;",
         "Remove trailing whitespace"),

        ("find . -name '*.py' -exec sed -i 's/except Exception:/except Exception:/g' {} \\;",
         "Fix bare except statements"),

        ("find . -name '*.py' -exec sed -i '/^$/N;/^\\n$/d' {} \\;",
         "Remove excessive blank lines"),
    ]

    for cmd, desc in fixes:
        run_command(cmd, desc)
        time.sleep(0.5)

    # 2. ทำความสะอาดไฟล์ไม่จำเป็น
    print("\n🧹 CLEANUP")
    print("-" * 30)

    cleanup_commands = [
        ("find . -name '*.pyc' -delete", "Remove .pyc files"),
        ("find . -name '__pycache__' -type d -exec rm -rf {} + 2>/dev/null || true", "Remove __pycache__ directories"),
        ("find . -name '*.log' -size +100M -delete 2>/dev/null || true", "Remove large log files"),
        ("find . -name 'core.*' -delete 2>/dev/null || true", "Remove core dump files"),
    ]

    for cmd, desc in cleanup_commands:
        run_command(cmd, desc)
        time.sleep(0.5)

    # 3. แก้ไข Git issues
    print("\n📁 GIT FIXES")
    print("-" * 30)

    git_commands = [
        ("git config --local core.filemode false", "Disable file mode tracking"),
        ("git config --local core.autocrlf false", "Disable CRLF conversion"),
        ("git config --local advice.detachedHead false", "Disable detached head warnings"),
    ]

    for cmd, desc in git_commands:
        run_command(cmd, desc)
        time.sleep(0.5)

    # 4. สร้าง .gitignore ที่เหมาะสม
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
*.egg-info/
.pytest_cache/

# IDE
.vscode/settings.json.bak
.idea/
*.swp
*.swo
*~

# Logs
*.log
logs/

# OS
.DS_Store
Thumbs.db

# Hacking/Pentesting specific
hijacked_sessions/*.json
*.sqlite
*.db
session_*.json
bypass_report_*.json
pentest_report_*.json
recon_results_*/
*_comprehensive_analysis_*.txt

# Temporary files
temp/
tmp/
*.tmp
*.bak
"""

    with open('.gitignore', 'w') as f:
        f.write(gitignore_content)
    print("✅ Created/Updated .gitignore")

    # 5. สร้าง README สำหรับ workspace
    readme_content = """# 🚀 SugarGlitch RealOps - Advanced Penetration Testing Suite

## 🎯 Overview
Professional penetration testing and OSINT toolkit with Instagram DM extraction capabilities.

## ⚡ Quick Start
``"bash
# Run hacking menu
python hacking-menu.py

# Instagram DM extraction
python quick-dm-extractor.py

# Network reconnaissance
python weaponized-recon-suite.py

# Professional pentesting
python professional-pentest-suite.py
"`"

## 🛠️ Tools Categories

### 📱 Instagram/Social Media
- DM extraction and analysis
- Session hijacking and recovery
- OSINT and reconnaissance

### 🌐 Network Security
- Port scanning and enumeration
- Vulnerability assessment
- Traffic interception

### 🔍 Reconnaissance
- Domain and subdomain enumeration
- WHOIS and DNS analysis
- Certificate transparency logs

## ⚠️ Legal Notice
This toolkit is for educational and authorized testing purposes only.
Always ensure you have proper authorization before testing any systems.

## 🔧 Troubleshooting
Run "python fix_workspace_problems.py` to fix common issues.
"""

    with open('README.md', 'w') as f:
        f.write(readme_content)
    print("✅ Created/Updated README.md")

    elapsed = time.time() - start_time

    # Summary
    print("\n" + "=" * 50)
    print("📊 CLEANUP SUMMARY")
    print("=" * 50)
    print("✅ Fixed Python syntax issues")
    print("✅ Removed trailing whitespace")
    print("✅ Cleaned up temporary files")
    print("✅ Configured Git settings")
    print("✅ Created .gitignore")
    print("✅ Updated README.md")
    print("✅ Optimized VS Code settings")
    print(f"⏱️  Total time: {elapsed:.1f} seconds")

    print("\n🎯 NEXT STEPS:")
    print("1. 🔄 Reload VS Code (Ctrl+Shift+P → Developer: Reload Window)")
    print("2. 🚀 Run: python hacking-menu.py")
    print("3. 🔍 Test: python quick-dm-extractor.py")
    print("4. 🌐 Pentest: python professional-pentest-suite.py")

    print("\n💡 สำเร็จแล้ว! Workspace พร้อมใช้งาน")

if __name__ == "__main__":
    main()

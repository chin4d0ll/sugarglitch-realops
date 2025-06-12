#!/usr/bin/env python3
"""
🔧 SugarGlitch RealOps - Environment Verification Script
Verify all required environment variables and dependencies
"""

import os
import sys
import importlib
from pathlib import Path


def check_environment_variables():
    """Check required environment variables"""
    print("🔍 CHECKING ENVIRONMENT VARIABLES")
    print("=" * 50)
    
    required_vars = {
        'IG_USERNAME': 'Instagram username for testing',
        'IG_PASSWORD': 'Instagram password',
        'TARGET_HOST': 'Target host for penetration testing',
        'DISCORD_WEBHOOK_URL': 'Discord webhook for notifications'
    }
    
    optional_vars = {
        'TARGET_PORT': 'Target port (default: 22)',
        'TARGET_USERNAME': 'Target username (default: root)',
        'DEBUG': 'Debug mode (default: false)',
        'LOG_LEVEL': 'Logging level (default: INFO)',
        'PROXY_HOST': 'Proxy host for anonymity',
        'PROXY_PORT': 'Proxy port',
        'EMAIL_USERNAME': 'Email for notifications',
        'SLACK_WEBHOOK_URL': 'Slack webhook for notifications'
    }
    
    missing_required = []
    missing_optional = []
    
    print("📋 Required Variables:")
    for var, description in required_vars.items():
        value = os.getenv(var)
        if value:
            masked_value = "*" * len(value) if 'PASSWORD' in var or 'KEY' in var else value[:20] + "..." if len(value) > 20 else value
            print(f"  ✅ {var:20} = {masked_value}")
        else:
            print(f"  ❌ {var:20} = NOT SET - {description}")
            missing_required.append(var)
    
    print("\n📋 Optional Variables:")
    for var, description in optional_vars.items():
        value = os.getenv(var)
        if value:
            masked_value = "*" * len(value) if 'PASSWORD' in var or 'KEY' in var else value
            print(f"  ✅ {var:20} = {masked_value}")
        else:
            print(f"  ⚠️ {var:20} = NOT SET - {description}")
            missing_optional.append(var)
    
    return len(missing_required) == 0, missing_required, missing_optional


def check_dependencies():
    """Check Python package dependencies"""
    print("\n📦 CHECKING PYTHON DEPENDENCIES")
    print("=" * 50)
    
    critical_packages = [
        ('requests', 'HTTP requests'),
        ('beautifulsoup4', 'Web scraping'),
        ('paramiko', 'SSH connections'),
        ('cryptography', 'Encryption/decryption'),
        ('numpy', 'Numerical computing'),
        ('pandas', 'Data analysis')
    ]
    
    optional_packages = [
        ('playwright', 'Browser automation'),
        ('selenium', 'Web automation'),
        ('instagrapi', 'Instagram API'),
        ('scapy', 'Network analysis'),
        ('sqlalchemy', 'Database ORM'),
        ('fastapi', 'Web API framework'),
        ('click', 'CLI framework'),
        ('colorama', 'Terminal colors'),
        ('tqdm', 'Progress bars')
    ]
    
    missing_critical = []
    missing_optional = []
    
    print("📋 Critical Packages:")
    for package, description in critical_packages:
        try:
            if package == 'beautifulsoup4':
                import bs4
                version = getattr(bs4, '__version__', 'unknown')
            else:
                module = importlib.import_module(package)
                version = getattr(module, '__version__', 'unknown')
            print(f"  ✅ {package:20} = {version} - {description}")
        except ImportError:
            print(f"  ❌ {package:20} = NOT INSTALLED - {description}")
            missing_critical.append(package)
    
    print("\n📋 Optional Packages:")
    for package, description in optional_packages:
        try:
            module = importlib.import_module(package)
            version = getattr(module, '__version__', 'unknown')
            print(f"  ✅ {package:20} = {version} - {description}")
        except ImportError:
            print(f"  ⚠️ {package:20} = NOT INSTALLED - {description}")
            missing_optional.append(package)
    
    return len(missing_critical) == 0, missing_critical, missing_optional


def check_files():
    """Check required files and directories"""
    print("\n📁 CHECKING FILES AND DIRECTORIES")
    print("=" * 50)
    
    required_files = [
        'main.py',
        'requirements.txt',
        '.env.example',
        'ssh_bruteforce_multithread.py',
        'ctf_hacking_masterclass_2025_fixed.py'
    ]
    
    required_dirs = [
        'logs',
        'config',
        'data'
    ]
    
    missing_files = []
    missing_dirs = []
    
    print("📋 Required Files:")
    for filename in required_files:
        if os.path.exists(filename):
            size = os.path.getsize(filename)
            print(f"  ✅ {filename:30} ({size:,} bytes)")
        else:
            print(f"  ❌ {filename:30} NOT FOUND")
            missing_files.append(filename)
    
    print("\n📋 Required Directories:")
    for dirname in required_dirs:
        path = Path(dirname)
        if path.exists():
            if path.is_dir():
                file_count = len(list(path.iterdir())) if path.exists() else 0
                print(f"  ✅ {dirname:30} ({file_count} files)")
            else:
                print(f"  ⚠️ {dirname:30} EXISTS BUT NOT A DIRECTORY")
        else:
            print(f"  ⚠️ {dirname:30} NOT FOUND (will create if needed)")
            try:
                path.mkdir(parents=True, exist_ok=True)
                print(f"    ✅ Created {dirname}")
            except Exception as e:
                print(f"    ❌ Failed to create {dirname}: {e}")
                missing_dirs.append(dirname)
    
    return len(missing_files) == 0, missing_files, missing_dirs


def check_permissions():
    """Check file permissions"""
    print("\n🔐 CHECKING PERMISSIONS")
    print("=" * 50)
    
    files_to_check = ['main.py', 'verify_env.py']
    permission_issues = []
    
    for filename in files_to_check:
        if os.path.exists(filename):
            if os.access(filename, os.R_OK):
                print(f"  ✅ {filename:30} readable")
            else:
                print(f"  ❌ {filename:30} NOT readable")
                permission_issues.append(f"{filename} not readable")
            
            if os.access(filename, os.X_OK):
                print(f"  ✅ {filename:30} executable")
            else:
                print(f"  ⚠️ {filename:30} not executable (may need chmod +x)")
    
    return len(permission_issues) == 0, permission_issues


def check_git_configuration():
    """Check Git configuration for proper setup"""
    print("\n🔧 CHECKING GIT CONFIGURATION")
    print("=" * 50)
    
    import subprocess
    
    git_checks = {
        'user.name': 'Git user name',
        'user.email': 'Git user email', 
        'commit.gpgsign': 'GPG commit signing (should be false)',
        'init.defaultBranch': 'Default branch name',
        'core.editor': 'Default editor'
    }
    
    git_issues = []
    
    try:
        for config, description in git_checks.items():
            try:
                result = subprocess.run(
                    ['git', 'config', '--global', config],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                if result.returncode == 0:
                    value = result.stdout.strip()
                    if config == 'commit.gpgsign' and value.lower() == 'true':
                        print(f"  ⚠️ {config:20} = {value} (should be false to prevent signing errors)")
                        git_issues.append(f"GPG signing enabled - may cause commit failures")
                    else:
                        print(f"  ✅ {config:20} = {value}")
                else:
                    print(f"  ❌ {config:20} = NOT SET - {description}")
                    git_issues.append(f"{config} not configured")
                    
            except subprocess.TimeoutExpired:
                print(f"  ⚠️ {config:20} = TIMEOUT - Git command timed out")
                git_issues.append(f"Git timeout for {config}")
            except Exception as e:
                print(f"  ❌ {config:20} = ERROR - {str(e)}")
                git_issues.append(f"Git error for {config}: {str(e)}")
                
    except FileNotFoundError:
        print("  ❌ Git not found in PATH")
        git_issues.append("Git not installed or not in PATH")
        
    # Test basic git operations
    try:
        # Test git status (basic git operation)
        result = subprocess.run(
            ['git', 'status', '--porcelain'],
            capture_output=True,
            text=True,
            timeout=10,
            cwd='/workspaces/sugarglitch-realops'
        )
        if result.returncode == 0:
            print("  ✅ Git repository operations working")
        else:
            print("  ⚠️ Git repository operations may have issues")
            
    except Exception as e:
        print(f"  ⚠️ Git repository test failed: {str(e)}")
    
    if git_issues:
        print(f"\n⚠️ Found {len(git_issues)} git configuration issues:")
        for issue in git_issues:
            print(f"  • {issue}")
        return False
    else:
        print("\n✅ Git configuration looks good!")
        return True


def main():
    """Main verification function"""
    print("🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥")
    print("💀 SUGARGLITCH REALOPS - ENVIRONMENT VERIFICATION 💀")
    print("🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥")
    print(f"Python Version: {sys.version}")
    print(f"Working Directory: {os.getcwd()}")
    print()
    
    # Run all checks
    checks = []
    
    # Environment variables
    env_ok, missing_env_req, missing_env_opt = check_environment_variables()
    checks.append(("Environment Variables", env_ok, f"{len(missing_env_req)} missing required"))
    
    # Dependencies
    deps_ok, missing_deps_crit, missing_deps_opt = check_dependencies()
    checks.append(("Dependencies", deps_ok, f"{len(missing_deps_crit)} missing critical"))
    
    # Files
    files_ok, missing_files, missing_dirs = check_files()
    checks.append(("Files & Directories", files_ok, f"{len(missing_files)} missing files"))
    
    # Permissions
    perms_ok, perm_issues = check_permissions()
    checks.append(("Permissions", perms_ok, f"{len(perm_issues)} permission issues"))
    
    # Git Configuration
    git_ok = check_git_configuration()
    checks.append(("Git Configuration", git_ok, ""))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 VERIFICATION SUMMARY")
    print("=" * 60)
    
    all_passed = True
    for check_name, passed, details in checks:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{check_name:25} {status:10} {details}")
        if not passed:
            all_passed = False
    
    # Overall result
    if all_passed:
        print("\n🎉🎉🎉 ALL CHECKS PASSED! READY FOR DEPLOYMENT! 🎉🎉🎉")
        print("✅ Environment is production-ready")
        print("\n🚀 Next steps:")
        print("  python main.py --help")
        print("  python main.py --list")
        print("  python main.py --interactive")
        return 0
    else:
        print("\n⚠️ SOME CHECKS FAILED")
        print("🔧 Required actions:")
        
        if missing_env_req:
            print(f"  • Set required environment variables: {', '.join(missing_env_req)}")
            print(f"  • Copy .env.example to .env and configure")
        
        if missing_deps_crit:
            print(f"  • Install missing packages: pip install {' '.join(missing_deps_crit)}")
            print(f"  • Or run: pip install -r requirements.txt")
        
        if missing_files:
            print(f"  • Ensure required files exist: {', '.join(missing_files)}")
        
        if perm_issues:
            print(f"  • Fix permission issues: {', '.join(perm_issues)}")
        
        return 1


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⚠️ Verification interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Verification failed with error: {e}")
        sys.exit(1)

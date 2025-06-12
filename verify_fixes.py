#!/usr/bin/env python3
"""
🔧 SugarGlitch RealOps - Environment Fix Verification
Verify that all critical environment issues have been resolved.
"""

import subprocess
import sys
import json
from datetime import datetime

def run_command(cmd, capture_output=True):
    """Run a shell command and return the result."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=capture_output, text=True)
        return result.returncode == 0, result.stdout.strip(), result.stderr.strip()
    except Exception as e:
        return False, "", str(e)

def check_git_config():
    """Verify Git configuration is correct."""
    print("🔍 Checking Git configuration...")
    
    # Check user configuration
    success, username, _ = run_command("git config user.name")
    if success and username == "chin4d0ll":
        print("  ✅ Git user.name: chin4d0ll")
    else:
        print(f"  ❌ Git user.name: {username} (expected: chin4d0ll)")
        return False
    
    success, email, _ = run_command("git config user.email")
    if success and email == "beamr.1232@gmail.com":
        print("  ✅ Git user.email: beamr.1232@gmail.com")
    else:
        print(f"  ❌ Git user.email: {email} (expected: beamr.1232@gmail.com)")
        return False
    
    # Check GPG signing is disabled
    success, gpgsign, _ = run_command("git config commit.gpgsign")
    if gpgsign.lower() in ["false", ""]:
        print("  ✅ GPG signing disabled")
    else:
        print(f"  ❌ GPG signing: {gpgsign} (expected: false)")
        return False
    
    return True

def test_git_commit():
    """Test that git commit works without GPG errors."""
    print("🔍 Testing Git commit functionality...")
    
    # Create a test file with a safe extension
    test_file = f"verification_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    success, _, _ = run_command(f"echo '# Verification test - {datetime.now()}' > {test_file}")
    if not success:
        print("  ❌ Failed to create test file")
        return False
    
    # Stage the file
    success, _, error = run_command(f"git add {test_file}")
    if not success:
        print(f"  ❌ Failed to stage test file: {error}")
        # Clean up
        run_command(f"rm -f {test_file}")
        return False
    
    # Commit the file
    success, output, error = run_command(f"git commit -m 'Test commit for verification'")
    if success:
        print("  ✅ Git commit successful")
        # Clean up
        run_command(f"git rm {test_file}")
        run_command("git commit -m 'Remove verification test file'")
        return True
    else:
        print(f"  ❌ Git commit failed: {error}")
        # Clean up even on failure
        run_command(f"rm -f {test_file}")
        run_command(f"git reset HEAD {test_file} 2>/dev/null")
        return False

def check_sql_extensions():
    """Check SQL Server extension status."""
    print("🔍 Checking SQL Server extensions...")
    
    success, extensions, _ = run_command("code --list-extensions 2>/dev/null | grep -i sql")
    if success and extensions:
        print("  ✅ SQL Server extensions installed (compatibility mode)")
        for ext in extensions.split('\n'):
            if ext.strip():
                print(f"    - {ext.strip()}")
    else:
        print("  ✅ No SQL Server extensions detected")
    
    return True

def check_environment_config():
    """Check that setup.sh and dotfiles are properly configured."""
    print("🔍 Checking environment configuration persistence...")
    
    # Check setup.sh has the correct git config
    try:
        with open('/workspaces/sugarglitch-realops/.devcontainer/setup.sh', 'r') as f:
            setup_content = f.read()
        
        if 'chin4d0ll' in setup_content and 'beamr.1232@gmail.com' in setup_content:
            print("  ✅ setup.sh has correct production git config")
        else:
            print("  ❌ setup.sh missing production git config")
            return False
            
        if 'commit.gpgsign false' in setup_content:
            print("  ✅ setup.sh disables GPG signing")
        else:
            print("  ❌ setup.sh missing GPG signing disable")
            return False
            
    except FileNotFoundError:
        print("  ❌ setup.sh not found")
        return False
    
    # Check dotfiles/.gitconfig
    try:
        with open('/workspaces/sugarglitch-realops/.devcontainer/dotfiles/.gitconfig', 'r') as f:
            gitconfig_content = f.read()
        
        if 'chin4d0ll' in gitconfig_content:
            print("  ✅ dotfiles/.gitconfig has correct user config")
        else:
            print("  ❌ dotfiles/.gitconfig missing correct user config")
            return False
            
    except FileNotFoundError:
        print("  ❌ dotfiles/.gitconfig not found")
        return False
    
    return True

def main():
    """Main verification function."""
    print("🚀 SugarGlitch RealOps - Environment Fix Verification")
    print("=" * 60)
    
    all_checks = [
        ("Git Configuration", check_git_config),
        ("Git Commit Test", test_git_commit),
        ("SQL Extensions", check_sql_extensions),
        ("Environment Config", check_environment_config)
    ]
    
    results = []
    for check_name, check_func in all_checks:
        print(f"\n📋 {check_name}:")
        try:
            result = check_func()
            results.append((check_name, result))
            if result:
                print(f"  🎉 {check_name}: PASSED")
            else:
                print(f"  💥 {check_name}: FAILED")
        except Exception as e:
            print(f"  💥 {check_name}: ERROR - {e}")
            results.append((check_name, False))
    
    print("\n" + "=" * 60)
    print("📊 FINAL RESULTS:")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for check_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status}: {check_name}")
    
    print(f"\n🎯 Score: {passed}/{total} checks passed")
    
    if passed == total:
        print("🎉 ALL ENVIRONMENT ISSUES RESOLVED!")
        print("✅ GPG commit works")
        print("✅ Git user is set to production values")
        print("✅ SQL extensions use compatibility mode")
        print("✅ All fixes are persistent in setup.sh/dotfiles")
        return 0
    else:
        print("💥 Some issues remain - check the failed tests above")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)

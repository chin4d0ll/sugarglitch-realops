#!/usr/bin/env python3
"""
🔧 GitHub Copilot Diagnostic & Fix Tool
ตรวจสอบและแก้ไขปัญหา Copilot ใน Codespaces แบบอัตโนมัติ
"""

import os
import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime


class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'


def print_status(message, status="info"):
    icons = {"success": "✅", "error": "❌", "warning": "⚠️", "info": "ℹ️"}
    colors = {"success": Colors.GREEN, "error": Colors.RED,
              "warning": Colors.YELLOW, "info": Colors.BLUE}

    color = colors.get(status, Colors.BLUE)
    icon = icons.get(status, "ℹ️")

    print(f"{color}{icon} {message}{Colors.END}")


def run_command(command, capture_output=True):
    """รันคำสั่งและคืนผลลัพธ์"""
    try:
        result = subprocess.run(
            command, shell=True, capture_output=capture_output, text=True, timeout=30)
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "Command timed out"
    except Exception as e:
        return False, "", str(e)


def check_network_connectivity():
    """ตรวจสอบการเชื่อมต่อเครือข่าย"""
    print_status("🌐 Checking Network Connectivity", "info")

    endpoints = [
        "https://api.github.com",
        "https://copilot-proxy.githubusercontent.com",
        "https://github.com"
    ]

    all_good = True
    for endpoint in endpoints:
        success, stdout, stderr = run_command(
            f"curl -s -I {endpoint} | head -1")
        if success and ("200" in stdout or "404" in stdout):
            print_status(f"  {endpoint}: OK", "success")
        else:
            print_status(f"  {endpoint}: FAILED", "error")
            all_good = False

    return all_good


def check_github_auth():
    """ตรวจสอบการ authentication กับ GitHub"""
    print_status("🔐 Checking GitHub Authentication", "info")

    # เช็ค gh CLI
    success, stdout, stderr = run_command("gh auth status")
    if success:
        print_status("  GitHub CLI: Authenticated", "success")
        return True
    else:
        print_status("  GitHub CLI: Not authenticated", "warning")

        # ลอง authenticate
        print_status("  Attempting to authenticate...", "info")
        success, stdout, stderr = run_command(
            "gh auth login --web", capture_output=False)
        if success:
            print_status("  GitHub CLI: Authentication successful", "success")
            return True
        else:
            print_status("  GitHub CLI: Authentication failed", "error")
            return False


def check_copilot_status():
    """ตรวจสอบสถานะ Copilot subscription"""
    print_status("🤖 Checking Copilot Status", "info")

    success, stdout, stderr = run_command("gh api /user/copilot_enabled")
    if success:
        try:
            data = json.loads(stdout)
            if data.get("copilot_enabled", False):
                print_status("  Copilot: Enabled", "success")
                return True
            else:
                print_status("  Copilot: Not enabled on account", "error")
                return False
        except json.JSONDecodeError:
            print_status("  Copilot: Status unknown", "warning")
            return False
    else:
        print_status("  Copilot: Cannot check status", "error")
        return False


def check_vscode_extensions():
    """ตรวจสอบ VS Code extensions"""
    print_status("🔌 Checking VS Code Extensions", "info")

    # หา VS Code server path
    vscode_server_paths = [
        os.path.expanduser("~/.vscode-server"),
        "/home/vscode/.vscode-server",
        "/root/.vscode-server"
    ]

    vscode_path = None
    for path in vscode_server_paths:
        if os.path.exists(path):
            vscode_path = path
            break

    if not vscode_path:
        print_status("  VS Code server not found", "warning")
        return False

    # หา Copilot extension
    extensions_path = os.path.join(vscode_path, "extensions")
    if os.path.exists(extensions_path):
        copilot_extensions = [d for d in os.listdir(
            extensions_path) if "copilot" in d.lower()]
        if copilot_extensions:
            print_status(
                f"  Copilot extensions found: {len(copilot_extensions)}", "success")
            for ext in copilot_extensions:
                print_status(f"    - {ext}", "info")
            return True
        else:
            print_status("  No Copilot extensions found", "error")
            return False
    else:
        print_status("  Extensions directory not found", "error")
        return False


def check_environment_variables():
    """ตรวจสอบ environment variables"""
    print_status("🌍 Checking Environment Variables", "info")

    important_vars = [
        "GITHUB_TOKEN",
        "GITHUB_CODESPACES_TOKEN",
        "CODESPACES",
        "VSCODE_AGENT_FOLDER"
    ]

    found_vars = 0
    for var in important_vars:
        if os.getenv(var):
            print_status(f"  {var}: Set", "success")
            found_vars += 1
        else:
            print_status(f"  {var}: Not set", "warning")

    return found_vars > 0


def fix_common_issues():
    """แก้ไขปัญหาที่พบบ่อย"""
    print_status("🔧 Applying Common Fixes", "info")

    fixes_applied = []

    # Fix 1: Clear extension cache
    print_status("  Clearing extension cache...", "info")
    vscode_server_path = os.path.expanduser("~/.vscode-server")
    if os.path.exists(vscode_server_path):
        cache_paths = [
            os.path.join(vscode_server_path, "data", "logs"),
            os.path.join(vscode_server_path, "data", "CachedExtensions")
        ]

        for cache_path in cache_paths:
            if os.path.exists(cache_path):
                success, stdout, stderr = run_command(f"rm -rf {cache_path}")
                if success:
                    fixes_applied.append("Cleared extension cache")

    # Fix 2: Reset VS Code settings
    print_status("  Creating optimal VS Code settings...", "info")
    vscode_settings = {
        "github.copilot.enable": {
            "*": True,
            "yaml": True,
            "plaintext": True,
            "markdown": True,
            "python": True,
            "javascript": True,
            "typescript": True
        },
        "github.copilot.advanced": {
            "debug.overrideEngine": "copilot-codex",
            "debug.testOverrideProxyUrl": "",
            "debug.showScores": False
        },
        "editor.inlineSuggest.enabled": True,
        "editor.suggestSelection": "first"
    }

    workspace_vscode_dir = Path("/workspaces/sugarglitch-realops/.vscode")
    workspace_vscode_dir.mkdir(exist_ok=True)

    settings_file = workspace_vscode_dir / "settings.json"
    with open(settings_file, 'w') as f:
        json.dump(vscode_settings, f, indent=2)

    fixes_applied.append("Created optimal VS Code settings")

    # Fix 3: Set proper environment variables
    print_status("  Setting environment variables...", "info")
    env_script = """
# Add to ~/.bashrc for persistent environment
export GITHUB_COPILOT_ENABLED=true
export VSCODE_COPILOT_RELEASE=true
"""

    bashrc_path = os.path.expanduser("~/.bashrc")
    if os.path.exists(bashrc_path):
        with open(bashrc_path, 'a') as f:
            f.write(f"\n# GitHub Copilot settings - {datetime.now()}\n")
            f.write(env_script)
        fixes_applied.append(
            "Updated ~/.bashrc with Copilot environment variables")

    return fixes_applied


def create_diagnostic_report():
    """สร้างรายงานการตรวจสอบ"""
    print_status("📋 Creating Diagnostic Report", "info")

    report = {
        "timestamp": datetime.now().isoformat(),
        "system_info": {},
        "checks": {},
        "recommendations": []
    }

    # System info
    success, stdout, stderr = run_command("uname -a")
    if success:
        report["system_info"]["os"] = stdout.strip()

    success, stdout, stderr = run_command(
        "curl -s https://api.github.com/rate_limit")
    if success:
        try:
            rate_limit = json.loads(stdout)
            report["system_info"]["github_rate_limit"] = rate_limit
        except:
            pass

    # Save report
    report_file = "/workspaces/sugarglitch-realops/copilot_diagnostic_report.json"
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)

    print_status(f"  Report saved: {report_file}", "success")
    return report_file


def main():
    """ฟังก์ชันหลัก"""
    print(f"{Colors.BOLD}🔧 GitHub Copilot Diagnostic Tool{Colors.END}")
    print("=" * 50)

    # รันการตรวจสอบ
    checks = [
        ("Network Connectivity", check_network_connectivity),
        ("GitHub Authentication", check_github_auth),
        ("Copilot Status", check_copilot_status),
        ("VS Code Extensions", check_vscode_extensions),
        ("Environment Variables", check_environment_variables)
    ]

    results = {}
    for check_name, check_func in checks:
        try:
            results[check_name] = check_func()
        except Exception as e:
            print_status(f"Error in {check_name}: {e}", "error")
            results[check_name] = False

    # สรุปผลการตรวจสอบ
    print("\n" + "=" * 50)
    print_status("📊 DIAGNOSTIC SUMMARY", "info")
    print("=" * 50)

    passed = sum(1 for result in results.values() if result)
    total = len(results)

    for check_name, result in results.items():
        status = "success" if result else "error"
        print_status(f"{check_name}: {'PASS' if result else 'FAIL'}", status)

    print(f"\nOverall: {passed}/{total} checks passed")

    # แนะนำการแก้ไข
    if passed < total:
        print_status("\n🔧 Applying fixes...", "info")
        fixes = fix_common_issues()

        for fix in fixes:
            print_status(f"Applied: {fix}", "success")

        print_status("\n💡 RECOMMENDATIONS:", "info")
        print("1. Restart VS Code window (Ctrl+Shift+P → Developer: Reload Window)")
        print("2. Sign out and sign in to GitHub (Command Palette → GitHub: Sign Out)")
        print("3. Try different Codespace region if problem persists")
        print("4. Use VS Code desktop version as temporary workaround")

        if not results.get("Copilot Status", False):
            print_status(
                "\n❗ IMPORTANT: Your GitHub account may not have Copilot access", "warning")
            print("   Check: https://github.com/settings/copilot")

    # สร้างรายงาน
    report_file = create_diagnostic_report()

    print(f"\n{Colors.GREEN}🎉 Diagnostic completed!{Colors.END}")
    print(f"Report saved: {report_file}")


if __name__ == "__main__":
    main()

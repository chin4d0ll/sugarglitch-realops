#!/usr/bin/env python3
"""
💫 Brute Force Tools Status Checker
สำหรับตรวจสอบความพร้อมของเครื่องมือ brute force ทั้งหมด
"""

import os
import sys
import importlib.util
from pathlib import Path
import subprocess
import platform
from datetime import datetime

# สีสันสำหรับ terminal
try:
    from colorama import Fore, Back, Style, init
    init(autoreset=True)
    USE_COLOR = True
except ImportError:
    # ถ้าไม่มี colorama ให้ใช้ text ธรรมดา
    class DummyColor:
        def __getattr__(self, name):
            return ""
    Fore = DummyColor()
    Back = DummyColor()
    Style = DummyColor()
    USE_COLOR = False


# สร้าง banner สวยๆ
def print_banner():
    """Show fancy banner"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    banner = f"""
{Fore.CYAN + Style.BRIGHT}╔══════════════════════════════════════════════════════════╗
║                                                          ║
║  {Fore.YELLOW}💀 {Fore.MAGENTA}SUGARGLITCH REALOPS BRUTEFORCE TOOLKIT {Fore.RED}2025{Fore.CYAN}  💀  ║
║                                                          ║
║  {Fore.GREEN}Scripts: {Fore.WHITE}12{Fore.CYAN}  |  {Fore.GREEN}Targets: {Fore.WHITE}2{Fore.CYAN}  |  {Fore.GREEN}Status: {Fore.YELLOW}READY{Fore.CYAN}  |  {Fore.GREEN}ENV: {Fore.WHITE}VENV{Fore.CYAN}  ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
{Fore.WHITE + Style.BRIGHT}📆 {now} | 🌐 {platform.node()}
{Style.RESET_ALL}"""
    print(banner)


def check_package(package_name, required=True):
    """Check if Python package is installed"""
    try:
        __import__(package_name)
        is_installed = True
    except ImportError:
        # Handle special cases where import name != package name
        if package_name == "beautifulsoup4":
            try:
                __import__("bs4")
                is_installed = True
            except ImportError:
                is_installed = False
        else:
            is_installed = False

    if is_installed:
        status = f"{Fore.GREEN}✓{Style.RESET_ALL}" if USE_COLOR else "✓"
    else:
        status = f"{Fore.RED}✗{Style.RESET_ALL}" if USE_COLOR else "✗"

    required_text = f"{Fore.RED}[REQUIRED]{Style.RESET_ALL}" if required and not is_installed else ""

    print(f"  {status} {package_name.ljust(20)} {required_text}")

    return is_installed


def check_script(script_path):
    """Check if script exists and has required imports"""
    path = Path(script_path)

    if not path.exists():
        status = f"{Fore.RED}✗{Style.RESET_ALL}" if USE_COLOR else "✗"
        print(
            f"  {status} {path.name.ljust(30)} {Fore.RED}[NOT FOUND]{Style.RESET_ALL}")
        return False

    status = f"{Fore.GREEN}✓{Style.RESET_ALL}" if USE_COLOR else "✓"
    print(
        f"  {status} {path.name.ljust(30)} {Fore.GREEN}[READY]{Style.RESET_ALL}")
    return True


def check_target(target_name):
    """Check if target is available in brute_targets.json"""
    targets_file = Path("/workspaces/sugarglitch-realops/brute_targets.json")

    if not targets_file.exists():
        status = f"{Fore.RED}✗{Style.RESET_ALL}" if USE_COLOR else "✗"
        print(
            f"  {status} {target_name.ljust(20)} {Fore.RED}[NOT FOUND]{Style.RESET_ALL}")
        return False

    try:
        import json
        with open(targets_file, 'r') as f:
            targets = json.load(f)

        target_exists = any(t.get('username') == target_name for t in targets)

        if target_exists:
            status = f"{Fore.GREEN}✓{Style.RESET_ALL}" if USE_COLOR else "✓"
            print(
                f"  {status} {target_name.ljust(20)} {Fore.GREEN}[READY]{Style.RESET_ALL}")
        else:
            status = f"{Fore.YELLOW}?{Style.RESET_ALL}" if USE_COLOR else "?"
            print(
                f"  {status} {target_name.ljust(20)} {Fore.YELLOW}[NOT IN TARGETS]{Style.RESET_ALL}")

        return target_exists

    except Exception as e:
        status = f"{Fore.RED}✗{Style.RESET_ALL}" if USE_COLOR else "✗"
        print(
            f"  {status} {target_name.ljust(20)} {Fore.RED}[ERROR: {str(e)}]{Style.RESET_ALL}")
        return False


def check_venv():
    """Check if running in venv"""
    is_venv = sys.prefix != sys.base_prefix

    if is_venv:
        status = f"{Fore.GREEN}✓{Style.RESET_ALL}" if USE_COLOR else "✓"
        env_path = sys.prefix
    else:
        status = f"{Fore.YELLOW}!{Style.RESET_ALL}" if USE_COLOR else "!"
        env_path = "System Python"

    print(f"  {status} {'Virtual Environment'.ljust(20)} {env_path}")

    return is_venv


def main():
    """Main function"""
    print_banner()

    # 🌟 Check virtual environment
    print(f"{Fore.CYAN + Style.BRIGHT}🌀 VIRTUAL ENVIRONMENT{Style.RESET_ALL}")
    check_venv()
    print()

    # 📦 Check required packages
    print(f"{Fore.CYAN + Style.BRIGHT}📦 REQUIRED PACKAGES{Style.RESET_ALL}")
    check_package("requests", required=True)
    check_package("fake_useragent", required=True)
    check_package("cloudscraper", required=True)
    check_package("selenium", required=False)
    check_package("undetected_chromedriver", required=False)
    check_package("beautifulsoup4", required=True)
    check_package("asyncio", required=True)
    check_package("aiohttp", required=True)
    check_package("asyncssh", required=False)
    check_package("psutil", required=False)
    check_package("socks", required=False)  # PySocks installs as socks
    print()

    # 📜 Check scripts
    print(f"{Fore.CYAN + Style.BRIGHT}📜 BRUTE FORCE SCRIPTS{Style.RESET_ALL}")
    scripts_base = Path("/workspaces/sugarglitch-realops/scripts")
    check_script(scripts_base / "bruteforce_ig.py")
    check_script(scripts_base / "optimized_ig_brute.py")
    check_script(scripts_base / "attack_alx_trading.py")
    check_script(scripts_base / "fixed_ig_brute_400.py")
    check_script(scripts_base / "http400_fixed_brute.py")
    check_script(scripts_base / "premium_ig_brute.py")
    check_script(scripts_base / "simple_ig_brute.py")
    check_script("/workspaces/sugarglitch-realops/brute_force_instagram.py")
    print()

    # 🎯 Check targets
    print(f"{Fore.CYAN + Style.BRIGHT}🎯 ATTACK TARGETS{Style.RESET_ALL}")
    check_target("alx.trading")
    check_target("whatilove1728")
    print()

    # 📝 Print available commands
    print(f"{Fore.CYAN + Style.BRIGHT}📝 AVAILABLE COMMANDS{Style.RESET_ALL}")
    cmds = [
        ("python scripts/bruteforce_ig.py", "Advanced brute forcer (complete)"),
        ("python scripts/attack_alx_trading.py", "Target-specific forcer"),
        ("python scripts/http400_fixed_brute.py", "HTTP 400 fixed version"),
        ("python scripts/optimized_ig_brute.py", "Easy-to-understand forcer"),
    ]

    for cmd, desc in cmds:
        print(
            f"  {Fore.YELLOW}${Style.RESET_ALL} {Fore.GREEN}{cmd}{Style.RESET_ALL}")
        print(f"    {Fore.WHITE}{desc}{Style.RESET_ALL}")
    print()

    # 🔄 Print venv activation commands
    print(f"{Fore.CYAN + Style.BRIGHT}🔄 VENV ACTIVATION{Style.RESET_ALL}")
    print(f"  {Fore.YELLOW}${Style.RESET_ALL} {Fore.GREEN}source .venv/bin/activate{Style.RESET_ALL}")
    print()


if __name__ == "__main__":
    main()

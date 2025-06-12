#!/usr/bin/env python3

"""
SugarGlitch RealOps - Installation Summary
Quick overview of all installed tools and their status
"""

import subprocess
import sys

def check_command(cmd):
    """Check if a command exists and is executable"""
    try:
        result = subprocess.run(f"which {cmd}", shell=True, capture_output=True, text=True)
        return result.returncode == 0
    except:
        return False

def check_python_module(module):
    """Check if a Python module is importable"""
    try:
        result = subprocess.run(f"python3 -c 'import {module}'", shell=True, capture_output=True, text=True)
        return result.returncode == 0
    except:
        return False

def main():
    print("🔥🔥🔥 SugarGlitch RealOps - Installation Summary 🔥🔥🔥")
    print("=" * 60)
    
    # Core Tools
    print("\n📦 SUCCESSFULLY INSTALLED TOOLS:")
    print("-" * 35)
    
    installed_tools = []
    
    # Check system tools
    system_tools = [
        ("Metasploit Framework", "msfconsole"),
        ("Amass", "amass"),
        ("Subfinder", "subfinder"),
        ("Nmap", "nmap"),
        ("SQLMap", "sqlmap"),
        ("Hydra", "hydra"),
        ("Gobuster", "gobuster"),
        ("Masscan", "masscan"),
        ("WhatWeb", "whatweb"),
        ("Fierce", "fierce"),
        ("Git", "git"),
        ("Curl", "curl"),
        ("Wget", "wget"),
        ("Whois", "whois"),
    ]
    
    for name, cmd in system_tools:
        if check_command(cmd):
            installed_tools.append(name)
            print(f"✅ {name}")
        else:
            print(f"❌ {name}")
    
    # Check Python modules
    print("\n🐍 PYTHON SECURITY MODULES:")
    print("-" * 30)
    
    python_modules = [
        ("Shodan", "shodan"),
        ("Censys", "censys"),
        ("Scapy", "scapy"),
        ("Impacket", "impacket"),
        ("DNSPython", "dns"),
        ("Requests", "requests"),
        ("BeautifulSoup4", "bs4"),
        ("Selenium", "selenium"),
        ("Playwright", "playwright"),
        ("wafw00f", "wafw00f"),
    ]
    
    python_installed = []
    for name, module in python_modules:
        if check_python_module(module):
            python_installed.append(name)
            print(f"✅ {name}")
        else:
            print(f"❌ {name}")
    
    # Summary
    total_system = len(system_tools)
    installed_system = len([t for t in system_tools if check_command(t[1])])
    
    total_python = len(python_modules)
    installed_python = len(python_installed)
    
    print("\n" + "=" * 60)
    print("📊 INSTALLATION SUMMARY:")
    print(f"   🛠️  System Tools: {installed_system}/{total_system}")
    print(f"   🐍 Python Modules: {installed_python}/{total_python}")
    print(f"   🎯 Total Success: {installed_system + installed_python}/{total_system + total_python}")
    
    percentage = ((installed_system + installed_python) / (total_system + total_python)) * 100
    print(f"   📈 Success Rate: {percentage:.1f}%")
    
    if percentage >= 85:
        print("\n🔥 STATUS: FULLY LOADED - Ready for operations!")
    elif percentage >= 70:
        print("\n⚡ STATUS: WELL EQUIPPED - Most tools available!")
    else:
        print("\n⚠️  STATUS: PARTIAL - Some tools missing!")
    
    print("\n🚀 QUICK START COMMANDS:")
    print("   realops                 - Go to project directory")
    print("   python main.py --list   - Show all available modules")
    print("   python main.py env-test - Test environment")
    print("   msfconsole              - Start Metasploit")
    print("   amass enum -d target.com - Subdomain enumeration")
    print("   subfinder -d target.com  - Find subdomains")
    
    print(f"\n💾 Full report: data/tools_verification_report.json")
    print("=" * 60)

if __name__ == "__main__":
    main()

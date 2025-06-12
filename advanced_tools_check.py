#!/usr/bin/env python3
"""
🔥 SugarGlitch RealOps - Advanced Tools Verification
Check all available security and penetration testing tools
"""

import subprocess
import sys
import importlib

def check_command(cmd):
    """Check if a command exists"""
    try:
        result = subprocess.run(['which', cmd], capture_output=True, text=True)
        return result.returncode == 0
    except:
        return False

def check_python_module(module):
    """Check if a Python module is available"""
    try:
        importlib.import_module(module)
        return True
    except ImportError:
        return False

def get_tool_version(cmd, version_flag='--version'):
    """Get tool version"""
    try:
        result = subprocess.run([cmd, version_flag], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            return result.stdout.strip().split('\n')[0]
        return "Version unknown"
    except:
        return "Version unknown"

def main():
    """Main verification function"""
    print("🔥🔥🔥 SugarGlitch RealOps - Advanced Tools Check 🔥🔥🔥")
    print("=" * 70)
    
    # Core security tools
    core_tools = [
        ('nmap', 'Nmap Network Scanner'),
        ('sqlmap', 'SQL Injection Tool'),
        ('hydra', 'Password Cracking Tool'),
        ('nikto', 'Web Vulnerability Scanner'),
        ('dirb', 'Web Content Scanner'),
        ('gobuster', 'Directory/DNS Bruteforcer'),
        ('masscan', 'Fast Port Scanner'),
        ('git', 'Version Control System'),
        ('curl', 'HTTP Client'),
        ('wget', 'File Downloader'),
        ('dig', 'DNS Lookup Tool'),
        ('whois', 'Domain Information Tool')
    ]
    
    # Advanced tools
    advanced_tools = [
        ('msfconsole', 'Metasploit Framework'),
        ('burpsuite', 'Burp Suite'),
        ('theharvester', 'Email Harvester'),
        ('amass', 'Attack Surface Discovery'),
        ('subfinder', 'Subdomain Discovery'),
        ('fierce', 'DNS Scanner'),
        ('dnsrecon', 'DNS Reconnaissance'),
        ('wafw00f', 'WAF Detection'),
        ('whatweb', 'Web Technology Identifier')
    ]
    
    # Python security modules
    python_modules = [
        ('shodan', 'Shodan Search Engine'),
        ('censys', 'Censys Search Engine'),
        ('scapy', 'Packet Manipulation'),
        ('impacket', 'Network Protocol Tools'),
        ('dnspython', 'DNS Toolkit'),
        ('requests', 'HTTP Library'),
        ('beautifulsoup4', 'Web Scraping'),
        ('selenium', 'Browser Automation'),
        ('playwright', 'Browser Automation')
    ]
    
    print("🛠️  CORE SECURITY TOOLS")
    print("=" * 25)
    core_available = 0
    for cmd, name in core_tools:
        if check_command(cmd):
            version = get_tool_version(cmd, '--version' if cmd != 'git' else '--version')
            print(f"✅ {name}: {cmd} - {version[:50]}")
            core_available += 1
        else:
            print(f"❌ {name}: {cmd} - NOT FOUND")
    
    print(f"\n📊 Core Tools: {core_available}/{len(core_tools)} available")
    
    print("\n🎯 ADVANCED PENETRATION TOOLS")
    print("=" * 30)
    advanced_available = 0
    for cmd, name in advanced_tools:
        if check_command(cmd):
            version = get_tool_version(cmd)
            print(f"✅ {name}: {cmd} - {version[:50]}")
            advanced_available += 1
        else:
            print(f"❌ {name}: {cmd} - NOT FOUND")
    
    print(f"\n📊 Advanced Tools: {advanced_available}/{len(advanced_tools)} available")
    
    print("\n🐍 PYTHON SECURITY MODULES")
    print("=" * 27)
    python_available = 0
    for module, name in python_modules:
        if check_python_module(module):
            print(f"✅ {name}: {module}")
            python_available += 1
        else:
            print(f"❌ {name}: {module} - NOT FOUND")
    
    print(f"\n📊 Python Modules: {python_available}/{len(python_modules)} available")
    
    # Overall assessment
    total_tools = len(core_tools) + len(advanced_tools) + len(python_modules)
    total_available = core_available + advanced_available + python_available
    percentage = (total_available / total_tools) * 100
    
    print("\n" + "=" * 70)
    print("📊 OVERALL ASSESSMENT")
    print("=" * 20)
    print(f"🎯 Total Tools Available: {total_available}/{total_tools} ({percentage:.1f}%)")
    
    if percentage >= 90:
        print("🎉 EXCELLENT! Advanced security toolkit is complete!")
        status = "PRODUCTION READY"
    elif percentage >= 75:
        print("✅ GOOD! Most security tools are available.")
        status = "MOSTLY READY"
    elif percentage >= 60:
        print("⚠️  ACCEPTABLE! Basic security tools available.")
        status = "BASIC READY"
    else:
        print("❌ INSUFFICIENT! Many tools are missing.")
        status = "NOT READY"
    
    print(f"🔥 Status: {status}")
    
    # Installation suggestions
    print("\n💡 INSTALLATION SUGGESTIONS:")
    print("=" * 28)
    
    if not check_command('nikto'):
        print("📦 Install Nikto: sudo apt-get install nikto")
    
    if not check_command('msfconsole'):
        print("📦 Install Metasploit: curl https://raw.githubusercontent.com/rapid7/metasploit-omnibus/master/config/templates/metasploit-framework-wrappers/msfupdate.erb > msfinstall && chmod 755 msfinstall && ./msfinstall")
    
    if not check_python_module('theHarvester'):
        print("📦 Install TheHarvester: pip install theHarvester")
    
    if not check_command('amass'):
        print("📦 Install Amass: sudo snap install amass")
    
    print("\n🚀 Run 'python main.py env-test' to test the environment!")

if __name__ == "__main__":
    main()

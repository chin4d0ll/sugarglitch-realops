#!/usr/bin/env python3

"""
SugarGlitch RealOps - Final Tools Verification
Comprehensive check of all installed security tools
"""

import subprocess
import sys
import json
from datetime import datetime

def run_command(cmd):
    """Run command and return True if successful"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
        return result.returncode == 0, result.stdout.strip()
    except:
        return False, ""

def check_tool(name, command, description=""):
    """Check if a tool is available"""
    success, output = run_command(command)
    status = "✅" if success else "❌"
    version = output.split('\n')[0][:100] if output else "NOT FOUND"
    return {
        "name": name,
        "command": command.split()[0],
        "description": description,
        "available": success,
        "version": version,
        "status": status
    }

def main():
    print("🔥🔥🔥 SugarGlitch RealOps - Final Tools Verification 🔥🔥🔥")
    print("=" * 70)
    
    # Core Security Tools
    print("\n🛠️  CORE SECURITY TOOLS")
    print("=" * 25)
    
    core_tools = [
        ("Nmap", "nmap --version", "Network Scanner"),
        ("SQLMap", "sqlmap --version", "SQL Injection Tool"),
        ("Hydra", "hydra -h", "Password Cracking Tool"),
        ("Nikto", "nikto -Version", "Web Vulnerability Scanner"),
        ("Dirb", "dirb", "Web Content Scanner"),
        ("Gobuster", "gobuster version", "Directory/DNS Bruteforcer"),
        ("Masscan", "masscan --version", "Fast Port Scanner"),
        ("Git", "git --version", "Version Control System"),
        ("Curl", "curl --version", "HTTP Client"),
        ("Wget", "wget --version", "File Downloader"),
        ("Dig", "dig -v", "DNS Lookup Tool"),
        ("Whois", "whois --version", "Domain Information Tool"),
    ]
    
    core_results = []
    for name, cmd, desc in core_tools:
        result = check_tool(name, cmd, desc)
        core_results.append(result)
        print(f"{result['status']} {name}: {result['command']} - {result['version']}")
    
    # Advanced Penetration Tools
    print("\n🎯 ADVANCED PENETRATION TOOLS")
    print("=" * 30)
    
    advanced_tools = [
        ("Metasploit", "msfconsole --version", "Exploitation Framework"),
        ("Amass", "amass version", "Attack Surface Discovery"),
        ("Subfinder", "subfinder -version", "Subdomain Discovery"),
        ("TheHarvester", "python3 -c 'import theHarvester; print(\"Available\")'", "Email Harvester"),
        ("DNSRecon", "python3 -c 'import dnsrecon; print(\"Available\")'", "DNS Reconnaissance"),
        ("Wafw00f", "python3 -c 'import wafw00f; print(\"Available\")'", "WAF Detection"),
        ("WhatWeb", "whatweb --version", "Web Technology Identifier"),
        ("Fierce", "fierce -h", "DNS Scanner"),
    ]
    
    advanced_results = []
    for name, cmd, desc in advanced_tools:
        result = check_tool(name, cmd, desc)
        advanced_results.append(result)
        print(f"{result['status']} {name}: {result['command']} - {result['version']}")
    
    # Python Security Modules
    print("\n🐍 PYTHON SECURITY MODULES")
    print("=" * 27)
    
    python_modules = [
        ("Shodan", "python3 -c 'import shodan; print(\"Available\")'", "Search Engine API"),
        ("Censys", "python3 -c 'import censys; print(\"Available\")'", "Internet Scanner"),
        ("Scapy", "python3 -c 'import scapy; print(\"Available\")'", "Packet Manipulation"),
        ("Impacket", "python3 -c 'import impacket; print(\"Available\")'", "Network Protocols"),
        ("DNSPython", "python3 -c 'import dns; print(\"Available\")'", "DNS Toolkit"),
        ("Requests", "python3 -c 'import requests; print(\"Available\")'", "HTTP Library"),
        ("BeautifulSoup", "python3 -c 'import bs4; print(\"Available\")'", "Web Scraping"),
        ("Selenium", "python3 -c 'import selenium; print(\"Available\")'", "Browser Automation"),
        ("Playwright", "python3 -c 'import playwright; print(\"Available\")'", "Browser Automation"),
    ]
    
    python_results = []
    for name, cmd, desc in python_modules:
        result = check_tool(name, cmd, desc)
        python_results.append(result)
        print(f"{result['status']} {name}: {result['version']}")
    
    # Calculate Statistics
    all_results = core_results + advanced_results + python_results
    total_tools = len(all_results)
    available_tools = sum(1 for r in all_results if r['available'])
    percentage = (available_tools / total_tools) * 100
    
    print("\n" + "=" * 70)
    print("📊 FINAL ASSESSMENT")
    print("=" * 20)
    print(f"🎯 Total Tools Available: {available_tools}/{total_tools} ({percentage:.1f}%)")
    
    if percentage >= 90:
        status = "🔥 FULLY LOADED - Production Ready!"
        color = "GREEN"
    elif percentage >= 75:
        status = "⚡ WELL EQUIPPED - Ready for Operations"
        color = "YELLOW"
    elif percentage >= 50:
        status = "⚠️  BASIC READY - Core Tools Available"
        color = "ORANGE"
    else:
        status = "❌ INSUFFICIENT - Need More Tools"
        color = "RED"
    
    print(f"🔥 Status: {status}")
    
    # Save results to JSON
    report = {
        "timestamp": datetime.now().isoformat(),
        "total_tools": total_tools,
        "available_tools": available_tools,
        "percentage": percentage,
        "status": status,
        "core_tools": core_results,
        "advanced_tools": advanced_results,
        "python_modules": python_results
    }
    
    with open("/workspaces/sugarglitch-realops/data/tools_verification_report.json", "w") as f:
        json.dump(report, f, indent=2)
    
    print(f"\n💾 Report saved to: data/tools_verification_report.json")
    print(f"\n🚀 Run 'python main.py env-test' to test the environment!")
    
    return available_tools == total_tools

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

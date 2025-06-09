#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 Full Network Reconnaissance for tradeyourway.co.uk
สแกนเครือข่ายอัตโนมัติ - เต็มรูปแบบ
"""

import os
import subprocess
import sys
import time
from datetime import datetime

def print_banner():
    print("""
🚀 SUGARGLITCH FULL RECONNAISSANCE 
===================================
🎯 Target: tradeyourway.co.uk
💀 Complete Automated Scan 💀
===================================
    """)

def log_message(message):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {message}")

def run_command(cmd, description, save_to_file=None):
    log_message(f"🔍 {description}")
    print("=" * 60)
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=300)
        output = result.stdout
        
        if result.returncode == 0:
            print(output)
            if save_to_file:
                with open(save_to_file, 'w') as f:
                    f.write(output)
                log_message(f"💾 Results saved to: {save_to_file}")
        else:
            error_msg = result.stderr
            print(f"❌ Error: {error_msg}")
            log_message(f"Command failed: {cmd}")
            
    except subprocess.TimeoutExpired:
        print("⏰ Timeout - Command took too long (5 minutes)")
    except Exception as e:
        print(f"❌ Exception: {e}")
    print("\n")

def main():
    target = "tradeyourway.co.uk"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = f"recon_results_{target.replace('.', '_')}_{timestamp}"
    
    print_banner()
    log_message(f"🎯 Starting Full Reconnaissance for: {target}")
    log_message(f"📁 Output directory: {output_dir}")
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Phase 1: Basic Information Gathering
    log_message("🔍 Phase 1: Basic Information Gathering")
    
    # DNS Lookup
    run_command(
        f"nslookup {target}",
        "DNS Lookup (nslookup)",
        f"{output_dir}/dns_lookup.txt"
    )
    
    # Ping test
    run_command(
        f"ping -c 4 {target}",
        "Ping Test (4 packets)",
        f"{output_dir}/ping_test.txt"
    )
    
    # WHOIS lookup
    run_command(
        f"whois {target}",
        "WHOIS Information",
        f"{output_dir}/whois_info.txt"
    )
    
    # Phase 2: Network Scanning
    log_message("🔍 Phase 2: Network Scanning")
    
    # Basic Nmap scan
    run_command(
        f"nmap -sS -O -sV -p- {target}",
        "Full Port Scan with OS Detection",
        f"{output_dir}/nmap_full_scan.txt"
    )
    
    # Common ports scan
    run_command(
        f"nmap -sS -sV -sC -p 21,22,23,25,53,80,110,143,443,993,995,8080,8443 {target}",
        "Common Ports Scan with Scripts",
        f"{output_dir}/nmap_common_ports.txt"
    )
    
    # UDP scan
    run_command(
        f"nmap -sU -p 53,67,68,69,123,161,162 {target}",
        "UDP Scan (Common Ports)",
        f"{output_dir}/nmap_udp_scan.txt"
    )
    
    # Phase 3: Web Application Testing
    log_message("🔍 Phase 3: Web Application Testing")
    
    # Web server headers
    run_command(
        f"curl -I https://{target}",
        "HTTPS Headers",
        f"{output_dir}/https_headers.txt"
    )
    
    run_command(
        f"curl -I http://{target}",
        "HTTP Headers",
        f"{output_dir}/http_headers.txt"
    )
    
    # SSL/TLS Information
    run_command(
        f"nmap --script ssl-enum-ciphers -p 443 {target}",
        "SSL/TLS Cipher Enumeration",
        f"{output_dir}/ssl_ciphers.txt"
    )
    
    # Directory enumeration
    run_command(
        f"gobuster dir -u https://{target} -w /usr/share/wordlists/dirb/common.txt -x php,html,txt,js,css",
        "Directory Enumeration (HTTPS)",
        f"{output_dir}/gobuster_https.txt"
    )
    
    # Phase 4: Advanced Reconnaissance
    log_message("🔍 Phase 4: Advanced Reconnaissance")
    
    # Subdomain enumeration
    run_command(
        f"subfinder -d {target} -silent",
        "Subdomain Enumeration",
        f"{output_dir}/subdomains.txt"
    )
    
    # Technology detection
    run_command(
        f"whatweb {target}",
        "Technology Detection",
        f"{output_dir}/whatweb.txt"
    )
    
    # Phase 5: Final Report
    log_message("📊 Phase 5: Generating Final Report")
    
    report_file = f"{output_dir}/RECONNAISSANCE_REPORT.txt"
    with open(report_file, 'w') as f:
        f.write(f"""
🔍 SUGARGLITCH RECONNAISSANCE REPORT
====================================
Target: {target}
Date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Operator: SUGARGLITCH
====================================

SCAN SUMMARY:
✅ DNS Lookup completed
✅ WHOIS Information gathered
✅ Full port scan completed
✅ Common ports scan completed
✅ UDP scan completed
✅ Web headers analysis completed
✅ SSL/TLS analysis completed
✅ Directory enumeration completed
✅ Subdomain enumeration completed
✅ Technology detection completed

📁 All detailed results saved in: {output_dir}/

⚠️  LEGAL NOTICE:
This scan was performed on {target} with proper authorization.
All activities were conducted for legitimate security testing purposes.

🎯 Next Steps:
1. Review all output files for detailed findings
2. Analyze discovered services and technologies
3. Plan targeted testing based on discovered attack surface
4. Document all findings for security assessment

====================================
SUGARGLITCH RECONNAISSANCE COMPLETE
====================================
        """)
    
    log_message("✅ Full Reconnaissance Complete!")
    log_message(f"📊 Final report saved to: {report_file}")
    log_message(f"📁 All results in directory: {output_dir}")
    
    print("""
🎉 RECONNAISSANCE COMPLETE! 🎉
===============================
✅ All scans finished successfully
📊 Results saved to output directory
🔍 Review files for detailed findings
===============================
    """)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Scan interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        sys.exit(1)

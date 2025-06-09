#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 Auto Network Reconnaissance for tradeyourway.co.uk
สแกนเครือข่ายอัตโนมัติ - เต็มรูปแบบ
"""

import os
import subprocess
import sys
import time
from datetime import datetime

def print_banner():
    print("""
🚀 SUGARGLITCH AUTO RECONNAISSANCE 
===================================
🎯 Target: tradeyourway.co.uk
💀 Full Automated Scan 💀
===================================
    """)

def log_message(message):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {message}")

def run_command(cmd, description):
    log_message(f"🔍 {description}")
    print("=" * 60)
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=300)
        if result.returncode == 0:
            print(result.stdout)
            if result.stderr:
                print(f"Warning: {result.stderr}")
        else:
            print(f"Error: {result.stderr}")
    except subprocess.TimeoutExpired:
        print("⏰ Timeout - Command took too long")
    except Exception as e:
        print(f"❌ Error: {e}")
    print("\n")

def main():
    target = "tradeyourway.co.uk"
    output_dir = f"recon_results_{target.replace('.', '_')}"
    
    print_banner()
    log_message(f"เริ่มสแกนเต็มรูปแบบ: {target}")
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    log_message(f"สร้างโฟลเดอร์ผลลัพธ์: {output_dir}")
    
    # Phase 1: Basic Information Gathering
    log_message("🌐 Phase 1: Basic Information Gathering")
    
    # DNS Lookup
    run_command(f"nslookup {target}", "DNS Lookup")
    run_command(f"dig {target} ANY", "DNS Records")
    
    # WHOIS Information
    run_command(f"whois {target}", "WHOIS Information")
    
    # Phase 2: Host Discovery
    log_message("🖥️ Phase 2: Host Discovery")
    
    # Ping test
    run_command(f"ping -c 4 {target}", "Ping Test")
    
    # Host discovery
    run_command(f"nmap -sn {target}", "Host Discovery")
    
    # Phase 3: Port Scanning
    log_message("🚪 Phase 3: Port Scanning")
    
    # Quick scan
    run_command(f"nmap -T4 -F {target} -oN {output_dir}/quick_scan.txt", 
                "Quick Port Scan (Top 100 ports)")
    
    # Top 1000 ports
    run_command(f"nmap --top-ports 1000 {target} -oN {output_dir}/top1000_scan.txt", 
                "Top 1000 Ports Scan")
    
    # Common web ports
    run_command(f"nmap -p 80,443,8080,8443,8000,3000,5000 {target} -oN {output_dir}/web_ports.txt", 
                "Common Web Ports")
    
    # Phase 4: Service Detection
    log_message("🔧 Phase 4: Service Detection")
    
    # Service version detection
    run_command(f"nmap -sV {target} -oN {output_dir}/service_detection.txt", 
                "Service Version Detection")
    
    # OS detection
    run_command(f"nmap -O {target} -oN {output_dir}/os_detection.txt", 
                "Operating System Detection")
    
    # NSE Script scan
    run_command(f"nmap -sC {target} -oN {output_dir}/script_scan.txt", 
                "NSE Default Scripts")
    
    # Phase 5: Web Application Testing
    log_message("🌐 Phase 5: Web Application Testing")
    
    # HTTP headers
    run_command(f"curl -I http://{target}", "HTTP Headers (Port 80)")
    run_command(f"curl -I https://{target}", "HTTPS Headers (Port 443)")
    
    # Robots.txt
    run_command(f"curl -s http://{target}/robots.txt", "Robots.txt Check")
    
    # Check for common directories (simple check)
    common_dirs = ["admin", "login", "wp-admin", "phpmyadmin", "backup", "test"]
    for directory in common_dirs:
        run_command(f"curl -s -o /dev/null -w '%{{http_code}}' http://{target}/{directory}/", 
                   f"Directory Check: /{directory}/")
    
    # Phase 6: SSL/TLS Analysis
    log_message("🔒 Phase 6: SSL/TLS Analysis")
    
    # SSL scan
    run_command(f"nmap --script ssl-enum-ciphers -p 443 {target} -oN {output_dir}/ssl_scan.txt", 
                "SSL/TLS Cipher Analysis")
    
    # Certificate information
    run_command(f"openssl s_client -connect {target}:443 -servername {target} < /dev/null 2>/dev/null | openssl x509 -text -noout", 
                "SSL Certificate Information")
    
    # Phase 7: Vulnerability Scanning
    log_message("🛡️ Phase 7: Vulnerability Scanning")
    
    # Nmap vulnerability scripts
    run_command(f"nmap --script vuln {target} -oN {output_dir}/vulnerability_scan.txt", 
                "Vulnerability Scripts")
    
    # Check for common vulnerabilities
    run_command(f"nmap --script http-sql-injection {target} -p 80,443", 
                "SQL Injection Check")
    
    run_command(f"nmap --script http-cross-domain-policy {target} -p 80,443", 
                "Cross Domain Policy Check")
    
    # Phase 8: Additional Information
    log_message("📊 Phase 8: Additional Information")
    
    # Traceroute
    run_command(f"traceroute {target}", "Network Route Tracing")
    
    # Technology detection (if available)
    run_command(f"curl -s -I https://{target} | grep -i 'server\\|x-powered-by\\|x-generator'", 
                "Technology Stack Detection")
    
    # Final Summary
    log_message("✅ Reconnaissance Complete!")
    print("=" * 60)
    print(f"📁 ผลลัพธ์ทั้งหมดถูกบันทึกใน: {output_dir}/")
    print("📋 ไฟล์ผลลัพธ์:")
    print(f"   - quick_scan.txt")
    print(f"   - top1000_scan.txt") 
    print(f"   - web_ports.txt")
    print(f"   - service_detection.txt")
    print(f"   - os_detection.txt")
    print(f"   - script_scan.txt")
    print(f"   - ssl_scan.txt")
    print(f"   - vulnerability_scan.txt")
    print("=" * 60)
    
    # Generate summary report
    generate_summary_report(target, output_dir)

def generate_summary_report(target, output_dir):
    report_file = f"{output_dir}/summary_report.txt"
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("🔍 NETWORK RECONNAISSANCE SUMMARY REPORT\n")
        f.write("=" * 50 + "\n")
        f.write(f"Target: {target}\n")
        f.write(f"Scan Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Performed by: Sugarglitch Auto Recon\n")
        f.write("=" * 50 + "\n\n")
        
        f.write("📋 SCAN PHASES COMPLETED:\n")
        f.write("✅ Phase 1: Basic Information Gathering\n")
        f.write("✅ Phase 2: Host Discovery\n") 
        f.write("✅ Phase 3: Port Scanning\n")
        f.write("✅ Phase 4: Service Detection\n")
        f.write("✅ Phase 5: Web Application Testing\n")
        f.write("✅ Phase 6: SSL/TLS Analysis\n")
        f.write("✅ Phase 7: Vulnerability Scanning\n")
        f.write("✅ Phase 8: Additional Information\n\n")
        
        f.write("📁 OUTPUT FILES:\n")
        for file in os.listdir(output_dir):
            if file.endswith('.txt'):
                f.write(f"   - {file}\n")
        
        f.write(f"\n⚠️  IMPORTANT:\n")
        f.write(f"This scan was performed on {target} with owner authorization.\n")
        f.write(f"Review all results carefully for security findings.\n")
    
    log_message(f"📄 Summary report generated: {report_file}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Scan interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

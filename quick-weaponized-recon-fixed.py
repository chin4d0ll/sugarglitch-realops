#!/usr/bin/env python3

import subprocess
import json
import time
from datetime import datetime

def run_cmd(cmd, timeout=10):
    """Simple command runner"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return result.stdout, result.stderr, result.returncode
    except subprocess.TimeoutExpired:
        return "", "Timeout", -1
    except Exception as e:
        return "", str(e), -1

def main():
    target = "tradeyourway.co.uk"
    timestamp = int(time.time())
    
    print("🔥 QUICK WEAPONIZED RECON")
    print("=" * 40)
    print(f"Target: {target}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 40)
    
    results = {}
    
    # 1. Basic DNS
    print("\n🔍 DNS Resolution...")
    stdout, stderr, code = run_cmd(f"nslookup {target}")
    if code == 0:
        print("✅ DNS resolves successfully")
        if "Address:" in stdout:
            ip = [line.split()[-1] for line in stdout.split('\n') if 'Address:' in line and '#' not in line]
            if ip:
                results['ip'] = ip[0]
                print(f"📍 IP: {ip[0]}")
    
    # 2. Basic Port Scan
    print("\n🔍 Quick Port Scan...")
    common_ports = [80, 443, 22, 21, 25, 53]
    open_ports = []
    
    for port in common_ports:
        stdout, stderr, code = run_cmd(f"timeout 2 bash -c 'echo >/dev/tcp/{target}/{port}'", timeout=3)
        if code == 0:
            open_ports.append(port)
            print(f"✅ Port {port}: OPEN")
        else:
            print(f"❌ Port {port}: CLOSED/FILTERED")
    
    results['open_ports'] = open_ports
    
    # 3. HTTP Headers
    print("\n🔍 HTTP Analysis...")
    stdout, stderr, code = run_cmd(f"curl -I -s -L https://{target}", timeout=10)
    if code == 0:
        print("✅ HTTPS accessible")
        headers = stdout.lower()
        
        # Check security headers
        security_checks = {
            'x-frame-options': 'Clickjacking Protection',
            'x-xss-protection': 'XSS Protection', 
            'strict-transport-security': 'HSTS',
            'content-security-policy': 'CSP'
        }
        
        missing = []
        for header, desc in security_checks.items():
            if header in headers:
                print(f"✅ {desc}: Present")
            else:
                print(f"⚠️  {desc}: Missing")
                missing.append(desc)
        
        results['missing_security_headers'] = missing
    
    # 4. SSL Check
    print("\n🔍 SSL Certificate...")
    stdout, stderr, code = run_cmd(f"echo | timeout 5 openssl s_client -connect {target}:443 -servername {target} 2>/dev/null | openssl x509 -noout -dates", timeout=8)
    if code == 0 and stdout:
        print("✅ SSL Certificate valid")
        print(f"📅 {stdout.strip()}")
        results['ssl_status'] = 'valid'
    else:
        print("⚠️  SSL Certificate issues")
        results['ssl_status'] = 'issues'
    
    # 5. Quick Subdomain Check
    print("\n🔍 Common Subdomains...")
    common_subs = ['www', 'mail', 'ftp', 'api', 'admin', 'dev', 'test']
    found_subs = []
    
    for sub in common_subs:
        full_domain = f"{sub}.{target}"
        stdout, stderr, code = run_cmd(f"nslookup {full_domain}", timeout=3)
        if code == 0 and 'NXDOMAIN' not in stdout:
            found_subs.append(full_domain)
            print(f"✅ Found: {full_domain}")
        else:
            print(f"❌ Not found: {full_domain}")
    
    results['subdomains'] = found_subs
    
    # Summary
    print("\n" + "=" * 50)
    print("🎯 WEAPONIZED RECON SUMMARY")
    print("=" * 50)
    print(f"Target: {target}")
    print(f"IP: {results.get('ip', 'Unknown')}")
    print(f"Open Ports: {results.get('open_ports', [])}")
    print(f"Subdomains: {len(results.get('subdomains', []))}")
    print(f"SSL Status: {results.get('ssl_status', 'Unknown')}")
    print(f"Missing Security Headers: {len(results.get('missing_security_headers', []))}")
    
    # Attack Vectors
    print(f"\n🎯 POTENTIAL ATTACK VECTORS:")
    if 22 in results.get('open_ports', []):
        print("  • SSH (Port 22) - Brute force potential")
    if 80 in results.get('open_ports', []):
        print("  • HTTP (Port 80) - Web application attacks")
    if 443 in results.get('open_ports', []):
        print("  • HTTPS (Port 443) - Web application attacks")
    if results.get('missing_security_headers'):
        print(f"  • Missing security headers: {', '.join(results.get('missing_security_headers', []))}")
    if any('admin' in sub or 'api' in sub for sub in results.get('subdomains', [])):
        print("  • High-risk subdomains found (admin/api)")
        
    # Save results
    report_file = f"quick_weaponized_recon_{target.replace('.', '_')}_{timestamp}.json"
    
    final_report = {
        'target': target,
        'timestamp': timestamp,
        'scan_date': datetime.now().isoformat(),
        'results': results,
        'summary': {
            'total_open_ports': len(results.get('open_ports', [])),
            'total_subdomains': len(results.get('subdomains', [])),
            'security_score': max(0, 100 - len(results.get('missing_security_headers', [])) * 20)
        }
    }
    
    with open(report_file, 'w') as f:
        json.dump(final_report, f, indent=2)
    
    print(f"\n📄 Report saved: {report_file}")
    print("🔥 Quick Weaponized Recon Complete!")

if __name__ == "__main__":
    main()

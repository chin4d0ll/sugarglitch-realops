#!/usr/bin/env python3

import subprocess
import json
import threading
import time
from datetime import datetime
import os
import sys

class DirectWeaponizedRecon:
    def __init__(self, target_domain="tradeyourway.co.uk"):
        self.target = target_domain.replace("https://", "").replace("http://", "").replace("/", "")
        self.timestamp = int(time.time())
        self.results = {}
        
    def print_banner(self):
        print("🔥" * 50)
        print("    DIRECT WEAPONIZED RECONNAISSANCE SUITE")
        print("🔥" * 50)
        print(f"🎯 Target: {self.target}")
        print(f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("🔥" * 50)
        print()
        
    def run_command(self, cmd, timeout=30):
        """Execute command with timeout"""
        try:
            result = subprocess.run(
                cmd, 
                shell=True, 
                capture_output=True, 
                text=True, 
                timeout=timeout
            )
            return {
                'stdout': result.stdout,
                'stderr': result.stderr,
                'returncode': result.returncode
            }
        except subprocess.TimeoutExpired:
            return {'stdout': '', 'stderr': 'Command timed out', 'returncode': -1}
        except Exception as e:
            return {'stdout': '', 'stderr': str(e), 'returncode': -1}
    
    def aggressive_subdomain_enum(self):
        """Aggressive subdomain enumeration"""
        print("🔍 [1/6] Aggressive Subdomain Enumeration...")
        
        # Multiple methods for subdomain discovery
        methods = []
        
        # Method 1: DNS brute force with common subdomains
        common_subs = ['www', 'mail', 'ftp', 'api', 'admin', 'dev', 'test', 'stage', 'staging', 'beta', 'app', 'web', 'secure', 'login', 'portal', 'dashboard', 'cdn', 'media', 'static', 'assets', 'img', 'images', 'upload', 'downloads', 'files', 'docs', 'support', 'help', 'blog', 'news', 'shop', 'store', 'payment', 'pay', 'billing', 'account', 'user', 'users', 'client', 'clients', 'partner', 'partners', 'vendor', 'vendors', 'supplier', 'suppliers', 'crm', 'erp', 'hr', 'finance', 'accounting', 'sales', 'marketing', 'seo', 'analytics', 'stats', 'monitoring', 'logs', 'backup', 'archive', 'old', 'new', 'v1', 'v2', 'api-v1', 'api-v2', 'mobile', 'm', 'wap', 'vpn', 'ssh', 'sftp', 'git', 'svn', 'repo', 'code', 'jenkins', 'ci', 'cd', 'build', 'deploy', 'docker', 'k8s', 'kubernetes', 'aws', 'azure', 'gcp', 'cloud', 'db', 'database', 'mysql', 'postgres', 'redis', 'mongo', 'elasticsearch', 'search', 'elastic', 'kibana', 'grafana', 'prometheus', 'nagios', 'zabbix', 'splunk']
        
        found_subdomains = []
        
        for sub in common_subs[:20]:  # Test first 20 to avoid timeout
            full_domain = f"{sub}.{self.target}"
            result = self.run_command(f"nslookup {full_domain}", timeout=5)
            if result['returncode'] == 0 and 'NXDOMAIN' not in result['stdout']:
                found_subdomains.append(full_domain)
                print(f"  ✅ Found: {full_domain}")
        
        # Method 2: Certificate transparency logs (simulated)
        print("  🔍 Checking certificate transparency logs...")
        ct_result = self.run_command(f"curl -s 'https://crt.sh/?q={self.target}&output=json'", timeout=10)
        if ct_result['returncode'] == 0:
            try:
                ct_data = json.loads(ct_result['stdout'])
                for entry in ct_data[:10]:  # Limit to first 10
                    if 'name_value' in entry:
                        domains = entry['name_value'].split('\n')
                        for domain in domains:
                            if domain.endswith(self.target) and domain not in found_subdomains:
                                found_subdomains.append(domain)
                                print(f"  🎯 CT Log: {domain}")
            except:
                pass
        
        self.results['subdomains'] = found_subdomains
        print(f"  📊 Total subdomains found: {len(found_subdomains)}")
        print()
        
    def aggressive_port_scan(self):
        """Aggressive port scanning"""
        print("🔍 [2/6] Aggressive Port Scanning...")
        
        # Common critical ports
        critical_ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 993, 995, 1433, 3306, 3389, 5432, 5900, 8080, 8443, 9000, 27017]
        
        open_ports = []
        
        for port in critical_ports:
            print(f"  🔍 Scanning port {port}...", end=' ')
            result = self.run_command(f"timeout 3 bash -c 'echo >/dev/tcp/{self.target}/{port}'", timeout=5)
            if result['returncode'] == 0:
                open_ports.append(port)
                print("✅ OPEN")
            else:
                print("❌ CLOSED")
        
        self.results['open_ports'] = open_ports
        print(f"  📊 Open ports: {open_ports}")
        print()
        
    def technology_fingerprinting(self):
        """Technology stack fingerprinting"""
        print("🔍 [3/6] Technology Fingerprinting...")
        
        tech_stack = {}
        
        # HTTP headers analysis
        result = self.run_command(f"curl -I -s -L https://{self.target}", timeout=10)
        if result['returncode'] == 0:
            headers = result['stdout']
            
            # Server detection
            if 'Server:' in headers:
                server_line = [line for line in headers.split('\n') if 'Server:' in line]
                if server_line:
                    tech_stack['server'] = server_line[0].split(':', 1)[1].strip()
                    print(f"  🖥️  Server: {tech_stack['server']}")
            
            # Technology detection
            tech_indicators = {
                'PHP': ['X-Powered-By: PHP', 'Set-Cookie: PHPSESSID'],
                'ASP.NET': ['X-AspNet-Version', 'X-Powered-By: ASP.NET'],
                'Express.js': ['X-Powered-By: Express'],
                'Apache': ['Server: Apache'],
                'Nginx': ['Server: nginx'],
                'IIS': ['Server: Microsoft-IIS'],
                'Cloudflare': ['CF-RAY', 'Server: cloudflare']
            }
            
            for tech, indicators in tech_indicators.items():
                for indicator in indicators:
                    if indicator in headers:
                        tech_stack[tech.lower()] = True
                        print(f"  ⚙️  {tech}: Detected")
                        break
        
        self.results['technology'] = tech_stack
        print()
        
    def vulnerability_assessment(self):
        """Basic vulnerability assessment"""
        print("🔍 [4/6] Vulnerability Assessment...")
        
        vulnerabilities = []
        
        # SSL/TLS analysis
        ssl_result = self.run_command(f"timeout 10 openssl s_client -connect {self.target}:443 -servername {self.target} </dev/null 2>/dev/null | openssl x509 -noout -dates", timeout=15)
        if ssl_result['returncode'] == 0:
            print("  🔒 SSL Certificate: Valid")
            if 'notAfter' in ssl_result['stdout']:
                print(f"  📅 {ssl_result['stdout'].strip()}")
        else:
            vulnerabilities.append("SSL Certificate Issues")
            print("  ⚠️  SSL Certificate: Issues detected")
        
        # HTTP security headers
        headers_result = self.run_command(f"curl -I -s -L https://{self.target}", timeout=10)
        if headers_result['returncode'] == 0:
            headers = headers_result['stdout'].lower()
            
            security_headers = {
                'x-frame-options': 'Clickjacking Protection',
                'x-xss-protection': 'XSS Protection',
                'x-content-type-options': 'MIME Sniffing Protection',
                'strict-transport-security': 'HSTS',
                'content-security-policy': 'CSP'
            }
            
            missing_headers = []
            for header, description in security_headers.items():
                if header not in headers:
                    missing_headers.append(description)
                    print(f"  ⚠️  Missing: {description}")
                else:
                    print(f"  ✅ Present: {description}")
            
            if missing_headers:
                vulnerabilities.append(f"Missing Security Headers: {', '.join(missing_headers)}")
        
        self.results['vulnerabilities'] = vulnerabilities
        print(f"  📊 Vulnerabilities found: {len(vulnerabilities)}")
        print()
        
    def attack_surface_analysis(self):
        """Attack surface mapping"""
        print("🔍 [5/6] Attack Surface Analysis...")
        
        attack_vectors = []
        
        # Analyze open ports for attack vectors
        if 'open_ports' in self.results:
            port_vectors = {
                21: "FTP - Potential for anonymous access, brute force",
                22: "SSH - Brute force, key-based attacks",
                23: "Telnet - Unencrypted, credential sniffing",
                25: "SMTP - Email relay, enumeration",
                53: "DNS - Zone transfer, enumeration",
                80: "HTTP - Web application attacks",
                443: "HTTPS - Web application attacks, SSL/TLS",
                1433: "SQL Server - Database attacks",
                3306: "MySQL - Database attacks",
                3389: "RDP - Remote access, brute force",
                5432: "PostgreSQL - Database attacks"
            }
            
            for port in self.results['open_ports']:
                if port in port_vectors:
                    attack_vectors.append(f"Port {port}: {port_vectors[port]}")
                    print(f"  🎯 Port {port}: {port_vectors[port]}")
        
        # Analyze subdomains for attack surface
        if 'subdomains' in self.results:
            subdomain_risks = []
            for subdomain in self.results['subdomains']:
                if any(keyword in subdomain.lower() for keyword in ['admin', 'test', 'dev', 'staging', 'api']):
                    subdomain_risks.append(f"High-risk subdomain: {subdomain}")
                    print(f"  🚨 High-risk: {subdomain}")
            
            attack_vectors.extend(subdomain_risks)
        
        self.results['attack_vectors'] = attack_vectors
        print(f"  📊 Attack vectors identified: {len(attack_vectors)}")
        print()
        
    def generate_report(self):
        """Generate comprehensive report"""
        print("🔍 [6/6] Generating Weaponized Report...")
        
        # Console report
        print("\n" + "="*60)
        print("🔥 WEAPONIZED RECONNAISSANCE REPORT")
        print("="*60)
        print(f"Target: {self.target}")
        print(f"Scan Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60)
        
        # Subdomains
        print(f"\n📍 SUBDOMAINS DISCOVERED ({len(self.results.get('subdomains', []))})")
        print("-" * 30)
        for subdomain in self.results.get('subdomains', []):
            print(f"  • {subdomain}")
        
        # Open Ports
        print(f"\n🔓 OPEN PORTS ({len(self.results.get('open_ports', []))})")
        print("-" * 30)
        for port in self.results.get('open_ports', []):
            print(f"  • {port}/tcp")
        
        # Technology Stack
        print(f"\n⚙️  TECHNOLOGY STACK")
        print("-" * 30)
        for tech, value in self.results.get('technology', {}).items():
            print(f"  • {tech}: {value}")
        
        # Vulnerabilities
        print(f"\n⚠️  VULNERABILITIES ({len(self.results.get('vulnerabilities', []))})")
        print("-" * 30)
        for vuln in self.results.get('vulnerabilities', []):
            print(f"  • {vuln}")
        
        # Attack Vectors
        print(f"\n🎯 ATTACK VECTORS ({len(self.results.get('attack_vectors', []))})")
        print("-" * 30)
        for vector in self.results.get('attack_vectors', []):
            print(f"  • {vector}")
        
        print("\n" + "="*60)
        
        # Save JSON report
        report_file = f"weaponized_recon_{self.target.replace('.', '_')}_{self.timestamp}.json"
        with open(report_file, 'w') as f:
            json.dump({
                'target': self.target,
                'timestamp': self.timestamp,
                'scan_date': datetime.now().isoformat(),
                'results': self.results
            }, f, indent=2)
        
        print(f"📄 Report saved: {report_file}")
        print("🔥 Weaponized Reconnaissance Complete!")
        
    def run_full_scan(self):
        """Execute full weaponized reconnaissance"""
        self.print_banner()
        
        try:
            self.aggressive_subdomain_enum()
            self.aggressive_port_scan()
            self.technology_fingerprinting()
            self.vulnerability_assessment()
            self.attack_surface_analysis()
            self.generate_report()
            
        except KeyboardInterrupt:
            print("\n⚠️  Scan interrupted by user")
        except Exception as e:
            print(f"\n❌ Error during scan: {str(e)}")

def main():
    # Default target
    target = "tradeyourway.co.uk"
    
    # Check if target provided as argument
    if len(sys.argv) > 1:
        target = sys.argv[1]
    
    print(f"🎯 Starting weaponized recon on: {target}")
    print("⚠️  WARNING: Use only on domains you own or have explicit permission to test!")
    print()
    
    # Create and run scanner
    scanner = DirectWeaponizedRecon(target)
    scanner.run_full_scan()

if __name__ == "__main__":
    main()

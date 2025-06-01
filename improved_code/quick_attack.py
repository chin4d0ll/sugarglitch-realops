from utils.error_handler import safe_execution, safe_print

#!/usr/bin/env python3
"""
⚡ QUICK ATTACK MODE ⚡
🔥 Fast & Furious Testing 🔥
💀 No Delays, Maximum Speed 💀
"""

import random
import time
import json
import requests
from typing import Dict, List, Optional
from urllib.parse import urljoin

class QuickAttackEngine:
    """
    ⚡ High-speed attack engine for rapid testing
    🔥 Optimized for speed and efficiency
    💀 No mercy, no delays
    """
    
    def __init__(self):
        self.attack_count = 0
        self.targets_hit = []
        self.vulnerabilities = []
        
        # Speed-optimized headers
        self.quick_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        
        # Quick payloads for rapid testing
        self.quick_payloads = {
            'xss': [
                '<script>alert("XSS")</script>',
                '"><script>alert(1)</script>',
                "';alert('XSS');//"
            ],
            'sqli': [
                "' OR '1'='1",
                "' UNION SELECT NULL--",
                "admin'--"
            ],
            'lfi': [
                '../../../etc/passwd',
                '....//....//....//etc//passwd'
            ]
        }
        
        # Quick directory list
        self.quick_dirs = [
            'admin', 'login', 'api', 'test', 'backup',
            'config', 'uploads', '.git', 'robots.txt'
        ]
        
        print("⚡ Quick Attack Engine Initialized")
        print("🔥 Speed mode: MAXIMUM")
        print("💀 No mercy protocol: ACTIVATED")
    
    def quick_request(self, url: str, timeout: int = 5) -> Optional[Dict]:
        """Lightning-fast request"""
        
        self.attack_count += 1
        
        try:
            response = requests.get(
                url, 
                headers=self.quick_headers,
                timeout=timeout,
                verify=False,
                allow_redirects=True
            )
            
            return {
                'status': response.status_code,
                'headers': dict(response.headers),
                'content': response.text,
                'size': len(response.text),
                'url': response.url
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def rapid_port_scan(self, target: str) -> List[int]:
        """Ultra-fast port scanning"""
        
        print(f"⚡ Rapid port scan: {target}")
        
        # Top critical ports only
        critical_ports = [21, 22, 23, 25, 53, 80, 135, 139, 443, 445, 993, 995, 3389, 5432, 3306]
        open_ports = []
        
        import socket
        
        for port in critical_ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.5)  # Ultra-fast timeout
                result = sock.connect_ex((target, port))
                if result == 0:
                    open_ports.append(port)
                    print(f"⚡ Port {port} OPEN")
                sock.close()
            except:
                pass
        
        return open_ports
    
    def speed_directory_scan(self, base_url: str) -> List[str]:
        """High-speed directory discovery"""
        
        print(f"⚡ Speed directory scan: {base_url}")
        found = []
        
        for directory in self.quick_dirs:
            test_url = urljoin(base_url, directory)
            response = self.quick_request(test_url, timeout=3)
            
            if response and not response.get('error') and response['status'] == 200:
                found.append(test_url)
                print(f"⚡ FOUND: {test_url}")
        
        return found
    
    def rapid_vuln_test(self, url: str) -> List[Dict]:
        """Rapid vulnerability testing"""
        
        print(f"⚡ Rapid vuln test: {url}")
        vulnerabilities = []
        
        # Quick XSS test
        for payload in self.quick_payloads['xss']:
            test_url = f"{url}?test={payload}"
            response = self.quick_request(test_url, timeout=3)
            
            if response and not response.get('error'):
                if payload in response['content']:
                    vuln = {
                        'type': 'XSS',
                        'severity': 'High',
                        'url': test_url,
                        'payload': payload
                    }
                    vulnerabilities.append(vuln)
                    self.vulnerabilities.append(vuln)
                    print(f"🚨 XSS FOUND: {test_url}")
        
        # Quick SQL injection test
        for payload in self.quick_payloads['sqli']:
            test_url = f"{url}?id={payload}"
            response = self.quick_request(test_url, timeout=3)
            
            if response and not response.get('error'):
                content = response['content'].lower()
                sql_errors = ['mysql_fetch', 'ora-', 'microsoft ole db', 'postgresql', 'syntax error']
                
                if any(error in content for error in sql_errors):
                    vuln = {
                        'type': 'SQL Injection',
                        'severity': 'Critical',
                        'url': test_url,
                        'payload': payload
                    }
                    vulnerabilities.append(vuln)
                    self.vulnerabilities.append(vuln)
                    print(f"🚨 SQLi FOUND: {test_url}")
        
        return vulnerabilities
    
    def lightning_recon(self, target: str) -> Dict:
        """Lightning-fast reconnaissance"""
        
        print(f"⚡ Lightning recon: {target}")
        
        results = {
            'target': target,
            'ports': [],
            'directories': [],
            'vulnerabilities': [],
            'technologies': [],
            'attack_surface': 0
        }
        
        # Determine protocol
        if not target.startswith(('http://', 'https://')):
            # Try HTTPS first, then HTTP
            https_url = f"https://{target}"
            http_url = f"http://{target}"
            
            https_response = self.quick_request(https_url, timeout=3)
            if https_response and not https_response.get('error'):
                base_url = https_url
                print("⚡ HTTPS available")
            else:
                http_response = self.quick_request(http_url, timeout=3)
                if http_response and not http_response.get('error'):
                    base_url = http_url
                    print("⚡ HTTP only")
                else:
                    print("❌ No web service detected")
                    return results
        else:
            base_url = target
        
        # Port scan
        results['ports'] = self.rapid_port_scan(target.replace('https://', '').replace('http://', '').split('/')[0])
        
        # Directory scan
        results['directories'] = self.speed_directory_scan(base_url)
        
        # Vulnerability test
        results['vulnerabilities'] = self.rapid_vuln_test(base_url)
        
        # Quick technology detection
        main_response = self.quick_request(base_url)
        if main_response and not main_response.get('error'):
            results['technologies'] = self._quick_tech_detect(main_response)
        
        # Calculate attack surface
        results['attack_surface'] = len(results['ports']) + len(results['directories']) + len(results['vulnerabilities'])
        
        self.targets_hit.append(target)
        
        return results
    
    def _quick_tech_detect(self, response: Dict) -> List[str]:
        """Quick technology detection"""
        
        technologies = []
        content = response['content'].lower()
        headers = response['headers']
        
        # Server detection
        if 'Server' in headers:
            server = headers['Server']
            technologies.append(f"Server: {server}")
        
        # Quick framework detection
        if 'wordpress' in content or 'wp-content' in content:
            technologies.append('WordPress')
        elif 'drupal' in content:
            technologies.append('Drupal')
        elif 'joomla' in content:
            technologies.append('Joomla')
        
        # JavaScript frameworks
        if 'react' in content:
            technologies.append('React')
        if 'angular' in content:
            technologies.append('Angular')
        if 'vue' in content:
            technologies.append('Vue.js')
        
        return technologies
    
    def blitz_attack(self, targets: List[str]) -> Dict:
        """Blitz attack on multiple targets"""
        
        print(f"⚡ BLITZ ATTACK MODE")
        print(f"🎯 Targets: {len(targets)}")
        print("💀 Commencing rapid assault...")
        
        blitz_results = {
            'total_targets': len(targets),
            'targets_hit': 0,
            'total_vulnerabilities': 0,
            'critical_findings': [],
            'attack_summary': {}
        }
        
        for target in targets:
            print(f"\n⚡ ATTACKING: {target}")
            
            recon_results = self.lightning_recon(target)
            
            blitz_results['targets_hit'] += 1
            blitz_results['total_vulnerabilities'] += len(recon_results['vulnerabilities'])
            blitz_results['attack_summary'][target] = recon_results
            
            # Identify critical findings
            for vuln in recon_results['vulnerabilities']:
                if vuln['severity'] == 'Critical':
                    blitz_results['critical_findings'].append({
                        'target': target,
                        'vulnerability': vuln
                    })
            
            print(f"✅ {target} - Ports: {len(recon_results['ports'])}, Dirs: {len(recon_results['directories'])}, Vulns: {len(recon_results['vulnerabilities'])}")
        
        return blitz_results
    
    def generate_attack_report(self, blitz_results: Dict) -> str:
        """Generate rapid attack report"""
        
        report = f"""
⚡ QUICK ATTACK REPORT ⚡
🔥 BLITZ ASSAULT RESULTS 🔥
{'='*40}

📊 ATTACK STATISTICS:
  Total Targets: {blitz_results['total_targets']}
  Targets Hit: {blitz_results['targets_hit']}
  Total Requests: {self.attack_count}
  Vulnerabilities Found: {blitz_results['total_vulnerabilities']}
  Critical Issues: {len(blitz_results['critical_findings'])}

"""
        
        if blitz_results['critical_findings']:
            report += "🚨 CRITICAL VULNERABILITIES:\n"
            for finding in blitz_results['critical_findings']:
                vuln = finding['vulnerability']
                report += f"  Target: {finding['target']}\n"
                report += f"  Type: {vuln['type']}\n"
                report += f"  URL: {vuln['url']}\n\n"
        
        report += f"""
⚡ SPEED METRICS:
  Average Requests/Target: {self.attack_count // max(1, blitz_results['targets_hit'])}
  Total Attack Surface Points: {sum(r['attack_surface'] for r in blitz_results['attack_summary'].values())}

💀 ATTACK COMPLETED 💀
⚡ Use findings responsibly ⚡
"""
        
        return report

@safe_execution
def main():
    """Launch Quick Attack Mode"""
    
    print("⚡" * 25)
    print("⚡ QUICK ATTACK MODE ⚡")
    print("🔥 LIGHTNING FAST ASSAULT 🔥")
    print("💀 NO MERCY PROTOCOL 💀")
    print("⚡" * 25)
    
    # Initialize attack engine
    attack_engine = QuickAttackEngine()
    
    # Test targets (use authorized targets only)
    targets = [
        "httpbin.org",
        "example.com"
    ]
    
    print(f"\n🎯 Preparing blitz attack on {len(targets)} targets")
    
    # Execute blitz attack
    blitz_results = attack_engine.blitz_attack(targets)
    
    # Generate and display report
    report = attack_engine.generate_attack_report(blitz_results)
    print(report)
    
    # Save attack log
    with open('attack_log.txt', 'w') as f:
        f.write(report)
        f.write("\n\nDETAILED RESULTS:\n")
        f.write(json.dumps(blitz_results, indent=2))
    
    print("📝 Attack log saved to attack_log.txt")
    print("⚡ BLITZ ATTACK COMPLETE ⚡")

if __name__ == "__main__":
    main()

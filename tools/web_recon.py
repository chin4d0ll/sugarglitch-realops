#!/usr/bin/env python3
"""
Professional Web Reconnaissance Tool
Real-world OSINT and web analysis
"""
import requests
import json
import sys
import socket
import urllib.parse
from datetime import datetime
from urllib.parse import urljoin, urlparse
import re

class WebRecon:
    def __init__(self, target):
        self.target = target
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        self.results = {
            'target': target,
            'timestamp': datetime.now().isoformat(),
            'reconnaissance': {}
        }
    
    def resolve_domain(self):
        """DNS resolution"""
        try:
            ip = socket.gethostbyname(self.target)
            self.results['reconnaissance']['ip_address'] = ip
            print(f"🌐 IP Address: {ip}")
            return ip
        except Exception as e:
            print(f"❌ DNS resolution failed: {e}")
            return None
    
    def check_http_https(self):
        """Check HTTP/HTTPS availability"""
        schemes = ['http', 'https']
        accessible = []
        
        for scheme in schemes:
            url = f"{scheme}://{self.target}"
            try:
                response = self.session.get(url, timeout=10, allow_redirects=False)
                status = {
                    'scheme': scheme,
                    'status_code': response.status_code,
                    'headers': dict(response.headers),
                    'accessible': True
                }
                accessible.append(status)
                print(f"✅ {scheme.upper()}: {response.status_code}")
                
                # Check for redirects
                if 300 <= response.status_code < 400:
                    location = response.headers.get('Location', '')
                    print(f"  ↳ Redirects to: {location}")
                    
            except Exception as e:
                print(f"❌ {scheme.upper()}: Not accessible ({e})")
        
        self.results['reconnaissance']['web_access'] = accessible
        return accessible
    
    def analyze_headers(self, url):
        """Analyze HTTP headers for security info"""
        try:
            response = self.session.get(url, timeout=10)
            headers = dict(response.headers)
            
            security_headers = {
                'X-Frame-Options': headers.get('X-Frame-Options'),
                'X-XSS-Protection': headers.get('X-XSS-Protection'),
                'X-Content-Type-Options': headers.get('X-Content-Type-Options'),
                'Strict-Transport-Security': headers.get('Strict-Transport-Security'),
                'Content-Security-Policy': headers.get('Content-Security-Policy'),
                'Server': headers.get('Server'),
                'X-Powered-By': headers.get('X-Powered-By'),
                'Set-Cookie': headers.get('Set-Cookie')
            }
            
            self.results['reconnaissance']['security_headers'] = security_headers
            
            print("🔒 Security Headers:")
            for header, value in security_headers.items():
                if value:
                    print(f"  ✅ {header}: {value[:50]}...")
                else:
                    print(f"  ❌ {header}: Missing")
                    
            return security_headers
            
        except Exception as e:
            print(f"❌ Header analysis failed: {e}")
            return {}
    
    def find_social_media_links(self, url):
        """Extract social media links from webpage"""
        try:
            response = self.session.get(url, timeout=10)
            content = response.text
            
            social_patterns = {
                'Instagram': r'(?:instagram\.com/|@)([a-zA-Z0-9_.]+)',
                'Twitter': r'(?:twitter\.com/|x\.com/)([a-zA-Z0-9_]+)',
                'Facebook': r'facebook\.com/([a-zA-Z0-9.]+)',
                'LinkedIn': r'linkedin\.com/(?:in/|company/)([a-zA-Z0-9-]+)',
                'TikTok': r'tiktok\.com/@([a-zA-Z0-9_.]+)',
                'YouTube': r'youtube\.com/(?:channel/|user/|c/)([a-zA-Z0-9_-]+)'
            }
            
            found_social = {}
            for platform, pattern in social_patterns.items():
                matches = re.findall(pattern, content, re.IGNORECASE)
                if matches:
                    found_social[platform] = list(set(matches))
            
            self.results['reconnaissance']['social_media'] = found_social
            
            if found_social:
                print("📱 Social Media Found:")
                for platform, accounts in found_social.items():
                    for account in accounts:
                        print(f"  ✅ {platform}: {account}")
            else:
                print("📱 No social media links found")
                
            return found_social
            
        except Exception as e:
            print(f"❌ Social media extraction failed: {e}")
            return {}
    
    def find_emails(self, url):
        """Extract email addresses from webpage"""
        try:
            response = self.session.get(url, timeout=10)
            content = response.text
            
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            emails = re.findall(email_pattern, content)
            emails = list(set(emails))  # Remove duplicates
            
            # Filter out common false positives
            filtered_emails = [email for email in emails 
                             if not any(fp in email.lower() for fp in 
                                      ['example.com', 'test.com', 'placeholder', 'your-email'])]
            
            self.results['reconnaissance']['emails'] = filtered_emails
            
            if filtered_emails:
                print("📧 Email Addresses Found:")
                for email in filtered_emails:
                    print(f"  ✅ {email}")
            else:
                print("📧 No email addresses found")
                
            return filtered_emails
            
        except Exception as e:
            print(f"❌ Email extraction failed: {e}")
            return []
    
    def check_common_files(self, base_url):
        """Check for common files and directories"""
        common_files = [
            'robots.txt',
            'sitemap.xml',
            'security.txt',
            '.well-known/security.txt',
            'admin',
            'login',
            'wp-admin',
            'phpmyadmin',
            'api',
            'backup',
            'config',
            '.git',
            '.env'
        ]
        
        found_files = []
        
        print("📁 Checking common files...")
        for file_path in common_files:
            url = urljoin(base_url, file_path)
            try:
                response = self.session.head(url, timeout=5)
                if response.status_code == 200:
                    found_files.append({
                        'path': file_path,
                        'url': url,
                        'status': response.status_code
                    })
                    print(f"  ✅ {file_path} - Found ({response.status_code})")
                elif response.status_code == 403:
                    print(f"  🔒 {file_path} - Forbidden ({response.status_code})")
                    
            except:
                pass  # Ignore errors for this quick check
        
        self.results['reconnaissance']['common_files'] = found_files
        return found_files
    
    def run_full_recon(self):
        """Run complete reconnaissance"""
        print(f"🔍 Starting reconnaissance on: {self.target}")
        print("=" * 60)
        
        # Basic checks
        self.resolve_domain()
        accessible = self.check_http_https()
        
        # If we have web access, do deeper analysis
        if accessible:
            # Use HTTPS if available, otherwise HTTP
            https_available = any(a['scheme'] == 'https' for a in accessible)
            base_url = f"https://{self.target}" if https_available else f"http://{self.target}"
            
            print(f"\n🌐 Analyzing: {base_url}")
            print("-" * 40)
            
            self.analyze_headers(base_url)
            print()
            self.find_social_media_links(base_url)
            print()
            self.find_emails(base_url)
            print()
            self.check_common_files(base_url)
        
        # Save results
        filename = f"/workspaces/sugarglitch-realops/results/webrecon_{self.target}_{int(datetime.now().timestamp())}.json"
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Results saved to: {filename}")
        print("=" * 60)

def main():
    if len(sys.argv) != 2:
        print("🔍 Professional Web Reconnaissance Tool")
        print("Usage: python3 web_recon.py <domain>")
        print("Example: python3 web_recon.py tradeyourway.co.uk")
        sys.exit(1)
    
    target = sys.argv[1]
    
    # Remove protocol if provided
    if target.startswith(('http://', 'https://')):
        target = urlparse(target).netloc
    
    recon = WebRecon(target)
    recon.run_full_recon()

if __name__ == "__main__":
    main()

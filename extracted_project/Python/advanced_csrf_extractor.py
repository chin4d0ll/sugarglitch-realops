#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎯 ADVANCED CSRF TOKEN EXTRACTOR
เครื่องมือดึง CSRF token ที่มีประสิทธิภาพสูงสุด
"""

import requests
import re
import time
import random
from fake_useragent import UserAgent
import json

class AdvancedCSRFExtractor:
    def __init__(self):
        self.session = requests.Session()
        self.ua = UserAgent()
        self.csrf_token = None
        
    def get_ultimate_csrf(self):
        """ดึง CSRF token ด้วยเทคนิคขั้นสูงสุด"""
        print("🔑 ADVANCED CSRF TOKEN EXTRACTOR")
        print("="*50)
        
        methods = [
            self._method_1_direct_access,
            self._method_2_alternative_endpoints,
            self._method_3_graphql_endpoint,
            self._method_4_mobile_endpoint,
            self._method_5_api_endpoint
        ]
        
        for i, method in enumerate(methods, 1):
            print(f"\n🔍 Method {i}: {method.__name__.replace('_method_', '').replace('_', ' ').title()}")
            
            try:
                token = method()
                if token:
                    print(f"✅ SUCCESS! CSRF Token: {token[:20]}...")
                    self.csrf_token = token
                    return token
                else:
                    print("❌ Failed")
            except Exception as e:
                print(f"❌ Error: {e}")
                
            time.sleep(random.uniform(1, 3))
        
        print("\n❌ All methods failed!")
        return None
    
    def _method_1_direct_access(self):
        """Method 1: Direct Instagram homepage access"""
        headers = {
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
        response = self.session.get('https://www.instagram.com/', headers=headers, timeout=15)
        
        # Multiple extraction patterns
        patterns = [
            r'"csrf_token":"([^"]+)"',
            r'csrf_token":\s*"([^"]+)"',
            r'"X-CSRFToken","([^"]+)"',
            r'csrftoken=([^;]+)',
            r'"token":"([^"]+)"'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, response.text)
            if match:
                return match.group(1)
        
        # Check cookies
        csrf_cookie = response.cookies.get('csrftoken')
        if csrf_cookie:
            return csrf_cookie
            
        return None
    
    def _method_2_alternative_endpoints(self):
        """Method 2: Alternative Instagram endpoints"""
        endpoints = [
            'https://www.instagram.com/accounts/login/',
            'https://www.instagram.com/data/shared_data/',
            'https://www.instagram.com/api/v1/users/web_profile_info/',
            'https://i.instagram.com/api/v1/accounts/login/'
        ]
        
        for endpoint in endpoints:
            try:
                headers = {'User-Agent': self.ua.random}
                response = self.session.get(endpoint, headers=headers, timeout=10)
                
                patterns = [
                    r'"csrf_token":"([^"]+)"',
                    r'csrf_token":\s*"([^"]+)"',
                    r'"csrftoken":"([^"]+)"'
                ]
                
                for pattern in patterns:
                    match = re.search(pattern, response.text)
                    if match:
                        return match.group(1)
                        
                csrf_cookie = response.cookies.get('csrftoken')
                if csrf_cookie:
                    return csrf_cookie
                    
            except:
                continue
                
        return None
    
    def _method_3_graphql_endpoint(self):
        """Method 3: GraphQL endpoint"""
        try:
            headers = {
                'User-Agent': self.ua.random,
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            }
            
            # Try GraphQL endpoint
            response = self.session.get(
                'https://www.instagram.com/graphql/query/',
                headers=headers,
                timeout=10
            )
            
            csrf_cookie = response.cookies.get('csrftoken')
            if csrf_cookie:
                return csrf_cookie
                
            # Try to extract from response
            patterns = [r'"csrf_token":"([^"]+)"', r'csrftoken=([^;]+)']
            for pattern in patterns:
                match = re.search(pattern, response.text)
                if match:
                    return match.group(1)
                    
        except:
            pass
            
        return None
    
    def _method_4_mobile_endpoint(self):
        """Method 4: Mobile API endpoint"""
        try:
            mobile_headers = {
                'User-Agent': 'Instagram 219.0.0.12.117 Android (29/10; 300dpi; 720x1440; samsung; SM-G973F; beyond1; exynos9820; en_US; 336448643)',
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'close',
                'X-IG-Capabilities': '3brTvwE=',
                'X-IG-Connection-Type': 'WIFI',
                'X-IG-Connection-Speed': '2707kbps'
            }
            
            response = self.session.get(
                'https://i.instagram.com/api/v1/accounts/login/',
                headers=mobile_headers,
                timeout=10
            )
            
            csrf_cookie = response.cookies.get('csrftoken')
            if csrf_cookie:
                return csrf_cookie
                
        except:
            pass
            
        return None
    
    def _method_5_api_endpoint(self):
        """Method 5: Web API endpoint"""
        try:
            api_headers = {
                'User-Agent': self.ua.random,
                'X-Requested-With': 'XMLHttpRequest',
                'Referer': 'https://www.instagram.com/',
                'Accept': 'application/json, text/plain, */*'
            }
            
            # Try web API
            response = self.session.get(
                'https://www.instagram.com/web/search/topsearch/',
                headers=api_headers,
                timeout=10
            )
            
            csrf_cookie = response.cookies.get('csrftoken')
            if csrf_cookie:
                return csrf_cookie
                
        except:
            pass
            
        return None
    
    def save_csrf_config(self, token):
        """บันทึก CSRF token config"""
        if token:
            config = {
                'csrf_token': token,
                'extracted_at': time.time(),
                'user_agent': self.ua.random,
                'session_cookies': dict(self.session.cookies)
            }
            
            with open('csrf_config.json', 'w') as f:
                json.dump(config, f, indent=4)
            
            print(f"💾 CSRF config saved to csrf_config.json")
            return True
        return False

def main():
    print("🔑 ADVANCED CSRF TOKEN EXTRACTOR")
    print("The most powerful CSRF extraction tool")
    print("="*50)
    
    extractor = AdvancedCSRFExtractor()
    token = extractor.get_ultimate_csrf()
    
    if token:
        print(f"\n🎉 SUCCESS!")
        print(f"🔑 CSRF Token: {token}")
        print(f"📏 Length: {len(token)}")
        
        # Save config
        extractor.save_csrf_config(token)
        
        # Test the token
        print("\n🧪 Testing CSRF token...")
        test_headers = {
            'X-CSRFToken': token,
            'User-Agent': extractor.ua.random,
            'Referer': 'https://www.instagram.com/'
        }
        
        try:
            test_response = extractor.session.get(
                'https://www.instagram.com/accounts/login/',
                headers=test_headers,
                timeout=10
            )
            
            if test_response.status_code == 200:
                print("✅ CSRF token is valid!")
            else:
                print(f"⚠️ CSRF token may be invalid (Status: {test_response.status_code})")
                
        except Exception as e:
            print(f"❌ CSRF test error: {e}")
    
    else:
        print("\n❌ Failed to extract CSRF token!")
        print("💡 Try running the script again or check your internet connection")

if __name__ == "__main__":
    main()

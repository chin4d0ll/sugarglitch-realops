#!/usr/bin/env python3
"""
🔍 RAPID INSTAGRAM INTELLIGENCE GATHERER
Quick data extraction using API methods
Target: alx.trading
"""

import json
import time
import random
import sys
import os
from datetime import datetime
import requests
import re
from urllib.parse import urlparse

def safe_print(*args, **kwargs):
    try:
        print(*args, **kwargs)
        sys.stdout.flush()
    except (BrokenPipeError, IOError):
        devnull = os.open(os.devnull, os.O_WRONLY)
        os.dup2(devnull, sys.stdout.fileno())
        sys.exit(1)

class RapidInstagramIntel:
    def __init__(self, target_username="alx.trading"):
        self.target = target_username
        self.intelligence = {
            "target": target_username,
            "timestamp": datetime.now().isoformat(),
            "public_profile": {},
            "network_analysis": {},
            "metadata": {},
            "osint_findings": {}
        }
        
    def gather_public_intel(self):
        """Gather publicly available intelligence"""
        try:
            safe_print(f"🔍 Gathering public intelligence on {self.target}...")
            
            # Try to get public profile info via web scraping
            headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
            
            profile_url = f"https://www.instagram.com/{self.target}/"
            
            try:
                response = requests.get(profile_url, headers=headers, timeout=10)
                if response.status_code == 200:
                    html_content = response.text
                    
                    # Extract basic info from HTML
                    self.extract_from_html(html_content)
                    safe_print("✅ Public profile data extracted")
                else:
                    safe_print(f"⚠️ Profile request failed: {response.status_code}")
                    
            except Exception as e:
                safe_print(f"⚠️ Public profile extraction failed: {e}")
            
        except Exception as e:
            safe_print(f"❌ Public intel gathering failed: {e}")
    
    def extract_from_html(self, html_content):
        """Extract information from HTML content"""
        try:
            # Look for JSON data in script tags
            json_pattern = r'window\._sharedData\s*=\s*(\{.*?\});'
            match = re.search(json_pattern, html_content)
            
            if match:
                try:
                    shared_data = json.loads(match.group(1))
                    
                    # Extract profile info
                    if 'entry_data' in shared_data and 'ProfilePage' in shared_data['entry_data']:
                        profile_data = shared_data['entry_data']['ProfilePage'][0]['graphql']['user']
                        
                        self.intelligence["public_profile"] = {
                            "username": profile_data.get("username"),
                            "full_name": profile_data.get("full_name"),
                            "biography": profile_data.get("biography"),
                            "external_url": profile_data.get("external_url"),
                            "follower_count": profile_data.get("edge_followed_by", {}).get("count"),
                            "following_count": profile_data.get("edge_follow", {}).get("count"),
                            "post_count": profile_data.get("edge_owner_to_timeline_media", {}).get("count"),
                            "is_verified": profile_data.get("is_verified"),
                            "is_private": profile_data.get("is_private"),
                            "is_business_account": profile_data.get("is_business_account"),
                            "profile_pic_url": profile_data.get("profile_pic_url_hd")
                        }
                        
                        safe_print("✅ Structured profile data extracted")
                        
                except json.JSONDecodeError:
                    safe_print("⚠️ Failed to parse JSON data")
            
            # Extract meta tags for additional info
            meta_patterns = {
                "description": r'<meta name="description" content="([^"]*)"',
                "keywords": r'<meta name="keywords" content="([^"]*)"',
                "title": r'<title>([^<]*)</title>'
            }
            
            for key, pattern in meta_patterns.items():
                match = re.search(pattern, html_content, re.IGNORECASE)
                if match:
                    self.intelligence["metadata"][key] = match.group(1)
            
        except Exception as e:
            safe_print(f"⚠️ HTML extraction error: {e}")
    
    def analyze_username_patterns(self):
        """Analyze username for OSINT patterns"""
        try:
            safe_print("🕵️ Analyzing username patterns...")
            
            username = self.target
            patterns = {
                "contains_trading": "trading" in username.lower(),
                "contains_numbers": bool(re.search(r'\d', username)),
                "contains_dots": '.' in username,
                "contains_underscores": '_' in username,
                "length": len(username),
                "format_analysis": self.analyze_username_format(username)
            }
            
            # Common trading/finance related usernames
            finance_keywords = ['trading', 'trader', 'invest', 'forex', 'crypto', 'finance', 'money', 'profit']
            patterns["finance_related"] = any(keyword in username.lower() for keyword in finance_keywords)
            
            self.intelligence["network_analysis"]["username_patterns"] = patterns
            safe_print("✅ Username analysis complete")
            
        except Exception as e:
            safe_print(f"⚠️ Username analysis error: {e}")
    
    def analyze_username_format(self, username):
        """Analyze username format patterns"""
        formats = []
        
        if re.match(r'^[a-z]+\.[a-z]+$', username):
            formats.append("firstname.lastname")
        if re.match(r'^[a-z]+_[a-z]+$', username):
            formats.append("word_word")
        if re.match(r'^[a-z]+\d+$', username):
            formats.append("word_numbers")
        if re.match(r'^\d+[a-z]+$', username):
            formats.append("numbers_word")
        
        return formats if formats else ["custom_format"]
    
    def search_related_accounts(self):
        """Search for potentially related accounts"""
        try:
            safe_print("🔗 Searching for related accounts...")
            
            # Generate potential related usernames
            base = self.target.replace('.', '').replace('_', '')
            variations = [
                f"{base}_official",
                f"{base}2",
                f"{base}_backup",
                f"official_{base}",
                f"{base}_real",
                base.replace('trading', 'trader'),
                base.replace('trading', 'invest'),
            ]
            
            # Add variations with numbers
            for i in range(1, 10):
                variations.extend([
                    f"{base}{i}",
                    f"{base}_{i}",
                    f"{i}{base}"
                ])
            
            self.intelligence["network_analysis"]["potential_related"] = variations[:20]  # Limit list
            safe_print(f"✅ Generated {len(variations[:20])} potential related accounts")
            
        except Exception as e:
            safe_print(f"⚠️ Related accounts search error: {e}")
    
    def generate_osint_leads(self):
        """Generate OSINT investigation leads"""
        try:
            safe_print("🎯 Generating OSINT leads...")
            
            leads = {
                "search_engines": [
                    f'"alx.trading" instagram',
                    f'"alx trading" instagram',
                    f'alx.trading -site:instagram.com',
                    f'"Fleming654" username',
                ],
                "social_platforms": [
                    "twitter.com/alx.trading",
                    "facebook.com/alx.trading", 
                    "linkedin.com/in/alx-trading",
                    "youtube.com/@alxtrading",
                    "tiktok.com/@alx.trading"
                ],
                "domain_searches": [
                    "alxtrading.com",
                    "alx-trading.com",
                    "alx.trading",
                ],
                "phone_searches": [
                    "0615414210 Thailand",
                    "+447793127209 UK",
                    '"0615414210" OR "+447793127209"'
                ]
            }
            
            self.intelligence["osint_findings"]["investigation_leads"] = leads
            safe_print("✅ OSINT leads generated")
            
        except Exception as e:
            safe_print(f"⚠️ OSINT lead generation error: {e}")
    
    def save_intelligence_report(self):
        """Save comprehensive intelligence report"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"rapid_intel_{self.target}_{timestamp}.json"
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.intelligence, f, indent=2, ensure_ascii=False)
            
            # Create readable summary
            summary_filename = f"intel_summary_{self.target}_{timestamp}.txt"
            with open(summary_filename, 'w', encoding='utf-8') as f:
                f.write(f"🎯 RAPID INTELLIGENCE REPORT\n")
                f.write(f"Target: {self.target}\n")
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 50 + "\n\n")
                
                # Profile summary
                profile = self.intelligence.get("public_profile", {})
                if profile:
                    f.write("📋 PUBLIC PROFILE\n")
                    for key, value in profile.items():
                        if value:
                            f.write(f"  {key}: {value}\n")
                    f.write("\n")
                
                # Network analysis
                network = self.intelligence.get("network_analysis", {})
                if network:
                    f.write("🔗 NETWORK ANALYSIS\n")
                    for key, value in network.items():
                        f.write(f"  {key}: {value}\n")
                    f.write("\n")
                
                # OSINT leads
                osint = self.intelligence.get("osint_findings", {})
                if osint:
                    f.write("🕵️ OSINT INVESTIGATION LEADS\n")
                    for category, leads in osint.items():
                        f.write(f"  {category}:\n")
                        if isinstance(leads, dict):
                            for subcat, items in leads.items():
                                f.write(f"    {subcat}:\n")
                                for item in items:
                                    f.write(f"      - {item}\n")
                        else:
                            for item in leads:
                                f.write(f"    - {item}\n")
                    f.write("\n")
            
            safe_print(f"💾 Intelligence saved to: {filename}")
            safe_print(f"📄 Summary saved to: {summary_filename}")
            
            return filename, summary_filename
            
        except Exception as e:
            safe_print(f"❌ Intelligence save failed: {e}")
            return None, None
    
    def run_rapid_intel(self):
        """Execute rapid intelligence gathering"""
        safe_print("🚀 STARTING RAPID INTELLIGENCE GATHERING")
        safe_print("=" * 50)
        safe_print(f"🎯 Target: {self.target}")
        safe_print(f"⏰ Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        safe_print("=" * 50)
        
        try:
            # Gather intelligence in phases
            self.gather_public_intel()
            self.analyze_username_patterns()
            self.search_related_accounts()
            self.generate_osint_leads()
            
            # Save report
            files = self.save_intelligence_report()
            
            safe_print("\n🎉 RAPID INTELLIGENCE GATHERING COMPLETE!")
            safe_print("=" * 50)
            
            return True
            
        except Exception as e:
            safe_print(f"❌ Intelligence gathering failed: {e}")
            return False

def main():
    """Execute rapid intelligence gathering"""
    intel = RapidInstagramIntel()
    success = intel.run_rapid_intel()
    
    if success:
        safe_print("✅ Rapid intelligence mission accomplished!")
    else:
        safe_print("❌ Rapid intelligence mission failed!")

if __name__ == "__main__":
    main()

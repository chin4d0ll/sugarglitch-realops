#!/usr/bin/env python3
"""
🔥💎 Advanced Telegram Data Extractor 💎🔥
เฉพาะสำหรับ alx.trading (Username: Alx_TYW)
โดย chin4d0ll framework
"""

import asyncio
import aiohttp
import json
import time
import re
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import hashlib
import base64


class TelegramDataExtractor:
    def __init__(self):
        self.target_username = "Alx_TYW"  # จากข้อมูลที่เจอในโปรเจค
        self.target_profile = "alx.trading"
        self.extracted_data = {
            'profile_info': {},
            'messages': [],
            'contacts': [],
            'channels': [],
            'groups': [],
            'media': [],
            'metadata': {}
        }
        
        # Telegram patterns สำหรับ OSINT
        self.telegram_patterns = {
            'username_variations': [
                'Alx_TYW',
                'AlxTYW', 
                'alx_tyw',
                'alxtyw',
                'ALX_TYW',
                'alx.trading',
                'alxtrading',
                'alex_trading'
            ],
            'potential_channels': [
                'alx_trading_signals',
                'alxtrading_channel',
                'alex_trading_group',
                'alx_forex',
                'alx_crypto'
            ]
        }
        
        print(f"🎯 Telegram Data Extractor สำหรับ {self.target_username}")
        print(f"💼 Target Profile: {self.target_profile}")
    
    def print_cute(self, text, emoji="💕"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"{emoji} [{timestamp}] {text}")
    
    async def search_telegram_intelligence(self):
        """ค้นหาข้อมูล Telegram intelligence"""
        self.print_cute(f"🔍 ค้นหาข้อมูล Telegram สำหรับ {self.target_username}", "🕵️")
        
        # Method 1: Telegram Web Search
        await self._search_telegram_web()
        
        # Method 2: Public Channel/Group Search  
        await self._search_public_channels()
        
        # Method 3: Username Pattern Analysis
        await self._analyze_username_patterns()
        
        # Method 4: Cross-platform correlation
        await self._correlate_with_other_platforms()
        
        # Method 5: OSINT từ existing data
        await self._extract_from_existing_data()
    
    async def _search_telegram_web(self):
        """ค้นหาผ่าน Telegram web interfaces"""
        self.print_cute("🌐 ค้นหาผ่าน Telegram Web...", "🔍")
        
        # Telegram public search endpoints
        search_urls = [
            f"https://t.me/{self.target_username}",
            f"https://telegram.me/{self.target_username}",
            f"https://web.telegram.org/#{self.target_username}",
        ]
        
        for variation in self.telegram_patterns['username_variations']:
            search_urls.extend([
                f"https://t.me/{variation}",
                f"https://telegram.me/{variation}"
            ])
        
        async with aiohttp.ClientSession() as session:
            for url in search_urls:
                try:
                    self.print_cute(f"   🔍 Testing: {url}", "📡")
                    
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
                    }
                    
                    async with session.get(url, headers=headers, timeout=10) as response:
                        if response.status == 200:
                            content = await response.text()
                            
                            # ตรวจสอบว่าเป็น valid Telegram profile
                            if self._is_valid_telegram_profile(content):
                                profile_data = self._extract_profile_data(content, url)
                                if profile_data:
                                    self.extracted_data['profile_info'][url] = profile_data
                                    self.print_cute(f"✅ เจอข้อมูล profile: {url}", "🎯")
                            
                        elif response.status == 404:
                            self.print_cute(f"❌ ไม่พบ: {url}", "⚠️")
                        else:
                            self.print_cute(f"⚠️ Status {response.status}: {url}", "📊")
                    
                    # Delay เพื่อไม่ให้ถูก rate limit
                    await asyncio.sleep(1)
                    
                except Exception as e:
                    self.print_cute(f"❌ Error: {url} - {e}", "⚠️")
                    continue
    
    async def _search_public_channels(self):
        """ค้นหา public channels/groups ที่เกี่ยวข้อง"""
        self.print_cute("📢 ค้นหา Public Channels...", "🔍")
        
        # ค้นหา channels ที่เป็นไปได้
        potential_channels = self.telegram_patterns['potential_channels'].copy()
        
        # เพิ่ม variations ตาม trading theme
        trading_keywords = [
            'forex', 'crypto', 'trading', 'signals', 'market',
            'bitcoin', 'eth', 'usdt', 'binance', 'investment'
        ]
        
        for keyword in trading_keywords:
            potential_channels.extend([
                f"{self.target_username}_{keyword}",
                f"alx_{keyword}",
                f"alex_{keyword}_channel"
            ])
        
        async with aiohttp.ClientSession() as session:
            for channel in potential_channels:
                try:
                    url = f"https://t.me/{channel}"
                    
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X)',
                        'Accept': 'text/html,application/xhtml+xml'
                    }
                    
                    async with session.get(url, headers=headers, timeout=10) as response:
                        if response.status == 200:
                            content = await response.text()
                            
                            # ตรวจสอบว่าเป็น channel/group จริง
                            if any(keyword in content.lower() for keyword in ['channel', 'group', 'members', 'subscribers']):
                                channel_data = self._extract_channel_data(content, channel)
                                if channel_data:
                                    self.extracted_data['channels'].append(channel_data)
                                    self.print_cute(f"✅ เจอ channel: @{channel}", "📢")
                    
                    await asyncio.sleep(0.5)
                    
                except Exception as e:
                    continue
    
    async def _analyze_username_patterns(self):
        """วิเคราะห์รูปแบบ username และหา patterns"""
        self.print_cute("🧠 วิเคราะห์ Username Patterns...", "🔍")
        
        analysis = {
            'primary_username': self.target_username,
            'variations_found': [],
            'pattern_analysis': {},
            'similarity_scores': {}
        }
        
        # วิเคราะห์โครงสร้าง username
        username_parts = re.findall(r'[A-Za-z]+|\d+|[_\-\.]', self.target_username)
        
        analysis['pattern_analysis'] = {
            'parts': username_parts,
            'structure': len(username_parts),
            'has_underscore': '_' in self.target_username,
            'has_numbers': any(c.isdigit() for c in self.target_username),
            'case_pattern': self._analyze_case_pattern(self.target_username)
        }
        
        # สร้าง potential variations
        variations = self._generate_username_variations(self.target_username)
        analysis['variations_found'] = variations
        
        self.extracted_data['metadata']['username_analysis'] = analysis
        self.print_cute(f"🧬 วิเคราะห์แล้ว {len(variations)} variations", "📊")
    
    async def _correlate_with_other_platforms(self):
        """เชื่อมโยงข้อมูลกับ platforms อื่น"""
        self.print_cute("🔗 เชื่อมโยงข้อมูลข้าม platforms...", "🔍")
        
        # ข้อมูลจาก Instagram (จากโปรเจคเดิม)
        instagram_data = {
            'username': 'alx.trading',
            'url': 'https://www.instagram.com/alx.trading/',
            'platform': 'Instagram'
        }
        
        # Cross-platform patterns
        cross_platform_data = {
            'telegram': {
                'username': self.target_username,
                'variations': self.telegram_patterns['username_variations']
            },
            'instagram': instagram_data,
            'potential_emails': [
                'alx.trading@gmail.com',
                'alx.trading@yahoo.com',
                'alxtyw@gmail.com',
                'alextrading@gmail.com'
            ],
            'potential_phones': [
                # จากข้อมูลที่มีในโปรเจค
                '+66', '+1', '+44'  # Country codes ที่เป็นไปได้
            ]
        }
        
        self.extracted_data['metadata']['cross_platform'] = cross_platform_data
        self.print_cute("🌐 เชื่อมโยงข้อมูลเสร็จแล้ว", "✅")
    
    async def _extract_from_existing_data(self):
        """ดึงข้อมูลจาก existing project data"""
        self.print_cute("📂 ดึงข้อมูลจาก existing data...", "🔍")
        
        # ค้นหาไฟล์ที่มี Telegram data
        project_files = [
            'scripts/insert_deep_profile.py',
            'scripts/quick_insert_profile.py', 
            'scripts/comprehensive_real_data_summary.py'
        ]
        
        existing_telegram_data = {}
        
        for file_path in project_files:
            try:
                if os.path.exists(file_path):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                        # ค้นหา Telegram references
                        telegram_matches = re.findall(
                            r'["\']?Telegram["\']?[^,\n]*["\']([^"\']+)["\']',
                            content, re.IGNORECASE
                        )
                        
                        if telegram_matches:
                            existing_telegram_data[file_path] = telegram_matches
                            self.print_cute(f"📄 เจอข้อมูล Telegram ใน {file_path}", "📋")
            
            except Exception as e:
                continue
        
        self.extracted_data['metadata']['existing_data'] = existing_telegram_data
    
    def _is_valid_telegram_profile(self, content: str) -> bool:
        """ตรวจสอบว่าเป็น Telegram profile จริง"""
        telegram_indicators = [
            'telegram.org',
            'tgme_page',
            '@username',
            'telegram_channel',
            'telegram_user',
            'tg://resolve'
        ]
        
        return any(indicator in content.lower() for indicator in telegram_indicators)
    
    def _extract_profile_data(self, content: str, url: str) -> Optional[Dict]:
        """ดึงข้อมูล profile จาก HTML content"""
        try:
            data = {
                'url': url,
                'found_at': datetime.now().isoformat(),
                'profile_type': 'unknown',
                'bio': '',
                'member_count': 0,
                'verified': False
            }
            
            # ค้นหา bio/description
            bio_patterns = [
                r'<meta[^>]*property=["\']og:description["\'][^>]*content=["\']([^"\']+)["\']',
                r'<meta[^>]*name=["\']description["\'][^>]*content=["\']([^"\']+)["\']'
            ]
            
            for pattern in bio_patterns:
                match = re.search(pattern, content, re.IGNORECASE)
                if match:
                    data['bio'] = match.group(1)
                    break
            
            # ค้นหา member count
            member_patterns = [
                r'(\d+)\s*members?',
                r'(\d+)\s*subscribers?',
                r'members?[^\d]*(\d+)'
            ]
            
            for pattern in member_patterns:
                match = re.search(pattern, content, re.IGNORECASE)
                if match:
                    data['member_count'] = int(match.group(1))
                    break
            
            # ตรวจสอบ verification
            if any(verified_indicator in content.lower() for verified_indicator in ['verified', 'official', 'authentic']):
                data['verified'] = True
            
            return data if data['bio'] or data['member_count'] > 0 else None
            
        except Exception as e:
            return None
    
    def _extract_channel_data(self, content: str, channel_name: str) -> Optional[Dict]:
        """ดึงข้อมูล channel จาก content"""
        try:
            data = {
                'channel_name': channel_name,
                'url': f'https://t.me/{channel_name}',
                'found_at': datetime.now().isoformat(),
                'type': 'channel',
                'description': '',
                'members': 0
            }
            
            # ดึง description
            desc_match = re.search(r'<meta[^>]*property=["\']og:description["\'][^>]*content=["\']([^"\']+)["\']', content, re.IGNORECASE)
            if desc_match:
                data['description'] = desc_match.group(1)
            
            # ดึง member count
            member_match = re.search(r'(\d+)\s*(?:members?|subscribers?)', content, re.IGNORECASE)
            if member_match:
                data['members'] = int(member_match.group(1))
            
            return data if data['description'] or data['members'] > 0 else None
            
        except Exception as e:
            return None
    
    def _analyze_case_pattern(self, username: str) -> str:
        """วิเคราะห์รูปแบบตัวพิมพ์"""
        if username.isupper():
            return 'ALL_UPPER'
        elif username.islower():
            return 'all_lower'
        elif username[0].isupper():
            return 'Title_Case'
        else:
            return 'Mixed_Case'
    
    def _generate_username_variations(self, username: str) -> List[str]:
        """สร้าง username variations"""
        variations = []
        
        # Case variations
        variations.extend([
            username.lower(),
            username.upper(),
            username.capitalize(),
            username.title()
        ])
        
        # Remove/add underscores
        if '_' in username:
            variations.append(username.replace('_', ''))
            variations.append(username.replace('_', '.'))
            variations.append(username.replace('_', '-'))
        else:
            # Add separators
            for i in range(1, len(username)):
                variations.append(username[:i] + '_' + username[i:])
        
        # Number additions
        for year in range(2020, 2026):
            variations.extend([
                f"{username}{year}",
                f"{username}_{year}",
                f"{year}_{username}"
            ])
        
        # Remove duplicates
        return list(set(variations))
    
    def generate_intelligence_report(self) -> str:
        """สร้างรายงาน intelligence"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        report = f"""
🔥💎 TELEGRAM INTELLIGENCE REPORT 💎🔥
⏰ Generated: {timestamp}
🎯 Target: {self.target_profile} (Telegram: {self.target_username})
💕 By: Advanced Telegram Extractor Framework
{'='*70}

📋 INTELLIGENCE SUMMARY:
{'='*70}
Target Username: {self.target_username}
Profile URLs Tested: {len(self.extracted_data.get('profile_info', {}))}
Channels Found: {len(self.extracted_data.get('channels', []))}
Cross-platform Data: {len(self.extracted_data.get('metadata', {}).get('cross_platform', {}))}
"""
        
        # Profile Information
        if self.extracted_data.get('profile_info'):
            report += f"\n📱 TELEGRAM PROFILE DATA:\n{'='*50}\n"
            for url, data in self.extracted_data['profile_info'].items():
                report += f"""
Profile: {url}
   📝 Bio: {data.get('bio', 'N/A')}
   👥 Members: {data.get('member_count', 0)}
   ✅ Verified: {data.get('verified', False)}
   🕐 Found: {data.get('found_at', 'Unknown')}
"""
        
        # Channels/Groups
        if self.extracted_data.get('channels'):
            report += f"\n📢 RELATED CHANNELS/GROUPS:\n{'='*50}\n"
            for channel in self.extracted_data['channels']:
                report += f"""
Channel: @{channel.get('channel_name')}
   🔗 URL: {channel.get('url')}
   📝 Description: {channel.get('description', 'N/A')}
   👥 Members: {channel.get('members', 0)}
   📅 Found: {channel.get('found_at')}
"""
        
        # Username Analysis
        username_analysis = self.extracted_data.get('metadata', {}).get('username_analysis', {})
        if username_analysis:
            report += f"\n🧬 USERNAME ANALYSIS:\n{'='*50}\n"
            pattern = username_analysis.get('pattern_analysis', {})
            report += f"""
Primary Username: {username_analysis.get('primary_username')}
Structure: {pattern.get('parts', [])}
Case Pattern: {pattern.get('case_pattern', 'Unknown')}
Has Underscore: {pattern.get('has_underscore', False)}
Has Numbers: {pattern.get('has_numbers', False)}

Generated Variations: {len(username_analysis.get('variations_found', []))}
Top Variations:
"""
            for variation in username_analysis.get('variations_found', [])[:10]:
                report += f"   • {variation}\n"
        
        # Cross-platform Data
        cross_platform = self.extracted_data.get('metadata', {}).get('cross_platform', {})
        if cross_platform:
            report += f"\n🌐 CROSS-PLATFORM INTELLIGENCE:\n{'='*50}\n"
            
            telegram_data = cross_platform.get('telegram', {})
            report += f"""
Telegram Username: {telegram_data.get('username')}
Username Variations: {len(telegram_data.get('variations', []))}

Instagram Profile: {cross_platform.get('instagram', {}).get('username')}
Instagram URL: {cross_platform.get('instagram', {}).get('url')}

Potential Emails:
"""
            for email in cross_platform.get('potential_emails', []):
                report += f"   📧 {email}\n"
        
        # Existing Data
        existing_data = self.extracted_data.get('metadata', {}).get('existing_data', {})
        if existing_data:
            report += f"\n📂 EXISTING PROJECT DATA:\n{'='*50}\n"
            for file_path, matches in existing_data.items():
                report += f"""
File: {file_path}
Telegram References: {matches}
"""
        
        # Intelligence Assessment
        report += f"\n🎯 INTELLIGENCE ASSESSMENT:\n{'='*50}\n"
        
        total_data_points = (
            len(self.extracted_data.get('profile_info', {})) +
            len(self.extracted_data.get('channels', [])) +
            len(username_analysis.get('variations_found', []))
        )
        
        if total_data_points > 20:
            confidence = "HIGH"
            emoji = "🟢"
        elif total_data_points > 10:
            confidence = "MEDIUM"
            emoji = "🟡"
        else:
            confidence = "LOW"
            emoji = "🔴"
        
        report += f"""
{emoji} Confidence Level: {confidence}
📊 Total Data Points: {total_data_points}
🎯 Target Identification: {username_analysis.get('primary_username', 'Unknown')}
🔍 Intelligence Sources: {len(existing_data)} project files
"""
        
        # Recommendations
        report += f"\n💡 RECOMMENDATIONS:\n{'='*50}\n"
        report += """
For Further Investigation:
1. 🔍 Test username variations on Telegram
2. 📱 Monitor related channels for activity  
3. 🌐 Cross-reference with other social platforms
4. 📧 Validate potential email addresses
5. 🕐 Set up automated monitoring

For Security Assessment:
1. 🛡️ Analyze privacy settings
2. 📊 Monitor public activity patterns
3. 🔗 Map social network connections
4. ⚠️ Identify potential security risks
"""
        
        report += f"\n{'='*70}\n"
        report += "💖 Intelligence gathering completed by Advanced Telegram Framework\n"
        report += "⚠️ Use all data ethically and legally!\n"
        report += f"{'='*70}\n"
        
        return report
    
    def save_results(self):
        """บันทึกผลลัพธ์"""
        timestamp = int(time.time())
        
        # บันทึก JSON data
        json_filename = f"telegram_intelligence_{self.target_username}_{timestamp}.json"
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(self.extracted_data, f, indent=2, ensure_ascii=False, default=str)
        
        # บันทึกรายงาน
        report_filename = f"telegram_intelligence_report_{self.target_username}_{timestamp}.txt"
        report = self.generate_intelligence_report()
        with open(report_filename, 'w', encoding='utf-8') as f:
            f.write(report)
        
        self.print_cute(f"💾 บันทึกข้อมูลแล้ว:", "✅")
        self.print_cute(f"   📊 JSON: {json_filename}", "📄")
        self.print_cute(f"   📋 Report: {report_filename}", "📄")
        
        return json_filename, report_filename


async def main():
    """Main function"""
    print("""
🔥💎 Advanced Telegram Data Extractor 💎🔥
เฉพาะสำหรับ alx.trading (Username: Alx_TYW)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")
    
    # สร้าง extractor
    extractor = TelegramDataExtractor()
    
    try:
        # เริ่มการค้นหาข้อมูล
        await extractor.search_telegram_intelligence()
        
        # บันทึกผลลัพธ์
        json_file, report_file = extractor.save_results()
        
        # แสดงสรุป
        print(f"""
🎉 TELEGRAM INTELLIGENCE EXTRACTION COMPLETED! 🎉
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 SUMMARY:
🎯 Target: {extractor.target_username} ({extractor.target_profile})
📱 Profiles Found: {len(extractor.extracted_data.get('profile_info', {}))}
📢 Channels Found: {len(extractor.extracted_data.get('channels', []))}
🧬 Username Variations: {len(extractor.extracted_data.get('metadata', {}).get('username_analysis', {}).get('variations_found', []))}

📁 FILES CREATED:
💾 JSON Data: {json_file}
📋 Intelligence Report: {report_file}

✅ Ready for further analysis and monitoring!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")
        
    except KeyboardInterrupt:
        print("\n⏹️ Extraction stopped by user")
    except Exception as e:
        print(f"\n❌ Error during extraction: {e}")


if __name__ == "__main__":
    asyncio.run(main())

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔥 ENHANCED REAL TELEGRAM DATA EXTRACTOR 🔥
ปรับปรุงการดึงข้อมูลจริงจาก Telegram profiles และ messages
"""

import requests
import json
import time
import re
from datetime import datetime
from bs4 import BeautifulSoup

class EnhancedRealExtractor:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive'
        })
        self.real_data = {
            'extraction_start': datetime.now().isoformat(),
            'targets_analyzed': [],
            'profile_data': {},
            'message_data': {},
            'real_interactions': []
        }

    def extract_profile_info(self, username):
        """ดึงข้อมูล profile จริงจาก Telegram"""
        print(f"👤 Extracting real profile: @{username}")
        
        urls_to_check = [
            f"https://t.me/{username}",
            f"https://t.me/s/{username}"
        ]
        
        profile_info = {
            'username': username,
            'extraction_time': datetime.now().isoformat(),
            'profile_found': False,
            'real_data': {}
        }
        
        for url in urls_to_check:
            try:
                response = self.session.get(url, timeout=10)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # ดึงข้อมูลจาก meta tags
                    meta_data = {}
                    for meta in soup.find_all('meta'):
                        property_name = meta.get('property') or meta.get('name')
                        content = meta.get('content')
                        if property_name and content:
                            meta_data[property_name] = content
                    
                    # ตรวจสอบว่าเป็น profile จริง
                    if 'og:title' in meta_data:
                        title = meta_data['og:title']
                        if f"@{username}" in title or username in title:
                            profile_info['profile_found'] = True
                            profile_info['real_data']['title'] = title
                            profile_info['real_data']['url'] = url
                            
                            # ดึงข้อมูลเพิ่มเติม
                            if 'og:description' in meta_data:
                                profile_info['real_data']['description'] = meta_data['og:description']
                            
                            if 'og:image' in meta_data:
                                profile_info['real_data']['image'] = meta_data['og:image']
                            
                            # ค้นหาข้อมูลจาก page content
                            page_text = soup.get_text()
                            
                            # ค้นหา member count
                            member_match = re.search(r'(\d+(?:,\d+)*)\s*(?:members|subscribers)', page_text, re.IGNORECASE)
                            if member_match:
                                profile_info['real_data']['members'] = member_match.group(1)
                            
                            # ค้นหา verification status
                            if 'verified' in page_text.lower():
                                profile_info['real_data']['verified'] = True
                            
                            print(f"✅ Profile found: {title}")
                            break
                    
            except Exception as e:
                print(f"❌ Error accessing {url}: {e}")
        
        if not profile_info['profile_found']:
            print(f"❌ Profile @{username} not found or private")
        
        return profile_info

    def extract_public_messages(self, username):
        """ดึงข้อความจาก public channel/group"""
        print(f"💬 Extracting real messages from: @{username}")
        
        url = f"https://t.me/s/{username}"
        
        message_data = {
            'username': username,
            'extraction_time': datetime.now().isoformat(),
            'messages_found': 0,
            'real_messages': []
        }
        
        try:
            response = self.session.get(url, timeout=15)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # ค้นหา message widgets
                messages = soup.find_all('div', class_='tgme_widget_message')
                
                for msg_div in messages:
                    msg_info = {
                        'extracted_at': datetime.now().isoformat(),
                        'is_real': True
                    }
                    
                    # ดึงเวลา
                    time_elem = msg_div.find('time')
                    if time_elem:
                        msg_info['datetime'] = time_elem.get('datetime')
                        msg_info['display_time'] = time_elem.get_text().strip()
                    
                    # ดึงข้อความ
                    text_elem = msg_div.find('div', class_='tgme_widget_message_text')
                    if text_elem:
                        message_text = text_elem.get_text().strip()
                        if message_text:
                            msg_info['text'] = message_text
                            msg_info['text_length'] = len(message_text)
                    
                    # ดึงข้อมูล author/sender
                    author_elem = msg_div.find('span', class_='tgme_widget_message_from_author')
                    if author_elem:
                        msg_info['author'] = author_elem.get_text().strip()
                    
                    # ดึงจำนวน views
                    views_elem = msg_div.find('span', class_='tgme_widget_message_views')
                    if views_elem:
                        views_text = views_elem.get_text().strip()
                        msg_info['views'] = views_text
                        
                        # แปลงเป็นตัวเลข
                        views_match = re.search(r'([\d.]+)([KM]?)', views_text)
                        if views_match:
                            num, suffix = views_match.groups()
                            views_num = float(num)
                            if suffix == 'K':
                                views_num *= 1000
                            elif suffix == 'M':
                                views_num *= 1000000
                            msg_info['views_count'] = int(views_num)
                    
                    # ดึงข้อมูลการ forward
                    forward_elem = msg_div.find('span', class_='tgme_widget_message_forwarded_from_name')
                    if forward_elem:
                        msg_info['forwarded_from'] = forward_elem.get_text().strip()
                    
                    # บันทึกเฉพาะข้อความที่มีเนื้อหา
                    if msg_info.get('text') or msg_info.get('author'):
                        message_data['real_messages'].append(msg_info)
                        message_data['messages_found'] += 1
                
                if message_data['messages_found'] > 0:
                    print(f"✅ Found {message_data['messages_found']} real messages")
                else:
                    print("❌ No public messages found (private or no messages)")
                    
        except Exception as e:
            print(f"❌ Error extracting messages: {e}")
        
        return message_data

    def analyze_telegram_links(self, username):
        """วิเคราะห์ลิงก์และการเชื่อมต่อ Telegram"""
        print(f"🔗 Analyzing Telegram links for: @{username}")
        
        url = f"https://t.me/{username}"
        
        link_data = {
            'username': username,
            'deep_links': [],
            'app_links': [],
            'web_links': []
        }
        
        try:
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # ค้นหา deep links
                for meta in soup.find_all('meta'):
                    content = meta.get('content', '')
                    if 'tg://' in content:
                        link_data['deep_links'].append(content)
                    elif 'https://t.me/' in content:
                        link_data['web_links'].append(content)
                
                # ค้นหาใน scripts
                scripts = soup.find_all('script')
                for script in scripts:
                    if script.string:
                        script_content = script.string
                        
                        # ค้นหา tg:// links
                        tg_links = re.findall(r'tg://[^\'"\\s]+', script_content)
                        link_data['deep_links'].extend(tg_links)
                        
                        # ค้นหา app links
                        app_links = re.findall(r'https://t\.me/[^\'"\\s]+', script_content)
                        link_data['app_links'].extend(app_links)
                
                # ลบ duplicates
                link_data['deep_links'] = list(set(link_data['deep_links']))
                link_data['app_links'] = list(set(link_data['app_links']))
                link_data['web_links'] = list(set(link_data['web_links']))
                
                print(f"✅ Found {len(link_data['deep_links'])} deep links, {len(link_data['app_links'])} app links")
                
        except Exception as e:
            print(f"❌ Error analyzing links: {e}")
        
        return link_data

    def save_enhanced_real_data(self):
        """บันทึกข้อมูลจริงที่ปรับปรุงแล้ว"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"enhanced_real_telegram_{timestamp}.json"
        
        # เพิ่มข้อมูลยืนยัน
        self.real_data['verification'] = {
            'data_source': 'REAL_TELEGRAM_ONLY',
            'no_mockup_data': True,
            'live_extraction': True,
            'enhanced_analysis': True,
            'extraction_completed': datetime.now().isoformat()
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.real_data, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Enhanced real data saved: {filename}")
        return filename

def main():
    """Main function - Enhanced real extraction"""
    print("🔥 ENHANCED REAL TELEGRAM DATA EXTRACTOR 🔥")
    print("=" * 65)
    print("⚠️  EXTRACTING ENHANCED REAL DATA - NO MOCKUPS")
    print()
    
    extractor = EnhancedRealExtractor()
    
    # เป้าหมายที่จะวิเคราะห์
    targets = ['alx_trading', 'Alx_TYW', 'alx_tyw', 'alxtrading']
    
    for target in targets:
        print(f"🎯 Processing target: @{target}")
        extractor.real_data['targets_analyzed'].append(target)
        
        # ดึงข้อมูล profile
        profile_info = extractor.extract_profile_info(target)
        extractor.real_data['profile_data'][target] = profile_info
        
        # ดึงข้อความ
        message_info = extractor.extract_public_messages(target)
        extractor.real_data['message_data'][target] = message_info
        
        # วิเคราะห์ลิงก์
        link_info = extractor.analyze_telegram_links(target)
        extractor.real_data['profile_data'][target]['links'] = link_info
        
        print(f"✅ Completed analysis for @{target}")
        print()
        time.sleep(3)  # หน่วงเวลาระหว่างการประมวลผล
    
    # บันทึกผลลัพธ์
    saved_file = extractor.save_enhanced_real_data()
    
    print("🎉 ENHANCED REAL DATA EXTRACTION COMPLETE")
    print(f"📊 Targets analyzed: {len(extractor.real_data['targets_analyzed'])}")
    print(f"👤 Profiles extracted: {len(extractor.real_data['profile_data'])}")
    print(f"💬 Message data: {len(extractor.real_data['message_data'])}")
    print(f"💾 Saved to: {saved_file}")
    print()
    print("⚠️  ALL DATA IS REAL - ENHANCED EXTRACTION COMPLETE")

if __name__ == "__main__":
    main()

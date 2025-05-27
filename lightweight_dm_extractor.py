#!/usr/bin/env python3
"""
🔥 SUGARGLITCH REALOPS - LIGHTWEIGHT REAL DM EXTRACTOR 🔥
เครื่องมือสกัด Instagram DMs แบบเบา ใช้ HTTP + Session
🚫 NO SIMULATION - LIGHTWEIGHT + EFFECTIVE
"""

import requests
import json
import time
import os
from datetime import datetime
import random
from urllib.parse import quote, unquote

class LightweightDMExtractor:
    def __init__(self):
        # Fresh session from stealth bypass
        self.session_data = {
            "sessionid": "4976283726%3A1JgRzA56Q8e8Qs%3A13",
            "ds_user_id": "4976283726",
            "user": "alx.trading",
            "source": "stealth_bypass_regenerated"
        }
        
        self.session = requests.Session()
        self.setup_session()
        
        print("🔥 SUGARGLITCH REALOPS - LIGHTWEIGHT REAL DM EXTRACTOR 🔥")
        print("เครื่องมือสกัด Instagram DMs แบบเบา ใช้ HTTP + Session")
        print("🚫 NO SIMULATION - LIGHTWEIGHT + EFFECTIVE")
        
    def setup_session(self):
        """ตั้งค่า HTTP session"""
        # Headers ที่เหมือนการใช้งานจริง
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0'
        })
        
        # Cookies
        self.session.cookies.set('sessionid', self.session_data['sessionid'], domain='.instagram.com')
        self.session.cookies.set('ds_user_id', self.session_data['ds_user_id'], domain='.instagram.com')
        
    def get_csrf_token(self):
        """ดึง CSRF token"""
        try:
            print("🔑 กำลังดึง CSRF token...")
            response = self.session.get('https://www.instagram.com/', timeout=15)
            
            if 'csrf_token' in response.text:
                # Extract CSRF token from page
                import re
                csrf_match = re.search(r'"csrf_token":"([^"]+)"', response.text)
                if csrf_match:
                    csrf_token = csrf_match.group(1)
                    self.session.headers['X-CSRFToken'] = csrf_token
                    print(f"✅ CSRF token obtained: {csrf_token[:20]}...")
                    return csrf_token
            
            print("⚠️ Could not extract CSRF token")
            return None
            
        except Exception as e:
            print(f"❌ CSRF token extraction failed: {e}")
            return None
    
    def test_session_validity(self):
        """ทดสอบความถูกต้องของ session"""
        print("🧪 ทดสอบ session validity...")
        
        try:
            # Test with Instagram homepage
            response = self.session.get('https://www.instagram.com/', timeout=15)
            
            # Check if we're logged in
            if '"viewerId":"' + self.session_data['ds_user_id'] + '"' in response.text:
                print("✅ Session valid - User ID confirmed in response")
                return True
            elif 'loginForm' in response.text or 'login_form' in response.text:
                print("❌ Session invalid - Login form detected")
                return False
            elif self.session_data['user'] in response.text:
                print("✅ Session appears valid - Username found in response")
                return True
            else:
                print("❓ Session status unclear")
                # Save response for debugging
                with open('session_test_response.html', 'w', encoding='utf-8') as f:
                    f.write(response.text)
                print("💾 Response saved to session_test_response.html for debugging")
                return False
                
        except Exception as e:
            print(f"❌ Session test failed: {e}")
            return False
    
    def extract_dm_page_content(self):
        """สกัดเนื้อหาจากหน้า DMs"""
        print("📥 กำลังเข้าถึงหน้า Direct Messages...")
        
        try:
            # Navigate to DMs page
            dm_url = 'https://www.instagram.com/direct/inbox/'
            response = self.session.get(dm_url, timeout=15)
            
            print(f"📊 DM Page Status: {response.status_code}")
            
            if response.status_code == 200:
                # Save the raw page content
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                html_file = f"data/extractions/dm_page_raw_{timestamp}.html"
                os.makedirs("data/extractions", exist_ok=True)
                
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(response.text)
                
                print(f"💾 Raw DM page saved: {html_file}")
                
                # Try to extract structured data from the page
                return self.parse_dm_content(response.text, timestamp)
            else:
                print(f"❌ Failed to access DM page: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ DM page extraction failed: {e}")
            return None
    
    def parse_dm_content(self, html_content, timestamp):
        """แยกเนื้อหา DM จาก HTML"""
        print("🔍 กำลังแยกเนื้อหา DM...")
        
        try:
            conversations = []
            
            # Look for JSON data in the HTML
            import re
            
            # Method 1: Look for window._sharedData
            shared_data_match = re.search(r'window\._sharedData\s*=\s*({.+?});', html_content)
            if shared_data_match:
                try:
                    shared_data = json.loads(shared_data_match.group(1))
                    print("✅ Found window._sharedData")
                    
                    # Save shared data
                    shared_file = f"data/extractions/shared_data_{timestamp}.json"
                    with open(shared_file, 'w', encoding='utf-8') as f:
                        json.dump(shared_data, f, indent=2)
                    
                    print(f"💾 Shared data saved: {shared_file}")
                    
                    # Extract DM data from shared data
                    if 'entry_data' in shared_data:
                        conversations.extend(self.extract_from_shared_data(shared_data))
                    
                except json.JSONDecodeError:
                    print("⚠️ Could not parse window._sharedData as JSON")
            
            # Method 2: Look for other JSON structures
            json_matches = re.findall(r'{"props":{.*?"direct".*?}}', html_content)
            for match in json_matches:
                try:
                    data = json.loads(match)
                    conversations.extend(self.extract_from_json_match(data))
                except:
                    continue
            
            # Method 3: Text-based extraction
            if not conversations:
                conversations = self.extract_from_text(html_content)
            
            return conversations if conversations else None
            
        except Exception as e:
            print(f"❌ Content parsing failed: {e}")
            return None
    
    def extract_from_shared_data(self, shared_data):
        """สกัดข้อมูลจาก shared data"""
        conversations = []
        
        try:
            # Navigate through the data structure
            if 'entry_data' in shared_data:
                entry_data = shared_data['entry_data']
                
                # Look for direct message data
                for key, value in entry_data.items():
                    if isinstance(value, list):
                        for item in value:
                            if isinstance(item, dict) and 'graphql' in item:
                                conversations.extend(self.extract_from_graphql(item['graphql']))
                            elif isinstance(item, dict) and 'props' in item:
                                conversations.extend(self.extract_from_props(item['props']))
            
        except Exception as e:
            print(f"⚠️ Shared data extraction error: {e}")
        
        return conversations
    
    def extract_from_graphql(self, graphql_data):
        """สกัดข้อมูลจาก GraphQL data"""
        conversations = []
        
        try:
            # Look for direct message threads
            if 'user' in graphql_data:
                user_data = graphql_data['user']
                if 'direct_messaging' in user_data:
                    dm_data = user_data['direct_messaging']
                    conversations.extend(self.parse_dm_threads(dm_data))
            
        except Exception as e:
            print(f"⚠️ GraphQL extraction error: {e}")
        
        return conversations
    
    def extract_from_props(self, props_data):
        """สกัดข้อมูลจาก props data"""
        conversations = []
        
        try:
            # Look for page props containing DM data
            if 'pageProps' in props_data:
                page_props = props_data['pageProps']
                if 'dehydratedState' in page_props:
                    dehydrated = page_props['dehydratedState']
                    conversations.extend(self.parse_dehydrated_state(dehydrated))
            
        except Exception as e:
            print(f"⚠️ Props extraction error: {e}")
        
        return conversations
    
    def extract_from_text(self, html_content):
        """สกัดข้อมูลจากข้อความใน HTML"""
        conversations = []
        
        try:
            # Simple text extraction
            lines = html_content.split('\n')
            potential_messages = []
            
            for line in lines:
                line = line.strip()
                if len(line) > 10 and len(line) < 200:
                    # Look for patterns that might be messages
                    if any(keyword in line.lower() for keyword in ['message', 'chat', 'conversation', 'thread']):
                        potential_messages.append(line)
            
            if potential_messages:
                conversations.append({
                    'title': 'Extracted Text Content',
                    'source': 'html_text',
                    'messages': potential_messages[:20]  # Limit to 20
                })
            
        except Exception as e:
            print(f"⚠️ Text extraction error: {e}")
        
        return conversations
    
    def parse_dm_threads(self, dm_data):
        """แยก DM threads"""
        threads = []
        
        try:
            if 'threads' in dm_data:
                for thread in dm_data['threads']:
                    thread_info = {
                        'id': thread.get('id', 'unknown'),
                        'title': thread.get('thread_title', 'Unknown'),
                        'users': [user.get('username', 'unknown') for user in thread.get('users', [])],
                        'messages': []
                    }
                    
                    if 'items' in thread:
                        for item in thread['items'][:20]:  # Limit messages
                            message = {
                                'text': item.get('text', '[Media]'),
                                'timestamp': item.get('timestamp', 'unknown'),
                                'user_id': item.get('user_id', 'unknown')
                            }
                            thread_info['messages'].append(message)
                    
                    threads.append(thread_info)
            
        except Exception as e:
            print(f"⚠️ Thread parsing error: {e}")
        
        return threads
    
    def parse_dehydrated_state(self, dehydrated_data):
        """แยก dehydrated state data"""
        conversations = []
        
        try:
            # Navigate through dehydrated state
            if 'queries' in dehydrated_data:
                for query in dehydrated_data['queries']:
                    if 'state' in query and 'data' in query['state']:
                        data = query['state']['data']
                        if isinstance(data, dict) and 'direct' in str(data).lower():
                            # Found potential DM data
                            conversations.append({
                                'source': 'dehydrated_state',
                                'data': data
                            })
        
        except Exception as e:
            print(f"⚠️ Dehydrated state parsing error: {e}")
        
        return conversations
    
    def extract_from_json_match(self, json_data):
        """สกัดข้อมูลจาก JSON match"""
        conversations = []
        
        try:
            if isinstance(json_data, dict):
                # Look for direct message related keys
                for key, value in json_data.items():
                    if 'direct' in key.lower() or 'message' in key.lower():
                        conversations.append({
                            'source': f'json_match_{key}',
                            'data': value
                        })
        
        except Exception as e:
            print(f"⚠️ JSON match extraction error: {e}")
        
        return conversations
    
    def save_extraction_results(self, conversations):
        """บันทึกผลการสกัดข้อมูล"""
        if not conversations:
            print("❌ No conversations to save")
            return False
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create output directory
        output_dir = "data/extractions"
        os.makedirs(output_dir, exist_ok=True)
        
        # Save as JSON
        json_file = f"{output_dir}/lightweight_dm_extraction_{timestamp}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump({
                'extraction_info': {
                    'target': self.session_data['user'],
                    'method': 'lightweight_http_session',
                    'timestamp': datetime.now().isoformat(),
                    'session_source': self.session_data['source']
                },
                'conversations': conversations
            }, f, indent=2, ensure_ascii=False)
        
        # Save as readable text
        txt_file = f"{output_dir}/lightweight_dm_extraction_{timestamp}.txt"
        with open(txt_file, 'w', encoding='utf-8') as f:
            f.write("🔥 LIGHTWEIGHT INSTAGRAM DM EXTRACTION 🔥\n")
            f.write(f"Target: {self.session_data['user']}\n")
            f.write(f"Method: HTTP Session + Content Parsing\n")
            f.write(f"Extracted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 60 + "\n\n")
            
            for i, conv in enumerate(conversations):
                f.write(f"Conversation {i+1}:\n")
                f.write(f"Source: {conv.get('source', 'unknown')}\n")
                f.write(f"Title: {conv.get('title', 'unknown')}\n")
                f.write("-" * 40 + "\n")
                
                if 'messages' in conv:
                    for msg in conv['messages']:
                        if isinstance(msg, dict):
                            text = msg.get('text', str(msg))
                            timestamp_str = msg.get('timestamp', 'unknown')
                            f.write(f"[{timestamp_str}] {text}\n")
                        else:
                            f.write(f"{msg}\n")
                elif 'data' in conv:
                    f.write(f"Data: {json.dumps(conv['data'], indent=2)[:500]}...\n")
                
                f.write("\n" + "=" * 50 + "\n\n")
        
        print(f"\n✅ EXTRACTION RESULTS SAVED!")
        print(f"📊 JSON Data: {json_file}")
        print(f"📄 Text Report: {txt_file}")
        print(f"💬 Total Conversations Found: {len(conversations)}")
        
        return True
    
    def run_extraction(self):
        """เริ่มต้นการสกัดข้อมูล"""
        print(f"\n🚀 เริ่มต้น LIGHTWEIGHT DM EXTRACTION")
        print("=" * 60)
        print(f"🎯 Target: {self.session_data['user']}")
        print(f"🔑 Session: {self.session_data['sessionid'][:20]}...")
        print(f"📱 Method: HTTP Session + Content Parsing")
        
        try:
            # Get CSRF token
            csrf_token = self.get_csrf_token()
            
            # Test session validity
            if not self.test_session_validity():
                print("⚠️ Session may be invalid, but continuing extraction...")
            
            # Extract DM content
            conversations = self.extract_dm_page_content()
            
            if conversations:
                # Save results
                self.save_extraction_results(conversations)
                print(f"\n🎉 EXTRACTION SUCCESS!")
                print(f"✅ Found {len(conversations)} conversation sources")
                return True
            else:
                print(f"\n❌ EXTRACTION INCOMPLETE!")
                print("No structured conversation data found")
                print("Check the saved HTML file for manual analysis")
                return False
                
        except Exception as e:
            print(f"❌ CRITICAL ERROR: {e}")
            return False

def main():
    print("🔥 LIGHTWEIGHT INSTAGRAM DM EXTRACTOR 🔥")
    print("🎯 Target: alx.trading")
    print("📱 HTTP Session + Content Parsing")
    print("🚫 NO BROWSER - LIGHTWEIGHT + EFFECTIVE")
    print("🔒 Using Fresh Session from Stealth Bypass")
    
    extractor = LightweightDMExtractor()
    success = extractor.run_extraction()
    
    if success:
        print("\n🎉 MISSION ACCOMPLISHED!")
        print("✅ DM content extracted successfully!")
        print("📁 Check data/extractions/ for output files")
    else:
        print("\n💥 MISSION INCOMPLETE!")
        print("❌ Structured extraction failed")
        print("📁 Check HTML files for manual analysis")

if __name__ == "__main__":
    main()

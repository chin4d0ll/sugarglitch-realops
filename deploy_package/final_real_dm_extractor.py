#!/usr/bin/env python3
"""
Real Instagram DM Extractor - Deployment Version
Uses sessions/session-alx.trading with cute rate limiting
"""

import os
import json
import requests
import time
from datetime import datetime
import urllib.parse
import random

def load_session():
    """Load session from sessions/session-alx.trading"""
    try:
        with open('sessions/session-alx.trading', 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Error loading session: {e}")
        return None

def cute_request(url, session, method='GET', **kwargs):
    """Cute rate limiting request with advanced protection"""
    max_retries = 8
    base_delay = 2
    
    for attempt in range(max_retries):
        try:
            if attempt > 0:
                jitter = random.uniform(1.0, 3.0)
                delay = (base_delay * (1.8 ** attempt)) + jitter
                print(f"😴 Cute sleep for {delay:.1f}s (attempt {attempt + 1})...")
                time.sleep(delay)
            
            print(f"🌟 Cute request #{attempt + 1}: {url}")
            
            kwargs['timeout'] = kwargs.get('timeout', 30)
            
            if method.upper() == 'GET':
                response = session.get(url, **kwargs)
            elif method.upper() == 'POST':
                response = session.post(url, **kwargs)
            else:
                response = session.request(method, url, **kwargs)
                
            status = response.status_code
            size = len(response.content)
            print(f"📊 Response: HTTP {status} | {size:,} bytes")
            
            if status == 429:
                retry_after = response.headers.get('Retry-After')
                wait_time = int(retry_after) + random.randint(10, 20) if retry_after else base_delay * (2 ** attempt) + random.randint(15, 30)
                print(f"🚫 Rate limited! Waiting {wait_time}s...")
                time.sleep(wait_time)
                continue
            
            elif status in [200, 201]:
                print(f"✅ Success! ({size:,} bytes)")
                return response
            
            elif status == 403:
                print("🔒 Forbidden - session may be expired")
                if attempt < 3:
                    continue
                return response
            
            else:
                print(f"⚠️ Status {status}")
                if attempt < max_retries - 1:
                    continue
                return response
                
        except requests.exceptions.Timeout:
            print("⏰ Timeout")
            if attempt < max_retries - 1:
                time.sleep(base_delay * (1.5 ** attempt))
        except Exception as e:
            print(f"❌ Error: {e}")
            if attempt < max_retries - 1:
                time.sleep(base_delay * (1.5 ** attempt))
    
    print("💀 All attempts failed!")
    return None

def extract_dms():
    """Main extraction function"""
    print("🎯 REAL INSTAGRAM DM EXTRACTOR")
    print("🛡️ Using cute rate limiting protection")
    print("=" * 50)
    
    # Load session
    session_data = load_session()
    if not session_data:
        return False
    
    print(f"✅ Session loaded: {list(session_data.keys())}")
    
    # Setup requests session
    session = requests.Session()
    
    # Configure cookies
    if 'cookies' in session_data:
        for name, value in session_data['cookies'].items():
            if '%' in str(value):
                value = urllib.parse.unquote(str(value))
            session.cookies.set(name, value, domain='.instagram.com')
            print(f"🍪 {name}: {str(value)[:20]}...")
    
    # Set headers
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6 Mobile/15E148 Safari/604.1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    })
    
    # Test Instagram homepage
    print(f"\n🏠 Testing Instagram homepage...")
    home_response = cute_request('https://www.instagram.com/', session)
    if not home_response or home_response.status_code != 200:
        print("❌ Cannot access Instagram")
        return False
    
    print("✅ Instagram accessible!")
    
    # Get CSRF token
    csrf_token = session.cookies.get('csrftoken')
    if csrf_token:
        session.headers['X-CSRFToken'] = csrf_token
        print(f"🔑 CSRF: {csrf_token[:15]}...")
    
    # Access direct inbox
    print(f"\n📬 Testing direct inbox...")
    inbox_response = cute_request('https://www.instagram.com/direct/inbox/', session)
    if not inbox_response or inbox_response.status_code != 200:
        print("❌ Cannot access inbox")
        return False
    
    print("✅ Inbox accessible!")
    
    # API request
    print(f"\n🔧 Accessing DM API...")
    api_headers = {
        'X-Requested-With': 'XMLHttpRequest',
        'X-IG-App-ID': '936619743392459',
        'Accept': 'application/json, text/plain, */*',
    }
    
    api_response = cute_request(
        'https://www.instagram.com/api/v1/direct_v2/inbox/',
        session,
        headers=api_headers
    )
    
    if not api_response or api_response.status_code != 200:
        print(f"❌ API failed: {api_response.status_code if api_response else 'No response'}")
        if api_response:
            print(f"Response: {api_response.text[:200]}...")
        return False
    
    print("✅ API successful!")
    
    # Process data
    try:
        dm_data = api_response.json()
        print(f"📊 API keys: {list(dm_data.keys())}")
        
        if 'inbox' in dm_data and 'threads' in dm_data['inbox']:
            threads = dm_data['inbox']['threads']
            print(f"\n🎯 Found {len(threads)} DM threads!")
            
            if len(threads) == 0:
                print("⚠️ No threads found")
                return False
            
            # Extract data
            extracted = {
                'extraction_info': {
                    'account': 'alx.trading',
                    'timestamp': datetime.now().isoformat(),
                    'total_threads': len(threads),
                    'data_type': 'REAL_INSTAGRAM_DMS'
                },
                'threads': []
            }
            
            for i, thread in enumerate(threads):
                print(f"📨 Thread {i+1}/{len(threads)}")
                
                thread_info = {
                    'thread_id': thread.get('thread_id'),
                    'thread_title': thread.get('thread_title', 'No title'),
                    'users': [],
                    'messages': []
                }
                
                # Users
                if 'users' in thread:
                    for user in thread['users']:
                        user_info = {
                            'username': user.get('username'),
                            'full_name': user.get('full_name'),
                            'is_verified': user.get('is_verified', False)
                        }
                        thread_info['users'].append(user_info)
                        print(f"   👤 {user_info['username']}")
                
                # Messages
                if 'items' in thread:
                    for msg in thread['items'][:10]:  # Last 10 messages
                        msg_info = {
                            'item_id': msg.get('item_id'),
                            'item_type': msg.get('item_type'),
                            'timestamp': msg.get('timestamp'),
                            'user_id': msg.get('user_id')
                        }
                        
                        if msg.get('item_type') == 'text':
                            msg_info['text'] = msg.get('text', '')
                        elif msg.get('item_type') == 'media':
                            msg_info['content'] = '[Media message]'
                        
                        thread_info['messages'].append(msg_info)
                    
                    print(f"   💬 {len(thread_info['messages'])} messages")
                
                extracted['threads'].append(thread_info)
                time.sleep(1)  # Small delay
            
            # Save results
            os.makedirs('data', exist_ok=True)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = f'data/REAL_ALX_TRADING_DMS_{timestamp}.json'
            
            with open(output_file, 'w') as f:
                json.dump(extracted, f, indent=2, ensure_ascii=False)
            
            print(f"\n💾 Results saved: {output_file}")
            print(f"📊 Summary:")
            print(f"   🎯 Account: alx.trading")
            print(f"   📨 Threads: {len(threads)}")
            print(f"   💬 Messages: {sum(len(t['messages']) for t in extracted['threads'])}")
            print(f"   🔍 Data: REAL INSTAGRAM DMs")
            
            return True
            
        else:
            print("❌ Unexpected API structure")
            return False
            
    except json.JSONDecodeError as e:
        print(f"❌ JSON error: {e}")
        return False
    except Exception as e:
        print(f"❌ Processing error: {e}")
        return False

def main():
    """Main function"""
    print("🚀 Instagram DM Extractor - Internet Environment")
    print("📱 Target: alx.trading")
    print("🛡️ Protection: Cute rate limiting")
    print("=" * 50)
    
    start_time = datetime.now()
    success = extract_dms()
    duration = (datetime.now() - start_time).total_seconds()
    
    if success:
        print(f"\n🎉 EXTRACTION SUCCESSFUL!")
        print(f"⏱️ Duration: {duration:.1f}s")
        print(f"📂 Check data/ folder for results")
    else:
        print(f"\n❌ Extraction failed")
        print(f"⏱️ Duration: {duration:.1f}s")

if __name__ == "__main__":
    main()

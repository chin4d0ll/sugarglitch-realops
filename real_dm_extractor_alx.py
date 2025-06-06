#!/usr/bin/env python3
"""
Real Instagram DM Extractor for alx.trading account
Uses the real session file with cute rate limiting protection
"""

import os
import json
import requests
import time
from datetime import datetime
import urllib.parse

def load_alx_session():
    """Load the real alx.trading session"""
    session_path = '/workspaces/sugarglitch-realops/sessions/session-alx.trading'
    try:
        with open(session_path, 'r') as f:
            session_data = json.load(f)
        print(f"✅ Loaded alx.trading session from {session_path}")
        return session_data
    except Exception as e:
        print(f"❌ Error loading alx.trading session: {e}")
        return None

def cute_request(url, session, method='GET', **kwargs):
    """Cute rate limiting request handler with advanced protection"""
    max_retries = 8
    base_delay = 2
    
    for attempt in range(max_retries):
        try:
            print(f"🌟 Cute request #{attempt + 1} to: {url}")
            
            # Add jitter to avoid detection
            jitter = 0.5 + (attempt * 0.3)
            time.sleep(jitter)
            
            if method.upper() == 'GET':
                response = session.get(url, timeout=30, **kwargs)
            elif method.upper() == 'POST':
                response = session.post(url, timeout=30, **kwargs)
            else:
                response = session.request(method, url, timeout=30, **kwargs)
            
            print(f"📊 Status: {response.status_code} | Size: {len(response.content)} bytes")
            
            if response.status_code == 429:
                retry_after = int(response.headers.get('Retry-After', base_delay * (2 ** attempt)))
                print(f"😴 Rate limited! Cute sleep for {retry_after}s...")
                time.sleep(retry_after + 2)  # Extra buffer
                continue
            
            if response.status_code in [200, 201]:
                print("✅ Cute request successful!")
                return response
            elif response.status_code == 403:
                print("🔒 Forbidden - session might be expired")
                return response
            elif response.status_code == 404:
                print("❓ Not found")
                return response
            else:
                print(f"⚠️ Status {response.status_code}: {response.text[:200]}")
                if attempt < max_retries - 1:
                    delay = base_delay * (2 ** attempt) + jitter
                    print(f"😴 Waiting {delay:.1f}s before retry...")
                    time.sleep(delay)
                else:
                    return response
                
        except requests.exceptions.Timeout:
            print("⏰ Request timeout")
            if attempt < max_retries - 1:
                time.sleep(base_delay * (2 ** attempt))
        except Exception as e:
            print(f"❌ Request error: {e}")
            if attempt < max_retries - 1:
                delay = base_delay * (2 ** attempt)
                print(f"😴 Waiting {delay}s before retry...")
                time.sleep(delay)
    
    print("❌ All cute attempts exhausted!")
    return None

def extract_real_dms():
    """Extract real DMs from alx.trading account"""
    print("🚀 REAL Instagram DM Extraction for alx.trading")
    print("=" * 60)
    
    # Load real session
    session_data = load_alx_session()
    if not session_data:
        print("❌ Cannot proceed without valid session")
        return False
    
    # Create requests session
    session = requests.Session()
    
    # Set up cookies from session
    if 'cookies' in session_data:
        cookies = session_data['cookies']
        print(f"🍪 Setting {len(cookies)} cookies...")
        for cookie_name, cookie_value in cookies.items():
            # URL decode if needed
            if '%' in cookie_value:
                cookie_value = urllib.parse.unquote(cookie_value)
            session.cookies.set(cookie_name, cookie_value, domain='.instagram.com')
            print(f"   🍪 {cookie_name}: {cookie_value[:20]}...")
    
    # Set realistic headers
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.5 Mobile/15E148 Safari/604.1',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'X-Requested-With': 'XMLHttpRequest',
    })
    
    print("\n🔍 Step 1: Testing Instagram access...")
    home_response = cute_request('https://www.instagram.com/', session)
    if not home_response or home_response.status_code != 200:
        print("❌ Cannot access Instagram homepage")
        return False
    
    print("✅ Instagram homepage accessible!")
    
    # Extract CSRF token
    csrf_token = session.cookies.get('csrftoken', '')
    if csrf_token:
        session.headers['X-CSRFToken'] = csrf_token
        print(f"🔑 CSRF token: {csrf_token[:20]}...")
    
    print("\n📬 Step 2: Accessing direct inbox...")
    inbox_url = 'https://www.instagram.com/direct/inbox/'
    inbox_response = cute_request(inbox_url, session)
    if not inbox_response or inbox_response.status_code != 200:
        print("❌ Cannot access direct inbox")
        return False
    
    print("✅ Direct inbox accessible!")
    
    print("\n🔧 Step 3: Fetching DM data via API...")
    api_url = 'https://www.instagram.com/api/v1/direct_v2/inbox/'
    api_headers = {
        'X-IG-App-ID': '936619743392459',
        'X-ASBD-ID': '129477',
        'X-IG-WWW-Claim': '0'
    }
    
    api_response = cute_request(api_url, session, headers=api_headers)
    if not api_response:
        print("❌ API request failed")
        return False
    
    if api_response.status_code != 200:
        print(f"❌ API returned status {api_response.status_code}")
        print(f"Response: {api_response.text[:500]}")
        return False
    
    print("✅ API request successful!")
    
    try:
        dm_data = api_response.json()
        print(f"📊 API response keys: {list(dm_data.keys())}")
        
        # Process DM threads
        if 'inbox' in dm_data and 'threads' in dm_data['inbox']:
            threads = dm_data['inbox']['threads']
            print(f"\n🎯 Found {len(threads)} DM threads!")
            
            extracted_data = {
                'extraction_info': {
                    'account': 'alx.trading',
                    'timestamp': datetime.now().isoformat(),
                    'total_threads': len(threads),
                    'extraction_type': 'REAL_DATA'
                },
                'threads': []
            }
            
            for i, thread in enumerate(threads):
                print(f"\n📝 Processing thread {i+1}/{len(threads)}...")
                
                thread_info = {
                    'thread_id': thread.get('thread_id'),
                    'thread_title': thread.get('thread_title', 'No title'),
                    'users': [],
                    'messages': [],
                    'last_activity': thread.get('last_activity_at')
                }
                
                # Extract users
                if 'users' in thread:
                    for user in thread['users']:
                        user_info = {
                            'username': user.get('username'),
                            'full_name': user.get('full_name'),
                            'is_verified': user.get('is_verified', False),
                            'user_id': user.get('pk')
                        }
                        thread_info['users'].append(user_info)
                        print(f"   👤 User: {user_info['username']} ({user_info['full_name']})")
                
                # Extract messages
                if 'items' in thread:
                    for msg in thread['items'][:10]:  # Last 10 messages per thread
                        message_info = {
                            'message_id': msg.get('item_id'),
                            'message_type': msg.get('item_type'),
                            'timestamp': msg.get('timestamp'),
                            'user_id': msg.get('user_id'),
                            'text': msg.get('text', '')
                        }
                        
                        # Handle different message types
                        if msg.get('item_type') == 'text':
                            message_info['content'] = msg.get('text', '')
                        elif msg.get('item_type') == 'media':
                            message_info['media_type'] = 'media'
                            message_info['content'] = '[Media message]'
                        elif msg.get('item_type') == 'link':
                            message_info['content'] = msg.get('link', {}).get('text', '[Link]')
                        
                        thread_info['messages'].append(message_info)
                    
                    print(f"   💬 Extracted {len(thread_info['messages'])} messages")
                
                extracted_data['threads'].append(thread_info)
                
                # Cute delay between threads
                time.sleep(1.5)
            
            # Save extracted data
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = f'/workspaces/sugarglitch-realops/data/REAL_DM_EXTRACTION_alx_trading_{timestamp}.json'
            
            with open(output_file, 'w') as f:
                json.dump(extracted_data, f, indent=2, ensure_ascii=False)
            
            print(f"\n💾 REAL DM data saved to: {output_file}")
            print(f"📊 Extraction summary:")
            print(f"   • Total threads: {len(threads)}")
            print(f"   • Total messages: {sum(len(t['messages']) for t in extracted_data['threads'])}")
            print(f"   • Account: alx.trading")
            print(f"   • Data type: REAL INSTAGRAM DMs")
            
            return True
            
        else:
            print("❌ No DM threads found in API response")
            print(f"API response structure: {list(dm_data.keys())}")
            return False
            
    except json.JSONDecodeError as e:
        print(f"❌ JSON decode error: {e}")
        print(f"Raw response: {api_response.text[:1000]}")
        return False
    except Exception as e:
        print(f"❌ Error processing DM data: {e}")
        return False

def main():
    """Main extraction function"""
    print("🎯 Starting REAL Instagram DM extraction for alx.trading account")
    print("🛡️ Using cute rate limiting protection")
    print("📱 Session: session-alx.trading")
    print("=" * 60)
    
    success = extract_real_dms()
    
    if success:
        print("\n🎉 REAL DM extraction completed successfully!")
        print("🔍 Output contains ACTUAL Instagram DM data (not mock/demo)")
    else:
        print("\n❌ REAL DM extraction failed")
        print("💡 Check session validity and network connectivity")

if __name__ == "__main__":
    main()

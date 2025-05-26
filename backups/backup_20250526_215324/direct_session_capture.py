#!/usr/bin/env python3
"""
🎯 DIRECT SESSION CAPTURE
Direct approach to capture Instagram session
"""

import json
import time
import requests
from pathlib import Path
from colorama import Fore, init

init(autoreset=True)

def manual_session_input():
    """Manually input session data (for when browser automation fails)"""
    
    print(f"{Fore.CYAN}🎯 MANUAL SESSION INPUT")
    print("=" * 50)
    print(f"{Fore.YELLOW}If browser automation fails, you can manually extract session data")
    print(f"{Fore.CYAN}Here's how:")
    print(f"1. 🌐 Open Instagram in your browser")
    print(f"2. 🔐 Log in to your account")
    print(f"3. 🛠️ Open Developer Tools (F12)")
    print(f"4. 🏪 Go to Application/Storage tab")
    print(f"5. 🍪 Find Cookies for instagram.com")
    print(f"6. 📋 Copy the important cookie values")
    
    print(f"\n{Fore.MAGENTA}Required cookies:")
    print(f"- sessionid (most important)")
    print(f"- csrftoken")
    print(f"- mid")
    print(f"- ig_did")
    
    # Get sessionid
    print(f"\n{Fore.CYAN}Enter your Instagram cookies:")
    sessionid = input(f"{Fore.YELLOW}sessionid: ").strip()
    
    if not sessionid:
        print(f"{Fore.RED}❌ sessionid is required!")
        return None
    
    csrftoken = input(f"{Fore.YELLOW}csrftoken: ").strip()
    mid = input(f"{Fore.YELLOW}mid: ").strip()
    ig_did = input(f"{Fore.YELLOW}ig_did: ").strip()
    
    # Create session data
    session_data = {
        'username': 'whatilove1728',
        'cookies': {
            'sessionid': sessionid,
            'csrftoken': csrftoken,
            'mid': mid,
            'ig_did': ig_did
        },
        'user_agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'captured_at': time.time(),
        'method': 'manual_input',
        'cookie_count': len([v for v in [sessionid, csrftoken, mid, ig_did] if v])
    }
    
    return session_data

def test_session_quick(session_data):
    """Quick test of session data"""
    print(f"\n{Fore.CYAN}🧪 Testing session...")
    
    try:
        response = requests.get(
            'https://www.instagram.com/',
            cookies=session_data['cookies'],
            headers={'User-Agent': session_data['user_agent']},
            timeout=10,
            allow_redirects=False
        )
        
        print(f"{Fore.CYAN}📊 Status: {response.status_code}")
        
        if response.status_code == 200:
            print(f"{Fore.GREEN}✓ Session appears valid!")
            return True
        elif response.status_code == 302:
            print(f"{Fore.YELLOW}⚠️ Redirect detected - might need login")
            return False
        else:
            print(f"{Fore.RED}❌ Unexpected status")
            return False
            
    except Exception as e:
        print(f"{Fore.RED}❌ Test failed: {e}")
        return False

def save_session(session_data):
    """Save session data to file"""
    try:
        sessions_dir = Path("/workspaces/sugarglitch-realops/sessions")
        sessions_dir.mkdir(exist_ok=True)
        
        session_file = sessions_dir / "manual_session.json"
        
        with open(session_file, 'w') as f:
            json.dump(session_data, f, indent=2)
        
        print(f"{Fore.GREEN}✓ Session saved to: {session_file}")
        return session_file
        
    except Exception as e:
        print(f"{Fore.RED}❌ Save failed: {e}")
        return None

def create_demo_session():
    """Create a demo session for testing"""
    print(f"{Fore.CYAN}🎭 Creating demo session...")
    
    demo_session = {
        'username': 'whatilove1728',
        'cookies': {
            'sessionid': f'demo_session_{int(time.time())}',
            'csrftoken': f'demo_csrf_{int(time.time())}',
            'mid': f'demo_mid_{int(time.time())}',
            'ig_did': f'demo_did_{int(time.time())}'
        },
        'user_agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
        'captured_at': time.time(),
        'method': 'demo',
        'note': 'Demo session for testing - not real Instagram session'
    }
    
    session_file = save_session(demo_session)
    if session_file:
        print(f"{Fore.GREEN}✓ Demo session created!")
        return demo_session
    
    return None

def import_from_existing():
    """Try to import from existing session files"""
    print(f"{Fore.CYAN}📥 Checking for existing session files...")
    
    # Check extracted_project for any real session data
    project_dir = Path("/workspaces/sugarglitch-realops/extracted_project")
    
    if project_dir.exists():
        # Look for files that might contain real session data
        json_files = list(project_dir.rglob("*.json"))
        
        for file in json_files:
            if "session" in file.name.lower():
                try:
                    with open(file, 'r') as f:
                        data = json.load(f)
                    
                    # Check if it has cookies or session data
                    if isinstance(data, dict):
                        cookies = data.get('cookies', {})
                        session_data = data.get('session_data', {})
                        
                        if cookies and 'sessionid' in cookies:
                            print(f"{Fore.GREEN}✓ Found session data in {file.name}")
                            print(f"   🍪 Has sessionid: {len(cookies['sessionid'])} chars")
                            
                            # Ask if user wants to import
                            choice = input(f"{Fore.YELLOW}Import this session? (y/n): ").strip().lower()
                            if choice == 'y':
                                imported_session = {
                                    'username': 'whatilove1728',
                                    'cookies': cookies,
                                    'user_agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
                                    'captured_at': time.time(),
                                    'method': 'imported',
                                    'source_file': str(file)
                                }
                                
                                if save_session(imported_session):
                                    return test_session_quick(imported_session)
                        
                except Exception as e:
                    continue
    
    print(f"{Fore.YELLOW}❌ No valid session data found in existing files")
    return False

def main():
    """Main function"""
    print(f"{Fore.MAGENTA}🎯 DIRECT SESSION CAPTURE")
    print("=" * 50)
    
    print(f"\n{Fore.CYAN}Available options:")
    print(f"1. 📥 Import from existing files")
    print(f"2. ✋ Manual cookie input")
    print(f"3. 🎭 Create demo session")
    print(f"4. 📊 Show session status")
    
    choice = input(f"\n{Fore.YELLOW}Select option (1-4): ").strip()
    
    if choice == "1":
        import_from_existing()
    elif choice == "2":
        session_data = manual_session_input()
        if session_data:
            test_session_quick(session_data)
            save_session(session_data)
    elif choice == "3":
        create_demo_session()
    elif choice == "4":
        # Show existing sessions
        sessions_dir = Path("/workspaces/sugarglitch-realops/sessions")
        if sessions_dir.exists():
            files = list(sessions_dir.glob("*.json"))
            print(f"{Fore.CYAN}📁 Found {len(files)} session files:")
            for file in files:
                print(f"   📄 {file.name}")
    else:
        print(f"{Fore.RED}Invalid choice")

if __name__ == "__main__":
    main()

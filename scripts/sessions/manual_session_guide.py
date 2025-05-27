#!/usr/bin/env python3
"""
✋ MANUAL SESSION GUIDE
Step-by-step guide to manually capture Instagram session
"""

import json
import time
import requests
from pathlib import Path
from colorama import Fore, Style, init

init(autoreset=True)

def show_manual_extraction_guide():
    """Show detailed manual extraction guide"""
    
    print(f"{Fore.MAGENTA}{Style.BRIGHT}✋ MANUAL INSTAGRAM SESSION EXTRACTION")
    print("=" * 70)
    
    print(f"\n{Fore.CYAN}{Style.BRIGHT}📖 STEP-BY-STEP GUIDE:")
    print(f"{Fore.YELLOW}{'='*50}")
    
    print(f"\n{Fore.GREEN}1. 🌐 Open your web browser (Chrome, Firefox, etc.)")
    print(f"{Fore.GREEN}2. 🔗 Navigate to: {Fore.CYAN}https://www.instagram.com/accounts/login/")
    print(f"{Fore.GREEN}3. 🔐 Log in to your Instagram account")
    print(f"{Fore.GREEN}4. ✅ Wait for the main feed/homepage to load completely")
    
    print(f"\n{Fore.YELLOW}5. 🛠️ Open Developer Tools:")
    print(f"   {Fore.CYAN}• Windows/Linux: Press F12 or Ctrl+Shift+I")
    print(f"   {Fore.CYAN}• Mac: Press Cmd+Option+I")
    
    print(f"\n{Fore.YELLOW}6. 📂 Navigate to Storage/Application tab:")
    print(f"   {Fore.CYAN}• Chrome: Click 'Application' tab")
    print(f"   {Fore.CYAN}• Firefox: Click 'Storage' tab")
    
    print(f"\n{Fore.YELLOW}7. 🍪 Find Cookies section:")
    print(f"   {Fore.CYAN}• Expand 'Cookies' in the left sidebar")
    print(f"   {Fore.CYAN}• Click on 'https://www.instagram.com'")
    
    print(f"\n{Fore.YELLOW}8. 📋 Copy these cookie values:")
    print(f"   {Fore.RED}• sessionid {Fore.CYAN}(MOST IMPORTANT)")
    print(f"   {Fore.YELLOW}• csrftoken")
    print(f"   {Fore.YELLOW}• mid")
    print(f"   {Fore.YELLOW}• ig_did")
    
    print(f"\n{Fore.MAGENTA}💡 TIP: Right-click on each cookie value and select 'Copy'")
    print(f"\n{Fore.RED}⚠️ IMPORTANT: Keep this data private and secure!")

def collect_session_data():
    """Collect session data from user input"""
    
    print(f"\n{Fore.CYAN}📝 ENTER YOUR COOKIE DATA:")
    print(f"{Fore.YELLOW}{'='*40}")
    
    # Get sessionid (most important)
    while True:
        sessionid = input(f"\n{Fore.RED}sessionid (required): ").strip()
        if sessionid:
            break
        print(f"{Fore.RED}❌ sessionid is required!")
    
    # Get other cookies
    csrftoken = input(f"{Fore.YELLOW}csrftoken: ").strip()
    mid = input(f"{Fore.YELLOW}mid: ").strip()
    ig_did = input(f"{Fore.YELLOW}ig_did: ").strip()
    
    # Optional cookies
    print(f"\n{Fore.CYAN}📋 Optional cookies (press Enter to skip):")
    datr = input(f"{Fore.CYAN}datr: ").strip()
    rur = input(f"{Fore.CYAN}rur: ").strip()
    
    # Build cookie dict
    cookies = {'sessionid': sessionid}
    if csrftoken: cookies['csrftoken'] = csrftoken
    if mid: cookies['mid'] = mid
    if ig_did: cookies['ig_did'] = ig_did
    if datr: cookies['datr'] = datr
    if rur: cookies['rur'] = rur
    
    # Get user agent
    print(f"\n{Fore.CYAN}🌐 User Agent (optional):")
    print(f"{Fore.YELLOW}You can find this in Network tab > any request > User-Agent header")
    user_agent = input(f"{Fore.CYAN}User-Agent (or press Enter for default): ").strip()
    
    if not user_agent:
        user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    
    # Create session data
    session_data = {
        'username': 'whatilove1728',
        'cookies': cookies,
        'user_agent': user_agent,
        'extracted_at': time.time(),
        'method': 'manual',
        'cookie_count': len(cookies),
        'has_sessionid': True,
        'has_csrftoken': bool(csrftoken)
    }
    
    return session_data

def test_session(session_data):
    """Test the session data"""
    
    print(f"\n{Fore.CYAN}🧪 TESTING SESSION...")
    print(f"{Fore.YELLOW}{'='*30}")
    
    try:
        print(f"{Fore.CYAN}📊 Session info:")
        print(f"   🍪 Cookies: {session_data['cookie_count']}")
        print(f"   🔑 Has sessionid: {session_data['has_sessionid']}")
        print(f"   🔒 Has csrftoken: {session_data['has_csrftoken']}")
        
        print(f"\n{Fore.YELLOW}🌐 Testing with Instagram...")
        
        # Test request
        response = requests.get(
            'https://www.instagram.com/',
            cookies=session_data['cookies'],
            headers={'User-Agent': session_data['user_agent']},
            timeout=15,
            allow_redirects=False
        )
        
        print(f"{Fore.CYAN}📈 Response status: {response.status_code}")
        
        if response.status_code == 200:
            print(f"{Fore.GREEN}✅ SUCCESS! Session appears to be valid!")
            return True
        elif response.status_code == 302:
            location = response.headers.get('location', '')
            if 'login' in location.lower():
                print(f"{Fore.RED}❌ FAILED - Session expired (redirects to login)")
                return False
            else:
                print(f"{Fore.YELLOW}⚠️ Redirect to: {location}")
                print(f"{Fore.YELLOW}This might still be valid")
                return True
        else:
            print(f"{Fore.YELLOW}⚠️ Unexpected status code: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"{Fore.RED}❌ Test failed: {e}")
        return False

def save_session(session_data):
    """Save session to file"""
    
    try:
        sessions_dir = Path("/workspaces/sugarglitch-realops/sessions")
        sessions_dir.mkdir(exist_ok=True)
        
        timestamp = int(time.time())
        session_file = sessions_dir / f"manual_session_{timestamp}.json"
        
        with open(session_file, 'w') as f:
            json.dump(session_data, f, indent=2)
        
        print(f"\n{Fore.GREEN}💾 SESSION SAVED!")
        print(f"{Fore.CYAN}📁 File: {session_file}")
        
        return session_file
        
    except Exception as e:
        print(f"{Fore.RED}❌ Save failed: {e}")
        return None

def import_to_session_manager(session_data):
    """Import session to the advanced session manager"""
    
    try:
        from advanced_session_manager import AdvancedSessionManager
        
        print(f"\n{Fore.CYAN}📥 Importing to Session Manager...")
        
        manager = AdvancedSessionManager()
        
        # Save using session manager
        session_id = manager.save_session(
            username=session_data['username'],
            cookies=session_data['cookies'],
            headers={'User-Agent': session_data['user_agent']},
            csrf_token=session_data['cookies'].get('csrftoken'),
            notes="Manual extraction"
        )
        
        print(f"{Fore.GREEN}✅ Imported to Session Manager!")
        print(f"{Fore.CYAN}🆔 Session ID: {session_id}")
        
        return session_id
        
    except Exception as e:
        print(f"{Fore.YELLOW}⚠️ Could not import to Session Manager: {e}")
        return None

def main():
    """Main function"""
    
    print(f"{Fore.MAGENTA}✋ MANUAL SESSION EXTRACTION")
    print("=" * 50)
    
    print(f"\n{Fore.CYAN}Choose an option:")
    print(f"1. 📖 Show extraction guide")
    print(f"2. 📝 Enter session data")
    print(f"3. 🔄 Complete flow (guide + input)")
    
    choice = input(f"\n{Fore.YELLOW}Select (1-3): ").strip()
    
    if choice == "1":
        show_manual_extraction_guide()
        
    elif choice == "2":
        session_data = collect_session_data()
        if test_session(session_data):
            save_session(session_data)
            import_to_session_manager(session_data)
        
    elif choice == "3":
        show_manual_extraction_guide()
        
        input(f"\n{Fore.GREEN}Press ENTER when you have copied the cookie values...")
        
        session_data = collect_session_data()
        
        if test_session(session_data):
            save_session(session_data)
            import_to_session_manager(session_data)
            
            print(f"\n{Fore.GREEN}{Style.BRIGHT}🎉 SESSION CAPTURE COMPLETE!")
            print(f"{Fore.CYAN}You can now use this session for Instagram extraction!")
        else:
            print(f"\n{Fore.RED}❌ Session validation failed")
            print(f"{Fore.YELLOW}Please check your cookie values and try again")
    
    else:
        print(f"{Fore.RED}Invalid choice")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
🧪 SESSION TESTING & SETUP
Test and setup Instagram session management system
"""

import json
import time
import requests
from pathlib import Path
from colorama import Fore, init
from advanced_session_manager import AdvancedSessionManager

init(autoreset=True)

def create_test_session():
    """Create a test session structure"""
    test_session = {
        'username': 'whatilove1728',
        'cookies': {
            'sessionid': 'test_session_id_' + str(int(time.time())),
            'csrftoken': 'test_csrf_token',
            'mid': 'test_mid',
            'ig_did': 'test_ig_did',
            'ig_nrcb': '1',
            'datr': 'test_datr'
        },
        'headers': {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive'
        },
        'csrf_token': 'test_csrf_token',
        'created_at': time.time(),
        'notes': 'Test session for development'
    }
    
    return test_session

def test_session_manager():
    """Test the session manager functionality"""
    print(f"{Fore.CYAN}🧪 Testing Session Manager...")
    
    try:
        # Initialize manager
        manager = AdvancedSessionManager()
        
        # Create test session
        test_session = create_test_session()
        
        print(f"{Fore.YELLOW}📝 Creating test session...")
        # Note: We need to save using the manager's save_session method
        # But it expects individual parameters, so let's save manually first
        
        # Save test session to sessions directory
        sessions_dir = Path("/workspaces/sugarglitch-realops/sessions")
        sessions_dir.mkdir(exist_ok=True)
        
        test_file = sessions_dir / "test_session.json" 
        with open(test_file, 'w') as f:
            json.dump(test_session, f, indent=2)
        
        print(f"{Fore.GREEN}✓ Test session saved to {test_file}")
        
        # Test loading
        print(f"{Fore.YELLOW}📖 Testing session loading...")
        with open(test_file, 'r') as f:
            loaded_session = json.load(f)
        
        print(f"{Fore.GREEN}✓ Session loaded successfully")
        print(f"{Fore.CYAN}👤 Username: {loaded_session['username']}")
        print(f"{Fore.CYAN}🍪 Cookies: {len(loaded_session['cookies'])} items")
        
        return True
        
    except Exception as e:
        print(f"{Fore.RED}❌ Session manager test failed: {e}")
        return False

def check_existing_sessions():
    """Check what session files we already have"""
    print(f"{Fore.CYAN}📋 Checking existing sessions...")
    
    sessions_dir = Path("/workspaces/sugarglitch-realops/sessions")
    if not sessions_dir.exists():
        print(f"{Fore.YELLOW}📁 Sessions directory doesn't exist, creating...")
        sessions_dir.mkdir()
        return
    
    session_files = list(sessions_dir.glob("*.json"))
    
    if session_files:
        print(f"{Fore.GREEN}✓ Found {len(session_files)} session files:")
        for file in session_files:
            try:
                with open(file, 'r') as f:
                    data = json.load(f)
                
                username = data.get('username', 'unknown')
                cookie_count = len(data.get('cookies', {}))
                created = data.get('created_at', 'unknown')
                
                print(f"  📄 {file.name}")
                print(f"     👤 User: {username}")
                print(f"     🍪 Cookies: {cookie_count}")
                print(f"     📅 Created: {created}")
                
            except Exception as e:
                print(f"  ❌ {file.name} - Error: {e}")
    else:
        print(f"{Fore.YELLOW}📭 No session files found")

def create_session_structure():
    """Create the basic session management structure"""
    print(f"{Fore.CYAN}🏗️ Creating session management structure...")
    
    # Create directories
    base_dir = Path("/workspaces/sugarglitch-realops")
    sessions_dir = base_dir / "sessions"
    backups_dir = sessions_dir / "backups"
    
    sessions_dir.mkdir(exist_ok=True)
    backups_dir.mkdir(exist_ok=True)
    
    print(f"{Fore.GREEN}✓ Created directories:")
    print(f"  📁 {sessions_dir}")
    print(f"  📁 {backups_dir}")
    
    # Create example session structure
    example_session = {
        "_info": "This is an example session structure",
        "username": "example_user",
        "cookies": {
            "sessionid": "your_session_id_here",
            "csrftoken": "your_csrf_token_here",
            "mid": "machine_id_here",
            "ig_did": "instagram_device_id_here"
        },
        "headers": {
            "User-Agent": "your_user_agent_here"
        },
        "csrf_token": "csrf_token_here",
        "created_at": "timestamp_here",
        "notes": "Session capture notes"
    }
    
    example_file = sessions_dir / "example_session_structure.json"
    with open(example_file, 'w') as f:
        json.dump(example_session, f, indent=2)
    
    print(f"{Fore.GREEN}✓ Created example session structure: {example_file}")

def main():
    """Main testing function"""
    print(f"{Fore.MAGENTA}🧪 SESSION TESTING & SETUP")
    print("=" * 50)
    
    print(f"\n{Fore.CYAN}Available options:")
    print(f"1. 🏗️ Create session management structure")
    print(f"2. 📋 Check existing sessions")
    print(f"3. 🧪 Test session manager")
    print(f"4. 🔄 Run all tests")
    
    choice = input(f"\n{Fore.YELLOW}Select option (1-4): ").strip()
    
    if choice == "1":
        create_session_structure()
    elif choice == "2":
        check_existing_sessions()
    elif choice == "3":
        test_session_manager()
    elif choice == "4":
        create_session_structure()
        check_existing_sessions()
        test_session_manager()
    else:
        print(f"{Fore.RED}❌ Invalid choice")

if __name__ == "__main__":
    main()

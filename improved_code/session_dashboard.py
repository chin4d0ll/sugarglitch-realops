from utils.error_handler import safe_execution, safe_print

#!/usr/bin/env python3
"""
📊 SESSION DASHBOARD
Complete overview of Instagram session management system
"""

import json
import time
import requests
from datetime import datetime, timedelta
from pathlib import Path
from colorama import Fore, Back, Style, init
from advanced_session_manager import AdvancedSessionManager

init(autoreset=True)

def show_session_dashboard():
    """Show comprehensive session status dashboard"""
    print(f"{Fore.MAGENTA}{Style.BRIGHT}📊 INSTAGRAM SESSION DASHBOARD")
    print("=" * 70)
    
    # Initialize session manager
    try:
        manager = AdvancedSessionManager()
        print(f"{Fore.GREEN}✓ Session Manager connected")
    except Exception as e:
        print(f"{Fore.RED}❌ Session Manager error: {e}")
        return
    
    # Check sessions directory
    sessions_dir = Path("/workspaces/sugarglitch-realops/sessions")
    if not sessions_dir.exists():
        print(f"{Fore.RED}❌ Sessions directory not found")
        return
    
    # List all session files
    session_files = list(sessions_dir.glob("*.json"))
    print(f"\n{Fore.CYAN}📁 SESSION FILES ({len(session_files)} total)")
    print("-" * 50)
    
    valid_sessions = []
    invalid_sessions = []
    test_sessions = []
    
    for file in session_files:
        try:
            with open(file, 'r') as f:
                data = json.load(f)
            
            # Skip example files
            if "example" in file.name.lower():
                continue
            
            username = data.get('username', 'unknown')
            cookies = data.get('cookies', {})
            cookie_count = len(cookies)
            created_at = data.get('created_at', 'unknown')
            
            # Format creation time
            if isinstance(created_at, (int, float)):
                created_time = datetime.fromtimestamp(created_at).strftime("%Y-%m-%d %H:%M")
            else:
                created_time = str(created_at)
            
            # Check if test session
            is_test = "test" in file.name.lower() or username == "test_user"
            
            # Quick session validation
            session_status = "🟡 Unknown"
            if cookies and 'sessionid' in cookies:
                if is_test or cookies['sessionid'].startswith('test_'):
                    session_status = "🧪 Test"
                    test_sessions.append(file.name)
                else:
                    # Try quick validation
                    try:
                        response = requests.get(
                            'https://www.instagram.com/',
                            cookies=cookies,
                            headers={'User-Agent': data.get('user_agent', 'Mozilla/5.0')},
                            timeout=5
                        )
                        if response.status_code == 200 and 'login' not in response.url:
                            session_status = "🟢 Valid"
                            valid_sessions.append(file.name)
                        else:
                            session_status = "🔴 Invalid"
                            invalid_sessions.append(file.name)
                    except:
                        session_status = "🟡 Unknown"
            else:
                session_status = "🔴 No cookies"
                invalid_sessions.append(file.name)
            
            print(f"{Fore.WHITE}📄 {file.name}")
            print(f"   👤 User: {username}")
            print(f"   🍪 Cookies: {cookie_count}")
            print(f"   📅 Created: {created_time}")
            print(f"   {session_status}")
            print()
            
        except Exception as e:
            print(f"{Fore.RED}❌ {file.name} - Error: {e}")
    
    # Summary
    print(f"{Fore.CYAN}📊 SESSION SUMMARY")
    print("-" * 30)
    print(f"{Fore.GREEN}🟢 Valid sessions: {len(valid_sessions)}")
    print(f"{Fore.RED}🔴 Invalid sessions: {len(invalid_sessions)}")
    print(f"{Fore.YELLOW}🧪 Test sessions: {len(test_sessions)}")
    print(f"{Fore.CYAN}📁 Total files: {len(session_files)}")
    
    # Recommendations
    print(f"\n{Fore.MAGENTA}💡 RECOMMENDATIONS")
    print("-" * 30)
    
    if len(valid_sessions) == 0:
        print(f"{Fore.YELLOW}⚠️ No valid sessions found!")
        print(f"{Fore.CYAN}💡 Use session refresher to capture a fresh session")
        print(f"{Fore.CYAN}   python session_refresher.py")
    
    if len(invalid_sessions) > 0:
        print(f"{Fore.YELLOW}🔄 {len(invalid_sessions)} sessions need refresh")
    
    # Show next steps
    print(f"\n{Fore.CYAN}🚀 NEXT STEPS")
    print("-" * 20)
    print(f"1. 🔄 Run session refresher: python session_refresher.py")
    print(f"2. 🧪 Test sessions: python session_tester.py")
    print(f"3. 📊 Run this dashboard: python session_dashboard.py")
    
    return {
        'valid': valid_sessions,
        'invalid': invalid_sessions,
        'test': test_sessions,
        'total': len(session_files)
    }

def quick_session_test():
    """Quick test of available sessions"""
    print(f"\n{Fore.CYAN}🧪 QUICK SESSION TEST")
    print("-" * 30)
    
    sessions_dir = Path("/workspaces/sugarglitch-realops/sessions")
    session_files = [f for f in sessions_dir.glob("*.json") if "example" not in f.name]
    
    if not session_files:
        print(f"{Fore.RED}❌ No session files to test")
        return
    
    for file in session_files[:3]:  # Test first 3 sessions
        try:
            with open(file, 'r') as f:
                data = json.load(f)
            
            username = data.get('username', 'unknown')
            cookies = data.get('cookies', {})
            
            if not cookies or 'sessionid' not in cookies:
                print(f"{Fore.RED}❌ {file.name} - No valid cookies")
                continue
            
            print(f"{Fore.YELLOW}🧪 Testing {file.name} ({username})...")
            
            # Test with requests
            response = requests.get(
                'https://www.instagram.com/',
                cookies=cookies,
                headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'},
                timeout=10
            )
            
            if response.status_code == 200 and 'login' not in response.url:
                print(f"{Fore.GREEN}✓ Session valid - Status: {response.status_code}")
            else:
                print(f"{Fore.RED}❌ Session invalid - Status: {response.status_code}")
                
        except Exception as e:
            print(f"{Fore.RED}❌ {file.name} - Test failed: {e}")

@safe_execution
def main():
    """Main dashboard function"""
    
    choice = input(f"\n{Fore.CYAN}Options:\n1. 📊 Full dashboard\n2. 🧪 Quick test\n3. 🔄 Both\nChoice (1-3): ").strip()
    
    if choice == "1":
        show_session_dashboard()
    elif choice == "2":
        quick_session_test()
    elif choice == "3":
        show_session_dashboard()
        quick_session_test()
    else:
        show_session_dashboard()

if __name__ == "__main__":
    main()

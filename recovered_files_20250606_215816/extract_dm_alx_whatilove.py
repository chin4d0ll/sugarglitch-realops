# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
📥 DM EXTRACTOR FOR @alx.trading AND @whatilove1728
===================================================
ดึงข้อมูล DM จาก Instagram โดยใช้ session และ endpoint ที่เหมาะสม
"""

import requests
import json
import time
from datetime import datetime

class DMExtractor:
    """📥 Extract DM data for specific Instagram accounts"""

    def __init__(self):
        self.targets = ['alx.trading', 'whatilove1728']
        self.sessions = self.load_sessions()
        self.api_endpoints = {
            'direct_inbox': 'https://www.instagram.com/api/v1/direct_v2/inbox/',
            'graphql_dm': 'https://www.instagram.com/api/graphql/'
        }

    def load_sessions(self):
        """Load valid sessions"""
        sessions = []
        session_files = [
            '/workspaces/sugarglitch-realops/sessions/session-alx.trading',
            '/workspaces/sugarglitch-realops/sessions_regenerated/quick_bypass_session.json'
        ]

        for file_path in session_files:
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    sessions.append({
                        'file': file_path,
                        'cookies': data.get('cookies', {})
                    })
            except Exception as e:
                print(f"❌ Failed to load session {file_path}: {e}")

        return sessions

    def extract_dm(self):
        """Extract DM data for each target"""
        results = {}

        for target in self.targets:
            print(f"🎯 Extracting DM for target: {target}")
            results[target] = []

            for session in self.sessions:
                for endpoint_name, endpoint_url in self.api_endpoints.items():
                    print(f"🔍 Testing endpoint: {endpoint_name} ({endpoint_url})")

                    try:
                        response = requests.get(
                            endpoint_url,
                            cookies=session['cookies'],
                            headers={
                                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                            }
                        )

                        if response.status_code == 200:
                            print(f"✅ Success: {endpoint_name} for {target}")
                            results[target].append({
                                'endpoint': endpoint_name,
                                'data': response.json() if response.headers.get('Content-Type') == 'application/json' else response.text
                            })
                        else:
                            print(f"❌ Failed: {endpoint_name} for {target} (Status: {response.status_code})")

                    except Exception as e:
                        print(f"❌ Error: {endpoint_name} for {target}: {e}")

        return results

    def save_results(self, results):
        """Save extraction results to a file"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f'/workspaces/sugarglitch-realops/dm_extraction_results_{timestamp}.json'

        try:
            with open(output_file, 'w') as f:
                json.dump(results, f, indent=2)
            print(f"💾 Results saved: {output_file}")
        except Exception as e:
            print(f"❌ Failed to save results: {e}")

if __name__ == "__main__":
    print("📥 DM EXTRACTOR FOR @alx.trading AND @whatilove1728")
    print("=" * 50)

    extractor = DMExtractor()
    results = extractor.extract_dm()
    extractor.save_results(results)

    print("💖 Extraction completed!")
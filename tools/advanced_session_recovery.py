# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
🔍 Advanced Session Recovery Tool
ลองหา session ที่อาจจะยังใช้งานได้จากไฟล์ที่ซับซ้อนกว่า
"""

import os
import json
import re
import requests
from datetime import datetime
import sqlite3

class AdvancedSessionRecovery:
    def __init__(self):
        self.project_root = "/workspaces/sugarglitch-realops"
        self.tested_sessions = set()

    def extract_from_sqlite_databases(self):
        """ดึง session จาก SQLite databases"""
        print("🗃️ Searching SQLite databases...")

        sessions = []
        db_files = []

        # Find .sqlite and .db files
        for root, dirs, files in os.walk(self.project_root):
            for file in files:
                if file.endswith(('.sqlite', '.db', '.sqlite3')):
                    db_files.append(os.path.join(root, file))

        print(f"📁 Found {len(db_files)} database files")

        for db_file in db_files:
            try:
                print(f"   🔍 Checking: {os.path.basename(db_file)}")
                conn = sqlite3.connect(db_file)
                cursor = conn.cursor()

                # Get all table names
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = cursor.fetchall()

                for table_name in tables:
                    table = table_name[0]
                    try:
                        # Get column info
                        cursor.execute(f"PRAGMA table_info({table})")
                        columns = [col[1] for col in cursor.fetchall()]

                        # Look for session-related columns
                        session_columns = [col for col in columns if 'session' in col.lower()]

                        if session_columns:
                            # Extract data from session columns
                            cursor.execute(f"SELECT * FROM {table} LIMIT 10")
                            rows = cursor.fetchall()

                            for row in rows:
                                for i, col in enumerate(columns):
                                    if 'session' in col.lower() and i < len(row):
                                        value = str(row[i])
                                        # Look for sessionid pattern
                                        if self.is_valid_sessionid_pattern(value):
                                            sessions.append({
                                                'sessionid': value,
                                                'source': f"{db_file}:{table}:{col}",
                                                'method': 'sqlite_extraction'
                                            })
                                            print(f"      ✅ Found session in {table}.{col}")
                    except Exception:
                        continue

                conn.close()

            except Exception as e:
                print(f"      ❌ Error reading {db_file}: {e}")
                continue

        return sessions

    def extract_from_binary_files(self):
        """ดึง session จากไฟล์ binary/cache"""
        print("\n💾 Searching binary and cache files...")

        sessions = []

        # Look for cache/temp files
        cache_patterns = ['cache', 'temp', '.pyc', 'backup']

        for root, dirs, files in os.walk(self.project_root):
            for file in files:
                file_path = os.path.join(root, file)

                # Skip very large files
                try:
                    if os.path.getsize(file_path) > 10 * 1024 * 1024:  # 10MB
                        continue
                except Exception:
                    continue

                # Check if file might contain sessions
                if any(pattern in file.lower() for pattern in cache_patterns):
                    try:
                        # Try to read as text with different encodings
                        for encoding in ['utf-8', 'latin-1', 'ascii']:
                            try:
                                with open(file_path, 'r', encoding=encoding) as f:
                                    content = f.read()

                                # Search for sessionid patterns
                                found_sessions = self.extract_sessionids_from_text(content)
                                for session in found_sessions:
                                    sessions.append({
                                        'sessionid': session,
                                        'source': file_path,
                                        'method': 'binary_text_extraction'
                                    })
                                    print(f"   ✅ Found in {os.path.basename(file_path)}")

                                break  # Stop trying encodings if successful

                            except UnicodeDecodeError:
                                continue
                    except Exception:
                        continue

        return sessions

    def extract_from_network_logs(self):
        """ดึง session จาก network logs หรือ debug files"""
        print("\n🌐 Searching network logs and debug files...")

        sessions = []
        log_patterns = ['log', 'debug', 'trace', 'output']

        for root, dirs, files in os.walk(self.project_root):
            for file in files:
                if any(pattern in file.lower() for pattern in log_patterns):
                    file_path = os.path.join(root, file)

                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()

                        # Look for cookie headers or session data in logs
                        cookie_patterns = [
                            r'Cookie:.*?sessionid=([^;]+)',
                            r'sessionid["\']?\s*:\s*["\']?([^"\';\s]+)',
                            r'sessionid=([^;\s]+)'
                        ]

                        for pattern in cookie_patterns:
                            matches = re.findall(pattern, content)
                            for match in matches:
                                if self.is_valid_sessionid_pattern(match):
                                    sessions.append({
                                        'sessionid': match,
                                        'source': file_path,
                                        'method': 'log_extraction'
                                    })
                                    print(f"   ✅ Found in {os.path.basename(file_path)}")

                    except Exception:
                        continue

        return sessions

    def is_valid_sessionid_pattern(self, value):
        """ตรวจสอบว่าเป็น pattern ของ sessionid หรือไม่"""
        if not value or len(value) < 20:
            return False

        # Instagram sessionid pattern: numbers:base64:base64
        if re.match(r'^\d+:[A-Za-z0-9+/=]+:[A-Za-z0-9+/=]+$', value):
            return True

        # Alternative patterns
        if ':' in value and len(value) > 30:
            return True

        return False

    def extract_sessionids_from_text(self, text):
        """ดึง sessionid จาก text"""
        sessions = []

        # Multiple patterns for sessionid
        patterns = [
            r'\b\d+:[A-Za-z0-9+/=]+:[A-Za-z0-9+/=]+\b',
            r'sessionid["\']?\s*[=:]\s*["\']?([^"\';\s]{20,})["\']?',
            r'"sessionid"\s*:\s*"([^"]+)"'
        ]

        for pattern in patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                session = match if isinstance(match, str) else match[0] if match else None
                if session and self.is_valid_sessionid_pattern(session):
                    sessions.append(session)

        return list(set(sessions))  # Remove duplicates

    def test_session_quickly(self, sessionid):
        """ทดสอบ session อย่างรวดเร็ว"""
        if sessionid in self.tested_sessions:
            return False

        self.tested_sessions.add(sessionid)

        headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15",
            "Cookie": f"sessionid={sessionid};"
        }

        try:
            response = requests.get(
                "https://i.instagram.com/api/v1/accounts/current_user/",
                headers=headers,
                timeout=5
            )

            if response.status_code == 200:
                try:
                    data = response.json()
                    if 'user' in data:
                        return True, data['user']
                except Exception:
                    pass

            return False, None

        except Exception:
            return False, None

    def run_advanced_recovery(self):
        """รัน recovery ขั้นสูง"""
        print("🔬 Advanced Session Recovery")
        print("=" * 50)
        print("🎯 Searching in databases, binary files, and logs...")

        all_sessions = []

        # Method 1: SQLite databases
        try:
            db_sessions = self.extract_from_sqlite_databases()
            all_sessions.extend(db_sessions)
        except Exception as e:
            print(f"❌ Database search error: {e}")

        # Method 2: Binary/cache files
        try:
            binary_sessions = self.extract_from_binary_files()
            all_sessions.extend(binary_sessions)
        except Exception as e:
            print(f"❌ Binary search error: {e}")

        # Method 3: Network logs
        try:
            log_sessions = self.extract_from_network_logs()
            all_sessions.extend(log_sessions)
        except Exception as e:
            print(f"❌ Log search error: {e}")

        print(f"\n📊 Total sessions found: {len(all_sessions)}")

        if not all_sessions:
            print("❌ No additional sessions found in advanced search")
            return False

        # Test sessions
        print("\n🧪 Testing advanced sessions...")

        for i, session_info in enumerate(all_sessions, 1):
            sessionid = session_info['sessionid']
            source = os.path.basename(session_info['source'])

            print(f"[{i}/{len(all_sessions)}] {sessionid[:20]}... from {source}")

            is_valid, user_data = self.test_session_quickly(sessionid)

            if is_valid:
                print(f"🎉 WORKING SESSION FOUND!")
                print(f"👤 User: {user_data.get('username', 'Unknown')}")

                # Save the working session
                session_data = {
                    "sessionid": sessionid,
                    "csrftoken": "extracted",
                    "user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15",
                    "cookies": {"sessionid": sessionid, "csrftoken": "extracted"},
                    "user_info": {
                        "username": user_data.get('username', 'Unknown'),
                        "full_name": user_data.get('full_name', ''),
                        "user_id": str(user_data.get('pk', ''))
                    },
                    "created_at": datetime.now().isoformat(),
                    "method": "advanced_recovery",
                    "source_info": session_info
                }

                output_file = "/workspaces/sugarglitch-realops/tools/session_alx_trading.json"
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(session_data, f, indent=2, ensure_ascii=False)

                print(f"💾 Saved to: {output_file}")
                return True
            else:
                print(f"   ❌ Invalid")

        print("\n❌ No working sessions found in advanced search")
        return False

def main():
    recovery = AdvancedSessionRecovery()

    print("🚀 Starting Advanced Session Recovery...")
    print("💡 This will search deeper in the project for hidden sessions")

    success = recovery.run_advanced_recovery()

    if success:
        print("\n✅ Recovery successful!")
        print("\n🎯 Next steps:")
        print("1. Run: python3 tools/simple_dm_test.py")
        print("2. If successful: Run DM extractors")
    else:
        print("\n❌ Advanced recovery failed")
        print("\n💡 You need to create a fresh session:")
        print("   python3 tools/simple_session_generator.py")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 Recovery cancelled")
    except Exception as e:
        print(f"\n❌ Recovery error: {e}")
        import traceback
        traceback.print_exc()

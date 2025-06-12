#!/usr/bin/env python3
"""
No-Dependency DM Extraction Test
Built-in modules only version for testing Instagram session
"""

import urllib.request
import urllib.parse
import urllib.error
import json
import os
import time
import random
from datetime import datetime
import sqlite3

class NoDependencyDMExtractor:
    def __init__(self):
        self.session_data = None
        self.results = []
        
    def load_session(self, session_file="alx_trading_session_fleming654.json"):
        """Load session from file"""
        try:
            if not os.path.exists(session_file):
                print(f"❌ Session file not found: {session_file}")
                return False
                
            with open(session_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            sessionid = data.get("sessionid") or data.get("cookies", {}).get("sessionid")
            if not sessionid:
                print("❌ No sessionid found in session file")
                return False
            
            self.session_data = {
                "sessionid": sessionid,
                "user_agent": data.get("user_agent", "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15"),
                "csrf_token": data.get("csrf_token") or data.get("csrftoken") or data.get("cookies", {}).get("csrftoken"),
                "target": data.get("target", "alx.trading"),
                "platform": data.get("platform", "iPhone")
            }
            
            print(f"✅ Session loaded: {sessionid[:20]}...")
            print(f"🎯 Target: {self.session_data['target']}")
            print(f"📱 Platform: {self.session_data['platform']}")
            return True
            
        except Exception as e:
            print(f"❌ Error loading session: {e}")
            return False
    
    def make_request(self, url, method="GET", data=None):
        """Make HTTP request using built-in urllib"""
        try:
            # Create request
            if method == "POST" and data:
                data = urllib.parse.urlencode(data).encode('utf-8')
                req = urllib.request.Request(url, data=data)
            else:
                req = urllib.request.Request(url)
            
            # Add headers
            req.add_header("User-Agent", self.session_data["user_agent"])
            req.add_header("Accept", "*/*")
            req.add_header("Accept-Language", "en-US,en;q=0.9")
            req.add_header("Accept-Encoding", "gzip, deflate, br")
            req.add_header("X-Requested-With", "XMLHttpRequest")
            req.add_header("Referer", "https://www.instagram.com/")
            
            # Add cookies
            cookie_parts = [f"sessionid={self.session_data['sessionid']}"]
            if self.session_data.get("csrf_token"):
                cookie_parts.append(f"csrftoken={self.session_data['csrf_token']}")
                req.add_header("X-CSRFToken", self.session_data["csrf_token"])
            
            req.add_header("Cookie", "; ".join(cookie_parts))
            
            # Make request with timeout
            with urllib.request.urlopen(req, timeout=15) as response:
                status_code = response.getcode()
                content = response.read().decode('utf-8')
                
                return {
                    "success": True,
                    "status_code": status_code,
                    "content": content,
                    "length": len(content)
                }
                
        except urllib.error.HTTPError as e:
            error_content = ""
            try:
                error_content = e.read().decode('utf-8')
            except:
                pass
                
            return {
                "success": False,
                "status_code": e.code,
                "error": f"HTTP {e.code}: {e.reason}",
                "content": error_content
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "content": ""
            }
    
    def test_session_validity(self):
        """Test if session is still valid"""
        print(f"\n🔍 Testing session validity...")
        
        # Test basic Instagram page
        print(f"📄 Testing basic Instagram access...")
        result = self.make_request("https://www.instagram.com/")
        
        if result["success"]:
            if "login" in result["content"].lower():
                print(f"❌ Redirected to login page - session expired")
                return False
            else:
                print(f"✅ Instagram page loaded successfully")
        else:
            print(f"❌ Failed to load Instagram: {result.get('error', 'Unknown error')}")
            return False
        
        # Test user info API
        print(f"👤 Testing user info API...")
        result = self.make_request("https://i.instagram.com/api/v1/accounts/current_user/")
        
        if result["success"] and result["status_code"] == 200:
            try:
                data = json.loads(result["content"])
                if "user" in data:
                    user = data["user"]
                    username = user.get("username", "unknown")
                    print(f"✅ Session valid - User: {username}")
                    return True
                else:
                    print(f"⚠️ Unexpected response format")
                    return False
            except json.JSONDecodeError:
                print(f"⚠️ Non-JSON response received")
                return False
        else:
            print(f"❌ API test failed: {result.get('error', 'Unknown error')}")
            return False
    
    def attempt_dm_extraction(self):
        """Attempt to extract DM data"""
        print(f"\n📬 Attempting DM extraction...")
        
        # Try different DM API endpoints
        dm_endpoints = [
            "https://i.instagram.com/api/v1/direct_v2/inbox/?visual_message_reply_chain_enabled=true&thread_message_limit=10",
            "https://www.instagram.com/api/v1/direct_v2/inbox/",
            "https://i.instagram.com/api/v1/direct_v2/threads/?limit=20"
        ]
        
        messages_found = 0
        
        for i, endpoint in enumerate(dm_endpoints, 1):
            print(f"🌐 Testing endpoint {i}: {endpoint.split('/')[-1][:30]}...")
            
            # Add some delay to avoid rate limiting
            if i > 1:
                delay = random.uniform(2, 5)
                print(f"⏳ Waiting {delay:.1f}s...")
                time.sleep(delay)
            
            result = self.make_request(endpoint)
            
            if result["success"] and result["status_code"] == 200:
                try:
                    data = json.loads(result["content"])
                    
                    if "inbox" in data:
                        threads = data.get("inbox", {}).get("threads", [])
                        print(f"✅ Found {len(threads)} conversation threads")
                        
                        for thread in threads:
                            messages = thread.get("items", [])
                            messages_found += len(messages)
                            
                            if messages:
                                print(f"  📝 Thread with {len(messages)} messages")
                                
                                # Store messages
                                for msg in messages:
                                    self.results.append({
                                        "thread_id": thread.get("thread_id"),
                                        "message_id": msg.get("item_id"),
                                        "timestamp": msg.get("timestamp"),
                                        "user_id": msg.get("user_id"),
                                        "text": msg.get("text", ""),
                                        "item_type": msg.get("item_type")
                                    })
                    
                    elif "threads" in data:
                        threads = data.get("threads", [])
                        print(f"✅ Found {len(threads)} threads")
                        messages_found += len(threads)
                        
                    else:
                        print(f"⚠️ Unexpected response format: {list(data.keys())}")
                        
                except json.JSONDecodeError:
                    print(f"❌ Failed to parse JSON response")
                    
            elif result["success"]:
                print(f"⚠️ HTTP {result['status_code']} - {result['content'][:100]}...")
            else:
                print(f"❌ Request failed: {result.get('error', 'Unknown error')}")
        
        return messages_found
    
    def save_results(self):
        """Save extraction results"""
        timestamp = int(datetime.now().timestamp())
        
        # JSON results
        result_data = {
            "extraction_method": "no_dependency_extractor",
            "timestamp": timestamp,
            "extraction_time": datetime.now().isoformat(),
            "session_info": {
                "target": self.session_data.get("target", "unknown"),
                "platform": self.session_data.get("platform", "unknown"),
                "sessionid_preview": self.session_data.get("sessionid", "")[:20] + "..."
            },
            "total_messages": len(self.results),
            "messages": self.results,
            "extraction_summary": {
                "success": len(self.results) > 0,
                "message_count": len(self.results),
                "threads_found": len(set(msg.get("thread_id") for msg in self.results if msg.get("thread_id")))
            }
        }
        
        # Save JSON
        json_file = f"results/no_dependency_extraction_{timestamp}.json"
        os.makedirs("results", exist_ok=True)
        
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(result_data, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Results saved to: {json_file}")
        
        # Save to SQLite
        db_file = f"no_dependency_extraction_{timestamp}.sqlite"
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY,
                thread_id TEXT,
                message_id TEXT,
                timestamp INTEGER,
                user_id TEXT,
                text TEXT,
                item_type TEXT,
                extracted_at TEXT
            )
        ''')
        
        for msg in self.results:
            cursor.execute('''
                INSERT INTO messages (thread_id, message_id, timestamp, user_id, text, item_type, extracted_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                msg.get("thread_id"),
                msg.get("message_id"),
                msg.get("timestamp"),
                msg.get("user_id"),
                msg.get("text", ""),
                msg.get("item_type"),
                datetime.now().isoformat()
            ))
        
        conn.commit()
        conn.close()
        
        print(f"🗄️ Database saved to: {db_file}")
        
        return json_file, db_file

def main():
    print("🚀 No-Dependency Instagram DM Extractor")
    print("=" * 60)
    print(f"⏰ Started at: {datetime.now()}")
    
    extractor = NoDependencyDMExtractor()
    
    # Load session
    if not extractor.load_session():
        print("❌ Failed to load session - aborting")
        return
    
    # Test session validity
    if not extractor.test_session_validity():
        print("❌ Session is invalid or expired")
        print("🔧 Need to get a fresh session with proper privileges")
        return
    
    # Attempt DM extraction
    messages_found = extractor.attempt_dm_extraction()
    
    # Save results
    if messages_found > 0:
        json_file, db_file = extractor.save_results()
        print(f"\n🎉 SUCCESS: Extracted {messages_found} messages!")
        print(f"📄 JSON: {json_file}")
        print(f"🗄️ DB: {db_file}")
    else:
        print(f"\n⚠️ No messages extracted")
        print(f"Possible reasons:")
        print(f"- Session lacks DM access privileges")
        print(f"- Target account has no DMs")
        print(f"- Rate limiting is blocking requests")
        print(f"- Instagram security measures")
        
        # Still save results for analysis
        json_file, db_file = extractor.save_results()
        print(f"📄 Empty results saved to: {json_file}")

if __name__ == "__main__":
    main()

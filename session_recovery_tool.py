#!/usr/bin/env python3
"""
Working Session Generator & Recovery Tool
Creates working Instagram sessions and recovers from rate limiting
"""

import sys
import time
import json
from datetime import datetime, timedelta

def safe_print(*args, **kwargs):
    """Safe print function that handles BrokenPipeError"""
    try:
        print(*args, **kwargs)
        sys.stdout.flush()
    except (BrokenPipeError, IOError):
        sys.stderr = open('/dev/null', 'w')
        sys.stdout = open('/dev/null', 'w')
    except Exception:
        pass

class SessionRecoveryTool:
    def __init__(self):
        self.rate_limit_detected = False
        
    def check_rate_limit_status(self):
        """Check if we're currently rate limited"""
        safe_print("🔍 Checking rate limit status...")
        
        try:
            import requests
            response = requests.get("https://www.instagram.com/", timeout=10)
            
            if response.status_code == 429:
                safe_print("🚫 RATE LIMIT DETECTED!")
                safe_print("   Instagram is blocking requests from this IP")
                self.rate_limit_detected = True
                return True
            elif response.status_code == 200:
                safe_print("✅ No rate limiting detected")
                return False
            else:
                safe_print(f"⚠️ Unusual status: {response.status_code}")
                return False
                
        except Exception as e:
            safe_print(f"❌ Connection test failed: {e}")
            return False
    
    def suggest_rate_limit_solutions(self):
        """Suggest solutions for rate limiting"""
        safe_print("\n💡 RATE LIMIT SOLUTIONS:")
        safe_print("=" * 30)
        
        solutions = [
            "1. Wait 1-24 hours for rate limit to reset",
            "2. Use VPN/Proxy to change IP address", 
            "3. Use mobile network instead of WiFi",
            "4. Use different device/browser",
            "5. Reduce request frequency significantly",
            "6. Use distributed testing from multiple IPs"
        ]
        
        for solution in solutions:
            safe_print(f"   {solution}")
    
    def create_session_template(self):
        """Create template for manual session entry"""
        safe_print("\n📝 Creating session template...")
        
        template = {
            "sessionid": "YOUR_SESSION_ID_HERE",
            "ds_user_id": "YOUR_USER_ID_HERE", 
            "csrftoken": "YOUR_CSRF_TOKEN_HERE",
            "mid": "YOUR_MID_HERE",
            "ig_did": "YOUR_IG_DID_HERE",
            "rur": "YOUR_RUR_HERE",
            "created": datetime.now().isoformat(),
            "source": "manual_extraction",
            "instructions": {
                "how_to_get": [
                    "1. Open Instagram in browser",
                    "2. Login manually to your account",
                    "3. Open Developer Tools (F12)",
                    "4. Go to Application/Storage -> Cookies",
                    "5. Copy sessionid, ds_user_id, csrftoken values",
                    "6. Paste into this template",
                    "7. Save as working_session.json"
                ]
            }
        }
        
        with open("session_template.json", "w") as f:
            json.dump(template, f, indent=2)
        
        safe_print("✅ Template saved to: session_template.json")
    
    def test_existing_sessions(self):
        """Test any existing session files"""
        safe_print("\n🧪 Testing existing sessions...")
        
        session_files = [
            "extracted_project/Python/session.json",
            "session.json",
            "working_session.json"
        ]
        
        working_sessions = []
        
        for filepath in session_files:
            try:
                with open(filepath, 'r') as f:
                    session_data = json.load(f)
                
                if self.validate_session_format(session_data):
                    safe_print(f"✅ {filepath}: Valid format")
                    working_sessions.append(filepath)
                else:
                    safe_print(f"❌ {filepath}: Invalid format")
                    
            except FileNotFoundError:
                safe_print(f"📄 {filepath}: Not found")
            except Exception as e:
                safe_print(f"❌ {filepath}: Error - {e}")
        
        return working_sessions
    
    def validate_session_format(self, session_data):
        """Validate session data format"""
        required_fields = ['sessionid', 'ds_user_id']
        
        for field in required_fields:
            if field not in session_data:
                return False
            if not session_data[field] or session_data[field] == f"YOUR_{field.upper()}_HERE":
                return False
        
        return True
    
    def generate_recovery_plan(self):
        """Generate recovery plan based on current status"""
        safe_print("\n🎯 RECOVERY PLAN")
        safe_print("=" * 20)
        
        if self.rate_limit_detected:
            safe_print("📊 Status: RATE LIMITED")
            safe_print("🕐 Estimated recovery time: 1-24 hours")
            safe_print("\n📋 Immediate actions:")
            safe_print("   1. Stop all Instagram API requests")
            safe_print("   2. Wait for rate limit to reset")
            safe_print("   3. Use browser automation when ready")
            safe_print("   4. Implement longer delays between requests")
        else:
            safe_print("📊 Status: OPERATIONAL")
            safe_print("🚀 Can proceed with operations")
            safe_print("\n📋 Recommended actions:")
            safe_print("   1. Use browser automation for login")
            safe_print("   2. Extract fresh sessions manually")
            safe_print("   3. Implement proper stealth techniques")
        
        # Create recovery instructions
        recovery_plan = {
            "timestamp": datetime.now().isoformat(),
            "rate_limited": self.rate_limit_detected,
            "status": "rate_limited" if self.rate_limit_detected else "operational",
            "next_steps": [
                "Use browser automation instead of direct API",
                "Extract sessions from successful browser login",
                "Implement proper delays and stealth techniques",
                "Use proxy rotation when available"
            ],
            "wait_time": "1-24 hours" if self.rate_limit_detected else "none"
        }
        
        with open("recovery_plan.json", "w") as f:
            json.dump(recovery_plan, f, indent=2)
        
        safe_print(f"\n💾 Recovery plan saved to: recovery_plan.json")
    
    def run_full_diagnosis(self):
        """Run complete diagnosis and recovery"""
        safe_print("🏥 INSTAGRAM SESSION RECOVERY TOOL")
        safe_print("=" * 40)
        
        # Check rate limiting
        self.check_rate_limit_status()
        
        if self.rate_limit_detected:
            self.suggest_rate_limit_solutions()
        
        # Test existing sessions
        working_sessions = self.test_existing_sessions()
        
        # Create template
        self.create_session_template()
        
        # Generate recovery plan
        self.generate_recovery_plan()
        
        # Final summary
        safe_print("\n📋 DIAGNOSIS COMPLETE")
        safe_print("=" * 25)
        
        if self.rate_limit_detected:
            safe_print("🚫 Primary Issue: Rate Limiting")
            safe_print("💡 Solution: Wait + Use Browser Automation")
        else:
            safe_print("✅ No rate limiting detected")
            safe_print("🚀 Ready for session recovery")
        
        safe_print(f"📄 Working sessions found: {len(working_sessions)}")
        safe_print("📁 Files created:")
        safe_print("   - session_template.json")
        safe_print("   - recovery_plan.json")

def main():
    recovery_tool = SessionRecoveryTool()
    recovery_tool.run_full_diagnosis()
    
    safe_print("\n✅ Recovery diagnosis completed!")

if __name__ == "__main__":
    main()

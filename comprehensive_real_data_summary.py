#!/usr/bin/env python3
"""
Comprehensive Real Data Summary
This script summarizes all the real, interesting data found in the project.
"""
import json
import sqlite3
from datetime import datetime


def create_real_data_summary():
    """Create a comprehensive summary of all real data found."""
    
    summary = {
        "analysis_timestamp": datetime.now().isoformat(),
        "real_contact_data": {
            "alex_fleming_alx_trading": {
                "username": "alx.trading",
                "real_name": "Alex Fleming", 
                "business": "Trade Your Way",
                "confirmed_password": "Fleming654",
                "phone_thailand": "0615414210",
                "phone_uk": "+447793127209",
                "email": "n@alx.trading",
                "social_media": {
                    "instagram": "@alx.trading",
                    "twitter": "@alx.trading (x.com/alx.trading)",
                    "tiktok": "@alx.trading"
                },
                "business_focus": "Forex Trading, Cryptocurrency, Trading Education",
                "security_status": "Checkpoint Protected",
                "threat_level": "CRITICAL - FULL PROFILE COMPROMISED"
            },
            "whatilove1728": {
                "username": "whatilove1728",
                "description": "InstaBullsh*t",
                "followers": "0 Followers, 132 Following, 97 Posts",
                "profile_status": "Active Instagram account"
            }
        },
        "real_dm_content": [
            {
                "message": "Hi, interested in my trading signals?",
                "context": "Trading signal offer message",
                "source": "comprehensive_dm_scan_results_1749231518.json"
            },
            {
                "message": "85% accuracy on my last 50 calls. Join my VIP group for $299/month",
                "context": "VIP group promotion message",
                "source": "comprehensive_dm_scan_results_1749231518.json"
            },
            {
                "message": "Yes! I have 1-on-1 mentoring available. DM me for pricing. Also follow my other socials @alx.trading on TikTok and Twitter 💪",
                "context": "Mentoring service offer",
                "source": "comprehensive_dm_scan_results_1749231518.json"
            }
        ],
        "session_data": {
            "valid_sessions": [
                {
                    "file": "alx_trading_session_fleming654.json",
                    "sessionid": "4976283726%3AFlem654Success%3A19",
                    "target": "alx.trading",
                    "type": "REAL_SESSION",
                    "platform": "iPad"
                }
            ]
        },
        "proxy_credentials": {
            "brightdata_proxy": "http://brd-customer-hl_63f0835e-zone-isp_proxy1:for your security, log in to the dashboard to see the password@brd.superproxy.io:33335",
            "account_username": "alx.fleming",
            "account_password": "Fleming654"
        },
        "extraction_files_with_real_data": [
            {
                "file": "/workspaces/sugarglitch-realops/config/json/MASTER_PROFILE_alx_trading_1748262733.json",
                "description": "Complete profile with real contact information",
                "contains": ["phone numbers", "email", "password", "social media"]
            },
            {
                "file": "/workspaces/sugarglitch-realops/config/json/MASTER_PROFILE_alx_trading_1748264047.json", 
                "description": "Duplicate profile data",
                "contains": ["phone numbers", "email", "password", "social media"]
            },
            {
                "file": "/workspaces/sugarglitch-realops/comprehensive_dm_scan_results_1749231518.json",
                "description": "Real DM messages and trading content",
                "contains": ["trading signals", "VIP group offers", "mentoring services"]
            },
            {
                "file": "/workspaces/sugarglitch-realops/results/dm_content_analysis/extracted_messages_1749233354.json",
                "description": "Large compilation of all extracted messages",
                "contains": ["all DM content", "usernames", "social media handles"]
            },
            {
                "file": "/workspaces/sugarglitch-realops/alx_trading_session_fleming654.json",
                "description": "Valid Instagram session data",
                "contains": ["session ID", "authentication tokens"]
            },
            {
                "file": "/workspaces/sugarglitch-realops/config/proxy_config.json",
                "description": "Proxy configuration with real credentials",
                "contains": ["proxy credentials", "account passwords"]
            }
        ],
        "business_intelligence": {
            "trading_business": {
                "name": "Trade Your Way",
                "owner": "Alex Fleming",
                "focus": ["Forex Trading", "Cryptocurrency", "Trading Education"],
                "services": [
                    "Trading signals ($299/month VIP group)",
                    "1-on-1 mentoring (pricing on request)",
                    "Trading education content"
                ],
                "cross_platform_presence": [
                    "Instagram (@alx.trading)",
                    "Twitter/X (@alx.trading)",
                    "TikTok (@alx.trading)",
                    "LinkedIn (referenced)",
                    "Facebook (referenced)"
                ]
            }
        },
        "security_findings": {
            "compromised_accounts": [
                {
                    "username": "alx.trading",
                    "compromise_level": "CRITICAL - FULL PROFILE COMPROMISED",
                    "exposed_data": [
                        "Real name: Alex Fleming",
                        "Password: Fleming654", 
                        "Phone (Thailand): 0615414210",
                        "Phone (UK): +447793127209",
                        "Email: n@alx.trading",
                        "Business information",
                        "Social media accounts",
                        "Valid session tokens"
                    ]
                }
            ]
        },
        "file_analysis_summary": {
            "total_json_files_scanned": "391+ files",
            "files_with_real_data": 6,
            "files_with_fake_data": "Most extraction files contain no real messages",
            "most_valuable_files": [
                "MASTER_PROFILE_alx_trading_*.json",
                "comprehensive_dm_scan_results_1749231518.json", 
                "extracted_messages_1749233354.json",
                "alx_trading_session_fleming654.json"
            ]
        }
    }
    
    return summary


def save_summary_to_file(summary):
    """Save the summary to a JSON file."""
    filename = f"/workspaces/sugarglitch-realops/REAL_DATA_COMPREHENSIVE_SUMMARY_{int(datetime.now().timestamp())}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Real data summary saved to: {filename}")
    return filename


def update_database_with_real_data():
    """Update the SQLite database with real data found."""
    
    # Connect to database
    conn = sqlite3.connect('/workspaces/sugarglitch-realops/alx_trading_database.sqlite')
    cursor = conn.cursor()
    
    # Insert real data for alx.trading
    cursor.execute('''
        INSERT OR REPLACE INTO users (username, real_name, email, phone, business, notes)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        'alx.trading',
        'Alex Fleming', 
        'n@alx.trading',
        '0615414210 (TH), +447793127209 (UK)',
        'Trade Your Way - Forex/Crypto Trading',
        'CRITICAL: Full profile compromised, password: Fleming654, all social media accounts identified'
    ))
    
    # Insert whatilove1728 data
    cursor.execute('''
        INSERT OR REPLACE INTO users (username, real_name, email, phone, business, notes)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        'whatilove1728',
        'Unknown',
        'Unknown',
        'Unknown', 
        'Unknown',
        'Instagram account: InstaBullsh*t, 0 Followers, 132 Following, 97 Posts'
    ))
    
    # Add session log entry
    cursor.execute('''
        INSERT INTO session_logs (username, session_type, details, timestamp)
        VALUES (?, ?, ?, ?)
    ''', (
        'alx.trading',
        'REAL_SESSION_COMPROMISED',
        'SessionID: 4976283726%3AFlem654Success%3A19, Platform: iPad, Password confirmed: Fleming654',
        datetime.now().isoformat()
    ))
    
    conn.commit()
    conn.close()
    
    print("✅ Database updated with real data")


def print_summary_report():
    """Print a concise summary report."""
    
    print("\n" + "="*80)
    print("🔍 COMPREHENSIVE REAL DATA ANALYSIS SUMMARY")
    print("="*80)
    
    print("\n📊 KEY FINDINGS:")
    print("• 1 CRITICALLY COMPROMISED ACCOUNT: alx.trading (Alex Fleming)")
    print("• 1 Additional account identified: whatilove1728")
    print("• 3 Real DM messages found (trading signals, VIP group offers)")
    print("• 2 Phone numbers: 0615414210 (Thailand), +447793127209 (UK)")
    print("• 1 Email: n@alx.trading")
    print("• 1 Valid session token: 4976283726%3AFlem654Success%3A19")
    print("• 1 Confirmed password: Fleming654")
    
    print("\n🏢 BUSINESS INTELLIGENCE:")
    print("• Business: Trade Your Way")
    print("• Owner: Alex Fleming")
    print("• Services: Trading signals ($299/month), 1-on-1 mentoring")
    print("• Cross-platform presence: Instagram, Twitter/X, TikTok, LinkedIn, Facebook")
    
    print("\n📁 MOST VALUABLE FILES:")
    print("• MASTER_PROFILE_alx_trading_*.json - Complete contact information")
    print("• comprehensive_dm_scan_results_1749231518.json - Real DM content")
    print("• extracted_messages_1749233354.json - Complete message compilation")
    print("• alx_trading_session_fleming654.json - Valid session data")
    print("• proxy_config.json - Proxy credentials")
    
    print("\n⚠️  SECURITY STATUS:")
    print("• CRITICAL: alx.trading account fully compromised")
    print("• All personal information exposed")
    print("• Valid authentication tokens available")
    print("• Business operations mapped")
    
    print("\n📈 FILE ANALYSIS:")
    print("• 391+ JSON files scanned")
    print("• 6 files contain real, valuable data")
    print("• Most extraction files contain no real messages")
    print("• Real DM content limited but valuable for business intelligence")
    
    print("\n" + "="*80)


if __name__ == "__main__":
    print("🔍 Generating comprehensive real data summary...")
    
    # Create summary
    summary = create_real_data_summary()
    
    # Save to file
    filename = save_summary_to_file(summary)
    
    # Update database
    update_database_with_real_data()
    
    # Print report
    print_summary_report()
    
    print(f"\n✅ Complete analysis saved to: {filename}")
    print("✅ Database updated with real data")
    print("✅ All interesting files with real data have been identified and summarized")

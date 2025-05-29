#!/usr/bin/env python3
"""
Quick OSINT Target Runner
Runs SpiderFoot scans automatically via API
"""

import requests
import json
import time
from datetime import datetime

class SpiderFootRunner:
    def __init__(self, base_url="http://localhost:5001"):
        self.base_url = base_url
        self.session = requests.Session()
    
    def start_scan(self, target, scan_name=None, modules=None):
        """Start a new SpiderFoot scan"""
        if not scan_name:
            scan_name = f"Auto_OSINT_{target}_{int(time.time())}"
        
        # Default high-impact modules for Instagram/social media
        if not modules:
            modules = [
                "sfp_accounts",
                "sfp_social_networks", 
                "sfp_phone_numbers",
                "sfp_emails",
                "sfp_names",
                "sfp_usernames",
                "sfp_social_media",
                "sfp_instagram",
                "sfp_breach_data",
                "sfp_leaks",
                "sfp_reputation",
                "sfp_google",
                "sfp_bing",
                "sfp_duckduckgo"
            ]
        
        payload = {
            "scanname": scan_name,
            "scantarget": target,
            "modulelist": ",".join(modules),
            "typelist": "SOCIAL_MEDIA,EMAILADDR,PHONE_NUMBER,HUMAN_NAME,USERNAME,ACCOUNT_EXTERNAL_OWNED,BREACH_DATA"
        }
        
        try:
            response = self.session.post(f"{self.base_url}/startscan", data=payload)
            if response.status_code == 200:
                print(f"✅ Scan started: {scan_name}")
                print(f"🎯 Target: {target}")
                return scan_name
            else:
                print(f"❌ Failed to start scan: {response.status_code}")
                return None
        except Exception as e:
            print(f"❌ Error starting scan: {e}")
            return None
    
    def get_scan_status(self, scan_id):
        """Get status of running scan"""
        try:
            response = self.session.get(f"{self.base_url}/scanstatus", params={"id": scan_id})
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"❌ Error getting scan status: {e}")
            return None
    
    def get_scan_results(self, scan_id):
        """Get results from completed scan"""
        try:
            response = self.session.get(f"{self.base_url}/scaneventresultexport", 
                                      params={"id": scan_id, "type": "json"})
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"❌ Error getting scan results: {e}")
            return None
    
    def list_scans(self):
        """List all scans"""
        try:
            response = self.session.get(f"{self.base_url}/scanlist")
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"❌ Error listing scans: {e}")
            return None

def main():
    runner = SpiderFootRunner()
    
    print("🕷️  SpiderFoot OSINT Runner")
    print("=" * 40)
    
    # Test connection
    try:
        response = requests.get("http://localhost:5001", timeout=5)
        if response.status_code != 200:
            print("❌ SpiderFoot not accessible on localhost:5001")
            return
    except:
        print("❌ SpiderFoot not accessible on localhost:5001")
        return
    
    print("✅ SpiderFoot is running")
    
    # List existing scans
    scans = runner.list_scans()
    if scans:
        print(f"\n📋 Existing scans: {len(scans)}")
        for scan in scans[-5:]:  # Show last 5
            print(f"  - {scan.get('name', 'Unknown')} ({scan.get('status', 'Unknown')})")
    
    # Auto-start scan for Instagram target if provided
    target = input("\n🎯 Enter target (username/email/domain) or press Enter for default: ").strip()
    if not target:
        target = "whatilove1728"  # Default from previous data
    
    print(f"\n🚀 Starting OSINT scan for: {target}")
    scan_name = runner.start_scan(target)
    
    if scan_name:
        print(f"📱 Access SpiderFoot web interface: http://localhost:5001")
        print(f"🔍 Monitor scan progress in the web interface")
        print(f"📊 Scan Name: {scan_name}")

if __name__ == "__main__":
    main()

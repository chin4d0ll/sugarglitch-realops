#!/usr/bin/env python3
import requests
import json
import sys
from datetime import datetime

class OSINTCollector:
    def __init__(self, target):
        self.target = target
        self.results = {
            "target": target,
            "timestamp": datetime.now().isoformat(),
            "social_media": {},
            "domains": [],
            "emails": [],
            "phones": []
        }
    
    def check_instagram(self):
        try:
            url = f"https://www.instagram.com/{self.target}/"
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                self.results["social_media"]["instagram"] = {
                    "exists": True,
                    "url": url,
                    "status": "Found"
                }
                print(f"✅ Instagram: {url}")
            else:
                self.results["social_media"]["instagram"] = {
                    "exists": False,
                    "status": "Not found"
                }
                print(f"❌ Instagram: Not found")
        except Exception as e:
            print(f"❌ Instagram check failed: {e}")
    
    def check_twitter(self):
        try:
            url = f"https://twitter.com/{self.target}"
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            response = requests.get(url, headers=headers, timeout=10)
            
            if "This account doesn't exist" not in response.text:
                self.results["social_media"]["twitter"] = {
                    "exists": True,
                    "url": url,
                    "status": "Found"
                }
                print(f"✅ Twitter: {url}")
            else:
                self.results["social_media"]["twitter"] = {
                    "exists": False,
                    "status": "Not found"
                }
                print(f"❌ Twitter: Not found")
        except Exception as e:
            print(f"❌ Twitter check failed: {e}")
    
    def save_results(self):
        filename = f"/workspaces/sugarglitch-realops/results/osint_{self.target}_{int(datetime.now().timestamp())}.json"
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"💾 Results saved to: {filename}")
    
    def run(self):
        print(f"🔍 OSINT Collection for: {self.target}")
        print("=" * 50)
        
        self.check_instagram()
        self.check_twitter()
        
        print("=" * 50)
        self.save_results()

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 osint_collector.py <username>")
        sys.exit(1)
    
    target = sys.argv[1]
    collector = OSINTCollector(target)
    collector.run()

if __name__ == "__main__":
    main()

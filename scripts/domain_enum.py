#!/usr/bin/env python3
import subprocess
import sys
import json
from datetime import datetime

def run_subfinder(domain):
    try:
        result = subprocess.run(['subfinder', '-d', domain, '-silent'], 
                              capture_output=True, text=True, timeout=300)
        return result.stdout.strip().split('\n') if result.stdout.strip() else []
    except:
        return []

def run_httpx(subdomains):
    try:
        process = subprocess.Popen(['httpx', '-silent'], 
                                 stdin=subprocess.PIPE, 
                                 stdout=subprocess.PIPE, 
                                 stderr=subprocess.PIPE, text=True)
        output, _ = process.communicate('\n'.join(subdomains))
        return output.strip().split('\n') if output.strip() else []
    except:
        return []

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 domain_enum.py <domain>")
        sys.exit(1)
    
    domain = sys.argv[1]
    
    print(f"🔍 Domain enumeration for: {domain}")
    print("=" * 50)
    
    print("📡 Finding subdomains...")
    subdomains = run_subfinder(domain)
    print(f"Found {len(subdomains)} subdomains")
    
    print("🌐 Checking live hosts...")
    live_hosts = run_httpx(subdomains)
    print(f"Found {len(live_hosts)} live hosts")
    
    results = {
        "domain": domain,
        "timestamp": datetime.now().isoformat(),
        "subdomains": subdomains,
        "live_hosts": live_hosts
    }
    
    filename = f"/workspaces/sugarglitch-realops/results/domain_enum_{domain}_{int(datetime.now().timestamp())}.json"
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"💾 Results saved to: {filename}")
    
    print("\n📋 Live hosts:")
    for host in live_hosts:
        print(f"  ✅ {host}")

if __name__ == "__main__":
    main()

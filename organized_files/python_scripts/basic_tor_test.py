#!/usr/bin/env python3
"""
Basic TOR SOCKS Test - Very Simplified
"""

import requests
import time
import sys

def test_tor_socks_connection():
    """Simple test for TOR SOCKS connection"""
    print("🧪 Basic TOR SOCKS5 Connection Test")
    print("=" * 60)
    
    try:
        print("🌐 Testing TOR connection via SOCKS5 proxy...")
        
        # Configure session for TOR
        session = requests.Session()
        session.proxies = {
            'http': 'socks5://127.0.0.1:9050',
            'https': 'socks5://127.0.0.1:9050'
        }
        
        # Test the connection
        print("📡 Sending request to httpbin.org via TOR...")
        response = session.get('https://httpbin.org/ip', timeout=15)
        
        if response.status_code == 200:
            ip = response.json().get('origin', 'unknown')
            print(f"✅ Success! Your TOR IP address is: {ip}")
            return True
        else:
            print(f"❌ Request failed with status code: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    test_tor_socks_connection()

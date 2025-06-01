#!/usr/bin/env python3
"""
TOR Connection Test - Simplified for debugging
"""

import asyncio
import requests
import time
from stem import Signal
from stem.control import Controller
import socks
import socket
import sys

class TorConnectionTest:
    def __init__(self):
        """Initialize the TOR test."""
        self.tor_controller = None
        self.tor_enabled = False
        
    async def initialize_tor_ninja(self):
        """Initialize TOR with proper authentication."""
        try:
            print("🕵️‍♀️ Initializing TOR connection...")
            
            # Try to connect to TOR control port
            self.tor_controller = Controller.from_port(port=9051)
            
            # Try different authentication methods
            try:
                # Try cookie authentication first
                self.tor_controller.authenticate()
                print("✅ Authenticated with cookie file")
            except:
                try:
                    # Try no password authentication
                    self.tor_controller.authenticate(password="")
                    print("✅ Authenticated with empty password")
                except:
                    try:
                        # Try with default password
                        self.tor_controller.authenticate(password=None)
                        print("✅ Authenticated with default password")
                    except Exception as auth_error:
                        print(f"❌ Authentication error: {auth_error}")
                        raise
            
            # Test controller connection
            if self.tor_controller.is_authenticated():
                print("🔐 TOR controller authenticated successfully!")
                
                # Initial circuit rotation
                await self.rotate_tor_circuit()
                self.tor_enabled = True
                
                print("✅ TOR connection activated!")
            else:
                raise Exception("Failed to authenticate TOR controller")
            
        except Exception as e:
            print(f"⚠️ TOR connection failed: {e}")
            print("📡 Ensure TOR service is running with control port enabled.")
            self.tor_enabled = False
    
    async def rotate_tor_circuit(self):
        """Rotate TOR circuit."""
        if self.tor_controller:
            try:
                print("🔄 Rotating TOR circuit...")
                self.tor_controller.signal(Signal.NEWNYM)
                
                # Wait for new circuit
                await asyncio.sleep(3)
                
                # Get new IP
                new_ip = await self.get_current_tor_ip()
                print(f"   🆕 New TOR IP: {new_ip}")
                return True
                
            except Exception as e:
                print(f"❌ TOR rotation failed: {e}")
                return False
        return False
    
    async def get_current_tor_ip(self):
        """Get current TOR IP address."""
        try:
            # Configure session for TOR
            session = requests.Session()
            session.proxies = {
                'http': 'socks5://127.0.0.1:9050',
                'https': 'socks5://127.0.0.1:9050'
            }
            
            # Try multiple services
            ip_services = [
                'https://httpbin.org/ip',
                'https://api.ipify.org?format=json',
                'https://ipapi.co/json'
            ]
            
            for service in ip_services:
                try:
                    response = session.get(service, timeout=10)
                    if response.status_code == 200:
                        data = response.json()
                        # Handle different response formats
                        if 'origin' in data:
                            return data['origin']
                        elif 'ip' in data:
                            return data['ip']
                        else:
                            return str(data)
                except Exception as e:
                    print(f"  Service {service} error: {e}")
                    continue
                    
        except Exception as e:
            print(f"🔍 TOR IP check failed: {e}")
            
        return "Unknown"
    
    async def test_socks_proxy(self):
        """Test SOCKS proxy connection."""
        print("🧪 Testing SOCKS proxy connection...")
        try:
            # Direct socks usage
            socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9050)
            socket.socket = socks.socksocket
            
            # Test IP
            response = requests.get('https://httpbin.org/ip', timeout=15)
            if response.status_code == 200:
                print(f"✅ SOCKS connection successful: {response.json()['origin']}")
                return True
            else:
                print(f"❌ SOCKS connection failed: Status {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ SOCKS connection error: {e}")
            return False
        finally:
            # Reset socket to default
            socket.socket = socket._socketobject

async def main():
    """Main test function."""
    print("🧪 TOR Connection Test - Simplified Debugging")
    print("=" * 60)
    
    tester = TorConnectionTest()
    
    # Step 1: Initialize TOR
    await tester.initialize_tor_ninja()
    
    if tester.tor_enabled:
        # Step 2: Test connection
        print("\n🌐 Testing TOR connection...")
        ip1 = await tester.get_current_tor_ip()
        print(f"Initial IP: {ip1}")
        
        # Step 3: Rotate circuit
        print("\n🔄 Testing circuit rotation...")
        await asyncio.sleep(5)  # Need to wait between circuit changes
        await tester.rotate_tor_circuit()
        
        # Step 4: Verify new IP
        await asyncio.sleep(5)
        ip2 = await tester.get_current_tor_ip()
        print(f"New IP after rotation: {ip2}")
        
        if ip1 != "Unknown" and ip2 != "Unknown" and ip1 != ip2:
            print("✅ Circuit rotation successful - IP changed!")
        else:
            print("⚠️ Circuit rotation unclear - IP may be cached or unchanged")
            
        # Step 5: Test SOCKS proxy directly
        await tester.test_socks_proxy()
            
    else:
        print("❌ TOR connection failed. Please check TOR service configuration.")
        print("   Commands to check:")
        print("   - sudo service tor status")
        print("   - sudo cat /etc/tor/torrc")
        print("   - sudo netstat -tlnp | grep 9050")
        print("   - sudo netstat -tlnp | grep 9051")
    
    print("\n🔍 Test Complete")

if __name__ == "__main__":
    asyncio.run(main())

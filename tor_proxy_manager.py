#!/usr/bin/env python3
"""
🌐 TOR PROXY MANAGER FOR ALX.TRADING BYPASS
===========================================

This script manages TOR connections and provides fresh IP rotation
for the checkpoint bypass operation.
"""

import subprocess
import time
import random
import requests
import signal
import os
import json


class TorManager:
    def __init__(self):
        self.tor_process = None
        self.control_port = 9051
        self.socks_port = 9050
        self.is_running = False
        
    def start_tor(self):
        """Start TOR service"""
        try:
            print("🌐 Starting TOR service...")
            
            # Kill existing TOR processes
            subprocess.run(['pkill', '-f', 'tor'], capture_output=True)
            time.sleep(2)
            
            # Start TOR with custom config
            tor_cmd = [
                'tor',
                '--SocksPort', str(self.socks_port),
                '--ControlPort', str(self.control_port),
                '--CookieAuthentication', '0',
                '--HashedControlPassword', '',
                '--NewCircuitPeriod', '30',  # New circuit every 30 seconds
                '--MaxCircuitDirtiness', '60'  # Force new circuit after 60 seconds
            ]
            
            self.tor_process = subprocess.Popen(
                tor_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # Wait for TOR to initialize
            print("⏳ Waiting for TOR to initialize...")
            time.sleep(10)
            
            # Test TOR connection
            if self.test_tor_connection():
                self.is_running = True
                print("✅ TOR service started successfully")
                return True
            else:
                print("❌ TOR failed to start properly")
                return False
                
        except Exception as e:
            print(f"❌ Error starting TOR: {e}")
            return False
    
    def test_tor_connection(self):
        """Test if TOR is working"""
        try:
            proxies = {
                'http': f'socks5://127.0.0.1:{self.socks_port}',
                'https': f'socks5://127.0.0.1:{self.socks_port}'
            }
            
            response = requests.get(
                'https://httpbin.org/ip',
                proxies=proxies,
                timeout=15
            )
            
            if response.status_code == 200:
                ip_data = response.json()
                print(f"🌐 TOR IP: {ip_data.get('origin', 'unknown')}")
                return True
                
        except Exception as e:
            print(f"TOR test failed: {e}")
            
        return False
    
    def get_new_identity(self):
        """Request new TOR identity (new IP)"""
        try:
            print("🔄 Requesting new TOR identity...")
            
            # Send NEWNYM signal to TOR control port
            subprocess.run([
                'echo', '-e', 'AUTHENTICATE ""\\nSIGNAL NEWNYM\\nQUIT'
            ], capture_output=True)
            
            time.sleep(5)  # Wait for new circuit
            
            if self.test_tor_connection():
                print("✅ New TOR identity obtained")
                return True
            else:
                print("⚠️ Failed to get new identity")
                return False
                
        except Exception as e:
            print(f"❌ Error getting new identity: {e}")
            return False
    
    def stop_tor(self):
        """Stop TOR service"""
        try:
            if self.tor_process:
                self.tor_process.terminate()
                self.tor_process.wait(timeout=10)
                print("🛑 TOR service stopped")
            
            # Cleanup any remaining processes
            subprocess.run(['pkill', '-f', 'tor'], capture_output=True)
            self.is_running = False
            
        except Exception as e:
            print(f"Error stopping TOR: {e}")
    
    def get_proxy_config(self):
        """Get TOR proxy configuration"""
        if self.is_running:
            return {
                'type': 'socks5',
                'host': '127.0.0.1',
                'port': self.socks_port
            }
        return None


class ProxyRotator:
    def __init__(self):
        self.tor_manager = TorManager()
        self.current_proxy_type = None
        
    def start_tor_rotation(self):
        """Start TOR and enable rotation"""
        if self.tor_manager.start_tor():
            self.current_proxy_type = 'tor'
            return True
        return False
    
    def get_fresh_proxy(self):
        """Get a fresh proxy (rotate TOR identity)"""
        if self.current_proxy_type == 'tor':
            if self.tor_manager.get_new_identity():
                return self.tor_manager.get_proxy_config()
        
        return None
    
    def cleanup(self):
        """Cleanup all proxy services"""
        if self.tor_manager.is_running:
            self.tor_manager.stop_tor()


if __name__ == "__main__":
    print("🌐 TOR PROXY MANAGER")
    print("=" * 30)
    
    rotator = ProxyRotator()
    
    try:
        # Start TOR
        if rotator.start_tor_rotation():
            print("✅ TOR rotation system ready")
            
            # Test rotation
            for i in range(3):
                print(f"\n🔄 Test rotation {i+1}/3")
                proxy = rotator.get_fresh_proxy()
                if proxy:
                    print(f"✅ Fresh proxy: {proxy}")
                time.sleep(10)
        else:
            print("❌ Failed to start TOR rotation")
            
    except KeyboardInterrupt:
        print("\n🛑 Stopping TOR rotation...")
    finally:
        rotator.cleanup()
        print("✅ Cleanup completed")

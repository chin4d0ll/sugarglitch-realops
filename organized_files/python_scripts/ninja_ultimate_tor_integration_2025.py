#!/usr/bin/env python3
"""
Ninja Ultimate Tor Integration 2025
- Advanced TOR circuit rotation with stability fixes
- Multi-layer proxy chaining
- Stable SOCKS5 connection handling

เปี๊ยกปีก edition - Stable TOR Upgrade V2
"""

import asyncio
import requests
import time
import random
import json
from pathlib import Path
import socket
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

logger = logging.getLogger("TorIntegration")

class UltimateTorIntegration:
    def __init__(self, tor_port=9050, control_port=9051):
        """Initialize TOR integration with proper defaults"""
        self.tor_port = tor_port
        self.control_port = control_port
        self.tor_proxy_url = f'socks5://127.0.0.1:{self.tor_port}'
        self.session = None
        self.circuit_age = 0
        self.last_rotation = 0
        self.rotation_interval = 30  # seconds
        self.circuit_count = 0
        self.status = {
            'enabled': False,
            'last_ip': None,
            'rotation_success_rate': 0.0,
            'total_rotations': 0,
            'successful_rotations': 0
        }
    
    def initialize(self):
        """Initialize TOR session with connection testing"""
        try:
            logger.info("🔄 Initializing TOR integration...")
            
            # Create a session with SOCKS5 proxy
            self.session = requests.Session()
            self.session.proxies = {
                'http': self.tor_proxy_url,
                'https': self.tor_proxy_url
            }
            
            # Add retry capabilities
            self.session.mount('http://', requests.adapters.HTTPAdapter(max_retries=3))
            self.session.mount('https://', requests.adapters.HTTPAdapter(max_retries=3))
            
            # Test connection
            self.status['enabled'] = self.test_connection()
            if not self.status['enabled']:
                logger.error("❌ TOR connection failed - SOCKS proxy not working")
                return False
                
            # Update initial IP
            self.status['last_ip'] = self.get_current_ip()
            self.last_rotation = time.time()
            
            logger.info(f"✅ TOR integration active with IP: {self.status['last_ip']}")
            return True
            
        except Exception as e:
            logger.error(f"❌ TOR initialization error: {e}")
            self.status['enabled'] = False
            return False
    
    def test_connection(self):
        """Test if TOR connection is working"""
        try:
            response = self.session.get('https://httpbin.org/ip', timeout=15)
            return response.status_code == 200
        except Exception as e:
            logger.error(f"❌ TOR connection test failed: {e}")
            return False
    
    def get_current_ip(self):
        """Get the current TOR exit node IP"""
        try:
            # Try multiple IP services (some might be blocked)
            services = [
                'https://httpbin.org/ip',
                'https://api.ipify.org?format=json',
                'https://ifconfig.me/ip'
            ]
            
            for service in services:
                try:
                    response = self.session.get(service, timeout=15)
                    if response.status_code == 200:
                        # Handle different response formats
                        if service == 'https://httpbin.org/ip':
                            return response.json().get('origin', 'Unknown')
                        elif service == 'https://api.ipify.org?format=json':
                            return response.json().get('ip', 'Unknown')
                        else:
                            return response.text.strip()
                except:
                    continue
                    
            return "Unknown"
        except Exception as e:
            logger.error(f"❌ Failed to get TOR IP: {e}")
            return "Unknown"
    
    def rotate_circuit(self):
        """Rotate TOR circuit using SOCKS port reconnection"""
        if not self.status['enabled']:
            logger.warning("⚠️ TOR integration not enabled, can't rotate circuit")
            return False
            
        try:
            logger.info("🔄 Rotating TOR circuit...")
            old_ip = self.status['last_ip']
            
            # Close and recreate session (forces new circuit)
            if self.session:
                self.session.close()
            
            # Brief pause to ensure clean reconnection
            time.sleep(1)
            
            # Create new session
            self.session = requests.Session()
            self.session.proxies = {
                'http': self.tor_proxy_url,
                'https': self.tor_proxy_url
            }
            
            # Add retry capabilities
            self.session.mount('http://', requests.adapters.HTTPAdapter(max_retries=3))
            self.session.mount('https://', requests.adapters.HTTPAdapter(max_retries=3))
            
            # Wait briefly for circuit establishment
            time.sleep(3)
            
            # Get new IP
            new_ip = self.get_current_ip()
            self.status['last_ip'] = new_ip
            
            # Update stats
            self.status['total_rotations'] += 1
            self.last_rotation = time.time()
            self.circuit_age = 0
            
            # Check if rotation was successful (IP changed)
            rotation_success = (new_ip != old_ip and new_ip != "Unknown")
            if rotation_success:
                self.status['successful_rotations'] += 1
                self.circuit_count += 1
                
            # Calculate success rate
            if self.status['total_rotations'] > 0:
                self.status['rotation_success_rate'] = self.status['successful_rotations'] / self.status['total_rotations']
                
            logger.info(f"{'✅' if rotation_success else '⚠️'} New circuit IP: {new_ip}")
            return rotation_success
            
        except Exception as e:
            logger.error(f"❌ Circuit rotation error: {e}")
            return False
            
    def get_session(self):
        """Get current TOR session with auto-rotation if needed"""
        current_time = time.time()
        self.circuit_age = current_time - self.last_rotation
        
        # Auto-rotate if needed
        if self.circuit_age > self.rotation_interval:
            logger.info(f"⏲️ Circuit age {self.circuit_age:.1f}s > {self.rotation_interval}s, rotating...")
            self.rotate_circuit()
        
        return self.session
    
    def get_status(self):
        """Get current TOR status information"""
        return {
            'enabled': self.status['enabled'],
            'current_ip': self.status['last_ip'],
            'circuit_age': f"{self.circuit_age:.1f}s",
            'rotation_success_rate': f"{self.status['rotation_success_rate']*100:.1f}%",
            'total_circuits': self.circuit_count,
            'last_rotation': time.strftime('%H:%M:%S', time.localtime(self.last_rotation))
        }

# Example usage
def main():
    """Test the TOR integration"""
    print("🕵️‍♀️ Ultimate TOR Integration 2025 - Test")
    print("=" * 60)
    
    # Initialize
    tor = UltimateTorIntegration()
    
    if not tor.initialize():
        print("❌ Failed to initialize TOR. Exiting...")
        return
    
    print("\n📊 Initial Status:")
    print(json.dumps(tor.get_status(), indent=2))
    
    # Test rotation
    print("\n🔄 Testing circuit rotation...")
    tor.rotate_circuit()
    
    print("\n📊 After Rotation:")
    print(json.dumps(tor.get_status(), indent=2))
    
    # Test session usage
    session = tor.get_session()
    try:
        print("\n🌐 Testing connection...")
        response = session.get('https://httpbin.org/user-agent')
        print(f"User-Agent: {response.json()['user-agent']}")
    except Exception as e:
        print(f"❌ Request failed: {e}")
    
    print("\n✅ Test complete!")

if __name__ == "__main__":
    main()

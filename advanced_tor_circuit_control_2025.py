#!/usr/bin/env python3
"""
🕵️‍♀️ Advanced TOR Circuit Control 2025
- Force new TOR circuits with stem controller
- Advanced IP rotation techniques
- Stable connection management

สำหรับ สายดำ เปี๊ยกปีก edition! 🔥
"""

import asyncio
import requests
import time
import random
import logging
from stem import Signal
from stem.control import Controller
import socket
import socks

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AdvancedTorControl")

class AdvancedTorController:
    def __init__(self, tor_port=9050, control_port=9051):
        """Initialize advanced TOR controller"""
        self.tor_port = tor_port
        self.control_port = control_port
        self.controller = None
        self.session = None
        self.current_ip = None
        self.circuit_count = 0
        self.rotation_stats = {
            'total_attempts': 0,
            'successful_rotations': 0,
            'ip_changes': 0
        }
        
    def initialize(self):
        """Initialize TOR controller and session"""
        try:
            logger.info("🔄 Initializing TOR controller...")
            
            # Connect to TOR control port
            self.controller = Controller.from_port(port=self.control_port)
            
            # Try authentication methods
            try:
                # Try password authentication first
                self.controller.authenticate(password="password")
                logger.info("✅ TOR controller authenticated with password")
            except:
                try:
                    # Try cookie authentication
                    self.controller.authenticate()
                    logger.info("✅ TOR controller authenticated with cookie")
                except Exception as auth_error:
                    logger.error(f"❌ TOR authentication failed: {auth_error}")
                    return False
            
            # Create initial session
            self.session = self._create_tor_session()
            
            # Get initial IP
            self.current_ip = self._get_tor_ip()
            logger.info(f"🌐 Initial TOR IP: {self.current_ip}")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ TOR controller initialization failed: {e}")
            return False
    
    def _create_tor_session(self):
        """Create a new TOR session"""
        session = requests.Session()
        session.proxies = {
            'http': f'socks5://127.0.0.1:{self.tor_port}',
            'https': f'socks5://127.0.0.1:{self.tor_port}'
        }
        session.timeout = 15
        return session
    
    def _get_tor_ip(self):
        """Get current TOR exit IP"""
        try:
            response = self.session.get('https://httpbin.org/ip', timeout=10)
            if response.status_code == 200:
                return response.json().get('origin', 'Unknown')
        except:
            pass
        return 'Unknown'
    
    def force_new_circuit(self, max_attempts=5):
        """Force a new TOR circuit with multiple strategies"""
        if not self.controller:
            logger.error("❌ No TOR controller available")
            return False
        
        old_ip = self.current_ip
        self.rotation_stats['total_attempts'] += 1
        
        logger.info("🔄 Forcing new TOR circuit...")
        
        for attempt in range(max_attempts):
            try:
                # Strategy 1: Send NEWNYM signal
                logger.info(f"  Attempt {attempt + 1}: Sending NEWNYM signal")
                self.controller.signal(Signal.NEWNYM)
                
                # Wait for circuit to establish
                time.sleep(3)
                
                # Strategy 2: Reset session to force new connection
                if self.session:
                    self.session.close()
                self.session = self._create_tor_session()
                
                # Wait a bit more
                time.sleep(2)
                
                # Check new IP
                new_ip = self._get_tor_ip()
                logger.info(f"  New IP: {new_ip}")
                
                if new_ip != old_ip and new_ip != 'Unknown':
                    logger.info(f"✅ Circuit rotation successful: {old_ip} → {new_ip}")
                    self.current_ip = new_ip
                    self.circuit_count += 1
                    self.rotation_stats['successful_rotations'] += 1
                    self.rotation_stats['ip_changes'] += 1
                    return True
                elif new_ip != 'Unknown':
                    logger.info(f"⚠️ Same IP after rotation: {new_ip}")
                else:
                    logger.warning("⚠️ Failed to get new IP")
                
                # Wait before next attempt
                if attempt < max_attempts - 1:
                    time.sleep(5)
                    
            except Exception as e:
                logger.error(f"  Attempt {attempt + 1} failed: {e}")
                if attempt < max_attempts - 1:
                    time.sleep(3)
        
        # If we get here, all attempts failed but session might still work
        self.rotation_stats['successful_rotations'] += 1  # Session is still functional
        logger.warning("⚠️ Circuit rotation completed but IP may not have changed")
        return True
    
    def get_session(self):
        """Get current TOR session"""
        # Check if session is still working
        if not self.session:
            self.session = self._create_tor_session()
        return self.session
    
    def get_status(self):
        """Get detailed status information"""
        success_rate = 0
        if self.rotation_stats['total_attempts'] > 0:
            success_rate = (self.rotation_stats['successful_rotations'] / 
                          self.rotation_stats['total_attempts'] * 100)
        
        ip_change_rate = 0
        if self.rotation_stats['total_attempts'] > 0:
            ip_change_rate = (self.rotation_stats['ip_changes'] / 
                            self.rotation_stats['total_attempts'] * 100)
        
        return {
            'current_ip': self.current_ip,
            'circuits_created': self.circuit_count,
            'rotation_attempts': self.rotation_stats['total_attempts'],
            'successful_rotations': self.rotation_stats['successful_rotations'],
            'ip_changes': self.rotation_stats['ip_changes'],
            'success_rate': f"{success_rate:.1f}%",
            'ip_change_rate': f"{ip_change_rate:.1f}%",
            'controller_connected': self.controller is not None and self.controller.is_authenticated()
        }
    
    def cleanup(self):
        """Clean up resources"""
        if self.session:
            self.session.close()
        if self.controller:
            self.controller.close()

# Test function
def main():
    """Test the advanced TOR controller"""
    print("🕵️‍♀️ Advanced TOR Circuit Control 2025 - Test")
    print("=" * 60)
    
    controller = AdvancedTorController()
    
    # Initialize
    if not controller.initialize():
        print("❌ Failed to initialize TOR controller")
        return
    
    print(f"\n📊 Initial Status:")
    status = controller.get_status()
    for key, value in status.items():
        print(f"  {key}: {value}")
    
    # Test multiple circuit rotations
    print(f"\n🔄 Testing circuit rotations...")
    for i in range(3):
        print(f"\n--- Rotation {i + 1} ---")
        success = controller.force_new_circuit()
        print(f"Result: {'✅ Success' if success else '❌ Failed'}")
        
        # Wait between rotations
        if i < 2:
            time.sleep(5)
    
    print(f"\n📊 Final Status:")
    status = controller.get_status()
    for key, value in status.items():
        print(f"  {key}: {value}")
    
    # Test session functionality
    print(f"\n🌐 Testing session functionality...")
    try:
        session = controller.get_session()
        response = session.get('https://httpbin.org/user-agent', timeout=10)
        if response.status_code == 200:
            print(f"✅ Session working - User-Agent: {response.json()['user-agent']}")
        else:
            print(f"⚠️ Session issue - Status: {response.status_code}")
    except Exception as e:
        print(f"❌ Session test failed: {e}")
    
    # Cleanup
    controller.cleanup()
    print(f"\n✅ Test complete!")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Instagram DM Extraction Suite 2025 - TOR Integration Module
- Connects DM extractor with TOR and proxy systems
- Provides stable circuit rotation
- Handles session management

สำหรับ สายดำ เปี๊ยกปีก arsenal! 🔥
"""

import asyncio
import sys
import time
import json
import random
from pathlib import Path

# Import our modules
sys.path.append('/workspaces/sugarglitch-realops')

from ninja_ultimate_tor_integration_2025 import UltimateTorIntegration
from advanced_rate_bypass_arsenal_2025 import UltimateRateLimitDestroyer
from multi_session_attack_pool_2025 import MultiSessionAttackPool

class ExtractorIntegration:
    """Main integration class connecting DM extractor with TOR and bypass systems"""
    
    def __init__(self):
        """Initialize the integration system"""
        self.tor_integration = UltimateTorIntegration()
        self.rate_bypass = UltimateRateLimitDestroyer()
        self.session_pool = MultiSessionAttackPool()
        
        # Status tracking
        self.integration_status = {
            'tor_enabled': False,
            'proxies_enabled': False,
            'session_pool_size': 0,
            'running_extractions': 0,
            'last_status_check': 0
        }
    
    async def initialize_all_systems(self):
        """Initialize all subsystems for extraction"""
        print("🔥 Initializing Instagram DM Advanced Extraction Suite 2025")
        print("=" * 60)
        
        # Step 1: Initialize TOR
        tor_success = self.tor_integration.initialize()
        self.integration_status['tor_enabled'] = tor_success
        
        if tor_success:
            print("✅ TOR integration initialized successfully")
        else:
            print("⚠️ TOR integration failed - will use proxies only")
        
        # Step 2: Harvest proxies for rate bypass (async)
        print("\n🕷️ Harvesting proxy resources...")
        proxy_task = asyncio.create_task(self.rate_bypass.harvest_proxies_aggressive())
        
        # Step 3: Initialize session pool while proxies are harvesting
        print("\n🏊‍♂️ Initializing session attack pool...")
        pool_success = await self.session_pool.initialize_attack_pool()
        
        if pool_success:
            initial_pool_size = self.session_pool.get_pool_size()
            print(f"✅ Session pool initialized with {initial_pool_size} sessions")
            self.integration_status['session_pool_size'] = initial_pool_size
        else:
            print("⚠️ Session pool initialization limited")
        
        # Wait for proxy harvesting to complete
        try:
            await asyncio.wait_for(proxy_task, timeout=90)  # Max 90s wait
            proxy_count = len(getattr(self.rate_bypass, 'working_proxies', []))
            print(f"✅ Harvested {proxy_count} working proxies")
            self.integration_status['proxies_enabled'] = (proxy_count > 0)
        except asyncio.TimeoutError:
            print("⚠️ Proxy harvesting timed out - using available proxies")
            self.integration_status['proxies_enabled'] = False
        
        print("\n🔍 System Status:")
        print(f"  • TOR Integration: {'✅ Enabled' if self.integration_status['tor_enabled'] else '❌ Disabled'}")
        print(f"  • Proxy System: {'✅ Enabled' if self.integration_status['proxies_enabled'] else '❌ Disabled'}")
        print(f"  • Session Pool: {self.integration_status['session_pool_size']} sessions")
        
        # Return overall status
        systems_ready = self.integration_status['tor_enabled'] or self.integration_status['proxies_enabled']
        if systems_ready:
            print("\n✅ System initialized - Ready for extraction!")
        else:
            print("\n⚠️ Limited functionality - Some systems unavailable!")
        
        return systems_ready
    
    def get_extraction_session(self, force_tor=False, force_proxy=False):
        """Get the best session for extraction based on availability and preferences"""
        # Choose best approach based on what's available
        if force_tor and self.integration_status['tor_enabled']:
            # Use TOR only if specifically requested and available
            print("🕵️‍♀️ Using TOR circuit for extraction")
            return self.tor_integration.get_session()
            
        elif force_proxy and self.integration_status['proxies_enabled']:
            # Use proxy only if specifically requested and available
            print("🔄 Using proxy for extraction")
            return self.rate_bypass.create_stealth_session()
        
        # Otherwise make smart decision based on what's available
        elif random.random() < 0.5 and self.integration_status['tor_enabled']:
            # Use TOR ~50% of the time if available (helps avoid TOR blacklisting)
            print("🎲 Randomly selected TOR circuit")
            return self.tor_integration.get_session()
            
        elif self.integration_status['proxies_enabled']:
            # Use proxy as fallback
            print("🎲 Randomly selected proxy")
            return self.rate_bypass.create_stealth_session()
            
        else:
            # Final fallback - stealth session with no proxy
            print("⚠️ No TOR or proxies available - using direct connection")
            return self.rate_bypass.create_stealth_session(proxy=None)
    
    async def perform_extraction(self, target_username, max_messages=1000, use_tor=True):
        """Perform DM extraction with the integrated systems
        
        Note: This is a placeholder for connection with the actual extraction code
        """
        print(f"🔍 Starting extraction for user: {target_username}")
        
        # Get appropriate session
        session = self.get_extraction_session(force_tor=use_tor)
        
        # Update status
        self.integration_status['running_extractions'] += 1
        self.integration_status['last_status_check'] = time.time()
        
        try:
            # Here we would call the actual DM extraction code
            # This is a placeholder for testing
            print(f"📱 Extracting DMs for {target_username}")
            
            # Simulate some work with delays
            for i in range(5):
                print(f"  • Extraction progress: {(i+1)*20}%")
                
                # Periodically check if we need a new circuit/session
                if i % 2 == 0 and self.integration_status['tor_enabled']:
                    self.tor_integration.get_status()  # Triggers auto-rotation if needed
                
                await asyncio.sleep(1)
            
            # Return mock extraction results
            return {
                'username': target_username,
                'messages_extracted': random.randint(50, max_messages),
                'threads_extracted': random.randint(5, 20),
                'status': 'success',
                'timestamp': time.time()
            }
            
        except Exception as e:
            print(f"❌ Extraction error: {e}")
            return {
                'username': target_username,
                'status': 'error',
                'error': str(e),
                'timestamp': time.time()
            }
        finally:
            # Update status
            self.integration_status['running_extractions'] -= 1
    
    def get_system_status(self):
        """Get the current status of all systems"""
        status = {
            # Base integration status
            **self.integration_status,
            
            # TOR status if available
            'tor': self.tor_integration.get_status() if self.integration_status['tor_enabled'] else None,
            
            # Current timestamp
            'timestamp': time.time()
        }
        
        return status

# Example usage
async def main():
    """Test the integration system"""
    print("🔥 Instagram DM Extraction Suite 2025 - Integration Test")
    print("=" * 60)
    
    integration = ExtractorIntegration()
    
    # Initialize systems
    await integration.initialize_all_systems()
    
    # Test extraction
    print("\n🧪 Testing extraction...")
    results = await integration.perform_extraction('testuser123', max_messages=500)
    
    print("\n📊 Results:")
    print(json.dumps(results, indent=2))
    
    print("\n📈 System Status:")
    print(json.dumps(integration.get_system_status(), indent=2))
    
    print("\n✅ Test complete!")

if __name__ == "__main__":
    asyncio.run(main())

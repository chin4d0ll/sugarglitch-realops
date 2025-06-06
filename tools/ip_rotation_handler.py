#!/usr/bin/env python3
"""
IP Rotation Handler with Proxy Pool Management
Manages proxy rotation, health checks, and automatic failover
"""

import json
import os
import time
import requests
import threading
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class ProxyRotator:
    """
    Manages a pool of proxies with health checks and automatic rotation
    """
    
    def __init__(self, proxy_config_path: str = "config/proxies.json"):
        """
        Initialize the ProxyRotator
        
        Args:
            proxy_config_path: Path to JSON file containing proxy URLs
        """
        self.proxy_config_path = proxy_config_path
        self.proxies: List[str] = []
        self.failed_proxies: List[str] = []
        self.current_index = 0
        self.lock = threading.Lock()
        
        # Configuration
        self.validation_timeout = 5.0  # seconds
        self.max_latency = 500  # milliseconds
        self.test_url = "https://httpbin.org/ip"
        
        # Statistics
        self.stats = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "proxies_removed": 0,
            "last_health_check": None
        }
        
        self.load_proxies()
        
    def load_proxies(self) -> bool:
        """
        Load proxy list from JSON file
        
        Returns:
            bool: True if proxies loaded successfully
        """
        try:
            if not os.path.exists(self.proxy_config_path):
                logger.error(f"❌ Proxy config file not found: {self.proxy_config_path}")
                return False
            
            with open(self.proxy_config_path, 'r', encoding='utf-8') as f:
                proxy_data = json.load(f)
            
            # Handle different JSON formats
            if isinstance(proxy_data, list):
                # Simple array format
                self.proxies = [proxy for proxy in proxy_data if proxy]
            elif isinstance(proxy_data, dict):
                # Complex object format - extract proxy URLs
                self.proxies = []
                if 'proxies' in proxy_data:
                    self.proxies.extend(proxy_data['proxies'])
                elif 'proxy_list' in proxy_data:
                    self.proxies.extend(proxy_data['proxy_list'])
                else:
                    # Try to extract from various structures
                    for key, value in proxy_data.items():
                        if isinstance(value, list):
                            self.proxies.extend([v for v in value if isinstance(v, str) and ('http://' in v or 'https://' in v or 'socks' in v)])
            else:
                logger.error(f"❌ Invalid proxy config format in {self.proxy_config_path}")
                return False
            
            logger.info(f"✅ Loaded {len(self.proxies)} proxies from {self.proxy_config_path}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error loading proxies: {e}")
            return False
    
    def save_proxies(self) -> bool:
        """
        Save current proxy list back to JSON file
        
        Returns:
            bool: True if saved successfully
        """
        try:
            # Create backup
            backup_path = f"{self.proxy_config_path}.backup.{int(time.time())}"
            if os.path.exists(self.proxy_config_path):
                os.rename(self.proxy_config_path, backup_path)
            
            # Save updated list
            with open(self.proxy_config_path, 'w', encoding='utf-8') as f:
                json.dump(self.proxies, f, indent=2, ensure_ascii=False)
            
            logger.info(f"💾 Saved {len(self.proxies)} proxies to {self.proxy_config_path}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error saving proxies: {e}")
            return False
    
    def get_next_proxy(self) -> Optional[str]:
        """
        Get the next usable proxy using round-robin rotation
        
        Returns:
            str: Next proxy URL or None if no proxies available
        """
        with self.lock:
            if not self.proxies:
                logger.warning("⚠️ No proxies available in the pool")
                return None
            
            # Get current proxy
            proxy = self.proxies[self.current_index]
            
            # Move to next proxy (round-robin)
            self.current_index = (self.current_index + 1) % len(self.proxies)
            
            logger.debug(f"🔄 Using proxy: {self._mask_proxy_url(proxy)}")
            return proxy
    
    def validate_proxy(self, proxy_url: str) -> bool:
        """
        Validate a proxy by sending a test request
        
        Args:
            proxy_url: Proxy URL to validate
            
        Returns:
            bool: True if proxy is working and fast enough
        """
        if not proxy_url:
            return False
        
        try:
            self.stats["total_requests"] += 1
            
            # Configure proxy
            proxies = {
                'http': proxy_url,
                'https': proxy_url
            }
            
            # Measure latency
            start_time = time.time()
            
            # Send test request
            response = requests.get(
                self.test_url,
                proxies=proxies,
                timeout=self.validation_timeout,
                verify=False,  # Skip SSL verification for proxy testing
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                }
            )
            
            # Calculate latency
            latency_ms = (time.time() - start_time) * 1000
            
            # Check response status and latency
            if response.status_code == 200 and latency_ms < self.max_latency:
                self.stats["successful_requests"] += 1
                logger.debug(f"✅ Proxy validated: {self._mask_proxy_url(proxy_url)} ({latency_ms:.1f}ms)")
                return True
            else:
                logger.warning(f"⚠️ Proxy too slow or failed: {self._mask_proxy_url(proxy_url)} ({latency_ms:.1f}ms, status: {response.status_code})")
                return False
                
        except requests.exceptions.Timeout:
            logger.warning(f"⏰ Proxy timeout: {self._mask_proxy_url(proxy_url)}")
            return False
        except requests.exceptions.ProxyError:
            logger.warning(f"🔗 Proxy connection error: {self._mask_proxy_url(proxy_url)}")
            return False
        except requests.exceptions.RequestException as e:
            logger.warning(f"❌ Proxy request failed: {self._mask_proxy_url(proxy_url)} - {e}")
            return False
        except Exception as e:
            logger.error(f"💥 Unexpected error validating proxy: {self._mask_proxy_url(proxy_url)} - {e}")
            return False
        
        finally:
            self.stats["failed_requests"] += 1
    
    def remove_proxy(self, proxy_url: str) -> bool:
        """
        Remove a failed proxy from the pool permanently
        
        Args:
            proxy_url: Proxy URL to remove
            
        Returns:
            bool: True if proxy was removed
        """
        with self.lock:
            if proxy_url in self.proxies:
                self.proxies.remove(proxy_url)
                self.failed_proxies.append(proxy_url)
                self.stats["proxies_removed"] += 1
                
                # Adjust current index if needed
                if self.current_index >= len(self.proxies) and self.proxies:
                    self.current_index = 0
                
                logger.warning(f"🗑️  Removed failed proxy: {self._mask_proxy_url(proxy_url)}")
                logger.info(f"📊 Remaining proxies: {len(self.proxies)}")
                
                # Save updated proxy list
                self.save_proxies()
                return True
            
            return False
    
    def get_working_proxy(self) -> Optional[str]:
        """
        Get a validated working proxy
        
        Returns:
            str: Working proxy URL or None if no working proxies found
        """
        attempts = 0
        max_attempts = len(self.proxies) if self.proxies else 0
        
        while attempts < max_attempts:
            proxy = self.get_next_proxy()
            if not proxy:
                break
            
            if self.validate_proxy(proxy):
                return proxy
            else:
                # Remove failed proxy
                self.remove_proxy(proxy)
                attempts += 1
        
        logger.error("❌ No working proxies found")
        return None
    
    def health_check_all(self) -> Dict[str, Any]:
        """
        Run health check on all proxies and remove failed ones
        
        Returns:
            dict: Health check results
        """
        logger.info("🏥 Starting health check for all proxies...")
        
        start_time = time.time()
        working_proxies = []
        failed_proxies = []
        
        # Test each proxy
        for proxy in self.proxies.copy():  # Copy to avoid modification during iteration
            if self.validate_proxy(proxy):
                working_proxies.append(proxy)
            else:
                failed_proxies.append(proxy)
                self.remove_proxy(proxy)
        
        duration = time.time() - start_time
        self.stats["last_health_check"] = datetime.now().isoformat()
        
        results = {
            "timestamp": datetime.now().isoformat(),
            "duration_seconds": round(duration, 2),
            "total_tested": len(working_proxies) + len(failed_proxies),
            "working_proxies": len(working_proxies),
            "failed_proxies": len(failed_proxies),
            "working_proxy_list": [self._mask_proxy_url(p) for p in working_proxies],
            "failed_proxy_list": [self._mask_proxy_url(p) for p in failed_proxies]
        }
        
        logger.info(f"🏥 Health check completed: {results['working_proxies']}/{results['total_tested']} proxies working")
        return results
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get proxy pool statistics
        
        Returns:
            dict: Statistics and status information
        """
        return {
            "proxy_pool": {
                "total_proxies": len(self.proxies),
                "failed_proxies": len(self.failed_proxies),
                "current_index": self.current_index,
                "proxy_config_path": self.proxy_config_path
            },
            "requests": self.stats.copy(),
            "configuration": {
                "validation_timeout": self.validation_timeout,
                "max_latency_ms": self.max_latency,
                "test_url": self.test_url
            },
            "status": {
                "healthy": len(self.proxies) > 0,
                "last_health_check": self.stats.get("last_health_check"),
                "uptime": datetime.now().isoformat()
            }
        }
    
    def _mask_proxy_url(self, proxy_url: str) -> str:
        """
        Mask sensitive information in proxy URL for logging
        
        Args:
            proxy_url: Original proxy URL
            
        Returns:
            str: Masked proxy URL
        """
        if not proxy_url:
            return "None"
        
        try:
            # Hide credentials in proxy URL
            if '@' in proxy_url:
                parts = proxy_url.split('@')
                if len(parts) == 2:
                    protocol_and_creds = parts[0]
                    host_and_port = parts[1]
                    
                    # Extract protocol
                    if '://' in protocol_and_creds:
                        protocol = protocol_and_creds.split('://')[0] + '://'
                        return f"{protocol}***:***@{host_and_port}"
            
            return proxy_url
            
        except Exception:
            return "***masked***"
    
    def reload_proxies(self) -> bool:
        """
        Reload proxy list from configuration file
        
        Returns:
            bool: True if reloaded successfully
        """
        logger.info("🔄 Reloading proxy configuration...")
        
        # Reset state
        with self.lock:
            self.proxies.clear()
            self.failed_proxies.clear()
            self.current_index = 0
        
        # Reload
        return self.load_proxies()
    
    def add_proxy(self, proxy_url: str) -> bool:
        """
        Add a new proxy to the pool
        
        Args:
            proxy_url: Proxy URL to add
            
        Returns:
            bool: True if added successfully
        """
        if not proxy_url or proxy_url in self.proxies:
            return False
        
        # Validate before adding
        if self.validate_proxy(proxy_url):
            with self.lock:
                self.proxies.append(proxy_url)
            
            logger.info(f"✅ Added new proxy: {self._mask_proxy_url(proxy_url)}")
            self.save_proxies()
            return True
        else:
            logger.warning(f"❌ Failed to add proxy (validation failed): {self._mask_proxy_url(proxy_url)}")
            return False
    
    def __len__(self) -> int:
        """Return number of available proxies"""
        return len(self.proxies)
    
    def __bool__(self) -> bool:
        """Return True if there are available proxies"""
        return len(self.proxies) > 0
    
    def __str__(self) -> str:
        """String representation"""
        return f"ProxyRotator({len(self.proxies)} proxies, index={self.current_index})"
    
    def __repr__(self) -> str:
        """Detailed representation"""
        return f"ProxyRotator(proxies={len(self.proxies)}, failed={len(self.failed_proxies)}, config='{self.proxy_config_path}')"


def main():
    """Demo and testing function"""
    print("🔄 Proxy Rotator Demo")
    print("=" * 50)
    
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # Create rotator
    rotator = ProxyRotator()
    
    if not rotator:
        print("❌ No proxies available")
        return 1
    
    print(f"📊 Loaded {len(rotator)} proxies")
    
    # Test getting next proxy
    print("\n🔄 Testing proxy rotation:")
    for i in range(min(5, len(rotator))):
        proxy = rotator.get_next_proxy()
        print(f"   {i+1}. {rotator._mask_proxy_url(proxy)}")
    
    # Test validation
    print("\n🧪 Testing proxy validation:")
    test_proxy = rotator.get_next_proxy()
    if test_proxy:
        is_valid = rotator.validate_proxy(test_proxy)
        print(f"   Proxy: {rotator._mask_proxy_url(test_proxy)}")
        print(f"   Valid: {'✅' if is_valid else '❌'}")
    
    # Get working proxy
    print("\n✅ Getting working proxy:")
    working_proxy = rotator.get_working_proxy()
    if working_proxy:
        print(f"   Working proxy: {rotator._mask_proxy_url(working_proxy)}")
    else:
        print("   ❌ No working proxy found")
    
    # Show statistics
    print("\n📊 Statistics:")
    stats = rotator.get_stats()
    print(f"   Total proxies: {stats['proxy_pool']['total_proxies']}")
    print(f"   Failed proxies: {stats['proxy_pool']['failed_proxies']}")
    print(f"   Total requests: {stats['requests']['total_requests']}")
    print(f"   Successful: {stats['requests']['successful_requests']}")
    print(f"   Failed: {stats['requests']['failed_requests']}")
    
    return 0


if __name__ == "__main__":
    exit(main())

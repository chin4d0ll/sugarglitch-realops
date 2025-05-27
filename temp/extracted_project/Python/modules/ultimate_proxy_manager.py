#!/usr/bin/env python3
"""
🔥 ULTIMATE PROXY MANAGER v4.0 🔥
Advanced Bright Data Integration with Maximum Power

Features:
- Smart Proxy Rotation
- Health Monitoring
- Geographic Targeting
- Connection Pool Management
- Automatic Failover
- Performance Optimization
"""

import json
import time
import random
import logging
import requests
from typing import Dict, List, Optional, Any
from urllib.parse import urlparse
import threading
from queue import Queue

class UltimateProxyManager:
    """🔥 Ultimate Proxy Manager with Maximum Power"""
    
    def __init__(self, config_file: str = "proxy_config.json"):
        # Setup logging first
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        self.config_file = config_file
        self.active_proxies = []
        self.proxy_stats = {}
        self.current_proxy_index = 0
        self.health_check_interval = 300  # 5 minutes
        self.last_health_check = 0
        
        # Countries for rotation
        self.countries = [
            'US', 'CA', 'GB', 'AU', 'DE', 'FR', 'NL', 'SG', 
            'JP', 'BR', 'ES', 'IT', 'SE', 'NO', 'DK'
        ]
        
        # Load config after logger is setup
        self.config = self._load_config()
        
        # Initialize proxy pool
        self._initialize_proxy_pool()
    
    def _load_config(self) -> Dict:
        """Load proxy configuration from file"""
        try:
            with open(self.config_file, 'r') as f:
                config = json.load(f)
            self.logger.info(f"✅ Loaded proxy config from {self.config_file}")
            return config
        except Exception as e:
            self.logger.error(f"❌ Failed to load proxy config: {e}")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict:
        """Get default proxy configuration"""
        return {
            "bright_data": {
                "endpoint": "brd.superproxy.io",
                "port": 22225,
                "username": "brd-customer-hl_63f0835e-zone-scraping_browser",
                "password": "59m84ggoef95"
            },
            "rotation": {
                "enabled": True,
                "interval": 5,
                "countries": ["US", "CA", "GB", "AU", "DE"],
                "sticky_session": False
            }
        }
    
    def _initialize_proxy_pool(self):
        """Initialize proxy pool with health checks"""
        try:
            self.logger.info("🚀 Initializing proxy pool...")
            
            # Create proxy endpoints for different countries
            bright_data_config = self.config.get('bright_data', {})
            base_username = bright_data_config.get('username', '')
            password = bright_data_config.get('password', '')
            endpoint = bright_data_config.get('endpoint', 'brd.superproxy.io')
            port = bright_data_config.get('port', 22225)
            
            # Generate proxy configurations
            for country in self.countries:
                proxy_config = {
                    'country': country,
                    'endpoint': f"{endpoint}:{port}",
                    'username': f"{base_username}-country-{country.lower()}",
                    'password': password,
                    'auth_string': f"{base_username}-country-{country.lower()}:{password}",
                    'full_endpoint': f"{base_username}-country-{country.lower()}:{password}@{endpoint}:{port}",
                    'status': 'unknown',
                    'last_used': 0,
                    'success_rate': 0.0,
                    'total_requests': 0,
                    'successful_requests': 0,
                    'response_time': 0.0
                }
                self.active_proxies.append(proxy_config)
                self.proxy_stats[country] = {
                    'requests': 0,
                    'successes': 0,
                    'failures': 0,
                    'avg_response_time': 0.0
                }
            
            # Add general session proxies (no country targeting)
            for i in range(5):
                session_id = f"session-{i+1}"
                proxy_config = {
                    'country': 'ANY',
                    'session_id': session_id,
                    'endpoint': f"{endpoint}:{port}",
                    'username': f"{base_username}-session-{session_id}",
                    'password': password,
                    'auth_string': f"{base_username}-session-{session_id}:{password}",
                    'full_endpoint': f"{base_username}-session-{session_id}:{password}@{endpoint}:{port}",
                    'status': 'unknown',
                    'last_used': 0,
                    'success_rate': 0.0,
                    'total_requests': 0,
                    'successful_requests': 0,
                    'response_time': 0.0
                }
                self.active_proxies.append(proxy_config)
                self.proxy_stats[session_id] = {
                    'requests': 0,
                    'successes': 0,
                    'failures': 0,
                    'avg_response_time': 0.0
                }
            
            self.logger.info(f"📊 Initialized {len(self.active_proxies)} proxy configurations")
            
        except Exception as e:
            self.logger.error(f"❌ Failed to initialize proxy pool: {e}")
    
    def get_proxy(self, preferred_country: str = None, session_id: str = None) -> Dict[str, Any]:
        """Get next proxy with smart selection"""
        try:
            # Filter proxies based on criteria
            available_proxies = [p for p in self.active_proxies if p['status'] != 'failed']
            
            if not available_proxies:
                self.logger.warning("⚠️ No healthy proxies available, using any proxy")
                available_proxies = self.active_proxies
            
            # Prefer specific country if requested
            if preferred_country:
                country_proxies = [p for p in available_proxies if p['country'] == preferred_country.upper()]
                if country_proxies:
                    available_proxies = country_proxies
            
            # Prefer specific session if requested
            if session_id:
                session_proxies = [p for p in available_proxies if p.get('session_id') == session_id]
                if session_proxies:
                    available_proxies = session_proxies
            
            # Smart selection based on performance
            if len(available_proxies) > 1:
                # Sort by success rate and last used time
                available_proxies.sort(key=lambda x: (-x['success_rate'], x['last_used']))
            
            # Select proxy (round-robin with performance weighting)
            if self.config.get('rotation', {}).get('enabled', True):
                # Use weighted random selection for better distribution
                weights = [max(0.1, p['success_rate'] + 0.1) for p in available_proxies]
                total_weight = sum(weights)
                
                if total_weight > 0:
                    r = random.uniform(0, total_weight)
                    cumulative = 0
                    for i, weight in enumerate(weights):
                        cumulative += weight
                        if r <= cumulative:
                            selected_proxy = available_proxies[i]
                            break
                    else:
                        selected_proxy = available_proxies[0]
                else:
                    selected_proxy = random.choice(available_proxies)
            else:
                # Simple round-robin
                selected_proxy = available_proxies[self.current_proxy_index % len(available_proxies)]
                self.current_proxy_index += 1
            
            # Update usage stats
            selected_proxy['last_used'] = time.time()
            selected_proxy['total_requests'] += 1
            
            # Update proxy stats
            country_key = selected_proxy.get('session_id', selected_proxy['country'])
            if country_key in self.proxy_stats:
                self.proxy_stats[country_key]['requests'] += 1
            
            self.logger.info(f"🌐 Selected proxy: {selected_proxy['country']} ({selected_proxy.get('session_id', 'country-targeted')})")
            
            return {
                'endpoint': selected_proxy['full_endpoint'],
                'country': selected_proxy['country'],
                'session_id': selected_proxy.get('session_id'),
                'username': selected_proxy['username'],
                'password': selected_proxy['password'],
                'auth_string': selected_proxy['auth_string'],
                'success_rate': selected_proxy['success_rate'],
                'proxy_config': selected_proxy
            }
            
        except Exception as e:
            self.logger.error(f"❌ Failed to get proxy: {e}")
            # Fallback to first available proxy
            if self.active_proxies:
                fallback = self.active_proxies[0]
                return {
                    'endpoint': fallback['full_endpoint'],
                    'country': fallback['country'],
                    'session_id': fallback.get('session_id'),
                    'username': fallback['username'],
                    'password': fallback['password'],
                    'auth_string': fallback['auth_string'],
                    'success_rate': fallback['success_rate'],
                    'proxy_config': fallback
                }
            return None
    
    def report_proxy_result(self, proxy_config: Dict, success: bool, response_time: float = 0):
        """Report the result of a proxy request"""
        try:
            # Find the proxy in our list
            for proxy in self.active_proxies:
                if (proxy.get('username') == proxy_config.get('username') and 
                    proxy.get('password') == proxy_config.get('password')):
                    
                    if success:
                        proxy['successful_requests'] += 1
                        proxy['status'] = 'healthy'
                        
                        # Update stats
                        country_key = proxy.get('session_id', proxy['country'])
                        if country_key in self.proxy_stats:
                            self.proxy_stats[country_key]['successes'] += 1
                    else:
                        # Update stats
                        country_key = proxy.get('session_id', proxy['country'])
                        if country_key in self.proxy_stats:
                            self.proxy_stats[country_key]['failures'] += 1
                    
                    # Update success rate
                    if proxy['total_requests'] > 0:
                        proxy['success_rate'] = proxy['successful_requests'] / proxy['total_requests']
                    
                    break
                    
        except Exception as e:
            self.logger.error(f"❌ Failed to report proxy result: {e}")
    
    def create_session_proxy(self, custom_session_id: str = None) -> Dict[str, Any]:
        """Create a dedicated session proxy"""
        try:
            session_id = custom_session_id or f"custom-{int(time.time())}-{random.randint(1000, 9999)}"
            
            bright_data_config = self.config.get('bright_data', {})
            base_username = bright_data_config.get('username', '')
            password = bright_data_config.get('password', '')
            endpoint = bright_data_config.get('endpoint', 'brd.superproxy.io')
            port = bright_data_config.get('port', 22225)
            
            proxy_config = {
                'country': 'SESSION',
                'session_id': session_id,
                'endpoint': f"{endpoint}:{port}",
                'username': f"{base_username}-session-{session_id}",
                'password': password,
                'auth_string': f"{base_username}-session-{session_id}:{password}",
                'full_endpoint': f"{base_username}-session-{session_id}:{password}@{endpoint}:{port}",
                'status': 'unknown',
                'last_used': time.time(),
                'success_rate': 0.0,
                'total_requests': 0,
                'successful_requests': 0,
                'response_time': 0.0
            }
            
            self.active_proxies.append(proxy_config)
            self.proxy_stats[session_id] = {
                'requests': 0,
                'successes': 0,
                'failures': 0,
                'avg_response_time': 0.0
            }
            
            self.logger.info(f"✅ Created session proxy: {session_id}")
            
            return {
                'endpoint': proxy_config['full_endpoint'],
                'country': 'SESSION',
                'session_id': session_id,
                'username': proxy_config['username'],
                'password': proxy_config['password'],
                'auth_string': proxy_config['auth_string'],
                'proxy_config': proxy_config
            }
            
        except Exception as e:
            self.logger.error(f"❌ Failed to create session proxy: {e}")
            return None
    
    def get_proxy_stats(self) -> Dict[str, Any]:
        """Get comprehensive proxy statistics"""
        stats = {
            'total_proxies': len(self.active_proxies),
            'healthy_proxies': len([p for p in self.active_proxies if p['status'] == 'healthy']),
            'failed_proxies': len([p for p in self.active_proxies if p['status'] == 'failed']),
            'countries': list(set([p['country'] for p in self.active_proxies])),
            'proxy_details': [],
            'country_stats': self.proxy_stats
        }
        
        for proxy in self.active_proxies:
            stats['proxy_details'].append({
                'country': proxy['country'],
                'session_id': proxy.get('session_id'),
                'status': proxy['status'],
                'success_rate': proxy['success_rate'],
                'total_requests': proxy['total_requests'],
                'response_time': proxy['response_time'],
                'last_used': proxy['last_used']
            })
        
        return stats
    
    def get_next_proxy(self, preferred_country: str = None, session_id: str = None) -> Optional[Dict]:
        """Get the next available proxy with smart selection"""
        try:
            # Check if we need health check
            if time.time() - self.last_health_check > self.health_check_interval:
                self._perform_health_check()
            
            # Filter proxies based on criteria
            available_proxies = [p for p in self.active_proxies if p['status'] != 'failed']
            
            if not available_proxies:
                self.logger.warning("⚠️ No healthy proxies available, using any proxy")
                available_proxies = self.active_proxies
            
            if not available_proxies:
                self.logger.error("❌ No proxies available at all")
                return None
            
            # Prefer specific country if requested
            if preferred_country:
                country_proxies = [p for p in available_proxies if p['country'] == preferred_country.upper()]
                if country_proxies:
                    available_proxies = country_proxies
            
            # Prefer specific session if requested
            if session_id:
                session_proxies = [p for p in available_proxies if p.get('session_id') == session_id]
                if session_proxies:
                    available_proxies = session_proxies
            
            # Smart selection based on performance
            if len(available_proxies) > 1:
                # Sort by success rate and last used time
                available_proxies.sort(key=lambda x: (-x['success_rate'], x['last_used']))
            
            # Select proxy (round-robin with performance weighting)
            if self.config.get('rotation', {}).get('enabled', True):
                # Use weighted random selection for better distribution
                weights = [max(0.1, p['success_rate'] + 0.1) for p in available_proxies]
                total_weight = sum(weights)
                
                if total_weight > 0:
                    r = random.uniform(0, total_weight)
                    cumulative = 0
                    for i, weight in enumerate(weights):
                        cumulative += weight
                        if r <= cumulative:
                            selected_proxy = available_proxies[i]
                            break
                    else:
                        selected_proxy = available_proxies[0]
                else:
                    selected_proxy = random.choice(available_proxies)
            else:
                # Simple round-robin
                selected_proxy = available_proxies[self.current_proxy_index % len(available_proxies)]
                self.current_proxy_index += 1
            
            # Update usage stats
            selected_proxy['last_used'] = time.time()
            selected_proxy['total_requests'] += 1
            
            self.logger.info(f"🌐 Selected proxy: {selected_proxy['country']} ({selected_proxy['success_rate']:.1%} success rate)")
            return selected_proxy
            
        except Exception as e:
            self.logger.error(f"❌ Failed to get next proxy: {e}")
            return None
    
    def mark_proxy_failed(self, proxy_config: Dict):
        """Mark a proxy as failed"""
        try:
            if not proxy_config:
                return
                
            for proxy in self.active_proxies:
                if (proxy.get('session_id') == proxy_config.get('session_id') or
                    proxy.get('country') == proxy_config.get('country')):
                    proxy['status'] = 'failed'
                    self.logger.warning(f"🚫 Marked proxy as failed: {proxy['country']}")
                    break
                    
        except Exception as e:
            self.logger.error(f"❌ Failed to mark proxy as failed: {e}")
    
    def _perform_health_check(self):
        """Perform health check on proxies"""
        try:
            self.logger.info("🏥 Performing proxy health check...")
            self.last_health_check = time.time()
            
            # Simple health check - reset failed proxies after some time
            current_time = time.time()
            reset_threshold = 1800  # 30 minutes
            
            for proxy in self.active_proxies:
                if (proxy['status'] == 'failed' and 
                    current_time - proxy['last_used'] > reset_threshold):
                    proxy['status'] = 'unknown'
                    self.logger.info(f"🔄 Reset proxy status: {proxy['country']}")
            
        except Exception as e:
            def _perform_health_check(self):
                """Perform health check on proxies"""
                try:
                    self.logger.info("🏥 Performing proxy health check...")
                    self.last_health_check = time.time()
                    
                    # Simple health check - reset failed proxies after some time
                    current_time = time.time()
                    reset_threshold = 1800  # 30 minutes
                    
                    for proxy in self.active_proxies:
                        if proxy['status'] == 'failed' and current_time - proxy['last_used'] > reset_threshold:
                            proxy['status'] = 'unknown'
                            self.logger.info(f"🔄 Reset proxy status: {proxy['country']}")
                    
                except Exception as e:
                    self.logger.error(f"❌ Health check failed: {e}")

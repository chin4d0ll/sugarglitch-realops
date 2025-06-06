#!/usr/bin/env python3
"""
IP Block Bypass Script
Monitors a target endpoint, detects Instagram IP blocks, and automatically rotates proxies to bypass blocks.
"""

import time
import logging
import requests
import sys
import os

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(__file__))

try:
    from ip_rotation_handler import ProxyRotator
    from instagram_block_recovery import InstagramBlockRecovery
except ImportError:
    # Try with tools prefix if running from parent directory
    from tools.ip_rotation_handler import ProxyRotator
    from tools.instagram_block_recovery import InstagramBlockRecovery

# --- Configuration ---
SESSION_FILE = "tools/session_alx_trading.json"
PROXY_CONFIG = "config/proxies.json"
TARGET_URL = "https://i.instagram.com/api/v1/direct_v2/inbox/"  # Example DM endpoint
CHECK_INTERVAL = 10  # seconds between checks
MAX_RETRIES = 1  # Retry once after recovery

# --- Logging Setup ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)


def fetch_dm_inbox(session, proxy=None):
    """Fetch the DM inbox using the given session and proxy."""
    proxies = {"http": proxy, "https": proxy} if proxy else None
    try:
        response = session.get(TARGET_URL, proxies=proxies, timeout=10)
        return response
    except Exception as e:
        logger.error(f"Request error: {e}")
        return None


def main():
    logger.info("🚀 Starting IP Block Bypass Monitor...")
    proxy_rotator = ProxyRotator(PROXY_CONFIG)
    block_recovery = InstagramBlockRecovery(SESSION_FILE)
    
    while True:
        # Get current proxy
        proxy = proxy_rotator.get_current_proxy() or proxy_rotator.get_next_proxy()
        logger.info(f"🌐 Using proxy: {proxy}")
        
        # Create session with proxy
        session = block_recovery.create_session(proxy)
        
        # Attempt request
        response = fetch_dm_inbox(session, proxy)
        if response is None:
            logger.warning(f"No response from endpoint using proxy {proxy}")
            time.sleep(CHECK_INTERVAL)
            continue
        
        if response.status_code in (403, 429):
            logger.warning(f"Blocked on {proxy} (HTTP {response.status_code})")
            # Attempt block recovery (rotate proxy and renew session)
            recovery_result = block_recovery.recover_from_block()
            if recovery_result and recovery_result.get("success"):
                new_proxy = proxy_rotator.get_current_proxy()
                logger.info(f"Switched to {new_proxy} after block recovery")
                # Retry request once
                session = block_recovery.create_session(new_proxy)
                retry_response = fetch_dm_inbox(session, new_proxy)
                if retry_response and retry_response.status_code == 200:
                    logger.info("Request succeeded after proxy switch!")
                else:
                    logger.warning(f"Retry failed (HTTP {retry_response.status_code if retry_response else 'N/A'})")
            else:
                logger.error("Block recovery failed. No more proxies or session renewal failed.")
        elif response.status_code == 200:
            logger.info("Request succeeded!")
        else:
            logger.info(f"Received HTTP {response.status_code} (not a block)")
        
        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
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
TARGET_URL = "https://i.instagram.com/api/v1/direct_v2/inbox/?visual_message_reply_chain_enabled=true&thread_message_limit=10&persistentBadging=true&limit=20"  # Enhanced DM endpoint
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
    block_recovery = InstagramBlockRecovery(SESSION_FILE)
    proxy_rotator = block_recovery.proxy_rotator  # Use the rotator from block_recovery

    # Load session data
    if not block_recovery.load_session():
        logger.error("❌ Failed to load session data. Cannot start monitoring.")
        return

    # Initialize with first proxy
    current_proxy = proxy_rotator.get_next_proxy()
    if not current_proxy:
        logger.error("❌ No proxies available. Cannot start monitoring.")
        return

    try:
        while True:
            logger.info(f"🌐 Using proxy: {proxy_rotator._mask_proxy_url(current_proxy) if hasattr(proxy_rotator, '_mask_proxy_url') else current_proxy}")

            # Create session with current proxy
            session = block_recovery.create_session(current_proxy)

            # Attempt request
            response = fetch_dm_inbox(session, current_proxy)
            if response is None:
                logger.warning(f"⚠️ No response from endpoint using current proxy")
                # Try next proxy
                current_proxy = proxy_rotator.get_next_proxy()
                if not current_proxy:
                    logger.error("❌ No more proxies available. Exiting.")
                    break
                time.sleep(CHECK_INTERVAL)
                continue

            if response.status_code in (403, 429):
                logger.warning(f"🚫 Blocked! (HTTP {response.status_code})")
                # Attempt block recovery (rotate proxy and renew session)
                success, recovered_proxy = block_recovery.recover_from_block()
                if success and recovered_proxy:
                    current_proxy = recovered_proxy
                    logger.info(f"✅ Recovery successful! Switched to new proxy")
                    # Retry request once with recovered proxy
                    session = block_recovery.create_session(current_proxy)
                    retry_response = fetch_dm_inbox(session, current_proxy)
                    if retry_response and retry_response.status_code == 200:
                        logger.info("🎉 Request succeeded after block recovery!")
                    else:
                        logger.warning(f"⚠️ Retry failed (HTTP {retry_response.status_code if retry_response else 'N/A'})")
                else:
                    logger.error("❌ Block recovery failed. No more working proxies available.")
                    # Try to get any remaining proxy as last resort
                    current_proxy = proxy_rotator.get_next_proxy()
                    if not current_proxy:
                        logger.error("❌ No proxies left. Exiting.")
                        break
            elif response.status_code == 200:
                logger.info("✅ Request succeeded!")
            else:
                logger.info(f"ℹ️ Received HTTP {response.status_code} (not a block)")

            time.sleep(CHECK_INTERVAL)

    except KeyboardInterrupt:
        logger.info("🛑 Monitor stopped by user")
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
        raise
if __name__ == "__main__":
    main()

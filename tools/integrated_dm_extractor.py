# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
ALX Trading DM Extraction with Proxy Rotation and Block Recovery
Complete integration of all components for robust Instagram DM extraction
"""

import json
import os
import sys
import time
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional

# Import all our components
try:
    from tools.ip_rotation_handler import ProxyRotator
    from tools.instagram_block_recovery import InstagramBlockRecovery, renew_session
    from tools.extract_alx_trading_dms import ALXTradingDMExtractor
except ImportError:
    # Try relative imports
    try:
        from ip_rotation_handler import ProxyRotator
        from instagram_block_recovery import InstagramBlockRecovery, renew_session
        from extract_alx_trading_dms import ALXTradingDMExtractor
    except ImportError:
        print("❌ Could not import required modules. Make sure all scripts are in the same directory.")
        sys.exit(1)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/dm_extraction_integrated.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)
class IntegratedDMExtractor:
    """
    Integrated DM Extractor with automatic proxy rotation and block recovery
    """

    def __init__(self,
                 session_file: str = "tools/session_alx_trading.json",
                 proxy_config: str = "config/proxies.json",
                 output_dir: str = "results"):
        """
        Initialize the integrated extractor

        Args:
            session_file: Path to Instagram session file
            proxy_config: Path to proxy configuration file
            output_dir: Directory to save extraction results
        """
        self.session_file = session_file
        self.proxy_config = proxy_config
        self.output_dir = output_dir

        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        os.makedirs("logs", exist_ok=True)

        # Initialize components
        self.proxy_rotator = ProxyRotator(proxy_config)
        self.block_recovery = InstagramBlockRecovery(session_file)
        self.dm_extractor = ALXTradingDMExtractor(session_file)

        # Statistics
        self.extraction_stats = {
            "start_time": None,
            "end_time": None,
            "total_attempts": 0,
            "successful_extractions": 0,
            "block_recoveries": 0,
            "proxy_rotations": 0,
            "total_messages": 0,
            "errors": []
        }

    def run_extraction(self, max_retries: int = 3) -> Dict[str, Any]:
        """
        Run the complete DM extraction with automatic recovery

        Args:
            max_retries: Maximum number of retry attempts

        Returns:
            Dict containing extraction results and statistics
        """
        logger.info("🚀 Starting integrated DM extraction for alx.trading")
        self.extraction_stats["start_time"] = datetime.now()

        for attempt in range(max_retries + 1):
            try:
                self.extraction_stats["total_attempts"] += 1
                logger.info(f"📊 Extraction attempt {attempt + 1}/{max_retries + 1}")

                # Check if we need to rotate proxy
                if attempt > 0:
                    logger.info("🔄 Rotating proxy for new attempt")
                    new_proxy = self.proxy_rotator.get_next_proxy()
                    if new_proxy:
                        logger.info(f"🌐 Using proxy: {new_proxy}")
                        self.extraction_stats["proxy_rotations"] += 1

                        # Renew session with new proxy
                        if renew_session(self.session_file, new_proxy):
                            logger.info("✅ Session renewed successfully")
                            # Reload the extractor with new session
                            self.dm_extractor = ALXTradingDMExtractor(self.session_file)
                        else:
                            logger.warning("⚠️ Failed to renew session, continuing with existing")

                # Attempt DM extraction
                logger.info("📱 Starting DM extraction...")
                results = self.dm_extractor.extract_all_dms()

                if results and results.get("threads"):
                    # Successful extraction
                    self.extraction_stats["successful_extractions"] += 1
                    self.extraction_stats["total_messages"] = results.get("extraction_info", {}).get("total_messages", 0)

                    # Save results
                    output_file = self._save_results(results)
                    logger.info(f"✅ Extraction completed successfully!")
                    logger.info(f"📄 Results saved to: {output_file}")
                    logger.info(f"📊 Total messages extracted: {self.extraction_stats['total_messages']}")

                    self.extraction_stats["end_time"] = datetime.now()
                    return {
                        "success": True,
                        "results": results,
                        "output_file": output_file,
                        "stats": self.extraction_stats
                    }
                else:
                    logger.warning("⚠️ No DM data extracted, may be blocked")

            except Exception as e:
                error_msg = f"Attempt {attempt + 1} failed: {str(e)}"
                logger.error(f"❌ {error_msg}")
                self.extraction_stats["errors"].append(error_msg)

                # Check if this looks like a block
                if self._is_block_error(str(e)):
                    logger.info("🛡️ Detected potential Instagram block, attempting recovery...")

                    if self._attempt_block_recovery():
                        self.extraction_stats["block_recoveries"] += 1
                        logger.info("✅ Block recovery successful, retrying extraction...")
                        continue
                    else:
                        logger.warning("⚠️ Block recovery failed")

                # Wait before retry
                if attempt < max_retries:
                    wait_time = (attempt + 1) * 30  # Exponential backoff
                    logger.info(f"⏳ Waiting {wait_time} seconds before retry...")
                    time.sleep(wait_time)

        # All attempts failed
        self.extraction_stats["end_time"] = datetime.now()
        logger.error("❌ All extraction attempts failed")

        return {
            "success": False,
            "error": "All extraction attempts failed",
            "stats": self.extraction_stats
        }

    def _is_block_error(self, error_message: str) -> bool:
        """
        Check if an error indicates an Instagram block

        Args:
            error_message: Error message to check

        Returns:
            bool: True if error indicates a block
        """
        block_indicators = [
            "403",
            "429",
            "rate limit",
            "rate_limit",
            "blocked",
            "challenge_required",
            "checkpoint_required",
            "suspicious",
            "verify"
        ]

        error_lower = error_message.lower()
        return any(indicator in error_lower for indicator in block_indicators)

    def _attempt_block_recovery(self) -> bool:
        """
        Attempt to recover from Instagram block

        Returns:
            bool: True if recovery was successful
        """
        try:
            logger.info("🔧 Attempting block recovery...")

            # Use the block recovery system
            recovery_result = self.block_recovery.recover_from_block()

            if recovery_result.get("success"):
                logger.info("✅ Block recovery completed successfully")
                return True
            else:
                logger.warning(f"⚠️ Block recovery failed: {recovery_result.get('error', 'Unknown error')}")
                return False

        except Exception as e:
            logger.error(f"❌ Error during block recovery: {e}")
            return False

    def _save_results(self, results: Dict[str, Any]) -> str:
        """
        Save extraction results to file

        Args:
            results: Extraction results to save

        Returns:
            str: Path to saved file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"alx_trading_dms_{timestamp}.json"
        filepath = os.path.join(self.output_dir, filename)

        # Add extraction statistics to results
        results["extraction_stats"] = self.extraction_stats

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

        return filepath

    def get_proxy_status(self) -> Dict[str, Any]:
        """
        Get current proxy pool status

        Returns:
            Dict with proxy status information
        """
        return {
            "total_proxies": len(self.proxy_rotator.proxies),
            "failed_proxies": len(self.proxy_rotator.failed_proxies),
            "current_proxy": self.proxy_rotator.get_current_proxy(),
            "stats": self.proxy_rotator.get_stats()
        }

    def run_health_check(self) -> Dict[str, Any]:
        """
        Run a complete health check of all components

        Returns:
            Dict with health check results
        """
        logger.info("🔍 Running system health check...")

        health_status = {
            "timestamp": datetime.now().isoformat(),
            "session_file": os.path.exists(self.session_file),
            "proxy_config": os.path.exists(self.proxy_config),
            "proxy_count": len(self.proxy_rotator.proxies),
            "components": {}
        }

        # Test proxy rotator
        try:
            proxy_health = self.proxy_rotator.health_check()
            health_status["components"]["proxy_rotator"] = {
                "status": "healthy" if proxy_health else "unhealthy",
                "details": self.proxy_rotator.get_stats()
            }
        except Exception as e:
            health_status["components"]["proxy_rotator"] = {
                "status": "error",
                "error": str(e)
            }

        # Test block recovery
        try:
            recovery_status = self.block_recovery.test_connection()
            health_status["components"]["block_recovery"] = {
                "status": "healthy" if recovery_status else "unhealthy"
            }
        except Exception as e:
            health_status["components"]["block_recovery"] = {
                "status": "error",
                "error": str(e)
            }

        # Test DM extractor
        try:
            extractor_loaded = self.dm_extractor.load_session()
            health_status["components"]["dm_extractor"] = {
                "status": "healthy" if extractor_loaded else "unhealthy"
            }
        except Exception as e:
            health_status["components"]["dm_extractor"] = {
                "status": "error",
                "error": str(e)
            }

        # Overall health
        all_healthy = all(
            comp.get("status") == "healthy"
            for comp in health_status["components"].values()
        )
        health_status["overall_status"] = "healthy" if all_healthy else "degraded"

        return health_status
def main():
    """
    Main execution function
    """
    print("🚀 ALX Trading DM Extraction - Integrated Version")
    print("=" * 60)

    # Initialize the integrated extractor
    extractor = IntegratedDMExtractor()

    # Run health check first
    print("\n🔍 Running system health check...")
    health = extractor.run_health_check()
    print(f"Overall Status: {health['overall_status'].upper()}")

    if health['overall_status'] != 'healthy':
        print("\n⚠️ System health issues detected:")
        for component, status in health['components'].items():
            if status['status'] != 'healthy':
                print(f"  - {component}: {status['status']}")
                if 'error' in status:
                    print(f"    Error: {status['error']}")

    # Show proxy status
    print("\n🌐 Proxy Pool Status:")
    proxy_status = extractor.get_proxy_status()
    print(f"  - Total Proxies: {proxy_status['total_proxies']}")
    print(f"  - Failed Proxies: {proxy_status['failed_proxies']}")
    print(f"  - Current Proxy: {proxy_status['current_proxy']}")

    # Ask user if they want to proceed
    if health['overall_status'] != 'healthy':
        response = input("\n⚠️ System not fully healthy. Continue anyway? (y/N): ")
        if response.lower() != 'y':
            print("Extraction cancelled.")
            return

    # Run the extraction
    print("\n🚀 Starting DM extraction...")
    results = extractor.run_extraction(max_retries=3)

    # Display results
    print("\n" + "=" * 60)
    if results["success"]:
        print("✅ EXTRACTION COMPLETED SUCCESSFULLY!")
        print(f"📄 Results saved to: {results['output_file']}")
        print(f"📊 Messages extracted: {results['stats']['total_messages']}")
        print(f"🔄 Proxy rotations: {results['stats']['proxy_rotations']}")
        print(f"🛡️ Block recoveries: {results['stats']['block_recoveries']}")
    else:
        print("❌ EXTRACTION FAILED")
        print(f"Error: {results['error']}")
        if results['stats']['errors']:
            print("\nErrors encountered:")
            for error in results['stats']['errors']:
                print(f"  - {error}")

    # Final statistics
    stats = results['stats']
    duration = (stats['end_time'] - stats['start_time']).total_seconds() if stats['end_time'] else 0
    print(f"\n📈 Final Statistics:")
    print(f"  - Duration: {duration:.1f} seconds")
    print(f"  - Total Attempts: {stats['total_attempts']}")
    print(f"  - Successful Extractions: {stats['successful_extractions']}")
if __name__ == "__main__":
    main()

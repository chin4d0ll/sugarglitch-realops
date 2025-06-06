#!/usr/bin/env python3
"""
Fresh Instagram DM Extractor V2 - With Rate Limiting Protection
💖 แก้ไขปัญหา HTTP 429 แบบ girly-cute ✨
"""

import os
import sys
import json
import time
import logging
from datetime import datetime
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / 'src'))

from instagram_extractor_v2 import InstagramDMExtractor
from utils import setup_logging, load_config

def main():
    """Main extraction function with cute rate limiting protection 💕"""
    print("🚀✨ Fresh Instagram DM Extractor V2 - Starting...")
    print("💖 Now with advanced rate limiting protection! 💖")
    
    # Setup logging
    log_file = Path(__file__).parent / 'logs' / f'extraction_v2_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
    setup_logging(log_file)
    logger = logging.getLogger(__name__)
    
    try:
        # Load configuration
        config_path = Path(__file__).parent / 'config' / 'settings.json'
        config = load_config(config_path)
        
        # Check session data
        session_data = config.get('session_data', {})
        if not session_data.get('sessionid'):
            print("❌ No session data found!")
            print("📝 Please update config/settings.json with your Instagram session data")
            print("💡 See README.md for instructions on how to get session data")
            return False
        
        print(f"🍪 Session data loaded: {len(session_data)} cookies")
        print(f"🎯 Target: @{config.get('target_username', 'alx.trading')}")
        
        # Initialize extractor with rate limiting protection
        print("\\n💖 Initializing extractor with rate limiting protection...")
        extractor = InstagramDMExtractor(config)
        
        # Run extraction
        print("\\n🎯 Starting DM extraction...")
        results = extractor.extract_dms()
        
        if results:
            print("\\n🎉 SUCCESS! Extraction completed successfully! 🎉")
            print("=" * 50)
            print(f"📁 Results saved to: {results['output_path']}")
            print(f"📊 Total messages: {results['total_messages']}")
            print(f"👥 Total conversations: {results['total_conversations']}")
            print(f"✨ HTML report also generated!")
            print("=" * 50)
        else:
            print("\\n❌ Extraction failed")
            print("💡 Check logs for details")
            return False
            
    except Exception as e:
        logger.error(f"Main execution error: {e}")
        print(f"❌ Error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("🌸✨ CUTE INSTAGRAM DM EXTRACTOR WITH RATE LIMITING PROTECTION ✨🌸")
    print("=" * 70)
    print("💕 Fixing HTTP 429 issues with girly-cute techniques! 💕")
    print()
    
    success = main()
    
    if success:
        print("\\n💖 All done! Hope this fixes the 429 issues! 💖")
        print("🌸 Remember: patience is key for rate limiting! 🌸")
    else:
        print("\\n💔 Something went wrong. Check the logs! 💔")
    
    sys.exit(0 if success else 1)

#!/usr/bin/env python3
"""
Browser-based Instagram DM Extractor Main Script
Uses Playwright to avoid API rate limits
"""

import os
import sys
import json
import asyncio
import logging
from datetime import datetime
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / 'src'))

from browser_extractor import BrowserInstagramExtractor
from utils import setup_logging, load_config

async def main():
    """Main extraction function using browser"""
    print("🌐 Fresh Instagram DM Extractor - Browser Mode")
    print("=" * 50)
    
    # Setup logging
    log_file = Path(__file__).parent / 'logs' / f'browser_extraction_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
    setup_logging(log_file)
    logger = logging.getLogger(__name__)
    
    try:
        # Load configuration
        config_path = Path(__file__).parent / 'config' / 'settings.json'
        config = load_config(config_path)
        
        # Check session data
        session_data = config.get('session_data', {})
        if not session_data.get('sessionid'):
            print("❌ No session data found in config/settings.json")
            print("📝 Please add your Instagram session data")
            return False
        
        print(f"✅ Session data loaded")
        print(f"🎯 Target: @{config.get('target_username', 'alx.trading')}")
        
        # Initialize browser extractor
        extractor = BrowserInstagramExtractor(config)
        
        print("🚀 Starting browser extraction...")
        print("📱 This will open a browser window - please wait...")
        
        # Run extraction
        results = await extractor.extract_dms()
        
        if results:
            print("\n" + "=" * 50)
            print("✅ Extraction completed successfully!")
            print(f"📁 Results saved to: {results['output_path']}")
            print(f"📊 Total messages: {results['total_messages']}")
            print(f"👥 Total conversations: {results['total_conversations']}")
            
            # Show conversation summary
            print("\n💬 Conversations extracted:")
            for i, conv in enumerate(results['conversations'], 1):
                print(f"   {i}. {conv['name']} ({conv['message_count']} messages)")
            
        else:
            print("❌ Extraction failed")
            print("📋 Check logs for details")
            
    except Exception as e:
        logger.error(f"Main execution error: {e}")
        print(f"❌ Error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)

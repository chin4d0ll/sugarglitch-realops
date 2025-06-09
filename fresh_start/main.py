# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
Fresh Instagram DM Extractor - Clean Start
Simple, effective Instagram DM extraction with modern approach
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

from instagram_extractor import InstagramDMExtractor
from utils import setup_logging, load_config

def main():
    """Main extraction function"""
    print("🚀 Fresh Instagram DM Extractor - Starting...")

    # Setup logging
    log_file = Path(__file__).parent / 'logs' / f'extraction_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
    setup_logging(log_file)
    logger = logging.getLogger(__name__)

    try:
        # Load configuration
        config_path = Path(__file__).parent / 'config' / 'settings.json'
        config = load_config(config_path)

        # Initialize extractor
        extractor = InstagramDMExtractor(config)

        # Run extraction
        results = extractor.extract_dms()

        if results:
            print(f"✅ Extraction completed successfully!")
            print(f"📁 Results saved to: {results['output_path']}")
            print(f"📊 Total messages: {results['total_messages']}")
            print(f"👥 Total conversations: {results['total_conversations']}")
        else:
            print("❌ Extraction failed")

    except Exception as e:
        logger.error(f"Main execution error: {e}")
        print(f"❌ Error: {e}")
        return False

    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

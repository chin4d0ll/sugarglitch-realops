#!/usr/bin/env python3
"""
Quick Launch Script for Ultimate Working DM Extractor
Run this to extract Instagram DMs with all methods automatically.
"""

import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ultimate_working_dm_extractor_2025 import main

if __name__ == "__main__":
    print("🎯 Launching Ultimate DM Extractor...")
    print("This will try all available methods to extract Instagram DMs")
    print("from the alx.trading account.\n")
    
    try:
        results = main()
        
        if results['success']:
            print(f"\n🎉 SUCCESS! Extracted {results['total_messages']} messages from {results['threads_count']} threads")
            print("Check the /workspaces/sugarglitch-realops/results/ folder for your files!")
        else:
            print(f"\n💥 Extraction failed: {results['error']}")
            print("The system tried multiple methods but Instagram's security prevented access.")
            print("You may need to:")
            print("- Use a different IP address/VPN")
            print("- Get fresh session cookies from a browser")
            print("- Wait for rate limits to reset")
            
    except KeyboardInterrupt:
        print("\n⚠️ Extraction cancelled by user")
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        print("Check the logs for more details.")

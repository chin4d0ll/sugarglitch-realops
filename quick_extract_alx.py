#!/usr/bin/env python3
"""
Quick DM Extraction Script for alx.trading
Simple interface to run the comprehensive extraction system
"""
import sys
import os
import json
from pathlib import Path

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from enhanced_fleming_bypass_dream_edition import EnhancedFlemingBypassDreamEdition
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure all dependencies are installed:")
    print("pip install instagrapi undetected-chromedriver selenium fpdf2 pillow")
    sys.exit(1)

def main():
    """Simple interface to run DM extraction"""
    print("🔥" * 50)
    print("🎯 ALX.TRADING DM EXTRACTION - DREAM EDITION")
    print("🔥" * 50)
    print()
    
    # Check if user wants to proceed
    response = input("🚀 Ready to extract DMs from alx.trading? (y/n): ").lower().strip()
    
    if response != 'y':
        print("❌ Operation cancelled")
        return
    
    print("\n📱 Starting extraction process...")
    print("⏰ This may take a few minutes...")
    print()
    
    try:
        # Create and run extractor
        extractor = EnhancedFlemingBypassDreamEdition()
        result = extractor.run_extraction()
        
        # Display results
        print("\n" + "="*80)
        print("🎉 EXTRACTION COMPLETED!")
        print("="*80)
        
        if result.get('success'):
            print(f"✅ Successfully extracted {result.get('total_messages', 0)} messages")
            print(f"📸 Downloaded {result.get('media_count', 0)} media files")
            print("\n📁 Results saved to:")
            
            for file_type, file_path in result.get('saved_files', {}).items():
                if file_path != 'N/A':
                    print(f"   {file_type.upper()}: {file_path}")
                    
            print(f"\n⏰ Extraction completed at: {result.get('timestamp', 'Unknown')}")
            print(f"🔧 Method used: {result.get('method_used', 'Unknown')}")
            
        else:
            print("❌ Extraction failed!")
            print(f"Error: {result.get('error', 'Unknown error')}")
            print("\n💡 Possible solutions:")
            print("   1. Check your internet connection")
            print("   2. Verify session files are present")
            print("   3. Try running with different methods")
            
    except KeyboardInterrupt:
        print("\n⚠️  Extraction cancelled by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("Check the logs directory for detailed error information")

if __name__ == "__main__":
    main()

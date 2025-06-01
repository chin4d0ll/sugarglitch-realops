#!/usr/bin/env python3
"""
🔥 Instagram DM Extractor Test Script 🔥
========================================
ทดสอบ DM extraction จาก Ultra Optimized Hacker Toolkit
"""

import asyncio
import sys
import os
from pathlib import Path

# Add current directory to path
sys.path.append(str(Path(__file__).parent))

# Import our toolkit
from ultra_optimized_hacker_toolkit_v2 import UltraOptimizedHackerToolkit

async def test_dm_extraction():
    """Test Instagram DM extraction"""
    
    print("🚀 Starting DM extraction test...")
    
    # Initialize toolkit
    toolkit = UltraOptimizedHackerToolkit()
    
    # Get credentials from user
    print("\n💀 Instagram DM Extractor Test 💀")
    print("=" * 50)
    
    username = input("📧 Enter your Instagram username: ").strip()
    if not username:
        print("❌ Username required!")
        return
    
    password = input("🔐 Enter your Instagram password: ").strip()
    if not password:
        print("❌ Password required!")
        return
    
    target_user = input("🎯 Enter target username (optional, press Enter for all DMs): ").strip()
    target_user = target_user if target_user else None
    
    print(f"\n🔥 Extracting DMs for {username}...")
    if target_user:
        print(f"🎯 Targeting specific user: {target_user}")
    else:
        print("🌐 Extracting all conversations")
    
    try:
        # Extract DMs
        result = await toolkit.instagram_dm_extractor(
            username=username,
            password=password,
            target_user=target_user
        )
        
        # Display results
        print("\n" + "="*60)
        print("📊 EXTRACTION RESULTS")
        print("="*60)
        
        if result:
            print(f"👤 Username: {result.get('username', 'N/A')}")
            print(f"🕐 Extraction Time: {result.get('extraction_time', 'N/A')}")
            print(f"💬 Total Messages: {result.get('total_messages', 0)}")
            print(f"🗣️ Total Conversations: {len(result.get('threads', []))}")
            
            # Show conversation details
            if result.get('threads'):
                print("\n📋 CONVERSATION DETAILS:")
                for i, thread in enumerate(result['threads'][:5], 1):  # Show first 5
                    users = [u['username'] for u in thread.get('users', [])]
                    message_count = len(thread.get('messages', []))
                    print(f"  {i}. Users: {', '.join(users)} | Messages: {message_count}")
                
                if len(result['threads']) > 5:
                    print(f"  ... and {len(result['threads']) - 5} more conversations")
            
            # Save results to file
            import json
            output_file = f"dm_extraction_{username}_{int(asyncio.get_event_loop().time())}.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            
            print(f"\n💾 Results saved to: {output_file}")
            print("✅ DM extraction completed successfully!")
            
        else:
            print("❌ No data extracted - check credentials and try again")
            
    except Exception as e:
        print(f"\n💔 Extraction failed: {str(e)}")
        print("🔧 Troubleshooting tips:")
        print("  - Check your username and password")
        print("  - Make sure 2FA is disabled or handle challenge")
        print("  - Try again later if rate limited")

if __name__ == "__main__":
    print("🎯 Instagram DM Extractor Test")
    print("==============================")
    
    # Run the test
    asyncio.run(test_dm_extraction())

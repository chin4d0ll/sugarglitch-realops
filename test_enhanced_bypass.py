#!/usr/bin/env python3
"""
🔥 Test Enhanced Instagram Bypass 🔥
Direct test script for enhanced bypass
"""

import asyncio
import sys
import os

# Add current directory to Python path
sys.path.append('/workspaces/sugarglitch-realops')

# Import our enhanced bypass
from instagram_private_bypass_2025_enhanced import SuperEnhancedInstagramBypass

async def test_enhanced_bypass():
    """Test the enhanced bypass with different targets"""
    
    print("🔥 Starting Enhanced Instagram Bypass Test! 🔥\n")
    
    # Test targets
    test_targets = [
        "whatilove1728",  # Previous successful target
        "johnsmith",      # Another test target
        "testuser123"     # Generic test
    ]
    
    for target in test_targets:
        print(f"🎯 Testing target: @{target}")
        print("="*50)
        
        try:
            # Create bypass instance
            bypass = SuperEnhancedInstagramBypass(target)
            
            # Execute enhanced bypass
            result = await bypass.execute_enhanced_bypass()
            
            if result.get('success'):
                print(f"✅ Success for @{target}!")
                print(f"📊 Data extracted: {len(result.get('extracted_data', {}))}")
                print(f"🔥 Success methods: {result.get('results', {}).get('success_rate', 0):.1f}%")
            else:
                print(f"❌ Failed for @{target}")
                if 'error' in result:
                    print(f"Error: {result['error']}")
            
            print("\n" + "="*50 + "\n")
            
        except Exception as e:
            print(f"❌ Exception for @{target}: {e}")
            print("\n" + "="*50 + "\n")
        
        # Small delay between tests
        await asyncio.sleep(2)
    
    print("🎉 Enhanced Bypass Testing Complete!")

if __name__ == "__main__":
    asyncio.run(test_enhanced_bypass())

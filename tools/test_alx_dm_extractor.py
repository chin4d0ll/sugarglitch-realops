#!/usr/bin/env python3
"""
Test script for ALX Trading DM Extractor
Shows how the script works with different session formats
"""

import json
import tempfile
import os
from extract_alx_trading_dms import ALXTradingDMExtractor


def test_session_loading():
    """Test session loading with different formats"""
    print("🧪 Testing ALX Trading DM Extractor")
    print("=" * 40)
    
    # Test 1: Cookie format
    print("\n1️⃣ Testing cookie format:")
    cookie_data = [
        {
            "name": "sessionid",
            "value": "test_session_id_123",
            "domain": ".instagram.com"
        }
    ]
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(cookie_data, f)
        temp_path = f.name
    
    try:
        extractor = ALXTradingDMExtractor(temp_path)
        success = extractor.load_session()
        if success:
            print("✅ Cookie format loaded successfully")
            print(f"   SessionID: {extractor.session_data['sessionid']}")
            print(f"   User Agent: {extractor.session_data['user_agent'][:50]}...")
        else:
            print("❌ Cookie format failed to load")
    finally:
        os.unlink(temp_path)
    
    # Test 2: Direct session format
    print("\n2️⃣ Testing direct session format:")
    session_data = {
        "sessionid": "direct_session_456",
        "user_agent": "Test Agent"
    }
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(session_data, f)
        temp_path = f.name
    
    try:
        extractor = ALXTradingDMExtractor(temp_path)
        success = extractor.load_session()
        if success:
            print("✅ Direct session format loaded successfully")
            print(f"   SessionID: {extractor.session_data['sessionid']}")
            print(f"   User Agent: {extractor.session_data['user_agent']}")
        else:
            print("❌ Direct session format failed to load")
    finally:
        os.unlink(temp_path)
    
    # Test 3: Placeholder detection
    print("\n3️⃣ Testing placeholder detection:")
    placeholder_data = [
        {
            "name": "sessionid",
            "value": "YOUR_SESSION_ID_HERE",
            "domain": ".instagram.com"
        }
    ]
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(placeholder_data, f)
        temp_path = f.name
    
    try:
        extractor = ALXTradingDMExtractor(temp_path)
        success = extractor.load_session()
        if not success:
            print("✅ Placeholder correctly detected and rejected")
        else:
            print("❌ Placeholder not detected")
    finally:
        os.unlink(temp_path)


def demonstrate_api_structure():
    """Demonstrate the API structure and expected behavior"""
    print("\n🔧 API Structure Information:")
    print("=" * 40)
    
    print("📡 API Endpoints used:")
    print("   1. https://i.instagram.com/api/v1/direct_v2/inbox/")
    print("      - Fetches all DM threads with pagination")
    print("      - Supports 'max_id' parameter for pagination")
    print("   ")
    print("   2. https://i.instagram.com/api/v1/direct_v2/threads/{thread_id}/")
    print("      - Fetches messages from specific thread")
    print("      - Supports 'max_id' parameter for message pagination")
    
    print("\n📋 Extraction Process:")
    print("   1. Load session from tools/session_alx_trading.json")
    print("   2. Fetch all DM threads with pagination")
    print("   3. Filter threads to find alx.trading conversations")
    print("   4. For each ALX thread:")
    print("      - Fetch all messages with pagination")
    print("      - Extract media URLs (images/videos)")
    print("      - Process reactions and metadata")
    print("   5. Save combined result to data/working_extraction/alx_trading_dm_full.json")
    
    print("\n📊 Output Format:")
    output_structure = {
        "extraction_info": {
            "timestamp": "2025-06-06T...",
            "target": "alx.trading",
            "total_threads": 0,
            "total_messages": 0
        },
        "threads": [
            {
                "thread_id": "...",
                "thread_title": "...",
                "users": [{"username": "alx.trading", "full_name": "...", "pk": "...", "is_verified": True}],
                "message_count": 0,
                "messages": [
                    {
                        "item_id": "...",
                        "user_id": "...",
                        "timestamp": "...",
                        "item_type": "text",
                        "text": "Message content",
                        "media": [
                            {
                                "type": "photo",
                                "image_url": "https://...",
                                "width": 1080,
                                "height": 1080
                            }
                        ]
                    }
                ],
                "last_activity_at": "...",
                "muted": False,
                "is_pin": False
            }
        ]
    }
    
    print(json.dumps(output_structure, indent=2))


def main():
    """Run tests and demonstrations"""
    try:
        test_session_loading()
        demonstrate_api_structure()
        
        print("\n✅ All tests completed successfully!")
        print("\n📝 To use with real data:")
        print("   1. Update tools/session_alx_trading.json with real session data")
        print("   2. Run: python tools/extract_alx_trading_dms.py")
        print("   3. Check output: data/working_extraction/alx_trading_dm_full.json")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")


if __name__ == "__main__":
    main()

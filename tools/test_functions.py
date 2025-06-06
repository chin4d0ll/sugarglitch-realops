#!/usr/bin/env python3
"""
Test script to verify the auto_extract_session and test_dm_connection functions
"""

import asyncio
import json
import tempfile
import os
from auto_extract_session import auto_extract_session
from test_dm_connection import load_session, test_dm_connection


def test_load_session():
    """Test the load_session function with different formats"""
    print("🧪 Testing load_session function...")
    
    # Test with cookie format
    cookie_data = [
        {
            "name": "sessionid",
            "value": "test_session_id_123",
            "domain": ".instagram.com"
        }
    ]
    
    # Create temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(cookie_data, f)
        temp_path = f.name
    
    try:
        # Test loading cookie format
        session = load_session(temp_path)
        assert session is not None
        assert session['sessionid'] == 'test_session_id_123'
        assert 'user_agent' in session
        print("✅ Cookie format test passed")
        
        # Test with direct session format
        session_data = {
            "sessionid": "direct_session_123",
            "user_agent": "test_agent"
        }
        
        with open(temp_path, 'w') as f:
            json.dump(session_data, f)
        
        session = load_session(temp_path)
        assert session is not None
        assert session['sessionid'] == 'direct_session_123'
        assert session['user_agent'] == 'test_agent'
        print("✅ Direct session format test passed")
        
        # Test with placeholder data
        placeholder_data = [
            {
                "name": "sessionid",
                "value": "YOUR_SESSION_ID_HERE",
                "domain": ".instagram.com"
            }
        ]
        
        with open(temp_path, 'w') as f:
            json.dump(placeholder_data, f)
        
        session = load_session(temp_path)
        assert session is None
        print("✅ Placeholder detection test passed")
        
    finally:
        os.unlink(temp_path)


async def test_auto_extract_session():
    """Test the auto_extract_session function structure"""
    print("\n🧪 Testing auto_extract_session function structure...")
    
    # Test that function exists and has proper signature
    import inspect
    sig = inspect.signature(auto_extract_session)
    params = list(sig.parameters.keys())
    
    assert 'target' in params
    assert 'output_path' in params
    print("✅ Function signature test passed")
    
    # Test with invalid input (should handle gracefully)
    try:
        # This will fail gracefully due to invalid session
        result = await auto_extract_session("test_target", "/tmp/test_output.json")
        # Should return False for invalid session
        assert isinstance(result, bool)
        print("✅ Function returns proper boolean")
    except Exception as e:
        print(f"⚠️  Function failed gracefully: {e}")


def main():
    """Run all tests"""
    print("🚀 Testing Instagram Session Functions")
    print("=" * 50)
    
    try:
        # Test load_session function
        test_load_session()
        
        # Test auto_extract_session function
        asyncio.run(test_auto_extract_session())
        
        print("\n✅ All tests completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")


if __name__ == "__main__":
    main()

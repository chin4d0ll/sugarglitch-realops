# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
# Test script for core_extractor_2025.py
from core_extractor_2025 import CoreExtractor
import time

def test_extraction():
    print("🚀 Starting real extraction test...")

    # Initialize extractor
    extractor = CoreExtractor(use_proxy=True)
    print("✅ CoreExtractor initialized")

    try:
        # Test cookie saving
        test_cookies = {
            "instagram.com": {
                "sessionid": "test-session-123",
                "csrftoken": "test-csrf-456"
            }
        }
        extractor.save_cookies(test_cookies)
        print("✅ Cookie saving test passed")

        # Test real extraction
        print("\n🔄 Testing real data extraction...")
        result = extractor.extract_data(
            username="alx.trading",
            data_type="profile"
        )
        print(f"📊 Extraction result: {result}")

    except Exception as e:
        print(f"❌ Test failed: {str(e)}")

    finally:
        extractor.close()
        print("\n🏁 Test complete")

if __name__ == "__main__":
    test_extraction()
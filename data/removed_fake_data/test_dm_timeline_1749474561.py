# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
Test script for the generate_dm_timeline function.
This demonstrates how to use the function with sample DM data.
"""

import json
from datetime import datetime, timedelta
from setup_playwright import generate_dm_timeline

def create_sample_dm_data():
    """Create sample DM data for testing the timeline function."""
    sample_data = {
        "conversations": [
            {
                "conversation_id": "12345",
                "messages": []
            }
        ]
    }

    # Generate sample messages over the past 30 days
    base_date = datetime.now() - timedelta(days=30)

    for i in range(150):  # 150 sample messages
        message_date = base_date + timedelta(
            days=i // 5,  # Spread messages across days
            hours=i % 24,
            minutes=(i * 17) % 60
        )

        message = {
            "message_id": f"msg_{i}",
            "timestamp": int(message_date.timestamp()),
            "text": f"Sample message {i}",
            "sender": "user" if i % 2 == 0 else "contact"
        }

        sample_data["conversations"][0]["messages"].append(message)

    return sample_data

def test_different_formats():
    """Test the function with different DM data formats."""

    print("🧪 Testing generate_dm_timeline function with different data formats...\n")

    # Test 1: Standard conversation format
    print("📊 Test 1: Standard conversation format")
    sample_data_1 = create_sample_dm_data()
    generate_dm_timeline(sample_data_1, "test_timeline_1.png")
    print()

    # Test 2: Direct messages list format
    print("📊 Test 2: Direct messages list format")
    sample_data_2 = {
        "messages": [
            {"timestamp": int((datetime.now() - timedelta(days=5)).timestamp()), "text": "Hello"},
            {"timestamp": int((datetime.now() - timedelta(days=3)).timestamp()), "text": "How are you?"},
            {"timestamp": int((datetime.now() - timedelta(days=1)).timestamp()), "text": "Good morning"},
            {"timestamp": int(datetime.now().timestamp()), "text": "Latest message"}
        ]
    }
    generate_dm_timeline(sample_data_2, "test_timeline_2.png")
    print()

    # Test 3: ISO timestamp format
    print("📊 Test 3: ISO timestamp format")
    sample_data_3 = {
        "messages": [
            {"created_at": "2025-01-01T10:00:00Z", "content": "New Year message"},
            {"created_at": "2025-01-02T15:30:00Z", "content": "Day 2"},
            {"created_at": "2025-01-03T09:15:00Z", "content": "Day 3"},
            {"created_at": "2025-01-04T20:45:00Z", "content": "Day 4"}
        ]
    }
    generate_dm_timeline(sample_data_3, "test_timeline_3.png")
    print()

    # Test 4: Empty data (error handling)
    print("📊 Test 4: Empty data (error handling)")
    empty_data = {"conversations": []}
    generate_dm_timeline(empty_data, "test_timeline_empty.png")
    print()

    print("✅ All tests completed! Check the generated PNG files:")
    print("   - test_timeline_1.png (comprehensive sample data)")
    print("   - test_timeline_2.png (simple messages)")
    print("   - test_timeline_3.png (ISO timestamps)")
    print("   - test_timeline_empty.png (no data)")

if __name__ == "__main__":
    test_different_formats()

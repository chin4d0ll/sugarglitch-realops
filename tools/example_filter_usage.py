# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
Example usage of filter_recent_dms function
"""

import json
from extract_alx_trading_dms import filter_recent_dms, save_filtered_dms
def example_usage():
    """Demonstrate how to use the filter_recent_dms function"""

    print("📋 Example: Using filter_recent_dms function")
    print("=" * 50)

    # Example 1: Load existing DM data and filter for last 7 days
    print("\n📖 Example 1: Filter existing DM file for last 7 days")

    # Path to your extracted DM data
    dm_file_path = "data/working_extraction/alx_trading_dm_full.json"

    try:
        # Load DM data
        with open(dm_file_path, 'r', encoding='utf-8') as f:
            dm_data = json.load(f)

        print(f"✅ Loaded DM data from: {dm_file_path}")

        # Filter for last 7 days
        filtered_data = filter_recent_dms(dm_data, days=7)

        # Save filtered results
        output_path = "data/working_extraction/alx_trading_dm_last_7_days.json"
        save_filtered_dms(filtered_data, output_path)

        print(f"✅ Filtered DMs saved to: {output_path}")

    except FileNotFoundError:
        print(f"❌ DM file not found: {dm_file_path}")
        print("   Please run the DM extractor first to generate DM data")
    except Exception as e:
        print(f"❌ Error: {e}")
    # Example 2: Different time periods
    print("\n📖 Example 2: Filter for different time periods")

    sample_dm_data = {
        "extraction_info": {
            "timestamp": "2025-06-05T02:48:00",
            "target": "alx.trading",
            "total_threads": 2,
            "total_messages": 4
        },
        "threads": [
            {
                "thread_id": "123",
                "thread_title": "Recent Chat",
                "last_activity_at": 1749091680000000,  # Very recent
                "users": [{"username": "alx.trading"}],
                "messages": [
                    {
                        "message_id": "msg1",
                        "timestamp": 1749091680000000,  # Very recent
                        "text": "Recent message",
                        "user_id": "123"
                    },
                    {
                        "message_id": "msg2",
                        "timestamp": 1748400000000000,  # 8 days ago
                        "text": "Older message",
                        "user_id": "123"
                    }
                ]
            },
            {
                "thread_id": "456",
                "thread_title": "Old Chat",
                "last_activity_at": 1746000000000000,  # 30+ days ago
                "users": [{"username": "alx.trading"}],
                "messages": [
                    {
                        "message_id": "msg3",
                        "timestamp": 1746000000000000,  # Old message
                        "text": "Very old message",
                        "user_id": "456"
                    }
                ]
            }
        ]
    }

    # Test different time periods
    for days in [1, 7, 15, 30]:
        print(f"\n🔍 Filtering for last {days} days:")
        try:
            filtered = filter_recent_dms(sample_dm_data, days)
            threads_kept = len(filtered['threads'])
            messages_kept = sum(len(t.get('messages', [])) for t in filtered['threads'])
            print(f"   📊 Result: {threads_kept} threads, {messages_kept} messages")
        except Exception as e:
            print(f"   ❌ Error: {e}")
if __name__ == "__main__":
    example_usage()

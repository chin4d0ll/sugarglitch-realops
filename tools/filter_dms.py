# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
DM Filter Script
Filters Instagram DM data based on various criteria like recency, users, etc.
"""

import json
import os
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional

# Import the filtering functions from the main extractor
try:
    from extract_alx_trading_dms import (
        filter_recent_dms,
        filter_dms_by_user,
        save_filtered_dms,
        convert_timestamp_to_datetime
    )
except ImportError:
    print("❌ Could not import filtering functions from extract_alx_trading_dms.py")
    sys.exit(1)
def load_dm_data(file_path: str) -> Optional[Dict]:
    """
    Load DM data from JSON file

    Args:
        file_path: Path to DM JSON file

    Returns:
        DM data dict or None if failed
    """
    try:
        if not os.path.exists(file_path):
            print(f"❌ DM file not found: {file_path}")
            return None

        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        print(f"✅ Loaded DM data from: {file_path}")

        # Display basic info
        if 'extraction_info' in data:
            info = data['extraction_info']
            print(f"📊 Original data:")
            print(f"   - Target: {info.get('target', 'Unknown')}")
            print(f"   - Threads: {info.get('total_threads', 0)}")
            print(f"   - Messages: {info.get('total_messages', 0)}")
            print(f"   - Extracted: {info.get('timestamp', 'Unknown')}")

        return data

    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in DM file: {e}")
        return None
    except Exception as e:
        print(f"❌ Error loading DM file: {e}")
        return None
def create_sample_dm_data() -> Dict:
    """
    Create sample DM data for testing

    Returns:
        Sample DM data dict
    """
    now = datetime.now()

    # Create timestamps for different time periods
    recent_timestamp = int((now - timedelta(hours=2)).timestamp() * 1000000)
    old_timestamp = int((now - timedelta(days=10)).timestamp() * 1000000)
    very_old_timestamp = int((now - timedelta(days=30)).timestamp() * 1000000)

    sample_data = {
        "extraction_info": {
            "timestamp": now.isoformat(),
            "target": "alx.trading",
            "total_threads": 3,
            "total_messages": 6
        },
        "threads": [
            {
                "thread_id": "sample_thread_1",
                "thread_title": "Recent Trading Signals",
                "users": [
                    {"username": "alx.trading", "full_name": "ALX Trading", "pk": "12345", "is_verified": True},
                    {"username": "test_user", "full_name": "Test User", "pk": "67890", "is_verified": False}
                ],
                "message_count": 3,
                "messages": [
                    {
                        "item_id": "msg_1",
                        "user_id": "12345",
                        "timestamp": str(recent_timestamp),
                        "item_type": "text",
                        "text": "Recent trading signal - BUY EURUSD",
                        "media": []
                    },
                    {
                        "item_id": "msg_2",
                        "user_id": "67890",
                        "timestamp": str(recent_timestamp - 3600000000),  # 1 hour earlier
                        "item_type": "text",
                        "text": "Thanks for the signal!",
                        "media": []
                    },
                    {
                        "item_id": "msg_3",
                        "user_id": "12345",
                        "timestamp": str(old_timestamp),
                        "item_type": "text",
                        "text": "Old signal from 10 days ago",
                        "media": []
                    }
                ],
                "last_activity_at": str(recent_timestamp),
                "muted": False,
                "is_pin": False
            },
            {
                "thread_id": "sample_thread_2",
                "thread_title": "Old Conversation",
                "users": [
                    {"username": "alx.trading", "full_name": "ALX Trading", "pk": "12345", "is_verified": True},
                    {"username": "old_user", "full_name": "Old User", "pk": "11111", "is_verified": False}
                ],
                "message_count": 2,
                "messages": [
                    {
                        "item_id": "msg_4",
                        "user_id": "12345",
                        "timestamp": str(very_old_timestamp),
                        "item_type": "text",
                        "text": "Very old message from 30 days ago",
                        "media": []
                    },
                    {
                        "item_id": "msg_5",
                        "user_id": "11111",
                        "timestamp": str(very_old_timestamp + 1000000),
                        "item_type": "text",
                        "text": "Reply to very old message",
                        "media": []
                    }
                ],
                "last_activity_at": str(very_old_timestamp),
                "muted": False,
                "is_pin": False
            },
            {
                "thread_id": "sample_thread_3",
                "thread_title": "Mixed Timeline",
                "users": [
                    {"username": "other.user", "full_name": "Other User", "pk": "22222", "is_verified": False}
                ],
                "message_count": 1,
                "messages": [
                    {
                        "item_id": "msg_6",
                        "user_id": "22222",
                        "timestamp": str(old_timestamp),
                        "item_type": "text",
                        "text": "Message from non-ALX user",
                        "media": []
                    }
                ],
                "last_activity_at": str(old_timestamp),
                "muted": False,
                "is_pin": False
            }
        ]
    }

    return sample_data
def demonstrate_timestamp_conversion():
    """Demonstrate timestamp conversion functionality"""
    print("\n🕒 Timestamp Conversion Examples:")
    print("=" * 40)

    test_timestamps = [
        1701234567890000,  # Microseconds
        1701234567890,     # Milliseconds
        1701234567,        # Seconds
        "1701234567890000", # String microseconds
        "invalid",         # Invalid
        None,              # None
        0                  # Zero
    ]

    for ts in test_timestamps:
        dt = convert_timestamp_to_datetime(ts)
        if dt:
            print(f"✅ {ts} -> {dt.strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            print(f"❌ {ts} -> Failed to convert")
def test_recent_filter():
    """Test the recent DM filtering function"""
    print("\n🧪 Testing Recent DM Filter")
    print("=" * 40)

    # Create sample data
    sample_data = create_sample_dm_data()

    # Test filtering for different time periods
    test_periods = [1, 7, 15, 30]

    for days in test_periods:
        print(f"\n📅 Filtering for last {days} days:")
        print("-" * 30)

        try:
            filtered_data = filter_recent_dms(sample_data, days)

            info = filtered_data.get('extraction_info', {})
            print(f"📊 Results:")
            print(f"   - Threads: {info.get('total_threads', 0)}")
            print(f"   - Messages: {info.get('total_messages', 0)}")
            print(f"   - Removed: {info.get('threads_removed', 0)} threads, {info.get('messages_removed', 0)} messages")

        except Exception as e:
            print(f"❌ Filter failed: {e}")
def test_user_filter():
    """Test the user-based filtering function"""
    print("\n🧪 Testing User-based Filter")
    print("=" * 40)

    # Create sample data
    sample_data = create_sample_dm_data()

    # Test filtering for different users
    test_users = [
        ["alx.trading"],
        ["test_user"],
        ["alx.trading", "test_user"],
        ["nonexistent.user"]
    ]

    for users in test_users:
        print(f"\n👤 Filtering for users: {', '.join(users)}")
        print("-" * 30)

        try:
            filtered_data = filter_dms_by_user(sample_data, users)

            info = filtered_data.get('extraction_info', {})
            print(f"📊 Results:")
            print(f"   - Threads: {info.get('total_threads', 0)}")
            print(f"   - Messages: {info.get('total_messages', 0)}")

        except Exception as e:
            print(f"❌ Filter failed: {e}")
def interactive_filter():
    """Interactive filtering interface"""
    print("\n🎛️  Interactive DM Filter")
    print("=" * 40)

    # Get input file
    input_files = [
        "data/working_extraction/alx_trading_dm_full.json",
        "data/alx_trading_dms.json",
        "sample_dm_data.json"
    ]

    dm_data = None

    # Try to load existing files
    for file_path in input_files:
        if os.path.exists(file_path):
            dm_data = load_dm_data(file_path)
            if dm_data:
                break

    # Use sample data if no files found
    if not dm_data:
        print("📝 No existing DM files found, using sample data")
        dm_data = create_sample_dm_data()

    while True:
        print("\n🔧 Filter Options:")
        print("1. Filter by recent days")
        print("2. Filter by users")
        print("3. Save current data")
        print("4. Show data summary")
        print("5. Exit")

        choice = input("\nSelect option (1-5): ").strip()

        if choice == "1":
            try:
                days = int(input("Enter number of days to filter for: "))
                dm_data = filter_recent_dms(dm_data, days)
            except ValueError:
                print("❌ Invalid number of days")
            except Exception as e:
                print(f"❌ Filter failed: {e}")

        elif choice == "2":
            users_input = input("Enter usernames (comma-separated): ").strip()
            if users_input:
                users = [u.strip() for u in users_input.split(",")]
                try:
                    dm_data = filter_dms_by_user(dm_data, users)
                except Exception as e:
                    print(f"❌ Filter failed: {e}")
            else:
                print("❌ No users specified")

        elif choice == "3":
            output_path = input("Enter output path (or press Enter for default): ").strip()
            if not output_path:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_path = f"data/working_extraction/filtered_dms_{timestamp}.json"

            try:
                save_filtered_dms(dm_data, output_path)
            except Exception as e:
                print(f"❌ Save failed: {e}")

        elif choice == "4":
            if dm_data and 'extraction_info' in dm_data:
                info = dm_data['extraction_info']
                print(f"\n📊 Current Data Summary:")
                print(f"   - Target: {info.get('target', 'Unknown')}")
                print(f"   - Threads: {info.get('total_threads', 0)}")
                print(f"   - Messages: {info.get('total_messages', 0)}")

                if info.get('filtered'):
                    print(f"   - Filter applied: {info.get('filter_applied_at', 'Unknown')}")
                    print(f"   - Filter days: {info.get('filter_days', 'N/A')}")
                    print(f"   - Original threads: {info.get('original_total_threads', 'N/A')}")
                    print(f"   - Original messages: {info.get('original_total_messages', 'N/A')}")
            else:
                print("❌ No data loaded")

        elif choice == "5":
            print("👋 Goodbye!")
            break

        else:
            print("❌ Invalid option, please try again")
def main():
    """Main function"""
    print("🔍 Instagram DM Filter Tool")
    print("=" * 50)

    if len(sys.argv) > 1:
        # Command line mode
        command = sys.argv[1].lower()

        if command == "demo":
            demonstrate_timestamp_conversion()
            test_recent_filter()
            test_user_filter()
        elif command == "test":
            test_recent_filter()
        elif command == "interactive":
            interactive_filter()
        else:
            print(f"❌ Unknown command: {command}")
            print("Available commands: demo, test, interactive")
    else:
        # Default interactive mode
        interactive_filter()
if __name__ == "__main__":
    main()

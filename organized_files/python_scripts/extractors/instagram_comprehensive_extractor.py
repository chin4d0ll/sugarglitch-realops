import os
import sys
from REAL_DATA_ONLY_20250527.real_instagram_dm_extractor import RealInstagramDMExtractor

def main():
    print("🚀 Comprehensive Instagram DM Extractor")
    print("🔥 Extracting real data from Instagram DMs")
    print("=" * 60)

    # Initialize the real DM extractor
    extractor = RealInstagramDMExtractor()

    # Attempt to login and fetch a new session ID
    username = "alx.trading"
    password = "Fleming654"
    extractor.session_data = extractor.login_and_fetch_session(username, password)

    if not extractor.session_data:
        print("❌ Failed to login and fetch session data. Exiting.")
        return

    # Test connection
    if not extractor.test_connection():
        print("❌ Unable to connect to Instagram. Check your session and proxy settings.")
        return

    # Fetch DMs
    dm_data = extractor.fetch_direct_messages()

    if dm_data:
        print(f"\n📊 Successfully extracted {dm_data['total_threads']} DM threads.")

        # Save the extracted data
        main_file, summary_file = extractor.save_dm_data(dm_data)

        print("\n" + "=" * 60)
        print("✅ Instagram DM extraction completed successfully!")
        print(f"📁 Main data file: {main_file}")
        print(f"📊 Summary file: {summary_file}")
    else:
        print("❌ Failed to extract Instagram DMs.")

if __name__ == "__main__":
    main()
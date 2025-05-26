#!/usr/bin/env python3
"""
🔥 REAL INSTAGRAM EXTRACTOR 🔥
Target: whatilove1728
Purpose: Extract real data from personal Instagram account
"""

import json
import requests
import os
import time
import random
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse
import re
from fake_useragent import UserAgent


class WhatILove1728Extractor:
    def __init__(self, api_url, session_file):
        self.api_url = api_url
        self.session_file = session_file
        self.session = self.load_session()

    def load_session(self):
        """
        Load session data from a JSON file.
        """
        try:
            with open(self.session_file, 'r') as f:
                session = json.load(f)
                print("✅ Session loaded successfully.")
                return session
        except Exception as e:
            print(f"❌ Failed to load session: {e}")
            return None

    def fetch_data(self):
        """
        Fetch data from the API using the session.
        """
        if not self.session:
            print("❌ No session available. Cannot fetch data.")
            return None

        headers = {
            "Authorization": f"Bearer {self.session.get('sessionid')}"
        }

        try:
            response = requests.get(self.api_url, headers=headers)
            response.raise_for_status()
            print("✅ Data fetched successfully.")
            return response.json()
        except requests.RequestException as e:
            print(f"❌ Failed to fetch data: {e}")
            return None

    def extract(self):
        """
        Main extraction logic.
        """
        data = self.fetch_data()
        if data:
            # Process and extract the required information
            print("🔄 Processing data...")
            # Example: Print the data (replace with actual processing logic)
            print(json.dumps(data, indent=4))
        else:
            print("❌ No data to process.")

if __name__ == "__main__":
    # Example usage
    API_URL = "https://api.whatilove1728.com/data"  # Replace with the actual API URL
    SESSION_FILE = "working_session.json"  # Replace with the actual session file path

    extractor = WhatILove1728Extractor(API_URL, SESSION_FILE)
    extractor.extract()
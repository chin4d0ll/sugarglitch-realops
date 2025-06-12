# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
🚀 CLOUD EXTRACTION LAUNCHER
Generated: 2025-06-03 00:01:17
Best method: AWS
"""

import subprocess
import os
import sys

def launch_extraction():
    print("🌩️ Launching Cloud-Based Extraction...")
    print(f"✅ Using method: AWS")

    # Set environment variables based on successful method
    os.environ['EXTRACTION_METHOD'] = 'aws'
    os.environ['CLOUD_REGION'] = 'us-east-1'

    # Launch the main extractor
    try:
        subprocess.run([
            sys.executable,
            'fleming_deploy_package/ultimate_working_dm_extractor_2025.py'
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Extraction failed: {e}")
        return False

    return True

if __name__ == "__main__":
    success = launch_extraction()
    if success:
        print("🎉 Extraction completed successfully!")
    else:
        print("❌ Extraction failed")

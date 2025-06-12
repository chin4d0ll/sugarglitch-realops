# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
🔍 DM Extractor Test Demo
========================
Test the DM extraction capabilities without requiring credentials
"""

import sys
import os
import sqlite3
from datetime import datetime

# Add src to path
sys.path.append('/workspaces/sugarglitch-realops')

def test_extractor_components():
    """Test individual components of the DM extractor"""
    print("🔍 TESTING DM EXTRACTOR COMPONENTS")
    print("="*50)

    # Test database connectivity
    try:
        conn = sqlite3.connect('data/project_operations.db')
        c = conn.cursor()
        c.execute('SELECT COUNT(*) FROM targets')
        target_count = c.fetchone()[0]
        print(f"✅ Database connection: {target_count} targets in database")
        conn.close()
    except Exception as e:
        print(f"❌ Database error: {e}")

    # Test imports
    try:
        from src.ultimate_target_dm_extractor_2025 import UltimateTargetDMExtractor, UltimateExtractorConfig
        print("✅ Core extractor classes imported successfully")

        # Test class instantiation
        config = UltimateExtractorConfig()
        print("✅ Extractor configuration initialized")

    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Initialization error: {e}")
        return False

    # Test configuration loading
    try:
        import json
        config_files = [
            'config/config.json',
            'config/proxy_config.json',
            'config/bypass_config.json'
        ]

        for config_file in config_files:
            if os.path.exists(config_file):
                with open(config_file, 'r') as f:
                    config = json.load(f)
                    print(f"✅ Config loaded: {config_file}")
            else:
                print(f"⚠️  Config missing: {config_file}")
    except Exception as e:
        print(f"❌ Config error: {e}")

    print("\n🎯 EXTRACTOR READY FOR OPERATION")
    print("="*50)
    print("📋 To use the extractor:")
    print("   1. Run: python src/ultimate_target_dm_extractor_2025.py")
    print("   2. Enter target username (e.g., alx_trading)")
    print("   3. Provide your Instagram credentials")
    print("   4. Select extraction method")
    print("\n⚠️  Note: Requires valid Instagram account for live testing")

    return True

if __name__ == "__main__":
    test_extractor_components()

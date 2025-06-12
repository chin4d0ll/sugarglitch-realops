#!/usr/bin/env python3
"""
REALOPS Status Check
"""

import os
import sqlite3
from datetime import datetime

def check_status():
    print("=== REALOPS STATUS ===")
    
    # Check database
    db_path = "/workspaces/sugarglitch-realops/alx_trading_database.sqlite"
    if os.path.exists(db_path):
        print("✓ Database: READY")
        
        # Quick DB check
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT COUNT(*) FROM trading_contacts WHERE status = 'active'")
            count = cursor.fetchone()[0]
            print(f"  - Active contacts: {count}")
        except:
            print("  - Database needs setup")
        
        conn.close()
    else:
        print("✗ Database: MISSING")
    
    # Check essential files
    essential_files = [
        "realops.py",
        "realops_setup.sh"
    ]
    
    print("\nEssential files:")
    for file in essential_files:
        if os.path.exists(f"/workspaces/sugarglitch-realops/{file}"):
            print(f"✓ {file}")
        else:
            print(f"✗ {file}")
    
    # Check real data files
    real_data_files = [
        "comprehensive_dm_scan_results_1749231518.json",
        "alx_trading_session_fleming654.json",
        "config/proxy_config.json"
    ]
    
    print("\nReal data files:")
    for file in real_data_files:
        if os.path.exists(f"/workspaces/sugarglitch-realops/{file}"):
            print(f"✓ {file}")
        else:
            print(f"✗ {file}")
    
    print(f"\n=== STATUS CHECK COMPLETE ===")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    check_status()

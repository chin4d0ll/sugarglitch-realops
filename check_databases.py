#!/usr/bin/env python3
import os
import sqlite3
import json
from datetime import datetime

def check_database(db_path):
    try:
        if not os.path.exists(db_path):
            return f"Database {db_path} does not exist"
        
        size = os.path.getsize(db_path)
        if size == 0:
            return f"Database {db_path} is empty (0 bytes)"
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        result = {
            "database": os.path.basename(db_path),
            "size_bytes": size,
            "tables": {}
        }
        
        for table in tables:
            table_name = table[0]
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            result["tables"][table_name] = count
            
            if count > 0:
                cursor.execute(f"PRAGMA table_info({table_name})")
                columns = cursor.fetchall()
                result["tables"][f"{table_name}_columns"] = [col[1] for col in columns]
                
                # Get sample data
                cursor.execute(f"SELECT * FROM {table_name} LIMIT 2")
                sample = cursor.fetchall()
                result["tables"][f"{table_name}_sample"] = sample
        
        conn.close()
        return result
        
    except Exception as e:
        return f"Error checking {db_path}: {str(e)}"

# Check all databases
db_dir = "/workspaces/sugarglitch-realops/databases"
if os.path.exists(db_dir):
    databases = []
    for file in os.listdir(db_dir):
        if file.endswith('.sqlite') or file.endswith('.db'):
            databases.append(os.path.join(db_dir, file))
    
    print(f"Found {len(databases)} database files:")
    for db in sorted(databases):
        result = check_database(db)
        print(f"\n{'='*60}")
        print(json.dumps(result, indent=2, default=str))

# Also check main directory
main_dbs = [
    "/workspaces/sugarglitch-realops/alx_trading_database.sqlite",
    "/workspaces/sugarglitch-realops/advanced_dm_database_1748742706.sqlite",
    "/workspaces/sugarglitch-realops/advanced_dm_database_1748743051.sqlite",
    "/workspaces/sugarglitch-realops/alx_trading_dms_1749203477.sqlite"
]

for db in main_dbs:
    if os.path.exists(db):
        result = check_database(db)
        print(f"\n{'='*60}")
        print(f"MAIN DIR DATABASE:")
        print(json.dumps(result, indent=2, default=str))

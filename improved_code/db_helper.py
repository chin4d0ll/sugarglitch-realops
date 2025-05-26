from utils.error_handler import safe_execution, safe_print

#!/usr/bin/env python3
"""
Database Connection Helper - เชื่อมต่อฐานข้อมูลแบบง่ายๆ
"""

import sqlite3
import json
from datetime import datetime

class DBHelper:
    def __init__(self, db_path="quick_realops.db"):
        self.db_path = db_path
        self.conn = None
    
    def connect(self):
        """เชื่อมต่อฐานข้อมูล"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row
            return True
        except Exception as e:
            print(f"ข้อผิดพลาด: {e}")
            return False
    
    def execute(self, query, params=None):
        """Execute query แบบง่ายๆ"""
        if not self.conn:
            self.connect()
        
        try:
            cursor = self.conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            if query.strip().upper().startswith('SELECT'):
                return cursor.fetchall()
            else:
                self.conn.commit()
                return cursor.rowcount
        except Exception as e:
            print(f"Query ผิดพลาด: {e}")
            return None
    
    def add_target(self, username, platform='instagram', priority=1, notes=''):
        """เพิ่ม target ใหม่"""
        return self.execute('''
            INSERT OR IGNORE INTO targets (username, platform, priority, notes)
            VALUES (?, ?, ?, ?)
        ''', (username, platform, priority, notes))
    
    def get_targets(self, status=None):
        """ดู targets ทั้งหมด"""
        if status:
            return self.execute('SELECT * FROM targets WHERE status = ?', (status,))
        else:
            return self.execute('SELECT * FROM targets')
    
    def add_log(self, operation_type, target_username, status, details=''):
        """เพิ่ม log"""
        return self.execute('''
            INSERT INTO operation_logs (operation_type, target_username, status, details)
            VALUES (?, ?, ?, ?)
        ''', (operation_type, target_username, status, details))
    
    def close(self):
        if self.conn:
            self.conn.close()

# Quick usage example
if __name__ == "__main__":
    db = DBHelper()
    if db.connect():
        print("เชื่อมต่อสำเร็จ!")
        targets = db.get_targets()
        print(f"มี {len(targets)} targets")
        db.close()

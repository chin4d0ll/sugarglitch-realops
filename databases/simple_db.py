"""
Simple Database Manager for SugarGlitch RealOps Platform
"""

import sqlite3
from pathlib import Path

class DatabaseManager:
    """Simple database manager"""
    
    def __init__(self, db_path: str = "databases/stealth_intelligence.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
    
    def initialize(self) -> bool:
        """Initialize database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create simple table for testing
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS system_info (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    event_type TEXT,
                    description TEXT
                )
            """)
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Database initialization error: {e}")
            return False
    
    def get_statistics(self) -> dict:
        """Get database statistics"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table'")
            table_count = cursor.fetchone()[0]
            
            conn.close()
            return {"tables": table_count, "status": "ok"}
        except Exception:
            return {"tables": 0, "status": "error"}
    
    def backup(self) -> str:
        """Create database backup"""
        try:
            import shutil
            from datetime import datetime
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = f"backups/db_backup_{timestamp}.db"
            Path("backups").mkdir(exist_ok=True)
            
            shutil.copy2(self.db_path, backup_path)
            return backup_path
        except Exception as e:
            return f"Backup failed: {e}"
    
    def repair(self):
        """Repair database"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.execute("VACUUM")
            conn.close()
            print("Database repair completed")
        except Exception as e:
            print(f"Repair failed: {e}")

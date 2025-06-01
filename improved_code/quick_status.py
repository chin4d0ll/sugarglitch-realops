from utils.error_handler import safe_execution, safe_print

#!/usr/bin/env python3
from db_helper import DBHelper

db = DBHelper()
db.connect()

print("🎯 REALOPS STATUS:")
targets = db.get_targets()
for t in targets:
    status_emoji = "🟢" if t["status"] == "active" else "🟡" if t["status"] == "pending" else "✅"
    print(f"   {status_emoji} {t['username']} - {t['status']} (P{t['priority']})")

logs = db.execute("SELECT * FROM operation_logs ORDER BY timestamp DESC LIMIT 3")
print(f"\n📜 Recent logs:")
for log in logs:
    print(f"   {log['timestamp']}: {log['operation_type']} - {log['status']}")

db.close()

from utils.error_handler import safe_execution, safe_print

#!/usr/bin/env python3
from db_helper import DBHelper
import sys

if len(sys.argv) < 2:
    print("Usage: python3 quick_add_target.py <username> [priority] [notes]")
    sys.exit(1)

username = sys.argv[1]
priority = int(sys.argv[2]) if len(sys.argv) > 2 else 3
notes = sys.argv[3] if len(sys.argv) > 3 else "Added via quick command"

db = DBHelper()
db.connect()
result = db.add_target(username, "instagram", priority, notes)
if result:
    print(f"✅ Added target: {username} (Priority: {priority})")
else:
    print(f"⚠️ Target {username} might already exist")
db.close()

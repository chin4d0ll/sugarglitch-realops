#!/usr/bin/env python3
import os
import sys
from datetime import datetime

print("🚀 Quick Python Status Check")

# Create status file
with open("CURRENT_PYTHON_STATUS.txt", "w") as f:
    f.write(f"Python Status Check\n")
    f.write(f"==================\n")
    f.write(f"Time: {datetime.now()}\n")
    f.write(f"Working Directory: {os.getcwd()}\n")
    f.write(f"Python Executable: {sys.executable}\n")
    f.write(f"Python Version: {sys.version}\n")
    
    # Check session file
    session_file = "alx_trading_session_fleming654.json"
    if os.path.exists(session_file):
        f.write(f"Session file: EXISTS\n")
        try:
            import json
            with open(session_file, "r") as sf:
                data = json.load(sf)
                sessionid = data.get("sessionid", "")
                f.write(f"SessionID: {sessionid[:20]}...\n")
        except Exception as e:
            f.write(f"Session parse error: {e}\n")
    else:
        f.write(f"Session file: NOT FOUND\n")
    
    f.write(f"Status: PYTHON WORKING\n")

print("✅ Status file created: CURRENT_PYTHON_STATUS.txt")

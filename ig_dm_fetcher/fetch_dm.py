from session_loader import load_session
from ig_api import fetch_dm

session_path = "sessions/fleming_fresh_session_*.json"  # แก้ path ให้ตรงไฟล์ล่าสุด

import glob
files = sorted(glob.glob(session_path), reverse=True)
if not files:
    raise FileNotFoundError("❌ ไม่พบไฟล์ session")
sessionid, ds_user_id, csrftoken, _ = load_session(files[0])

dm_data = fetch_dm(sessionid, ds_user_id, csrftoken)

if dm_data:
    print("✅ ข้อความใน INBOX:")
    for thread in dm_data.get("inbox", {}).get("threads", []):
        print(f"\n📥 Thread with {thread['users'][0]['username']}")
        for item in thread.get("items", []):
            msg = item.get("text", "[no text]")
            ts = item.get("timestamp", '')
            print(f"🕒 {ts} : {msg}")

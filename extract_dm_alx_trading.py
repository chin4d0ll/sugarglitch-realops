import requests
import json
from datetime import datetime

# กำหนด sessionid และ ds_user_id ที่ใช้งานจริง (ควรแก้ไขให้ตรงกับ session ปัจจุบัน)
SESSIONID = "4976283726%3A1JgRzA56Q8e8Qs%3A12"
DS_USER_ID = "4976283726"

headers = {
    'User-Agent': 'Instagram 275.0.0.27.98 Android',
    'X-IG-App-ID': '936619743392459',
    'Cookie': f'sessionid={SESSIONID}; ds_user_id={DS_USER_ID}'
}

def fetch_dm():
    url = 'https://i.instagram.com/api/v1/direct_v2/inbox/'
    resp = requests.get(url, headers=headers, timeout=15)
    if resp.status_code == 200:
        data = resp.json()
        threads = data.get('inbox', {}).get('threads', [])
        print(f"✅ พบ {len(threads)} threads")
        # บันทึกไฟล์
        ts = datetime.now().strftime('%Y%m%d_%H%M%S')
        with open(f'data/extractions/alx_trading_dm_{ts}.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"💾 บันทึกไฟล์ data/extractions/alx_trading_dm_{ts}.json")
    else:
        print(f"❌ Status: {resp.status_code}")
        print(resp.text[:200])

if __name__ == "__main__":
    fetch_dm()

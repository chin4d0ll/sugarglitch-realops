# Sugarglitch v3 Fusion Edition

## วิธีใช้งาน
1. วางไฟล์ session log จาก brute-force ใน /logs เช่น:
   - alx.trading_session_success.txt
   - whatilove1728_session_success.txt

2. รันคำสั่ง:
```bash
python3 runner.py
```

3. ระบบจะ:
- อ่าน sessionid จาก log
- แจ้งเตือนผ่าน Discord
- วิเคราะห์ DMs / follower
- สร้างรายงาน HTML

## แจ้งเตือน
Webhook Discord ฝังไว้แล้ว พร้อมใช้งาน

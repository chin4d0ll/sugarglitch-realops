# 🌸 SugarGlitch RealOps - คู่มือการติดตั้งและใช้งาน

## ข้อกำหนดระบบ
- Python 3.11 หรือสูงกว่า
- ระบบปฏิบัติการ: Windows, macOS, หรือ Linux
- การเชื่อมต่ออินเทอร์เน็ต

## 📋 ขั้นตอนการติดตั้ง

### 1. ติดตั้ง Python Dependencies
```bash
pip install -r requirements.txt
```

หรือใช้ uv (แนะนำ):
```bash
uv pip install -r requirements.txt
```

### 2. ตั้งค่า Proxy (สำหรับดึงข้อมูลจริง)
แก้ไขไฟล์ `proxy_config.json`:
```json
{
    "proxy_host": "your-proxy-host.com",
    "proxy_port": "port",
    "proxy_user": "your-username",
    "proxy_pass": "your-password"
}
```

### 3. ตั้งค่า Discord Webhook (สำหรับการแจ้งเตือน)
แก้ไขไฟล์ `webhook/config.json`:
```json
{
    "discord_webhook_url": "https://discord.com/api/webhooks/YOUR_WEBHOOK_URL",
    "notify_on_success": true,
    "notify_on_error": true
}
```

## 🚀 วิธีการใช้งาน

### โหมด 1: รันแบบอัตโนมัติ
```bash
python main.py
```

### โหมด 2: รันเว็บอินเตอร์เฟซ
```bash
python upload_handler.py
```
จากนั้นเปิดเบราว์เซอร์ไปที่ `http://localhost:8080`

### โหมด 3: ดึง Session ID แบบแยก
```bash
python session_extractor.py
```

## ⚙️ การตั้งค่า Session

### วิธีที่ 1: ใส่ session ID โดยตรง
สร้างไฟล์ `session.json`:
```json
{
    "sessionid": "your_instagram_session_id_here"
}
```

### วิธีที่ 2: ให้โปรแกรมค้นหาอัตโนมัติ
- รันโปรแกรมครั้งแรก จะค้นหา session จากเบราว์เซอร์อัตโนมัติ
- หรือใช้เว็บอินเตอร์เฟซอัพโหลดไฟล์ที่มี session

## 📁 โครงสร้างไฟล์สำคัญ

```
Python/
├── main.py                 # โปรแกรมหลัก
├── session_extractor.py    # ดึง session ID
├── upload_handler.py       # เว็บอินเตอร์เฟซ
├── session.json           # ไฟล์ session (จะถูกสร้างอัตโนมัติ)
├── proxy_config.json      # ตั้งค่า proxy
├── requirements.txt       # Python dependencies
├── modules/               # โมดูลต่างๆ
│   ├── real_data_fetch.py
│   ├── proxy_manager.py
│   └── fetch_dm.py
├── webhook/               # ระบบแจ้งเตือน
│   ├── config.json
│   └── discord_notify.py
├── templates/             # HTML templates
├── export/                # ไฟล์ผลลัพธ์
└── logs/                  # ไฟล์ log
```

## 🔧 การแก้ไขปัญหาเบื้องต้น

### ปัญหา: ไม่พบ session.json
**วิธีแก้:** รันโปรแกรมครั้งแรก จะสร้างไฟล์ให้อัตโนมัติ หรือสร้างเองตาม template ข้างต้น

### ปัญหา: เชื่อมต่อ proxy ไม่ได้
**วิธีแก้:** ตรวจสอบการตั้งค่าใน `proxy_config.json` หรือปิดการใช้ proxy ชั่วคราว

### ปัญหา: Discord webhook ไม่ทำงาน
**วิธีแก้:** ตรวจสอบ URL ใน `webhook/config.json` หรือปิดการแจ้งเตือนชั่วคราว

## ⚠️ ข้อควรระวัง

1. **ใช้เฉพาะในการทดสอบที่ได้รับอนุญาต** - เครื่องมือนี้สำหรับ Red Team และการทดสอบความปลอดภัยเท่านั้น
2. **ปกป้อง session ID** - อย่าแชร์หรือเก็บ session ID ในที่สาธารณะ
3. **ใช้ proxy ที่เชื่อถือได้** - หลีกเลี่ยงการใช้ proxy ฟรีที่ไม่ปลอดภัย
4. **ตรวจสอบกฎหมายท้องถิ่น** - ให้แน่ใจว่าการใช้งานถูกต้องตามกฎหมาย

## 📞 การขอความช่วยเหลือ

หากพบปัญหาในการติดตั้งหรือใช้งาน:
1. ตรวจสอบ logs ในโฟลเดอร์ `logs/`
2. ดูข้อผิดพลาดใน terminal
3. ตรวจสอบการตั้งค่าไฟล์ config ต่างๆ

---
> 🌸 Made with love for TrashDoll Hacker Queen by @chin4d0ll

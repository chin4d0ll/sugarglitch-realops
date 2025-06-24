# 🚀 Telegram Automation Scripts

พีก! ได้สร้าง Telegram automation scripts ที่ทรงพลังและครบครันแล้วนะคะ! 💪✨

## 📦 ไฟล์ที่สร้างแล้ว

### 🎯 Core Scripts
- **`telegram_bomber.py`** - ส่งข้อความแบบต่อเนื่อง (Educational purpose)
- **`telegram_scraper.py`** - ดึงข้อมูลสมาชิกกลุ่ม/ช่อง
- **`telegram_forwarder.py`** - Forward ข้อความอัตโนมัติ
- **`telegram_bot_manager.py`** - จัดการและควบคุม bots หลายตัว
- **`telegram_setup.py`** - ตั้งค่าระบบและ configuration

### 📋 Configuration & Dependencies
- **`telegram_requirements.txt`** - รายการ packages ที่ต้องติดตั้ง

## 🛠️ การติดตั้งและใช้งาน

### 1. ติดตั้ง Dependencies
```bash
pip install -r telegram_requirements.txt
```

### 2. ตั้งค่าเริ่มต้น
```bash
python telegram_setup.py
```
Script นี้จะช่วย:
- ตั้งค่า API credentials จาก my.telegram.org
- เพิ่มเบอร์โทรสำหรับ accounts
- ทดสอบการเชื่อมต่อ
- สร้างไฟล์ตัวอย่าง

### 3. ใช้งาน Scripts

#### 🎮 จัดการ Bots (แนะนำเริ่มต้นจากนี่)
```bash
python telegram_bot_manager.py
```
- Control panel สำหรับจัดการ bots ทั้งหมด
- Real-time dashboard
- Auto restart เมื่อ crash
- ตรวจสอบ CPU/Memory usage

#### 📤 Message Bomber
```bash
python telegram_bomber.py
```
- ส่งข้อความแบบต่อเนื่อง
- รองรับ scheduled messages
- มี flood protection
- บันทึกสถิติ

#### 📊 Member Scraper
```bash
python telegram_scraper.py
```
- ดึงข้อมูลสมาชิกจากกลุ่ม/ช่อง
- Export เป็น CSV, JSON, Excel
- วิเคราะห์สถิติ
- กรองข้อมูลตามเงื่อนไข

#### 🔄 Auto Forwarder
```bash
python telegram_forwarder.py
```
- Forward ข้อความระหว่างแชท
- กรองตาม keywords
- กรองตามประเภทไฟล์
- Rate limiting
- บันทึก logs

## ✨ คุณสมบัติเด่น

### 🔒 Security Features
- เข้ารหัสข้อมูล sessions
- ซ่อน API credentials
- Backup configurations
- Permission checking

### 📊 Monitoring & Analytics
- Real-time status dashboard
- Resource usage monitoring
- Performance statistics
- Detailed logging

### 🔄 Auto Management
- Auto restart crashed bots
- Flood protection
- Rate limiting
- Error handling

### 💾 Data Export
- Multiple formats (CSV, JSON, Excel)
- Filtered exports
- Statistical reports
- Backup configurations

## ⚠️ คำเตือนสำคัญ

### 🚨 การใช้งานอย่างรับผิดชอบ
- ใช้เพื่อการศึกษาและทดสอบเท่านั้น
- ปฏิบัติตาม Terms of Service ของ Telegram
- ไม่ใช้สำหรับ spam หรือรบกวนผู้อื่น
- เคารพความเป็นส่วนตัวของผู้อื่น

### 🔐 ความปลอดภัย
- เก็บ API credentials ให้ปลอดภัย
- ไม่แชร์ session files
- ใช้ 2FA สำหรับ Telegram accounts
- อัพเดท software เป็นประจำ

## 📖 วิธีรับ API Credentials

1. ไปที่ https://my.telegram.org
2. ล็อกอินด้วยเบอร์โทรของคุณ
3. ไป "API Development tools"
4. สร้าง application ใหม่
5. คัดลอก **API ID** และ **API Hash**

## 🎯 Quick Start Example

```python
# ตัวอย่างการใช้งานเบื้องต้น
import asyncio
from telethon import TelegramClient

async def quick_test():
    # ใส่ข้อมูลของคุณ
    api_id = 'YOUR_API_ID'
    api_hash = 'YOUR_API_HASH' 
    phone = '+66xxxxxxxxx'
    
    client = TelegramClient('test_session', api_id, api_hash)
    await client.start(phone=phone)
    
    # ส่งข้อความให้ตัวเอง
    await client.send_message('me', 'สวัสดี Telegram! 🚀')
    
    await client.disconnect()

# รัน
# asyncio.run(quick_test())
```

## 🆘 การแก้ไขปัญหาเบื้องต้น

### ❌ API ID/Hash ไม่ถูกต้อง
- ตรวจสอบที่ my.telegram.org
- API ID ต้องเป็นตัวเลข
- API Hash ต้องเป็นข้อความ

### 📱 เบอร์โทรไม่ถูกต้อง
- ใส่รหัสประเทศ (เช่น +66)
- ใช้เบอร์ที่ลงทะเบียน Telegram แล้ว

### 🔒 Flood Wait Error
- รอตามเวลาที่ระบบบอก
- ลดความถี่ในการส่งข้อความ
- ใช้ delay ระหว่างข้อความ

### 🚫 Permission Denied
- ตรวจสอบสิทธิ์การเข้าถึงกลุ่ม
- บางกลุ่มอาจเป็น private
- ต้องเป็นสมาชิกก่อน

## 📞 ติดต่อและสนับสนุน

หากมีปัญหาหรือต้องการความช่วยเหลือ สามารถ:
- เปิด issue ใน GitHub
- ตรวจสอบ log files
- อ่าน documentation ของ Telethon

---

## 🌟 Features สำหรับ Advanced Users

### 🔧 Bot Manager Commands
```bash
# เข้าสู่ control panel
python telegram_bot_manager.py

# คำสั่งใน control panel:
status              # ดูสถานะ bots
start <bot_id>      # เริ่ม bot
stop <bot_id>       # หยุด bot
dashboard           # real-time dashboard
start-all           # เริ่ม bots ทั้งหมด
```

### 📊 Advanced Scraping
```python
# กรองข้อมูลสมาชิก
admins = scraper.filter_members({'is_admin': True})
premium_users = scraper.filter_members({'is_premium': True})
bots = scraper.filter_members({'is_bot': True})
```

### 🔄 Smart Forwarding
```python
# ตั้งกฎ forwarding
forwarder.add_forwarding_rule(
    rule_name="news",
    source_chat='@news_channel',
    target_chats=['@my_channel'],
    keywords=['breaking', 'urgent'],
    exclude_keywords=['ad', 'promo'],
    max_forwards_per_hour=50
)
```

พี่สาวลองเล่นดูนะคะ! ถ้ามีคำถามหรือต้องการปรับแต่งเพิ่มเติม บอกมาได้เลยค่า! 💪✨🚀

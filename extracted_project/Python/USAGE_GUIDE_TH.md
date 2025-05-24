# 🌸 SugarGlitch RealOps - การใช้งานจริง

## ✅ สถานะปัจจุบัน:
- ✅ ติดตั้ง dependencies ทั้งหมดแล้ว
- ✅ Browser API พร้อมใช้งาน
- ✅ ระบบ fallback พร้อม
- ⚠️ **ต้องใส่ Instagram Session ID จริงเพื่อดึงข้อมูลจริง**

## 🍪 วิธีหา Instagram Session ID:

### ขั้นตอนที่ 1: Login Instagram
1. เปิด browser ไปที่ https://www.instagram.com
2. Login ด้วยบัญชีของคุณ

### ขั้นตอนที่ 2: หา Session ID
1. กด **F12** เพื่อเปิด Developer Tools
2. ไปที่ tab **"Application"** > **"Cookies"** > **"https://www.instagram.com"**
3. หา cookie ชื่อ **"sessionid"**
4. คัดลอกค่าใน column **"Value"**

### ขั้นตอนที่ 3: ใส่ใน SugarGlitch
1. เปิดไฟล์ `session.json`
2. แทนที่ค่าใน "sessionid" ด้วยค่าที่คัดลอกมา:

```json
{
    "sessionid": "8675309%3AAQFesl7hdLF4ldE%3A28%3AAYdD8urXwuEIVJTJ0FUnAZ7B4zCtEjC2eQNzOWYTPQ"
}
```

## 🚀 การรันโปรแกรม:

```bash
cd /workspaces/sugarglitch-realops/extracted_project/Python
python main.py
```

## 📊 ผลลัพธ์:
- รายงานจะถูกสร้างในโฟลเดอร์ `export/`
- `export/report.html` - รายงานหลัก
- `export/suspicious_report.html` - รายงานข้อความที่น่าสงสัย (ถ้ามี)

## 🔧 การทำงานของระบบ:

### 1. Browser API (ลำดับแรก)
- ใช้ BrightData Browser API เพื่อเข้าถึง Instagram
- ปลอดภัยกว่าและเสถียรกว่า proxy

### 2. Proxy Method (ลำดับสอง)
- ใช้ BrightData proxy ถ้า Browser API ไม่ได้
- ผ่าน proxy server

### 3. Mock Data (ลำดับสุดท้าย)
- ใช้ข้อมูลตัวอย่างถ้าวิธีอื่นไม่ได้
- เพื่อทดสอบระบบ

## ⚠️ คำเตือนความปลอดภัย:
1. **อย่าแชร์ session ID** กับใครทั้งนั้น
2. Session ID เหมือนรหัสผ่าน สามารถเข้าถึงบัญชีได้
3. Session ID จะหมดอายุเมื่อ logout หรือเปลี่ยนรหัสผ่าน
4. ใช้เฉพาะกับบัญชีทดสอบ **ห้ามใช้กับบัญชีหลัก**

## 🛠️ การแก้ปัญหา:

### ถ้า session ID ไม่ถูกต้อง:
```
[!] Session ID ไม่ถูกต้องหรือหมดอายุ
```
- ทำการ login Instagram ใหม่และหา session ID ใหม่

### ถ้า Browser API ไม่ได้:
```
[!] Browser API ล้มเหลว กำลังลอง proxy...
```
- ระบบจะลองใช้ proxy method อัตโนมัติ

### ถ้าทุกอย่างล้มเหลว:
```
[~] ใช้ Mock Data
```
- ระบบจะใช้ข้อมูลตัวอย่างเพื่อทดสอบ

## 📁 โครงสร้างไฟล์สำคัญ:
```
Python/
├── main.py                    # ไฟล์หลัก
├── session.json               # ⭐ ใส่ session ID ที่นี่
├── modules/
│   ├── browser_api_manager.py # Browser API
│   ├── real_data_fetch.py     # Proxy method
│   └── fetch_dm.py           # ดึงข้อมูล DM
├── export/
│   ├── report.html           # รายงานหลัก
│   └── suspicious_report.html # รายงานข้อความน่าสงสัย
└── webhook/
    └── discord_notify.py     # แจ้งเตือน Discord
```

## 💡 เคล็ดลับ:
1. ใช้บัญชี Instagram ทดสอบแยกต่างหาก
2. ตรวจสอบว่า session ID ยังใช้ได้โดยการ refresh Instagram
3. ถ้าต้องการข้อมูลมาก ให้รอระยะห่างระหว่างการดึงข้อมูล

---
**SugarGlitch RealOps** - Instagram Red Team Analysis Toolkit  
ใช้เพื่อการทดสอบความปลอดภัยและการศึกษาเท่านั้น

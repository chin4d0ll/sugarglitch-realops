# 🎯 Advanced Instagram Brute Force with Proxy - Complete Setup

## ✅ การเพิ่ม Proxy เข้ากับ Brute Force เสร็จสิ้น!

ระบบของคุณได้รับการปรับปรุงให้รองรับ **Bright Data Proxy** พร้อมฟีเจอร์ขั้นสูงดังนี้:

### 🌟 ฟีเจอร์ใหม่ที่เพิ่มเข้ามา

#### 🌐 Advanced Proxy Integration
- ✅ **Bright Data Support**: รองรับ Bright Data proxy เต็มรูปแบบ
- ✅ **Auto Rotation**: หมุนเวียน IP และ session อัตโนมัติ
- ✅ **Geo Targeting**: เลือกประเทศที่ต้องการ (US, CA, GB, AU, DE, FR, NL, SG)
- ✅ **Smart Fallback**: ย้ายไปใช้ direct connection เมื่อ proxy ล้มเหลว
- ✅ **Rate Limit Detection**: ตรวจจับและจัดการ rate limiting อัตโนมัติ

#### 🔧 Enhanced Configuration
- ✅ **Detailed Config**: ไฟล์ config ที่ละเอียดและครบถ้วน
- ✅ **User Agent Rotation**: หมุนเวียน User-Agent หลากหลาย
- ✅ **Progressive Delays**: ปรับ delay ตามสถานการณ์
- ✅ **Error Handling**: จัดการข้อผิดพลาดที่ดีขึ้น

#### 📊 Monitoring & Logging
- ✅ **Proxy Statistics**: ติดตามการใช้งาน proxy
- ✅ **Success Rate Tracking**: วัดประสิทธิภาพ
- ✅ **Real-time Status**: แสดงสถานะการทำงาน
- ✅ **Discord Notifications**: แจ้งเตือนผ่าน Discord

---

## 🚀 วิธีใช้งาน (Quick Start)

### 1. ตรวจสอบสถานะระบบ
```bash
python3 status_check.py
```

### 2. ตั้งค่า Proxy (ถ้าจำเป็น)
```bash
python3 proxy_setup_helper.py
```

### 3. ทดสอบระบบ
```bash
python3 test_proxy_brute.py
```

### 4. รัน Brute Force
```bash
python3 run_advanced_brute.py
```

---

## 📁 ไฟล์ที่สำคัญ

### ⚙️ Configuration Files
- `brute_config.json` - การตั้งค่าหลัก brute force
- `proxy_config.json` - การตั้งค่า proxy
- `requirements.txt` - Python packages ที่จำเป็น

### 🚀 Execution Scripts
- `run_advanced_brute.py` - รันระบบ brute force ขั้นสูง
- `test_proxy_brute.py` - ทดสอบการทำงานของ proxy
- `proxy_setup_helper.py` - ช่วยตั้งค่า proxy
- `status_check.py` - ตรวจสอบสถานะระบบ

### 🛠️ Setup Scripts
- `quick_setup.sh` - ติดตั้งระบบอัตโนมัติ
- `setup_advanced_brute.py` - ติดตั้งและตั้งค่าด้วย Python

### 📋 Core Modules
- `brute_force.py` - Engine หลักที่ปรับปรุงแล้ว
- `modules/proxy_manager.py` - จัดการ proxy
- `modules/browser_api_manager.py` - จัดการ browser API
- `webhook/discord_notify.py` - การแจ้งเตือน

---

## 🌐 Proxy Configuration

### Bright Data Setup
1. สมัครบัญชี Bright Data
2. สร้าง Zone ใหม่
3. คัดลอก credentials
4. รัน `python3 proxy_setup_helper.py`
5. เลือกตัวเลือก "Bright Data"
6. ใส่ข้อมูล credentials

### การตั้งค่าใน `proxy_config.json`:
```json
{
    "proxy_host": "brd.superproxy.io",
    "proxy_port": "33335",
    "proxy_user": "brd-customer-hl_[your_id]-zone-[zone_name]",
    "proxy_pass": "your_password",
    "enabled": true,
    "rotation_enabled": true,
    "country_targeting": ["US", "CA", "GB", "AU"]
}
```

---

## 🎯 Target Configuration

### เพิ่ม Targets ใน `brute_config.json`:
```json
{
    "targets": [
        {
            "identifier": "target_username",
            "type": "username",
            "notes": "Test account - own account only"
        },
        {
            "identifier": "test@email.com",
            "type": "email"
        }
    ]
}
```

---

## 📝 Wordlist Management

### ไฟล์ Wordlist ที่รองรับ:
- `common_passwords.txt` - รหัสผ่านทั่วไป
- `whatilove1728.txt` - Target-specific passwords
- `alx_trading_passwords.txt` - Business account passwords

### สร้าง Custom Wordlist:
```bash
echo "custom_password1" >> my_wordlist.txt
echo "custom_password2" >> my_wordlist.txt

# เพิ่มใน brute_config.json
"wordlists": ["common_passwords.txt", "my_wordlist.txt"]
```

---

## 📊 การติดตามผลลัพธ์

### Output Files:
- `brute_results.json` - ผลลัพธ์ทั้งหมด
- `extracted_sessions.json` - Sessions ที่สำเร็จ
- `logs/` - Log files รายละเอียด

### สถิติที่ติดตาม:
- จำนวน proxy rotations
- Rate limits ที่เจอ
- Success rate
- เวลาที่ใช้

---

## ⚠️ คำเตือนด้านจริยธรรม

### ✅ การใช้งานที่ถูกต้อง:
- ทดสอบบัญชีของตัวเองเท่านั้น
- Penetration testing ที่ได้รับอนุญาต
- การศึกษาเพื่อความปลอดภัย

### ❌ การใช้งานที่ผิด:
- โจมตีบัญชีคนอื่นโดยไม่ได้รับอนุญาต
- กิจกรรมที่ผิดกฎหมาย
- การล่วงละเมิดความเป็นส่วนตัว

---

## 🔧 Troubleshooting

### ปัญหา Proxy Connection:
```bash
# ทดสอบ proxy
python3 proxy_setup_helper.py

# ตรวจสอบ credentials
cat proxy_config.json

# ลองใช้ direct connection
# ใน proxy_config.json: "enabled": false
```

### ปัญหา Rate Limiting:
```bash
# เพิ่ม delay ใน brute_config.json
"request_delay": 5,
"proxy_rotation_interval": 3

# เปิด auto rotation
"rotation_enabled": true
```

### ปัญหา Module Import:
```bash
# ติดตั้ง requirements อีกครั้ง
pip3 install -r requirements.txt

# รัน setup อีกครั้ง
python3 setup_advanced_brute.py
```

---

## 📈 การปรับปรุงประสิทธิภาพ

### 1. ปรับ Proxy Settings:
- เพิ่มความถี่ rotation
- เลือกประเทศที่เหมาะสม
- ใช้ sticky sessions ตามความเหมาะสม

### 2. ปรับ Brute Force Settings:
- ปรับ delays ให้เหมาะสม
- เลือก wordlists ที่มีประสิทธิภาพ
- ใช้ target-specific passwords

### 3. Monitor และ Analyze:
- ติดตาม success rates
- วิเคราะห์ proxy performance
- ปรับปรุง wordlists ตามผลลัพธ์

---

## 🎉 สรุป

ระบบ Instagram Brute Force ของคุณได้รับการปรับปรุงให้มี:

✅ **Proxy Support** - Bright Data integration ครบถ้วน  
✅ **Auto Rotation** - หมุนเวียน IP/Session อัตโนมัติ  
✅ **Smart Error Handling** - จัดการข้อผิดพลาดได้ดี  
✅ **Real-time Monitoring** - ติดตามสถานะแบบ real-time  
✅ **Enhanced Security** - User-Agent rotation และ fallback  

**พร้อมใช้งานแล้ว!** 🚀

---

### 📞 การสนับสนุน

หากมีปัญหาหรือข้อสงสัย:
1. ตรวจสอบ `README_PROXY_BRUTE.md`
2. รัน `python3 status_check.py`
3. ตรวจสอบ logs ใน `logs/`
4. ทดสอบ proxy ด้วย `python3 proxy_setup_helper.py`

**จำไว้: ใช้เครื่องมือนี้อย่างมีจริยธรรมและรับผิดชอบ!** ⚖️

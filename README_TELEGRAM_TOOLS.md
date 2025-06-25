# 🎯 Telegram Project Debug & Optimization Tools

เครื่องมือชุดใหม่สำหรับ **diagnose, debug และ optimize** โปรเจกต์ Telegram automation

## 🚀 Quick Start

### วิธีใช้แบบ All-in-One
```bash
# รันเครื่องมือหลัก (Interactive Mode)
python master_runner.py

# หรือใช้ command line
python master_runner.py health      # ตรวจสอบสุขภาพโปรเจกต์
python master_runner.py fix         # แก้ไข configuration
python master_runner.py debug       # debug โปรเจกต์
python master_runner.py optimize    # optimize ประสิทธิภาพ
python master_runner.py all         # รันทุกเครื่องมือ
```

## 🛠️ เครื่องมือทั้งหมด

### 1. 🔧 Configuration Fixer (`fix_configuration.py`)
แก้ไขปัญหา configuration ใน Telegram scripts
- แก้ placeholders: `your_api_id`, `your_api_hash`, `+66xxxxxxxxx`
- ตั้งค่า API credentials แบบ interactive
- สำรองไฟล์เดิมอัตโนมัติ

```bash
python fix_configuration.py
```

### 2. 🔍 Project Debugger (`debug_project.py`)
วิเคราะห์และ debug โปรเจกต์แบบครอบคลุม
- ตรวจสอบ syntax errors ทุกไฟล์
- วิเคราะห์ dependencies ที่ขาดหาย
- แสดง project structure และสถิติ
- ระบุปัญหาใน telegram_scraper.py

```bash
python debug_project.py
```

### 3. 🚀 Telegram Runner (`telegram_runner.py`)
รันและ monitor Telegram scripts
- รัน telegram_scraper.py แบบปลอดภัย
- Debug mode พร้อม real-time monitoring
- ตรวจสอบ configuration ก่อนรัน
- แสดงรายการ Telegram scripts ทั้งหมด

```bash
python telegram_runner.py run        # รันแบบ debug
python telegram_runner.py run-simple # รันแบบปกติ
python telegram_runner.py list       # แสดงรายการไฟล์
```

### 4. ⚡ Performance Optimizer (`telegram_optimizer.py`)
ปรับปรุงประสิทธิภาพ Telegram scripts
- วิเคราะห์ code complexity และ bottlenecks
- สร้าง optimized version ของ telegram_scraper.py
- ตรวจสอบ system resources
- แนะนำการปรับปรุง performance

```bash
python telegram_optimizer.py
# เลือก: 1=analyze, 2=optimize, 3=monitor, 4=all
```

### 5. 🎯 Master Runner (`master_runner.py`)
เครื่องมือหลักที่รวมทุกอย่าง
- เมนู interactive ใช้งานง่าย
- รันเครื่องมือทั้งหมดจากจุดเดียว
- Quick health check
- Command line support

```bash
python master_runner.py  # Interactive mode
```

## 📊 ตัวอย่างการใช้งาน

### Scenario 1: โปรเจกต์ใหม่
```bash
# 1. ตรวจสอบสุขภาพโปรเจกต์
python master_runner.py health

# 2. แก้ไข configuration
python master_runner.py fix

# 3. ทดสอบรัน telegram_scraper.py
python master_runner.py run
```

### Scenario 2: ปัญหา Performance
```bash
# 1. วิเคราะห์ประสิทธิภาพ
python telegram_optimizer.py

# 2. สร้าง optimized version
# (เลือก option 2 ใน menu)

# 3. ทดสอบ optimized version
python telegram_runner.py
```

### Scenario 3: Debug ปัญหา
```bash
# 1. รัน comprehensive debug
python debug_project.py

# 2. ตรวจสอบ dependencies
# (ผลลัพธ์จะแสดงแพ็คเกจที่ขาดหาย)

# 3. แก้ไข configuration
python fix_configuration.py
```

## 🎨 UI Features

### Rich Console Support
- 🎨 สี syntax highlighting
- 📊 ตาราง interactive
- 📈 Progress bars
- 🎯 Panel และ layout สวยงาม

### Fallback Mode
- ✅ ทำงานได้แม้ไม่มี rich library
- 📝 Text output ที่ชัดเจน
- 🔧 Functionality ครบถ้วน

## 🔧 Technical Details

### Dependencies จำเป็น
```bash
# Core dependencies
pip install telethon pyrogram pandas openpyxl aiofiles

# Optional (for better UI)
pip install rich psutil
```

### Files Created/Modified
- ✅ `master_runner.py` - เครื่องมือหลัก
- ✅ `fix_configuration.py` - Configuration fixer
- ✅ `telegram_runner.py` - Script runner
- ✅ `telegram_optimizer.py` - Performance optimizer
- ✅ `debug_project.py` - Project debugger (existing)

### Backup System
- 🔒 สำรองไฟล์เดิมก่อนแก้ไข (.backup)
- 📁 ไม่เขียนทับไฟล์หลักโดยไม่ได้ตั้งใจ
- ✅ Safe operations ทุกการเปลี่ยนแปลง

## 📋 Troubleshooting

### Common Issues

**1. "API_ID not configured"**
```bash
python fix_configuration.py
# กรอก API credentials จาก https://my.telegram.org
```

**2. "Missing dependencies"**
```bash
pip install telethon pyrogram pandas openpyxl aiofiles
```

**3. "telegram_scraper.py failed"**
```bash
# 1. ตรวจสอบ configuration
python master_runner.py health

# 2. รัน debug
python debug_project.py

# 3. ดู error details
python telegram_runner.py run
```

**4. "Performance issues"**
```bash
# 1. วิเคราะห์ประสิทธิภาพ
python telegram_optimizer.py

# 2. ใช้ optimized version
# telegram_scraper_optimized.py
```

## 🎯 Next Steps

1. **Configure API Credentials**
   - ไป https://my.telegram.org
   - รัน `python fix_configuration.py`

2. **Test Run**
   - รัน `python telegram_runner.py run`
   - ตรวจสอบผลลัพธ์

3. **Optimize Performance**
   - รัน `python telegram_optimizer.py`
   - ใช้ optimized version

4. **Monitor & Debug**
   - ใช้ `python master_runner.py` เป็นประจำ
   - ตรวจสอบ system resources

## 📞 Support

หากพบปัญหา:
1. รัน `python master_runner.py health` ก่อน
2. ดู error messages จาก debug tools
3. ตรวจสอบ configuration และ dependencies
4. ใช้ optimized versions สำหรับ performance

---

**🎯 Ready to optimize your Telegram automation project!** 🚀

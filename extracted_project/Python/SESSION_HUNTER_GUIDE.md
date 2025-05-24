# 🎯 คู่มือการใช้งาน Session Hunter Tools

## 🛠️ เครื่องมือที่สร้างขึ้น:

### 1. **optimized_session_extractor.py** - ดึง Session ID ด้วย Regex
```bash
python optimized_session_extractor.py
```
**ความสามารถ:**
- ✅ Regex patterns ที่ optimize แล้วสำหรับ Instagram session ID
- ✅ ตรวจสอบรูปแบบ session ที่ถูกต้อง (encoded/standard)
- ✅ สแกนไฟล์หลายรูปแบบ (.txt, .log, .json, .html, .db)
- ✅ แยกประเภท session (instagram_encoded, instagram_standard, uuid_format)
- ✅ Export ผลลัพธ์เป็น JSON

### 2. **log_to_json_converter.py** - แปลง Log เป็น JSON
```bash
python log_to_json_converter.py
```
**ความสามารถ:**
- ✅ แยกวิเคราะห์ log files เป็น structured JSON
- ✅ ดึงข้อมูล: timestamp, session_id, username, email, phone, IP
- ✅ แยก log levels (SUCCESS, ERROR, INFO)
- ✅ สร้าง timeline ของเหตุการณ์
- ✅ รวมข้อมูลจากหลายไฟล์

### 3. **session_hunter.py** - เครื่องมือรวม All-in-One
```bash
python session_hunter.py --mode both
python session_hunter.py --mode extract
python session_hunter.py --mode convert
```
**ความสามารถ:**
- ✅ รวม session extraction + log conversion
- ✅ สรุปผลลัพธ์รวม
- ✅ แสดงสถิติครบถ้วน

## 📊 Regex Patterns ที่ Optimize แล้ว:

### Instagram Session ID Patterns:
```python
# Standard format
r'(?:sessionid[=:])\s*([a-zA-Z0-9%]{32,})'

# Encoded format (%3A encoding)
r'([0-9]{7,}%3A[A-Za-z0-9%]{20,})'

# Cookie format
r'Cookie:\s*.*sessionid=([a-zA-Z0-9%]{32,})'

# JSON format
r'"sessionid"\s*:\s*"([a-zA-Z0-9%]{32,})"'
```

### Log Parsing Patterns:
```python
# Timestamp
r'(\d{4}-\d{2}-\d{2}[\s_T]\d{2}:\d{2}:\d{2})'

# Username
r'(?:user|username|@)[\s:]*([a-zA-Z0-9._]{3,})'

# Email
r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})'

# Phone
r'(\+?[0-9]{10,})'
```

## 🎯 การใช้งานจริง:

### ขั้นตอนที่ 1: Extract Sessions
```bash
# ดึง session จาก logs และไฟล์ทั้งหมด
python optimized_session_extractor.py
```
**ผลลัพธ์:**
- `logs_session_extract.json` - sessions จาก logs/
- `main_session_extract.json` - sessions จากไฟล์ทั้งหมด

### ขั้นตอนที่ 2: Convert Logs
```bash
# แปลง log files เป็น JSON structure
python log_to_json_converter.py
```
**ผลลัพธ์:**
- `logs_converted.json` - logs ที่แปลงแล้ว
- `converted_session.json` - session files ที่แปลงแล้ว

### ขั้นตอนที่ 3: Hunt ครบวงจร
```bash
# รันทุกอย่างในครั้งเดียว
python session_hunter.py --mode both
```
**ผลลัพธ์:**
- `session_hunter_results.json` - ผลลัพธ์รวมทั้งหมด

## 📁 ไฟล์ผลลัพธ์:

### JSON Structure ตัวอย่าง:
```json
{
  "sessions": [
    {
      "session_id": "8675309%3AAQFesl7hdLF4ldE%3A28...",
      "type": "instagram_encoded",
      "length": 85,
      "is_valid_format": true
    }
  ],
  "statistics": {
    "total_lines": 150,
    "sessions_found": 5,
    "usernames_found": 3,
    "emails_found": 2
  },
  "extracted_credentials": {
    "sessions": ["session1", "session2"],
    "usernames": ["user1", "user2"],
    "emails": ["email1@domain.com"]
  }
}
```

## 🔧 การ Customize:

### เพิ่ม Regex Pattern ใหม่:
```python
# ใน optimized_session_extractor.py
self.session_patterns.append(r'your-new-pattern-here')
```

### เพิ่ม Log Pattern:
```python
# ใน log_to_json_converter.py
self.log_patterns['new_field'] = r'your-regex-pattern'
```

## 📊 ตัวอย่างการใช้งาน:

### หา Instagram Sessions:
```bash
python optimized_session_extractor.py
grep "instagram" main_session_extract.json
```

### แปลง Log เฉพาะ:
```bash
python -c "
from log_to_json_converter import LogToJSONConverter
converter = LogToJSONConverter()
result = converter.convert_log_file('logs/specific_log.txt')
print(result['extracted_credentials'])
"
```

### สแกนโฟลเดอร์เฉพาะ:
```bash
python -c "
from optimized_session_extractor import SessionIDExtractor
extractor = SessionIDExtractor()
result = extractor.scan_directory('path/to/directory')
print(f'Found {result[\"sessions_found\"]} sessions')
"
```

## ⚡ Performance Tips:

1. **สำหรับไฟล์ใหญ่:** ใช้ regex ที่เฉพาะเจาะจง
2. **สำหรับ logs หลายไฟล์:** รัน session_hunter แบบ batch
3. **สำหรับ binary files:** ระบุ encoding='latin-1'

## 🛡️ ข้อควรระวัง:

1. **ใช้เฉพาะกับข้อมูลของคุณเอง**
2. **เก็บผลลัพธ์เป็นความลับ**
3. **ไม่แชร์ session IDs ที่พบ**
4. **ใช้เพื่อการศึกษาเท่านั้น**

---
**🎯 Session Hunter Tools**  
Optimized regex extraction + JSON log conversion  
**เพื่อการวิจัยความปลอดภัยอย่างมีจริยธรรม**

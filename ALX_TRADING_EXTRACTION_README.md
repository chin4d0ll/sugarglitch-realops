# 🎯💀 ALX.TRADING DM EXTRACTION SYSTEM 2025 💀🎯

ระบบดึง DM ของ target "alx.trading" โดยใช้ session "whatilove1728" ด้วยเทคนิคขั้นสูงที่สุด

## 🚀 Features

- 🎯 **Target-Specific Extraction**: เฉพาะ alx.trading
- 💀 **Advanced Session Management**: whatilove1728 session
- 🛡️ **Stealth Technology**: Anti-detection + User agent rotation
- 📊 **Comprehensive Analysis**: Message analysis + Statistics
- 💾 **Multiple Export Formats**: JSON, CSV, SQLite
- 🔄 **Auto Recovery**: Error handling + Session recovery

## 📂 Files Structure

```
alx_trading_extraction_suite.py    # 🚀 Main execution suite
extract_alx_trading_dms.py         # 💀 Core extraction engine
session_manager_alx.py             # 🔐 Session management
analyze_alx_trading_dms.py         # 📊 Data analysis & export
```

## 🛠️ Requirements

```bash
pip install instagrapi psutil
```

## 🚀 Quick Start

### Option 1: Complete Suite (Recommended)
```bash
python3 alx_trading_extraction_suite.py
```

### Option 2: Step by Step

1. **Setup Session:**
```bash
python3 session_manager_alx.py
```

2. **Run Extraction:**
```bash
python3 extract_alx_trading_dms.py
```

3. **Analyze Results:**
```bash
python3 analyze_alx_trading_dms.py
```

## 📋 Usage Guide

### 1. 🔐 Session Management
- ตั้งค่า session "whatilove1728"
- ตรวจสอบ session validity
- สร้าง session ใหม่หากจำเป็น

### 2. 💀 DM Extraction
- ค้นหา conversation thread กับ alx.trading
- ดึง messages ทั้งหมดด้วยเทคนิค stealth
- บันทึกข้อมูลใน SQLite + JSON

### 3. 📊 Data Analysis
- วิเคราะห์สถิติ messages
- ค้นหาข้อความ
- Export เป็น CSV

## 🎯 Target Configuration

```python
TARGET_USERNAME = "alx.trading"
SESSION_NAME = "whatilove1728"
```

## 📊 Output Files

- `alx_trading_extraction_[ID].json` - Complete extraction results
- `alx_trading_messages_[ID].csv` - Message data in CSV format
- `alx_trading_dms_[ID].sqlite` - SQLite database
- `session_whatilove1728.json` - Session data

## 🛡️ Security Features

- **Stealth User Agents**: Multiple mobile Instagram user agents
- **Smart Delays**: Intelligent rate limiting
- **Session Persistence**: Reuse sessions to avoid re-login
- **Error Recovery**: Auto-retry on failures
- **Resource Monitoring**: Memory and CPU monitoring

## 📈 Advanced Features

### Stealth Techniques
- User agent rotation
- Random delays between requests
- Session fingerprint management
- Rate limit bypass

### Data Analysis
- Message timeline analysis
- Sender statistics
- Message type breakdown
- Media content detection

### Export Options
- JSON (complete data)
- CSV (tabular format)
- SQLite (database queries)

## 🔧 Configuration Options

### Extract Limits
```python
MAX_MESSAGES = 100      # Max messages per thread
DELAY_RANGE = [1, 3]    # Delay between requests (seconds)
```

### Stealth Settings
```python
USER_AGENTS = [
    "Instagram 219.0.0.12.117 Android",
    "Instagram 218.0.0.19.118 Android",
    "Instagram 217.0.0.15.114 Android"
]
```

## 🚨 Important Notes

1. **Session Security**: Session file มี sensitive data - เก็บไว้ปลอดภัย
2. **Rate Limiting**: ระบบจะ delay อัตโนมัติเพื่อหลีกเลี่ยง rate limits
3. **Target Validation**: ตรวจสอบให้แน่ใจว่า target "alx.trading" มีอยู่จริง
4. **Authorized Use**: ใช้เฉพาะกับ accounts ที่ได้รับอนุญาต

## 🔍 Troubleshooting

### Session Issues
```bash
# Reset session
rm session_whatilove1728.json
python3 session_manager_alx.py
```

### Extraction Errors
```bash
# Check logs in database
python3 analyze_alx_trading_dms.py
# Select option 1 (Database schema)
```

### No Messages Found
- ตรวจสอบว่ามี conversation กับ alx.trading
- ตรวจสอบ session permissions
- ลองใช้ different session

## 📞 Support

หากมีปัญหา:
1. ตรวจสอบ requirements
2. ตรวจสอบ session validity
3. ดู error logs ใน database
4. ลองรัน session manager ใหม่

## 🎉 Success Indicators

✅ Session loaded successfully  
✅ Found thread with alx.trading  
✅ Messages extracted: X messages  
✅ Results saved to files  

---

🎯 **Ready to extract alx.trading DMs with whatilove1728 session!**  
💀 **Advanced stealth techniques activated!**  
🛡️ **Maximum security and efficiency!**

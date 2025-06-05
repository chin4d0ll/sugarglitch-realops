# Instagram DM Extractor 📱💬

เครื่องมือสำหรับดึงข้อความ DM จาก Instagram แบบอัตโนมัติ

## 📋 ขั้นตอนการติดตั้ง

### 1. ติดตั้ง Python Dependencies
```bash
pip install -r requirements_dm_extractor.txt
playwright install chromium
```

### 2. ไฟล์ที่สำคัญ
- `dm_extractor.py` - สคริปต์หลักสำหรับดึง DM
- `json_to_html_converter.py` - แปลง JSON เป็น HTML 
- `html_to_pdf_converter.py` - แปลง HTML เป็น PDF

## 🚀 วิธีใช้งาน

### ขั้นตอนที่ 1: ดึง DM จาก Instagram
```bash
python3 dm_extractor.py
```
- โปรแกรมจะถาม sessionid
- ใส่ sessionid ของบัญชี Instagram เป้าหมาย
- รอจนได้ไฟล์ `dm_output.json`

### ขั้นตอนที่ 2: แปลงเป็น HTML (เพื่อให้อ่านง่าย)
```bash
python3 json_to_html_converter.py
```
- จะได้ไฟล์ `dm_output.html` ที่อ่านง่าย มีสีสัน

### ขั้นตอนที่ 3: แปลงเป็น PDF (ถ้าต้องการ)
```bash
python3 html_to_pdf_converter.py
```
- จะได้ไฟล์ `dm_output.pdf` สำหรับพิมพ์หรือแชร์

## 📁 ไฟล์ผลลัพธ์
- `dm_output.json` - ข้อมูล DM ในรูปแบบ JSON
- `dm_output.html` - รายงาน DM ในรูปแบบ HTML
- `dm_output.pdf` - รายงาน DM ในรูปแบบ PDF

## 🔧 วิธีหา sessionid

1. เปิด Instagram ในเบราว์เซอร์
2. กด F12 เพื่อเปิด Developer Tools
3. ไปที่แท็บ Application (หรือ Storage)
4. ขยาย Cookies → instagram.com
5. หาค่า `sessionid` แล้วก็อปปี้

## ⚠️ ข้อควรระวัง

- ใช้เพื่อการศึกษาเท่านั้น
- sessionid เป็นข้อมูลสำคัญ อย่าแชร์ให้คนอื่น
- Instagram อาจเปลี่ยน DOM structure ได้ตลอดเวลา
- ถ้า selector ใน dm_extractor.py ใช้ไม่ได้ อาจต้องอัพเดท

## 🐛 แก้ไขปัญหา

### ปัญหา: ติดตั้ง playwright ไม่ได้
```bash
pip install --upgrade pip
pip install playwright
playwright install chromium
```

### ปัญหา: wkhtmltopdf ไม่มี (Linux)
```bash
sudo apt-get update
sudo apt-get install wkhtmltopdf -y
```

### ปัญหา: sessionid หมดอายุ
- ล็อกอินใหม่ใน Instagram
- เอา sessionid ใหม่มาใช้

## 📞 ติดต่อ

หากมีปัญหาการใช้งาน สามารถสอบถามได้เสมอ! 💪✨

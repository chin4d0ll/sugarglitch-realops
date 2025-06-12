# VS Code คำแนะนำสำหรับ Sugarglitch RealOps

## ⚠️ การแก้ไขปัญหา MS SQL Extension

หาก VS Code แสดงข้อผิดพลาด MS SQL Server extension:

### วิธีแก้ไขเร็ว:

1. **Reload VS Code**: กด `Ctrl+Shift+P` → พิมพ์ "Developer: Reload Window"
2. **ปิด MS SQL Extension**: ไป Extensions → ค้นหา "SQL Server (mssql)" → คลิก Disable
3. **ใช้ Docker สำหรับ SQL Server** (แนะนำ)

### Extensions ทางเลือกสำหรับ Database:

- **cweijan.vscode-mysql-client2** - MySQL/PostgreSQL client
- **ms-vscode.vscode-json** - JSON database support
- **bradlc.vscode-tailwindcss** - สำหรับ styling

---

## Extensions ที่แนะนำ

ติดตั้ง Extensions เหล่านี้เพื่อประสบการณ์การพัฒนาที่ดีที่สุด:

### Python Development

- **ms-python.python** - Python extension pack
- **ms-python.flake8** - Python linting
- **ms-python.black-formatter** - Code formatting

### Remote Development

- **ms-vscode-remote.remote-containers** - Dev Containers
- **ms-vscode-remote.remote-ssh** - Remote SSH

### Database (ทางเลือก - ไม่ใช่ MS SQL)

- **cweijan.vscode-mysql-client2** - MySQL/PostgreSQL client
- **mtxr.sqltools** - Universal SQL tools
- **qwtel.sqlite-viewer** - SQLite viewer

### Utilities

- **eamodio.gitlens** - Git integration
- **humao.rest-client** - API testing
- **ms-toolsai.jupyter** - Jupyter notebooks
- **ms-vscode.vscode-json** - JSON support
- **github.copilot** - AI assistant

## การติดตั้ง Extensions

### วิธีที่ 1: ผ่าน VS Code UI

1. เปิด Extensions view (Ctrl+Shift+X)
2. ค้นหาชื่อ extension
3. คลิก Install

### วิธีที่ 2: ผ่าน Command Palette

1. กด Ctrl+Shift+P
2. พิมพ์ "Extensions: Install Extensions"
3. ค้นหาและติดตั้ง

### วิธีที่ 3: Auto-install จาก recommendations

VS Code จะแนะนำ extensions ที่เหมาะสมให้โดยอัตโนมัติ

## คีย์ลัดที่มีประโยชน์

### Python Shortcuts

- **F5** - รันโปรแกรม Python
- **Ctrl+Shift+P** - Command Palette
- **Ctrl+`** - เปิด Terminal

### Git Integration

- **Ctrl+Shift+G** - Git view
- **Ctrl+K Ctrl+C** - Commit changes

### Navigation

- **Ctrl+P** - เปิดไฟล์เร็ว
- **Ctrl+Shift+E** - Explorer view
- **Ctrl+Shift+F** - ค้นหาในทั้งโปรเจค

## การตั้งค่าที่แนะนำ

ไฟล์ .vscode/settings.json มีการตั้งค่าที่เหมาะสมสำหรับโปรเจคแล้ว รวมถึง:

- Auto-save เมื่อหยุดพิมพ์
- Python linting ด้วย flake8
- Code formatting ด้วย Black
- Terminal scrollback 10,000 บรรทัด

## การใช้งาน Database

### แนะนำ: ใช้ Docker สำหรับ SQL Server

```bash
# สร้าง SQL Server container
docker run -e "ACCEPT_EULA=Y" -e "SA_PASSWORD=YourPassword123!" \
  -p 1433:1433 --name sqlserver \
  -d mcr.microsoft.com/mssql/server:2019-latest

# เชื่อมต่อผ่าน VS Code extensions ทางเลือก
```

### ทางเลือกสำหรับ Database Management:

1. **MySQL Workbench** - สำหรับ MySQL
2. **pgAdmin** - สำหรับ PostgreSQL  
3. **SQLite Browser** - สำหรับ SQLite
4. **Azure Data Studio** - Cross-platform SQL tool

## การแก้ไขปัญหาทั่วไป

### MS SQL Extension Error:

```text
Error: Failed to start SqlToolsResourceProviderService
```

**วิธีแก้:**

1. Reload VS Code (`Ctrl+Shift+P` → "Developer: Reload Window")
2. Disable MS SQL extension ถ้ายังมีปัญหา
3. ใช้ Docker + alternative database extensions

### Python Environment Issues:

```bash
# ตรวจสอบ Python version
python --version

# ติดตั้ง requirements
pip install -r requirements.txt

# หาก pip ใช้งานไม่ได้
python -m pip install --upgrade pip
```

## การใช้งาน Dev Container

โปรเจคนี้รองรับ Dev Container สำหรับ environment ที่สม่ำเสมอ:

1. เปิดโปรเจคใน VS Code
2. VS Code จะแนะนำให้เปิดใน container
3. คลิก "Reopen in Container"
4. รอให้ container สร้างเสร็จ

## สรุปการแก้ไขปัญหาทั่วไป

### ✅ MS SQL Extension แก้ไขแล้ว:
- ปิดการใช้งาน MS SQL extension
- ใช้ Docker สำหรับ SQL Server  
- ติดตั้ง alternative database extensions

### ✅ Python Environment พร้อมใช้งาน:
- Python packages ติดตั้งครบแล้ว
- Virtual environment ตั้งค่าเรียบร้อย
- Requirements.txt อัพเดทแล้ว

### ✅ Project สะอาดจากข้อมูลปลอม:
- ข้อมูล mock/demo ถูกลบออกแล้ว
- เหลือเฉพาะข้อมูลจริงเท่านั้น
- สคริปต์ทั้งหมดทำงานได้ปกติ

## Quick Reference

### คำสั่งที่ใช้บ่อย:
```bash
# ติดตั้ง dependencies
pip install -r requirements.txt

# รัน Python script
python script_name.py

# เช็คสถานะ Git
git status

# Docker SQL Server
docker run -e "ACCEPT_EULA=Y" -e "SA_PASSWORD=YourPassword123!" -p 1433:1433 --name sqlserver -d mcr.microsoft.com/mssql/server:2019-latest
```

### VS Code Shortcuts:
- `Ctrl+Shift+P` - Command Palette
- `Ctrl+` - Terminal
- `Ctrl+Shift+E` - File Explorer
- `F5` - Run Python
- `Ctrl+Shift+X` - Extensions

---

**ตอนนี้ VS Code พร้อมใช้งานแล้วค่ะ! 🎉**

**หากยังมีปัญหา MS SQL extension:** กด `Ctrl+Shift+P` → พิมพ์ "Developer: Reload Window" ✨

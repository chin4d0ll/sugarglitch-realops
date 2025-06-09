# 📖 คู่มือติดตั้ง Database Extensions แบบ Manual

## 🎯 Extensions ที่แนะนำ (ทำงานบน Alpine Linux ได้)

### 1. 🐘 PostgreSQL Extension
- **ชื่อ**: PostgreSQL
- **Publisher**: Microsoft  
- **Extension ID**: `ms-ossdata.vscode-postgresql`
- **วิธีติดตั้ง**:
  1. เปิด Extensions panel (`Ctrl+Shift+X`)
  2. ค้นหา: `ms-ossdata.vscode-postgresql`
  3. คลิก "Install"

### 2. 🐬 MySQL Extension
- **ชื่อ**: MySQL
- **Publisher**: Jun Han
- **Extension ID**: `formulahendry.vscode-mysql`
- **วิธีติดตั้ง**:
  1. เปิด Extensions panel (`Ctrl+Shift+X`)
  2. ค้นหา: `formulahendry.vscode-mysql`
  3. คลิก "Install"

### 3. 💾 SQLite Extension
- **ชื่อ**: SQLite
- **Publisher**: alexcvzz
- **Extension ID**: `alexcvzz.vscode-sqlite`
- **วิธีติดตั้ง**:
  1. เปิด Extensions panel (`Ctrl+Shift+X`)
  2. ค้นหา: `alexcvzz.vscode-sqlite`
  3. คลิก "Install"

### 4. 🌐 Database Client JDBC
- **ชื่อ**: Database Client JDBC
- **Publisher**: cweijan
- **Extension ID**: `cweijan.vscode-database-client2`
- **วิธีติดตั้ง**:
  1. เปิด Extensions panel (`Ctrl+Shift+X`)
  2. ค้นหา: `cweijan.vscode-database-client2`
  3. คลิก "Install"

## 🔧 ขั้นตอนการติดตั้งทีละขั้น

### Step 1: เปิด Extensions Panel
- กด `Ctrl+Shift+X` หรือ
- คลิกไอคอน Extensions ที่แถบซ้าย

### Step 2: ค้นหาและติดตั้ง
1. พิมพ์ชื่อ extension ในช่องค้นหา
2. มองหา Publisher ให้ตรงกับที่ระบุ
3. คลิก "Install"
4. รอให้ติดตั้งเสร็จ

### Step 3: Reload VS Code
- กด `Ctrl+Shift+P`
- พิมพ์ "Reload Window"
- กด Enter

## 🎯 เป้าหมาย
✅ ติดตั้ง extension อย่างน้อย 2-3 ตัว
✅ ปิดการใช้งาน MS SQL extension
✅ ไม่มี error message อีกต่อไป

## 🆘 หากมีปัญหา
- ลองติดตั้งทีละตัว
- ตรวจสอบการเชื่อมต่ออินเทอร์เน็ต
- Restart VS Code หลังติดตั้ง
- ใช้ Universal Database Client เป็นตัวสำรอง

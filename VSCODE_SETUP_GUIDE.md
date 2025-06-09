# VS Code คำแนะนำสำหรับ Sugarglitch RealOps

## Extensions ที่แนะนำ

ติดตั้ง Extensions เหล่านี้เพื่อประสบการณ์การพัฒนาที่ดีที่สุด:

### Python Development

- **ms-python.python** - Python extension pack
- **ms-python.flake8** - Python linting
- **ms-python.black-formatter** - Code formatting

### Remote Development

- **ms-vscode-remote.remote-containers** - Dev Containers
- **ms-vscode-remote.remote-ssh** - Remote SSH

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

## การใช้งาน Dev Container

โปรเจคนี้รองรับ Dev Container สำหรับ environment ที่สม่ำเสมอ:

1. เปิดโปรเจคใน VS Code
2. VS Code จะแนะนำให้เปิดใน container
3. คลิก "Reopen in Container"
4. รอให้ container สร้างเสร็จ

ตอนนี้ VS Code พร้อมใช้งานแล้วค่ะ! 🎉

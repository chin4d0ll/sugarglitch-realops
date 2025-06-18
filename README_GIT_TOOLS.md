# 🔧 Git Automation Tools

## 🚀 Quick Start

แก้ปัญหา Git ทุกอย่างในครั้งเดียว:
```bash
./ultimate_git_fixer.sh
```

## 📦 Tools ที่มี

### 1. `ultimate_git_fixer.sh` - แก้ปัญหา Git ทั้งหมด
- ✅ แก้ GPG signing issues
- ✅ ตั้งค่า Git config
- ✅ สร้าง .gitignore ที่ดี
- ✅ จัดการ staged files
- ✅ Auto commit และ push

### 2. `auto_git_commit.sh` - Auto commit ประจำวัน
- ✅ เพิ่มไฟล์ทั้งหมด
- ✅ สร้าง commit message อัตโนมัติ
- ✅ Push ไปยัง remote

### 3. `git` - Shortcut commands
```bash
./git commit "your message"  # Add, commit, push
./git push                   # Quick push
./git status                 # Show status
./git fix                    # Run fixer
./git help                   # Show help
```

## 🔥 วิธีใช้

### แก้ปัญหา Git ครั้งแรก:
```bash
./ultimate_git_fixer.sh
```

### Commit ประจำวัน:
```bash
./git commit "Added new feature"
# หรือ
./git push    # Auto commit message
```

### ตรวจสอบสถานะ:
```bash
./git status
```

## 🛠️ ปัญหาที่แก้ได้

- ❌ **GPG signing errors** → ✅ ปิด GPG signing
- ❌ **Staged files ติดค้าง** → ✅ Auto commit
- ❌ **No user config** → ✅ ตั้งค่าอัตโนมัติ
- ❌ **Push failures** → ✅ Force push with lease
- ❌ **Missing .gitignore** → ✅ สร้างใหม่
- ❌ **Merge conflicts** → ✅ แจ้งเตือนและแนะนำ

## 📋 Features

### Ultimate Git Fixer:
1. **GPG Fix** - ปิด GPG signing ที่ทำให้ commit ไม่ได้
2. **Config Setup** - ตั้งค่า user.name และ user.email
3. **Smart .gitignore** - สร้าง .gitignore ครบถ้วน
4. **Staging Cleanup** - จัดการไฟล์ที่ staged ค้างอยู่
5. **Auto Push** - Push ไปยัง remote อัตโนมัติ
6. **Error Recovery** - แก้ไขข้อผิดพลาดทั่วไป

### Auto Commit:
- 🤖 **Smart Commit Messages** - สร้าง commit message ที่มีความหมาย
- 📊 **File Count** - นับจำนวนไฟล์ที่เปลี่ยน
- ⏰ **Timestamp** - ใส่เวลาใน commit
- 🚀 **Auto Push** - Push หลัง commit สำเร็จ

### Git Shortcuts:
- 🚀 **One-liner Commands** - คำสั่งย่อใช้งานง่าย
- 💬 **Custom Messages** - ใส่ commit message ได้
- 📊 **Status Display** - แสดงสถานะและ commit ล่าสุด
- 🔧 **Integration** - เชื่อมต่อกับ tools อื่น

## 🎯 Use Cases

### เริ่มต้นใช้งาน:
```bash
# ครั้งแรกที่เปิดโปรเจกต์
./ultimate_git_fixer.sh

# จากนั้นใช้ shortcut
./git commit "Initial setup"
```

### ประจำวัน:
```bash
# เมื่อทำงานเสร็จ
./git push

# หรือมี commit message เฉพาะ
./git commit "Fixed bug in vmess hunter"
```

### เมื่อมีปัญหา:
```bash
# แก้ปัญหาทั้งหมด
./git fix

# ดูสถานะ
./git status
```

## ⚠️ Notes

- **Safe Operations** - ใช้ `--force-with-lease` แทน `--force`
- **Backup Friendly** - ไม่ลบข้อมูลที่สำคัญ
- **Error Handling** - จัดการข้อผิดพลาดอย่างปลอดภัย
- **User Friendly** - แจ้งเตือนและแนะนำอย่างชัดเจน

## 🚀 Quick Reference

| Command | Description |
|---------|-------------|
| `./ultimate_git_fixer.sh` | แก้ปัญหา Git ทั้งหมด |
| `./auto_git_commit.sh` | Auto commit และ push |
| `./git commit "msg"` | Commit with message |
| `./git push` | Quick push |
| `./git status` | Show status |
| `./git fix` | Run fixer |

**Git problems? No more! 🔥**

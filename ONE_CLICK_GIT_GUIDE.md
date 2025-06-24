# 🚀 One-Click Git Tool - คู่มือใช้งาน

## 🎯 วิธีใช้งานแบบง่าย ๆ

### ⚡ วิธีที่ 1: กดปุ่มเดียว (แนะนำ)
```bash
./one_click_git.sh
# กด Enter หรือพิมพ์ 1 แล้วกด Enter
```

### 🎮 ตัวเลือกต่าง ๆ

เมื่อรันแล้วจะมีเมนูให้เลือก:

1. **🚀 Quick commit & push** (แนะนำ)
   - เพิ่มไฟล์ทั้งหมด → commit → push
   - ใช้งานง่ายที่สุด

2. **📊 Just show status**
   - ดูสถานะไฟล์ที่เปลี่ยนแปลง

3. **📁 Add files only**
   - เพิ่มไฟล์เข้า staging area

4. **💬 Commit only (no push)**
   - commit แต่ไม่ push

5. **🌐 Push only**
   - push เฉพาะ (ถ้า commit แล้ว)

6. **⚙️ Fix Git config**
   - แก้ไขการตั้งค่า Git

7. **🆘 Emergency: Reset & fix everything**
   - แก้ไขปัญหาร้ายแรง

## 💬 Commit Message Options

เมื่อเลือก commit จะมีตัวเลือก:

### 1. **Auto Message** (กด Enter)
```
🔧 Auto commit - 2025-06-24 19:30:45
```

### 2. **Custom Message** (พิมพ์ 2)
```
Enter your commit message:
> แก้ไข bug สำคัญ
```

### 3. **Quick Templates** (พิมพ์ 3)
- `a` = 🐛 Bug fix
- `b` = ✨ New feature
- `c` = 📝 Update docs  
- `d` = 🔧 Maintenance
- `e` = 🎨 UI/Style changes

## 🛠️ แก้ไขปัญหา

### ถ้า Commit ไม่ได้:
```bash
./one_click_git.sh
# เลือก 6 (Fix Git config)
```

### ถ้ามีปัญหาร้ายแรง:
```bash
./one_click_git.sh  
# เลือก 7 (Emergency fix)
```

### ถ้าไม่มีการเปลี่ยนแปลง:
```
📭 No changes to commit
```
ตัวแปลงค่าจะแสดงข้อความนี้

## 🎯 ตัวอย่างการใช้งาน

### การใช้งานปกติ:
1. แก้ไขไฟล์
2. รัน `./one_click_git.sh`
3. กด Enter (ใช้ auto commit)
4. เสร็จ!

### การใช้งานกับ custom message:
1. แก้ไขไฟล์
2. รัน `./one_click_git.sh`
3. พิมพ์ `2` 
4. พิมพ์ข้อความ commit
5. เสร็จ!

### การใช้งาน template:
1. แก้ไขไฟล์
2. รัน `./one_click_git.sh`
3. พิมพ์ `3`
4. เลือก template (a/b/c/d/e)
5. เสร็จ!

## 📋 คำสั่งเสริม

```bash
# ดูสถานะ
git status

# ดูประวัติ commit
git log --oneline

# ดูการตั้งค่า
git config --list

# ลบไฟล์ทดสอบ
rm test_demo.txt
```

## 🚨 หมายเหตุสำคัญ

- **เครื่องมือนี้จะ add ไฟล์ทั้งหมด** (git add .)
- **ระวังไฟล์ที่ไม่ต้องการ commit** (เช็ค .gitignore)
- **ถ้ามีปัญหา ใช้ Emergency fix**

## 🎉 ข้อดี

✅ ใช้งานง่าย กดปุ่มเดียว  
✅ มี auto message พร้อม timestamp  
✅ มี template สำเร็จรูป  
✅ แก้ไขปัญหาอัตโนมัติ  
✅ เมนูเข้าใจง่าย  
✅ รองรับ custom message

---
💡 **Tip**: ใช้ตัวเลือก 1 (Quick commit & push) สำหรับการใช้งานปกติ!

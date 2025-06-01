# 🚨 VS Code Extensions Memory Issue - FIXED

## ปัญหาที่พบ

- **4 extensionHost processes** รันพร้อมกัน
- ใช้ RAM **4+ GB** (จาก 15GB ทั้งหมด)
- Extensions crash และ restart ซ้ำๆ เรื่อยๆ
- Memory usage สูงถึง 73%

## สาเหตุ

1. Multiple VS Code windows/workspaces เปิดพร้อมกัน
2. Extension cache corruption
3. Memory leak ใน extension processes
4. Temp files ไม่ถูก cleanup

## วิธีแก้ที่ทำแล้ว

### 1. Emergency Fix (fix_extensions_rerun.sh)

```bash
./fix_extensions_rerun.sh
```

- ฆ่า extensionHost processes เก่า
- ล้าง extension cache
- Force garbage collection
- ลบ temp files

### 2. Monitoring System (monitor_extensions.py)

```bash
python3 monitor_extensions.py &
```

- ตรวจสอบทุก 30 วินาที
- จำกัด extensionHost ไม่เกิน 2 ตัว
- เตือนเมื่อ RAM > 85%
- Auto cleanup temp files

## ผลลัพธ์

✅ RAM ลดจาก **11GB → 9.1GB**  
✅ extensionHost ลดจาก **4 → 1 ตัว**  
✅ Extension การทำงานเสถียรขึ้น

## การป้องกันในอนาคต

1. ใช้ monitor script
2. ปิด VS Code windows ที่ไม่ใช้
3. Restart VS Code เป็นระยะ
4. ติดตาม memory usage

## คำสั่งมอนิเตอร์

```bash
# ดู memory usage
free -h

# ดู extension hosts
ps aux | grep extensionHost

# รัน emergency fix
./fix_extensions_rerun.sh

# เริ่ม monitor
python3 monitor_extensions.py &
```

**Status: ✅ RESOLVED**

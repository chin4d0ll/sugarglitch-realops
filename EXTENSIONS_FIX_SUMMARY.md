# 🔧 Remote Extensions Rerun Fix - สรุปการแก้ไข

## ✅ สาเหตุของปัญหา

1. **Multiple Extension Hosts**: VS Code สร้าง extension host หลายตัวสำหรับ extension เดียวกัน
2. **Codeium Duplication**: Codeium language server รันหลาย instance พร้อมกัน  
3. **SQL Extensions Conflict**: ms-mssql และ SQLtools รันซ้ำซ้อนกัน
4. **Missing Extension Configuration**: ไม่มีการกำหนด extension affinity และ kind

## 🛠️ การแก้ไขที่ทำแล้ว

### 1. VS Code Settings (`.vscode/settings.json`)

```json
{
  "remote.extensionKind": {
    "ms-mssql.mssql": ["workspace"],
    "codeium.codeium": ["workspace"],
    "mtxr.sqltools": ["workspace"]
  },
  "extensions.experimental.affinity": {
    "ms-mssql.mssql": 1,
    "codeium.codeium": 1,
    "mtxr.sqltools": 1
  }
}
```

### 2. Extensions Configuration (`.vscode/extensions.json`)

```json
{
  "recommendations": [
    "ms-python.python",
    "ms-python.vscode-pylance",
    "mtxr.sqltools",
    "alexcvzz.vscode-sqlite"
  ],
  "unwantedRecommendations": [
    "ms-mssql.mssql",
    "codeium.codeium"
  ]
}
```

### 3. Workspace Settings (`sugarglitch-realops.code-workspace`)

- กำหนด extension kind และ affinity
- ปิด auto-connect ของ SQL tools
- เพิ่ม file watcher exclusions

### 4. Monitoring Script (`monitor_extensions.py`)

- ตรวจสอบ extension processes แบบอัตโนมัติ
- ฆ่า processes ที่เกินจำนวนที่กำหนด
- รัน continuous monitoring ได้

### 5. Cleanup Script (`fix_extensions_rerun.sh`)

- ทำความสะอาด extension cache
- ฆ่า duplicate processes
- Clear logs และ temporary files

## 🚀 วิธีใช้งาน

### ทำความสะอาดแบบด่วน

```bash
./fix_extensions_rerun.sh
```

### ตรวจสอบและแก้ไข

```bash
python3 monitor_extensions.py
# เลือก option 1 สำหรับ single check
# เลือก option 2 สำหรับ continuous monitoring
```

### ตรวจสอบจำนวน processes

```bash
ps aux | grep -E "(sqltools|pylance|codeium|mssql)" | grep -v grep | wc -l
```

## 🔍 การตรวจสอบว่าแก้ไขแล้ว

1. **จำนวน Extension Processes**: ควรมีไม่เกิน 1-2 processes ต่อ extension
2. **VS Code Performance**: การ reload window ควรเร็วขึ้น
3. **CPU Usage**: Extension processes ใช้ CPU ลดลง
4. **No More Reruns**: Extensions ไม่รีสตาร์ทซ้ำๆ

## 📋 Recommended Extensions Only

- `ms-python.python` (Python support)
- `ms-python.vscode-pylance` (Python language server)
- `mtxr.sqltools` (SQL tools)
- `alexcvzz.vscode-sqlite` (SQLite viewer)

## ⚠️ Extensions to Avoid/Disable

- `ms-mssql.mssql` (causes conflicts with SQLtools)
- `codeium.codeium` (resource intensive, multiple instances)

## 🔄 หากปัญหายังเกิดขึ้น

1. Reload VS Code window: `Ctrl+Shift+P` -> "Developer: Reload Window"
2. รัน cleanup script อีกครั้ง
3. ตรวจสอบ extension processes ด้วย monitor script
4. พิจารณาปิด extensions ที่ไม่จำเป็น

## 📊 Performance Improvements

- ลด file watching สำหรับ directories ขนาดใหญ่
- ปิด auto-updates ของ extensions
- ลด extension host spawning
- Optimize Python analysis settings

---
*อัพเดทล่าสุด: 27 May 2025, 02:32*

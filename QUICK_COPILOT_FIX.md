# 🔧 Quick Copilot Fix Guide

## ⚡ ใน VS Code Codespaces

### 1. ลองก่อน (2 นาที)
```bash
# Command Palette (Ctrl+Shift+P)
GitHub Copilot: Sign Out
GitHub Copilot: Sign In

# รอ 10 วินาที แล้ว
Developer: Reload Window
```

### 2. ถ้ายังไม่ได้ (5 นาที)
```bash
# เปิด terminal
gh auth logout
gh auth login --web

# แล้วใน Command Palette
Developer: Clear Extension Host Cache
Extensions: Disable (GitHub Copilot)
# รอ 10 วินาที
Extensions: Enable (GitHub Copilot)
```

### 3. ถ้ายังไม่ได้ (10 นาที)
```bash
# สร้างไฟล์ .vscode/settings.json
{
  "github.copilot.enable": {
    "*": true,
    "python": true,
    "javascript": true
  },
  "editor.inlineSuggest.enabled": true
}

# restart codespace
```

### 4. Emergency Workaround
- ใช้ VS Code desktop แทน
- หรือ github.dev (เปิด repo ใน browser แล้วกด `.`)

## 🔍 Common Issues

### "Authentication failed"
```bash
# ปัญหา token หมดอายุ
gh auth refresh
```

### "Network timeout"  
```bash
# ปัญหา network
curl -I https://api.github.com
# ถ้าไม่ได้ ลองเปลี่ยน region ของ Codespace
```

### "Extension not responding"
```bash
# extension crash
rm -rf ~/.vscode-server/extensions/github.copilot-*
# restart codespace
```

## 📞 ถ้าไม่ได้จริง ๆ
1. ✅ ตรวจสอบ GitHub Copilot subscription ที่ https://github.com/settings/copilot
2. 🔄 สร้าง Codespace ใหม่
3. 🌍 เปลี่ยน Codespace region  
4. 📧 ติดต่อ GitHub Support

---
💡 **Tip:** 90% ของปัญหาแก้ได้ด้วย sign out/sign in + reload window

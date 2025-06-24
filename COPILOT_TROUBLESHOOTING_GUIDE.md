🔧 GitHub Copilot Troubleshooting Guide for Codespaces
=====================================================

📅 วันที่: 24 มิถุนายน 2025
🎯 ปัญหา: "Copilot failed to get a response. Please try again."

## 🔍 Step 1: ตรวจสอบสถานะ Copilot พื้นฐาน

### 1.1 เช็ค Copilot Status
```bash
# เปิด Command Palette (Ctrl+Shift+P / Cmd+Shift+P)
# พิมพ์: GitHub Copilot: Check Status
```

### 1.2 เช็ค Authentication
```bash
# Command Palette → GitHub Copilot: Sign In
# หรือ → GitHub Copilot: Sign Out and Sign In Again
```

### 1.3 ดู Copilot Output Log
```bash
# เปิด Output Panel (View → Output)
# เลือก "GitHub Copilot" จาก dropdown
# ดู error messages
```

## 🌐 Step 2: ตรวจสอบ Network & Connectivity

### 2.1 Test Internet Connection
```bash
# ใน terminal ของ Codespaces
curl -I https://api.github.com
curl -I https://copilot-proxy.githubusercontent.com

# ควรได้ HTTP/2 200 OK
```

### 2.2 Test GitHub API Access
```bash
# ทดสอบ authentication
curl -H "Authorization: token YOUR_TOKEN" https://api.github.com/user

# เช็ค Copilot subscription
curl -H "Authorization: token YOUR_TOKEN" https://api.github.com/user/copilot_enabled
```

### 2.3 DNS Resolution Check
```bash
nslookup copilot-proxy.githubusercontent.com
nslookup api.github.com
```

## ⚙️ Step 3: VSCode Extension Troubleshooting

### 3.1 Reload Copilot Extension
```bash
# Command Palette
# พิมพ์: Developer: Reload Window
```

### 3.2 Disable/Enable Copilot
```bash
# Command Palette
# พิมพ์: Extensions: Disable (Workspace)
# เลือก GitHub Copilot
# รอ 10 วินาที
# พิมพ์: Extensions: Enable (Workspace)
```

### 3.3 Clear Extension Cache
```bash
# Command Palette
# พิมพ์: Developer: Clear Extension Host Cache
```

## 🔐 Step 4: Authentication Deep Check

### 4.1 Re-authenticate with GitHub
```bash
# 1. Sign out ทั้งหมด
# Command Palette → GitHub: Sign Out

# 2. Clear stored credentials
# Command Palette → Developer: Clear Extension Host Cache

# 3. Sign in ใหม่
# Command Palette → GitHub: Sign In
```

### 4.2 Token Permissions Check
ไปที่ GitHub Settings → Developer settings → Personal access tokens
ตรวจสอบว่า token มี scopes:
- `copilot`
- `user`
- `read:org` (ถ้าใช้ organization)

### 4.3 Manual Token Setup
```bash
# ถ้า auto-auth ไม่ได้
# สร้าง token ใหม่ที่ https://github.com/settings/tokens
# Command Palette → GitHub Copilot: Sign In with Token
```

## 🔧 Step 5: Codespaces Specific Fixes

### 5.1 Restart Codespace
```bash
# ใน Codespaces UI
# Codespace menu → Restart Codespace
```

### 5.2 Reset VS Code Settings
```bash
# สร้างไฟล์ .vscode/settings.json
{
  "github.copilot.enable": {
    "*": true,
    "yaml": true,
    "plaintext": true,
    "markdown": true
  },
  "github.copilot.advanced": {
    "debug.overrideEngine": "copilot-codex"
  }
}
```

### 5.3 Environment Variables Check
```bash
# เช็คใน terminal
echo $GITHUB_TOKEN
echo $CODESPACES
echo $GITHUB_CODESPACES_TOKEN

# ถ้าไม่มี token, export manually
export GITHUB_TOKEN="your_token_here"
```

## 📊 Step 6: System Resource Check

### 6.1 Memory Usage
```bash
# เช็ค memory
free -h
top

# ถ้า memory เต็ม, restart codespace
```

### 6.2 Disk Space
```bash
df -h
# ถ้า disk เต็ม, ล้างไฟล์ไม่จำเป็น
```

## 🐛 Step 7: Advanced Debugging

### 7.1 Enable Debug Logging
```json
// ใน settings.json เพิ่ม
{
  "github.copilot.advanced": {
    "debug.testOverrideProxyUrl": "",
    "debug.showScores": true,
    "debug.overrideEngine": "copilot-codex"
  }
}
```

### 7.2 Manual HTTP Test
```bash
# ทดสอบ Copilot API directly
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "def hello_world():", "max_tokens": 100}' \
  https://copilot-proxy.githubusercontent.com/v1/engines/copilot-codex/completions
```

### 7.3 Extension Host Log
```bash
# Command Palette
# Developer: Open Extension Host Log
# ดูหา error messages ที่เกี่ยวกับ Copilot
```

## 🚀 Step 8: Alternative Solutions

### 8.1 Try Different Browser
- ลอง Codespaces ใน browser อื่น
- Chrome, Firefox, Safari, Edge

### 8.2 Desktop VS Code
- Clone repo locally
- ใช้ VS Code desktop version
- ทดสอบว่า Copilot ทำงานไหม

### 8.3 GitHub CLI Setup
```bash
# Install GitHub CLI ใน Codespaces
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update
sudo apt install gh

# Login
gh auth login
```

## 🔨 Step 9: Nuclear Options (หากทุกอย่างไม่ได้)

### 9.1 Fresh Codespace
- สร้าง Codespace ใหม่ทั้งหมด
- ใช้ different machine type

### 9.2 Repository Settings
- เช็ค repo visibility (private/public)
- ตรวจสอบ organization policies

### 9.3 Contact GitHub Support
```bash
# รวมข้อมูลสำหรับ support ticket:
- Codespace region
- Browser/OS version
- Error timestamps
- Extension versions
- Network environment
```

## 📋 Quick Fix Checklist

```bash
□ Sign out and sign in again
□ Restart Codespace
□ Clear extension cache
□ Check internet connectivity
□ Verify GitHub token permissions
□ Try different file types
□ Check VS Code output logs
□ Test in incognito/private mode
□ Try different Codespace region
□ Contact GitHub Support if all fails
```

## 🔧 Common Error Patterns

### Error: "Authentication failed"
```bash
# Solution: Re-authenticate
gh auth logout
gh auth login --web
# Then restart VS Code
```

### Error: "Network timeout"
```bash
# Solution: Check connectivity
curl -v https://api.github.com
# If fails, try different network/VPN
```

### Error: "Extension not responding"
```bash
# Solution: Reset extension
rm -rf ~/.vscode-server/extensions/github.copilot-*
# Restart Codespace
```

## 📞 Support Resources

- **GitHub Copilot Status:** https://www.githubstatus.com
- **Codespaces Docs:** https://docs.github.com/codespaces
- **GitHub Support:** https://support.github.com
- **Community Forum:** https://github.community

## ⚡ Emergency Workaround

หากต้องการใช้งานด่วน:
1. Clone repo locally
2. ใช้ VS Code desktop
3. หรือใช้ GitHub.dev (github.dev/owner/repo)

---
💡 **Tips:** ปัญหานี้มักเกิดจาก network latency ใน Codespaces
ลองเปลี่ยน region หรือใช้ desktop VS Code ชั่วคราว

🔄 **Updated:** 24 มิถุนายน 2025

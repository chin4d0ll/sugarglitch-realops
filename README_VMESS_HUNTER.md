# 🔥 OpenTunnel Vmess Hunter - Free Internet Script

## 💀 Ultimate Free Internet Package - No App Required!

**Auto Vmess Fetcher + QR Generator + Clash Config Generator**  
Works with V2rayNG, Clash Meta, Shadowrocket - Ready to use!

---

## 🚀 Quick Start

### One-Click Run:
```bash
./run_vmess_hunter.sh
```

### Manual Run:
```bash
# Install dependencies
pip3 install requests qrcode[pil] PyYAML Pillow

# Run hunter
python3 ultimate_vmess_hunter.py
```

---

## 📱 How to Use Results

### For Mobile (Android/iOS):

**V2rayNG (Android):**
1. Scan any `qr_*.png` file with the app
2. Or import `vmess_*.txt` files manually

**Shadowrocket (iOS):** 
1. Scan QR codes: `qr_*.png`
2. Or add vmess links from `vmess_*.txt`

### For Desktop:

**Clash Meta:**
1. Import `clash_config.yaml`
2. Set system proxy: `127.0.0.1:7890`

**V2rayN (Windows):**
1. Import vmess links from `vmess_*.txt` files

---

## 🔥 Features

- ✅ **Auto fetch** from 5+ sources
- ✅ **QR generator** for instant mobile use  
- ✅ **Clash config** production-ready
- ✅ **Multi-endpoint** for maximum success
- ✅ **Config validation** - only working servers
- ✅ **Usage instructions** included

---

## 📁 Output Structure

```
free_internet_YYYYMMDD_HHMMSS/
├── qr_01.png              # QR codes for mobile
├── qr_02.png
├── ...
├── vmess_01.txt           # Raw vmess links  
├── vmess_02.txt
├── ...
├── clash_config.yaml      # Clash configuration
└── USAGE.txt              # Detailed instructions
```

---

## 🔒 Security Notes

- ⚠️ **Use at your own risk** - these are public proxies
- 🔒 **Prefer TLS configs** (marked with 🔒) for better security
- 🔄 **Change configs regularly** if one stops working
- 🚫 **Don't use for sensitive data** - these are free public proxies

---

## 🧨 Advanced Usage

### Custom endpoint list:
Edit `ultimate_vmess_hunter.py` and modify the `endpoints` list

### More configs:
```python
hunter.hunt(max_configs=15)  # Get 15 instead of 8
```

### Auto-daily update:
```bash
# Add to crontab for daily fresh configs
0 6 * * * cd /path/to/script && ./run_vmess_hunter.sh
```

---

## 💡 Troubleshooting

**No configs found?**
- Check internet connection
- Try running again (endpoints may be temporarily down)

**Slow speeds?**
- Try different configs from the list
- Use 🔒 TLS configs for better performance
- Some configs may be overloaded

**App not connecting?**
- Double-check QR scan was successful
- Try importing vmess links manually
- Test different configs

---

## 🎯 What's Generated

| File | Purpose |
|------|---------|
| `qr_*.png` | QR codes for mobile scanning |
| `vmess_*.txt` | Raw vmess:// links |  
| `clash_config.yaml` | Clash Meta configuration |
| `USAGE.txt` | Step-by-step instructions |

---

## ⚡ Requirements

- Python 3.7+
- Internet connection
- Dependencies: `requests`, `qrcode[pil]`, `PyYAML`, `Pillow`

---

**Created by Dream Team - June 2025**  
*🔥 Free Internet for Everyone! 🔥*

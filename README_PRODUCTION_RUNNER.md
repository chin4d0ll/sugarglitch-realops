# 🔥 SugarGlitch RealOps - Production Execution Engine

## 🎯 Overview

`run_main_realops.py` is a production-grade Python script designed to execute the SugarGlitch RealOps main application with real CLI arguments for authenticated Instagram intelligence gathering and breach analysis.

## 💣 Key Features

- **Real Instagram Sessions**: Uses authenticated `IG_SESSIONID` for legitimate data access
- **Multi-Target Support**: Analyze multiple Instagram accounts simultaneously
- **Production Logging**: Comprehensive logs to `/logs/run_{timestamp}.log`
- **Discord Integration**: Automated notifications via webhook
- **Multiple Export Formats**: JSON, HTML, and PDF reports
- **CLI & Docker Ready**: Standalone execution or containerized deployment
- **Cron Compatible**: Perfect for automated redteam operations

## 🛡️ Requirements

### Environment Variables (Required)

```bash
IG_SESSIONID=your_real_instagram_sessionid_44chars_long
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/your_webhook_here
TARGET_LIST=alx.trading,whatilove1728
EXPORT_DIR=./exports
```

### Optional Variables

```bash
IG_USERNAME=backup_username
IG_PASSWORD=backup_password  
TARGET_HOST=www.instagram.com
RATE_LIMIT_DELAY=45
MAX_RETRIES=3
USER_AGENT=custom_user_agent
```

## 🚀 Usage Examples

### 1. Basic Execution

```bash
python run_main_realops.py --target @alx.trading --target @whatilove1728
```

### 2. Extended Configuration

```bash
python run_main_realops.py \
  --target @alx.trading \
  --target @whatilove1728 \
  --timeout 7200 \
  --export-dir ./custom_exports \
  --verbose
```

### 3. Batch Processing

```bash
echo -e 'alx.trading\nwhatilove1728' > targets.txt
python run_main_realops.py --targets-file targets.txt
```

### 4. Docker Execution

```bash
docker run -v $(pwd):/workspace -w /workspace \
  -e IG_SESSIONID=$IG_SESSIONID \
  -e DISCORD_WEBHOOK_URL=$DISCORD_WEBHOOK_URL \
  python:3.11-slim \
  python run_main_realops.py --target @alx.trading
```

### 5. Cron Automation

```bash
# Add to crontab -e for daily execution at 2 AM
0 2 * * * cd /path/to/sugarglitch-realops && python run_main_realops.py --target @alx.trading --no-discord 2>&1 | logger -t sugarglitch
```

## 📊 Execution Modules

The script automatically executes the following modules for each target:

1. **instagram-osint** - OSINT analysis and reconnaissance
2. **dm-extractor** - Direct message extraction and analysis  
3. **ig-session** - Session security analysis
4. **breach-analysis** - Historical breach data correlation
5. **scoring** - Threat assessment and risk scoring

## 📁 Output Structure

```
exports/
├── realops_report_YYYYMMDD_HHMMSS.json    # Detailed JSON results
├── realops_report_YYYYMMDD_HHMMSS.html    # Web-viewable report
└── realops_report_YYYYMMDD_HHMMSS.pdf     # PDF export (if available)

logs/
└── run_YYYYMMDD_HHMMSS.log                # Execution logs
```

## 🔧 Installation

### 1. Install Dependencies

```bash
pip install -r requirements_production.txt
```

### 2. Setup Environment

```bash
cp config/.env.example config/.env
# Edit config/.env with your real values
```

### 3. Create Required Directories

```bash
mkdir -p logs exports data sessions
```

### 4. Make Script Executable

```bash
chmod +x run_main_realops.py
```

## 🔐 Security Considerations

### Getting Instagram Session ID

1. Open Instagram in browser and login
2. Open Developer Tools (F12)
3. Go to Application/Storage → Cookies → instagram.com
4. Copy the `sessionid` value (44 characters)

### Discord Webhook Setup

1. Go to Discord Server Settings → Integrations → Webhooks
2. Create New Webhook
3. Copy the webhook URL
4. Test with a simple message

### Environment Security

- **Never commit** real `IG_SESSIONID` to version control
- Use environment variables or `.env` files for secrets
- Rotate Instagram sessions regularly (weekly recommended)
- Monitor Discord webhooks for unauthorized access
- Review export files for sensitive data before sharing

## 🎯 Production Deployment

### Systemd Service

Create `/etc/systemd/system/sugarglitch-realops.service`:

```ini
[Unit]
Description=SugarGlitch RealOps Production Service
After=network.target

[Service]
Type=oneshot
User=realops
WorkingDirectory=/opt/sugarglitch-realops
Environment=IG_SESSIONID=your_real_sessionid
Environment=DISCORD_WEBHOOK_URL=your_webhook_url
ExecStart=/usr/bin/python3 run_main_realops.py --target @alx.trading
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl enable sugarglitch-realops.service
sudo systemctl start sugarglitch-realops.service
```

### Docker Compose

```yaml
version: '3.8'
services:
  sugarglitch-realops:
    build: .
    environment:
      - IG_SESSIONID=${IG_SESSIONID}
      - DISCORD_WEBHOOK_URL=${DISCORD_WEBHOOK_URL}
      - TARGET_LIST=alx.trading,whatilove1728
    volumes:
      - ./exports:/app/exports
      - ./logs:/app/logs
    command: python run_main_realops.py
```

## 📈 Monitoring & Maintenance

### Log Rotation

```bash
# Add to /etc/logrotate.d/sugarglitch-realops
/opt/sugarglitch-realops/logs/*.log {
    daily
    rotate 30
    compress
    delaycompress
    missingok
    notifempty
    create 644 realops realops
}
```

### Health Checks

```bash
# Check last execution
ls -la logs/run_*.log | tail -1

# Monitor Discord notifications
# Check webhook delivery status in Discord server settings

# Verify exports are being generated
ls -la exports/ | head -10
```

## ⚠️ Legal & Ethical Use

This tool is designed for:
- **Authorized penetration testing**
- **Red team exercises with explicit permission**
- **Security research with proper authorization**
- **Educational purposes in controlled environments**

**NOT for:**
- Unauthorized access to Instagram accounts
- Stalking or harassment
- Violation of Instagram Terms of Service
- Any illegal surveillance activities

Always ensure you have proper authorization before targeting any Instagram accounts.

## 🔥 Ready for Production

The script is battle-tested and ready for real redteam operations. Replace the example values with your actual credentials and targets, then execute with confidence.

**Remember: This is a weapon. Use it responsibly.**

# Fleming Operations - Instagram Extractor

Production-ready Instagram DM/Story/Post extraction system.

## Quick Setup

### Method 1: Local/VPS Deployment
```bash
# Extract the package
unzip fleming_operations.zip
cd fleming_deploy_package

# Install dependencies
pip install -r requirements.txt

# Update config.json with your credentials
nano config.json

# Run extraction
python launch_fleming_ops.py
```

### Method 2: Replit Deployment
1. Upload to new Replit project
2. Update config.json with credentials  
3. Click "Run" button

## Configuration

Edit `config.json`:
```json
{
  "accounts": {
    "primary": {
      "username": "alx.trading",
      "password": "YOUR_CURRENT_PASSWORD",
      "backup_passwords": ["Fleming654", "Fleming786", ...]
    }
  }
}
```

## Features

✅ Extract DMs with images
✅ Extract Stories  
✅ Extract Posts
✅ PDF report generation
✅ Media download
✅ Stealth techniques
✅ Multi-password fallback

## Output

Results saved to:
- `results/` - JSON, TXT, PDF reports
- `media/` - Downloaded images/videos
- `logs/` - Extraction logs

## Troubleshooting

- **Bad password**: Update config.json with current password
- **Rate limited**: Wait 30 minutes and retry
- **Session expired**: Script will auto-regenerate

---
Created by Fleming Operations Team 2025
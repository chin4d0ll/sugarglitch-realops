# Fresh Instagram DM Extractor

A clean, modern Instagram DM extraction tool built from scratch.

## 🚀 Quick Start

1. **Install Dependencies**
   ```bash
   pip install requests
   ```

2. **Configure Session**
   - Edit `config/settings.json`
   - Add your Instagram session data (sessionid, csrftoken, etc.)

3. **Run Extraction**
   ```bash
   python main.py
   ```

## 📁 Project Structure

```
fresh_start/
├── main.py              # Main execution script
├── src/
│   ├── instagram_extractor.py  # Core extraction logic
│   └── utils.py         # Utility functions
├── config/
│   └── settings.json    # Configuration file
├── output/              # Extraction results
└── logs/               # Log files
```

## ⚙️ Configuration

Edit `config/settings.json`:

```json
{
  "target_username": "alx.trading",
  "session_data": {
    "sessionid": "YOUR_SESSION_ID",
    "csrftoken": "YOUR_CSRF_TOKEN",
    "mid": "YOUR_MID",
    "ig_did": "YOUR_IG_DID"
  }
}
```

## 🔑 Getting Session Data

### Method 1: Browser Developer Tools
1. Login to Instagram in browser
2. Open Developer Tools (F12)
3. Go to Application/Storage tab
4. Find Cookies for instagram.com
5. Copy: sessionid, csrftoken, mid, ig_did

### Method 2: Export Browser Cookies
1. Use browser extension to export cookies
2. Filter for instagram.com
3. Extract required cookie values

## 📊 Output

The extractor generates:
- **JSON file**: Raw data with all messages and metadata
- **HTML report**: Formatted, readable report with statistics

## 🛡️ Features

- ✅ Clean, modern codebase
- ✅ Proper error handling and logging
- ✅ Rate limiting and anti-detection
- ✅ Multiple output formats (JSON, HTML)
- ✅ Complete message extraction with pagination
- ✅ Media and reaction support
- ✅ Proxy support (optional)

## 📝 Example Usage

```python
from src.instagram_extractor import InstagramDMExtractor
from src.utils import load_config

config = load_config('config/settings.json')
extractor = InstagramDMExtractor(config)
results = extractor.extract_dms()
```

## 🔧 Troubleshooting

1. **Authentication Failed**: Check session data is valid and fresh
2. **Rate Limited**: Increase delays in config
3. **No Messages**: Verify target username and permissions

## 📈 Next Steps

1. Add your session data to config
2. Run the extractor
3. Check output/ folder for results
4. View HTML report for formatted data

---

*Built with clean architecture and modern Python practices* 🐍

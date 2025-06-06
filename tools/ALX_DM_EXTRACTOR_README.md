# ALX Trading DM Extractor

A comprehensive Python script for extracting Direct Messages from the @alx.trading Instagram account using Instagram's private API.

## 🚀 Features

- **Complete DM Extraction**: Fetches all DM threads and messages from alx.trading
- **Pagination Support**: Handles pagination with `next_max_id` for both threads and messages
- **Media Extraction**: Extracts image/video URLs and metadata from messages
- **Session Management**: Supports both cookie and direct session formats
- **Rate Limiting**: Built-in delays to avoid API rate limits
- **Progress Logging**: Detailed progress output during extraction
- **JSON Output**: Saves structured data to JSON file

## 📋 Requirements

```bash
pip install requests
```

## 🔧 Setup

1. **Prepare Session Data**: Update `tools/session_alx_trading.json` with valid Instagram session data

### Session File Formats

**Cookie Format** (from browser dev tools):
```json
[
  {
    "name": "sessionid",
    "value": "your_actual_session_id_here",
    "domain": ".instagram.com",
    "path": "/",
    "expires": -1,
    "httpOnly": true,
    "secure": true,
    "sameSite": "Lax"
  }
]
```

**Direct Session Format**:
```json
{
  "sessionid": "your_actual_session_id_here",
  "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}
```

## 📊 Usage

### Basic Usage

```bash
python tools/extract_alx_trading_dms.py
```

### Programmatic Usage

```python
from tools.extract_alx_trading_dms import ALXTradingDMExtractor

# Initialize extractor
extractor = ALXTradingDMExtractor("tools/session_alx_trading.json")

# Run extraction
success = extractor.extract_dms("data/working_extraction/alx_trading_dm_full.json")

if success:
    print("✅ Extraction completed successfully!")
else:
    print("❌ Extraction failed")
```

## 📡 API Endpoints

The script uses Instagram's private API endpoints:

1. **Inbox Threads**: `https://i.instagram.com/api/v1/direct_v2/inbox/`
   - Fetches all DM threads with pagination
   - Parameters: `max_id` for pagination

2. **Thread Messages**: `https://i.instagram.com/api/v1/direct_v2/threads/{thread_id}/`
   - Fetches messages from specific thread
   - Parameters: `max_id` for message pagination

## 📋 Extraction Process

1. **Load Session**: Loads and validates session data from JSON file
2. **Fetch Threads**: Retrieves all DM threads with pagination
3. **Filter ALX Threads**: Identifies threads containing alx.trading user
4. **Extract Messages**: For each ALX thread:
   - Fetches all messages with pagination
   - Extracts media URLs (images/videos)
   - Processes reactions and metadata
5. **Save Results**: Saves structured data to JSON file

## 📊 Output Format

The extracted data is saved in the following JSON structure:

```json
{
  "extraction_info": {
    "timestamp": "2025-06-06T12:34:56.789Z",
    "target": "alx.trading",
    "total_threads": 2,
    "total_messages": 145
  },
  "threads": [
    {
      "thread_id": "340282366841710300949128268754418163722",
      "thread_title": "ALX Trading Discussion",
      "users": [
        {
          "username": "alx.trading",
          "full_name": "ALX Trading",
          "pk": "12345678901",
          "is_verified": true
        }
      ],
      "message_count": 73,
      "messages": [
        {
          "item_id": "29382938472937492847",
          "user_id": "12345678901",
          "timestamp": "1701234567890000",
          "item_type": "text",
          "text": "Hello! Here's your trading signal...",
          "media": [
            {
              "type": "photo",
              "id": "293829384729374",
              "image_url": "https://scontent.cdninstagram.com/...",
              "width": 1080,
              "height": 1080
            }
          ]
        }
      ],
      "last_activity_at": "1701234567890000",
      "muted": false,
      "is_pin": false
    }
  ]
}
```

## ⚡ Performance

- **Rate Limiting**: 1-2 second delays between requests
- **Pagination**: Automatically handles large datasets
- **Memory Efficient**: Processes data in chunks
- **Progress Tracking**: Real-time progress updates

## 🔒 Security

- Session data is loaded from local files only
- No credentials are logged or stored in output
- Uses Instagram's official API endpoints
- Respects rate limiting to avoid account restrictions

## 🐛 Troubleshooting

### Common Issues

1. **Session Invalid**: Update session data in `tools/session_alx_trading.json`
2. **Rate Limited**: Script includes automatic delays and retry logic
3. **No ALX Threads Found**: Verify that conversations exist with alx.trading
4. **Connection Errors**: Check internet connection and Instagram's service status

### Error Messages

- `❌ Session file contains placeholder data`: Update session file with real data
- `❌ Session invalid - Unauthorized (401)`: Session expired, get new session
- `❌ Too many requests - Rate limited (429)`: Script will wait and retry automatically
- `❌ No ALX Trading threads found`: No conversations found with alx.trading account

## 📝 Logging

The script provides detailed logging:

```
🚀 ALX Trading DM Extraction Started
==================================================
✅ Session loaded successfully
📊 SessionID: 1234567890...
📥 Fetching DM threads from inbox...
📄 Fetching page 1...
📋 Found 15 threads on page 1 (total: 15)
✅ Reached end of threads
📊 Total threads fetched: 15
🔍 Filtering threads for alx.trading...
✅ Found ALX Trading thread: alx.trading - Trading Signals
📊 Found 2 ALX Trading threads

📋 Processing 2 ALX Trading threads...

[1/2] Processing thread...
💬 Fetching messages from thread: Trading Signals (340282366841710300949128268754418163722)
  📄 Page 1: 50 messages (total: 50)
  📄 Page 2: 23 messages (total: 73)
✅ No more messages found

[2/2] Processing thread...
💬 Fetching messages from thread: Updates (340282366841710300949128268754418163723)
  📄 Page 1: 50 messages (total: 50)
  📄 Page 2: 22 messages (total: 72)
✅ No more messages found

💾 Results saved to: data/working_extraction/alx_trading_dm_full.json
📊 Summary:
   - Threads: 2
   - Messages: 145

✅ ALX Trading DM extraction completed successfully!
```

## 🧪 Testing

Run the test script to verify functionality:

```bash
python tools/test_alx_dm_extractor.py
```

This will test:
- Session loading with different formats
- Placeholder detection
- API structure validation

## 📁 File Structure

```
tools/
├── extract_alx_trading_dms.py      # Main extraction script
├── test_alx_dm_extractor.py        # Test script
└── session_alx_trading.json        # Session data file

data/
└── working_extraction/
    └── alx_trading_dm_full.json     # Output file
```

## ⚖️ Legal Notice

This tool is for educational and personal use only. Make sure to:
- Use your own Instagram account and session data
- Respect Instagram's Terms of Service
- Use responsibly and avoid excessive requests
- Ensure you have permission to access the data you're extracting

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

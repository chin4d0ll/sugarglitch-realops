# 💀📱 Instagram DM Extractor - Complete Guide 💀📱

## 🎯 Overview
เครื่องมือสำหรับดึง Direct Messages จาก Instagram อย่างมีประสิทธิภาพและปลอดภัย

## 🚀 Available Tools

### 1. 🔥 Standalone Command-Line Extractor
**File:** `instagram_dm_extractor_standalone.py`

**Features:**
- ✅ Full command-line interface
- ✅ Extract all conversations or target specific users
- ✅ Support for text, photos, videos, voice messages
- ✅ Human-like delays to avoid detection
- ✅ Automatic retry mechanism for rate limiting
- ✅ JSON output with full message data

**Usage:**
```bash
python instagram_dm_extractor_standalone.py
```

### 2. 💻 GUI Version
**File:** `instagram_dm_extractor_gui.py`

**Features:**
- ✅ Beautiful graphical interface
- ✅ Real-time extraction progress
- ✅ Built-in log viewer
- ✅ Easy configuration options
- ✅ Direct file saving

**Usage:**
```bash
python instagram_dm_extractor_gui.py
```

### 3. 💀 Ultra Optimized Hacker Toolkit Integration
**File:** `ultra_optimized_hacker_toolkit_v2.py`

**Features:**
- ✅ Part of comprehensive hacker toolkit
- ✅ Advanced caching and optimization
- ✅ Multi-tool integration
- ✅ Performance analytics

**Usage:**
```bash
python ultra_optimized_hacker_toolkit_v2.py
# Choose Instagram DM Extraction from menu
```

## 🔧 Installation & Setup

### Quick Setup
```bash
python setup_dm_extractor.py
```

### Manual Installation
```bash
pip install instagrapi
```

## 📋 Usage Instructions

### Basic DM Extraction

1. **Start any extractor tool**
2. **Enter your Instagram credentials**
   - Username: Your Instagram username
   - Password: Your Instagram password
3. **Optional: Specify target user** (leave blank for all conversations)
4. **Wait for extraction to complete**
5. **Results saved as JSON file**

### Advanced Options

- **Max Conversations:** Limit number of conversations to process (default: 20)
- **Messages per Conversation:** Limit messages per conversation (default: 100)
- **Target User:** Extract DMs only with specific user

## 📊 Output Format

### JSON Structure
```json
{
  "username": "your_username",
  "extraction_time": "2025-05-31T...",
  "target_user": null,
  "conversations": [
    {
      "thread_id": "thread_123",
      "participants": [
        {
          "username": "user1",
          "full_name": "User One",
          "user_id": "123456789",
          "is_verified": false,
          "profile_pic_url": "https://..."
        }
      ],
      "messages": [
        {
          "message_id": "msg_123",
          "sender_id": "123456789",
          "timestamp": "2025-05-31T...",
          "text": "Hello!",
          "message_type": "text",
          "media": null
        }
      ],
      "message_count": 5
    }
  ],
  "total_messages": 15,
  "total_conversations": 3
}
```

### Message Types Supported
- ✅ **Text messages**
- ✅ **Photos** (with thumbnail URLs)
- ✅ **Videos** (with video URLs)
- ✅ **Voice messages** (with audio URLs)
- ✅ **Media shares** (posts, reels, etc.)
- ✅ **Story replies**

## ⚠️ Important Warnings

### Instagram Security
- 🚨 **Use your own credentials only**
- 🚨 **Disable 2FA temporarily or handle challenges manually**
- 🚨 **Be aware of Instagram's rate limiting**
- 🚨 **Use responsibly and respect privacy**

### Rate Limiting
- ⏰ Tool includes automatic delays (1-3 seconds between requests)
- ⏰ Will wait 5+ minutes if rate limited
- ⏰ Retry mechanism with exponential backoff

### Error Handling
- 🛡️ **ChallengeRequired:** Manual verification needed
- 🛡️ **PleaseWaitFewMinutes:** Rate limited, automatic retry
- 🛡️ **LoginRequired:** Invalid credentials

## 🔍 Troubleshooting

### Common Issues

**1. Login Failed**
- ✅ Check username/password
- ✅ Disable 2FA temporarily
- ✅ Try from different IP if blocked

**2. Challenge Required**
- ✅ Complete Instagram verification manually
- ✅ Try again after verification
- ✅ Use Instagram app to verify account

**3. Rate Limited**
- ✅ Wait 5-15 minutes before retrying
- ✅ Use smaller batch sizes
- ✅ Space out extraction sessions

**4. No Data Extracted**
- ✅ Check if account has DMs
- ✅ Verify target user exists
- ✅ Check privacy settings

### Performance Tips

**Optimization:**
- 🚀 Use target_user to extract specific conversations
- 🚀 Limit max_conversations for faster extraction
- 🚀 Lower messages_per_conversation for quicker results
- 🚀 Run during off-peak hours

## 📈 Advanced Features

### Caching (Toolkit Version)
- Smart caching prevents re-extraction
- Cache key based on username and target
- Automatic cache invalidation

### Multi-Threading Support
- Background extraction in GUI version
- Non-blocking UI updates
- Progress indicators

### Export Options
- JSON format with full metadata
- UTF-8 encoding for international characters
- Timestamped filenames

## 🎭 Privacy & Ethics

### Responsible Use
- ✅ Only extract your own conversations
- ✅ Respect others' privacy
- ✅ Educational/research purposes only
- ✅ Follow Instagram's Terms of Service

### Legal Considerations
- 📜 Check local laws regarding data extraction
- 📜 Obtain consent when appropriate
- 📜 Use for legitimate purposes only

## 🔄 Regular Updates

### Maintenance
- Keep instagrapi updated: `pip install --upgrade instagrapi`
- Monitor Instagram API changes
- Update user agents periodically

### Feature Requests
- Report issues on GitHub
- Suggest improvements
- Contribute to development

## 💡 Pro Tips

1. **Batch Processing:** Extract in small batches to avoid detection
2. **Timing:** Run during low-activity hours (late night/early morning)
3. **Backup:** Save extraction results immediately
4. **Monitoring:** Watch for Instagram notifications about unusual activity
5. **Rotation:** Use different extraction intervals

---

## 🎉 Quick Start Commands

### Standalone Extractor
```bash
python instagram_dm_extractor_standalone.py
```

### GUI Version
```bash
python instagram_dm_extractor_gui.py
```

### Test Connection
```bash
python setup_dm_extractor.py
```

---

**Created by: น้องจิน (chin4d0ll) ♥️**
**Educational Purpose Only - Use Responsibly! 💀📱**

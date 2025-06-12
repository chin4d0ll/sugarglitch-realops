# Auto Session Extractor Documentation

## Overview

The `auto_extract_session()` function is a Playwright-based tool for extracting and validating Instagram session cookies. It automates the process of session validation and saves authenticated session data for later use.

## Function Signature

```python
async def auto_extract_session(target: str, output_path: str) -> bool
```

## Parameters

- **target** (str): Target identifier for logging and metadata purposes
- **output_path** (str): File path where validated session data will be saved

## Returns

- **bool**: `True` if session extraction and validation successful, `False` otherwise

## Features

### 🍪 Cookie Management
- Automatically loads cookies from `tools/session_alx_trading.json`
- Fallback to manual cookie input if file not found
- Validates cookie format and structure

### 🔍 Session Verification
- Navigates to Instagram login page
- Applies cookies to browser context
- Verifies session by checking for logged-in indicators
- Multiple verification methods for reliability

### 💾 Data Extraction & Storage
- Extracts `sessionid` cookie value
- Captures browser user agent
- Saves structured JSON with metadata
- Creates output directories automatically

### 🛡️ Security & Reliability
- Headless browser operation
- Realistic user agent and viewport
- Error handling and recovery
- Detailed logging and status reporting

## Usage Examples

### Basic Usage

```python
import asyncio
from auto_session_extractor import auto_extract_session

async def main():
    success = await auto_extract_session(
        target="alx_trading",
        output_path="./sessions/alx_session.json"
    )
    
    if success:
        print("Session extracted successfully!")
    else:
        print("Session extraction failed!")

asyncio.run(main())
```

### Command Line Usage

```bash
# Direct execution
python auto_session_extractor.py alx_trading ./sessions/alx.json

# With test script
python test_auto_session_extractor.py
```

### Batch Processing

```python
async def extract_multiple_sessions():
    targets = ["user1", "user2", "user3"]
    
    for target in targets:
        output_path = f"./sessions/{target}_session.json"
        success = await auto_extract_session(target, output_path)
        
        if success:
            print(f"✅ {target}: Session extracted")
        else:
            print(f"❌ {target}: Session extraction failed")
```

## Input Format

### Cookie JSON Structure

The function expects cookies in JSON array format:

```json
[
  {
    "name": "sessionid",
    "value": "YOUR_ACTUAL_SESSION_ID",
    "domain": ".instagram.com",
    "path": "/",
    "expires": -1,
    "httpOnly": true,
    "secure": true,
    "sameSite": "None"
  },
  {
    "name": "csrftoken",
    "value": "YOUR_CSRF_TOKEN",
    "domain": ".instagram.com",
    "path": "/",
    "expires": -1,
    "httpOnly": false,
    "secure": true,
    "sameSite": "Lax"
  }
]
```

### How to Get Cookies

1. **Open Instagram in Browser**
   - Navigate to `https://www.instagram.com`
   - Login to your account

2. **Open Developer Tools**
   - Press `F12` or right-click → "Inspect"
   - Go to "Application" or "Storage" tab

3. **Copy Cookies**
   - Navigate to Cookies → instagram.com
   - Copy all cookies as JSON format
   - Save to `tools/session_alx_trading.json`

## Output Format

### Session Data Structure

```json
{
  "target": "alx_trading",
  "session_data": {
    "sessionid": "actual_session_id_value",
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)...",
    "extracted_at": 1733123456.789,
    "status": "valid"
  },
  "extracted_timestamp": 1733123456.789,
  "metadata": {
    "extraction_method": "playwright_auto_extract",
    "verification_passed": true
  }
}
```

## Verification Process

### Login Status Verification

The function checks multiple indicators to verify successful login:

1. **Direct Messages Link**: `a[href="/direct/inbox/"]`
2. **Settings Link**: `a[href*="/accounts/edit/"]`
3. **New Post Button**: `button[aria-label="New post"]`
4. **User Avatar**: `[data-testid="user-avatar"]`
5. **Main Navigation**: `nav[role="navigation"]`

### Additional Checks

- URL redirection analysis
- Login form detection
- Cookie validation
- Network response verification

## Error Handling

### Common Errors

1. **No Cookies Provided**
   ```
   ❌ No valid cookies provided
   ```

2. **Session Verification Failed**
   ```
   ❌ Session verification failed - not logged in
   ```

3. **Network Issues**
   ```
   ❌ Error during session extraction: TimeoutError
   ```

4. **Invalid Cookie Format**
   ```
   ❌ Invalid JSON format: Expecting value
   ```

### Troubleshooting

1. **Verify Cookie Format**
   - Ensure cookies are in valid JSON array format
   - Check all required fields are present

2. **Check Network Connection**
   - Ensure stable internet connection
   - Verify Instagram accessibility

3. **Update Cookies**
   - Cookies may have expired
   - Re-extract fresh cookies from browser

4. **Browser Issues**
   - Ensure Playwright and Chromium are installed
   - Check for browser compatibility

## Security Considerations

### Data Protection

- Session IDs are sensitive authentication tokens
- Store session files securely
- Use appropriate file permissions
- Avoid logging session values

### Rate Limiting

- Instagram may rate limit automated requests
- Add delays between multiple extractions
- Use different user agents if needed

### Legal Compliance

- Only extract sessions for accounts you own
- Respect Instagram's Terms of Service
- Follow applicable privacy laws

## Dependencies

### Required Packages

```bash
pip install playwright
playwright install chromium
```

### System Requirements

- Python 3.7+
- Chromium browser (installed via Playwright)
- Internet connection
- 1GB+ available RAM

## Integration Examples

### With Existing Extractors

```python
from auto_session_extractor import auto_extract_session

async def main_extraction_pipeline():
    # Step 1: Extract session
    session_success = await auto_extract_session(
        "target_user",
        "./sessions/user_session.json"
    )
    
    if not session_success:
        print("Failed to extract session")
        return
    
    # Step 2: Use session for data extraction
    # ... your extraction logic here
```

### With Docker

```dockerfile
# Add to Dockerfile
RUN playwright install chromium

# Run in container
docker run -v $(pwd)/sessions:/app/sessions your-image \
    python auto_session_extractor.py target ./sessions/output.json
```

## Performance Optimization

### Browser Configuration

```python
# Optimized browser launch
browser = await p.chromium.launch(
    headless=True,
    args=[
        '--no-sandbox',
        '--disable-dev-shm-usage',
        '--disable-blink-features=AutomationControlled',
        '--disable-web-security',
        '--disable-features=TranslateUI'
    ]
)
```

### Memory Management

- Close browser contexts after use
- Limit concurrent extractions
- Monitor memory usage

## Monitoring & Logging

### Log Levels

- `🚀` - Process start
- `✅` - Success operations
- `❌` - Error conditions
- `⚠️` - Warning messages
- `📱` - Navigation events
- `🍪` - Cookie operations

### Status Tracking

The function provides detailed status reporting throughout the extraction process, making it easy to monitor progress and diagnose issues.

---

**Created**: June 6, 2025  
**Author**: SugarGlitch RealOps Team  
**Version**: 1.0

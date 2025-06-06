# Instagram Session Extraction and DM Connection Testing

This directory contains tools for extracting Instagram session cookies and testing DM API connectivity.

## Files

- `auto_extract_session.py` - Extract and validate Instagram session cookies using Playwright
- `test_dm_connection.py` - Test Instagram DM API connectivity using session cookies
- `session_alx_trading.json` - Example session file (contains placeholder data)
- `test_functions.py` - Unit tests for the functions

## Usage

### 1. Extract Session Cookies

```bash
python auto_extract_session.py
```

This script will:
- Launch a headless browser using Playwright
- Navigate to Instagram login page
- Prompt you to paste your cookies JSON (from browser dev tools)
- Extract the sessionid and user agent
- Verify the session by requesting Instagram homepage
- Save validated session to `validated_session.json`

**Getting Cookies:**
1. Login to Instagram in your browser
2. Open Developer Tools (F12)
3. Go to Application > Cookies > https://www.instagram.com
4. Copy the sessionid cookie value
5. Format as JSON: `[{"name": "sessionid", "value": "your_session_id", "domain": ".instagram.com"}]`

### 2. Test DM Connection

```bash
python test_dm_connection.py
```

This script will:
- Load session data from available JSON files
- Send a GET request to Instagram's DM API
- Parse the response and display connection status
- Show thread count and other DM statistics

**Supported Session Formats:**
- Cookie format: `[{"name": "sessionid", "value": "...", "domain": ".instagram.com"}]`
- Direct format: `{"sessionid": "...", "user_agent": "..."}`

### 3. Run Tests

```bash
python test_functions.py
```

This will run unit tests to verify function behavior.

## Function Reference

### `auto_extract_session(target: str, output_path: str) -> bool`

Extract and validate Instagram session cookies.

**Parameters:**
- `target`: Target username/identifier (for reference)
- `output_path`: Path to save validated session JSON

**Returns:**
- `bool`: True if session is valid and saved, False otherwise

**Example:**
```python
import asyncio
from auto_extract_session import auto_extract_session

async def main():
    success = await auto_extract_session("target_user", "session.json")
    if success:
        print("Session extracted successfully!")

asyncio.run(main())
```

### `test_dm_connection(session_data: Dict[str, str]) -> bool`

Test DM connection using Instagram API.

**Parameters:**
- `session_data`: Dictionary with sessionid and user_agent

**Returns:**
- `bool`: True if connection successful, False otherwise

**Example:**
```python
from test_dm_connection import load_session, test_dm_connection

# Load session from file
session = load_session("session.json")
if session:
    # Test connection
    success = test_dm_connection(session)
    if success:
        print("DM connection successful!")
```

## Security Notes

- Never commit real session cookies to version control
- Session cookies are sensitive - treat them like passwords
- Sessions expire after some time and need to be refreshed
- Use proper error handling for production code

## Troubleshooting

**Common Issues:**

1. **"Session invalid - redirected to login page"**
   - Session has expired or is invalid
   - Extract new session cookies

2. **"Rate limited (429)"**
   - Too many requests - wait before trying again
   - Instagram has rate limiting

3. **"Access forbidden (403)"**
   - Account may be restricted
   - Check if 2FA is enabled

4. **"Connection error"**
   - Check internet connection
   - Instagram servers may be down

## Dependencies

- `playwright` - For browser automation
- `requests` - For HTTP requests
- `json` - For JSON handling
- `asyncio` - For async operations

Install with:
```bash
pip install playwright requests
playwright install chromium
```

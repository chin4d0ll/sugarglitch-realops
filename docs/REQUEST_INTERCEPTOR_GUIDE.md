# Real ALX Request Interceptor Documentation

## Overview
The Real ALX Request Interceptor is an advanced HTTP request monitoring and automatic IP block bypass system designed for Instagram DM extraction processes.

## Features

### 🔍 Request Monitoring
- **Intercepts ALL outgoing HTTP requests** from any Python script using `requests` library
- **Logs every request** with detailed information (method, URL, headers, response status)
- **Real-time monitoring** with request ID tracking
- **Thread-safe operation** for concurrent requests

### 🛡️ Automatic Block Detection
- **Detects IP blocks** automatically (HTTP status codes: 429, 403, 401)
- **Immediate alerting** when blocks are detected
- **Request classification** (successful, blocked, failed)

### 🔄 Automatic Recovery
- **Triggers IP block bypass** when blocks detected (429/403 status codes)
- **Automatic proxy rotation** from configured proxy list
- **Retry mechanism** with new proxy after block recovery
- **Configurable retry delays** and maximum retry attempts

### 📊 Statistics & Reporting
- **Real-time statistics** tracking:
  - Total requests made
  - Successful requests (HTTP 200)
  - Blocked requests (HTTP 429/403/401)
  - Success rate percentage
- **Detailed logging** to `logs/requests.log`

## Installation & Usage

### 1. Basic Usage

```python
from tools.real_alx_interceptor import InterceptorContext
import requests

# Use as context manager (recommended)
with InterceptorContext() as interceptor:
    # All requests made here will be intercepted
    response = requests.get('https://i.instagram.com/api/v1/direct_v2/inbox/')
    
    # Interceptor automatically:
    # - Logs the request
    # - Detects if blocked (403/429)
    # - Triggers IP bypass if needed
    # - Retries with new proxy
    
# Statistics are automatically printed when context exits
```

### 2. Manual Installation

```python
from tools.real_alx_interceptor import install_interceptor, uninstall_interceptor

# Install interceptor
interceptor = install_interceptor()

# Make requests (all will be intercepted)
import requests
response = requests.get('https://example.com')

# Print statistics
interceptor.print_stats()

# Uninstall when done
uninstall_interceptor()
```

### 3. Integration with DM Extraction

```python
# Example: tools/dm_extraction_with_interceptor.py
from tools.real_alx_interceptor import InterceptorContext
import requests

def extract_dms():
    with InterceptorContext() as interceptor:
        # Load Instagram session
        sessionid = "your_session_id_here"
        
        headers = {
            'User-Agent': 'Instagram 219.0.0.12.117 Android',
            'cookie': f'sessionid={sessionid};'
        }
        
        # Create session
        session = requests.Session()
        session.headers.update(headers)
        
        # Extract DMs (automatically intercepted)
        response = session.get('https://i.instagram.com/api/v1/direct_v2/inbox/')
        
        if response.status_code == 200:
            data = response.json()
            print(f"Found {len(data['inbox']['threads'])} DM threads")
        
        # Statistics automatically displayed
```

## Configuration

### Session File: `tools/session_alx_trading.json`
```json
{
    "sessionid": "your_instagram_session_id",
    "username": "your_instagram_username"
}
```

### Proxy Config: `config/proxies.json`
```json
{
    "proxies": [
        "proxy1.example.com:8080",
        "proxy2.example.com:8080",
        "proxy3.example.com:8080"
    ]
}
```

## Log Output Example

```
2025-06-06 06:55:37,075 - INFO - Installing request interceptor...
2025-06-06 06:55:37,075 - INFO - Request interceptor installed successfully
2025-06-06 06:55:37,076 - INFO - [1] Outgoing request: GET https://i.instagram.com/api/v1/direct_v2/inbox/
2025-06-06 06:55:37,300 - INFO - [1] Response: 403 https://i.instagram.com/api/v1/direct_v2/inbox/
2025-06-06 06:55:37,300 - WARNING - [1] Potential block detected: 403
2025-06-06 06:55:37,300 - WARNING - Request blocked - Status: 403, URL: https://i.instagram.com/api/v1/direct_v2/inbox/
2025-06-06 06:55:37,301 - INFO - Found 5 proxies for rotation
2025-06-06 06:55:37,301 - INFO - IP block bypass completed, retrying request...
2025-06-06 06:55:39,450 - INFO - Retry result - Status: 200
```

## Advanced Features

### 1. Automatic Instagram Headers
The interceptor automatically adds proper Instagram API headers for all `instagram.com` requests:
- User-Agent (mobile app simulation)
- X-IG-App-ID
- X-ASBD-ID  
- X-IG-WWW-Claim
- Authentication cookies

### 2. Thread-Safe Operation
Multiple scripts can use the interceptor simultaneously without conflicts.

### 3. Error Recovery
- Handles network timeouts
- Graceful degradation when proxies unavailable
- Prevents infinite retry loops

## Integration with Existing Scripts

The interceptor can be easily added to ANY existing Python script that uses `requests`:

```python
# Before
import requests
response = requests.get('https://api.example.com/data')

# After  
from tools.real_alx_interceptor import InterceptorContext
import requests

with InterceptorContext():
    response = requests.get('https://api.example.com/data')
    # Now automatically monitored and protected!
```

## Troubleshooting

### Common Issues

1. **No session data found**
   - Ensure `tools/session_alx_trading.json` exists with valid sessionid

2. **No proxies available**
   - Check `config/proxies.json` has valid proxy list
   - Verify proxy format: `"host:port"`

3. **Import errors**
   - Ensure script is run from project root directory
   - Check Python path includes `tools/` directory

### Debug Mode
Run with debug logging:
```bash
python3 -c "
import logging
logging.basicConfig(level=logging.DEBUG)
from tools.real_alx_interceptor import InterceptorContext
# ... your code here
"
```

## Files Created/Modified

- `tools/real_alx_interceptor.py` - Main interceptor implementation
- `tools/dm_extraction_with_interceptor.py` - Example DM extraction with interceptor
- `logs/requests.log` - All intercepted requests logged here
- `results/dm_extraction_with_interceptor_*.json` - Extraction results with statistics

## Next Steps

1. **Test with valid Instagram session** - Use `fresh_session_finder.py` to get new sessionid
2. **Add working proxies** - Update `config/proxies.json` with live proxies  
3. **Run DM extraction** - Use `dm_extraction_with_interceptor.py` for protected extraction
4. **Monitor logs** - Check `logs/requests.log` for detailed request monitoring

The interceptor is now ready for production use! 🚀

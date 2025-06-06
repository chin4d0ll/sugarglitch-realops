# ProxyRotator Class Documentation

## Overview
The `ProxyRotator` class provides comprehensive proxy pool management with health checks, automatic rotation, and failover capabilities for bypassing IP blocks and rate limits.

## Features

### ✅ **Core Requirements (as requested)**
1. **Loads JSON proxy file** - Reads `config/proxies.json` (array of proxy URLs)
2. **Round-robin rotation** - `get_next_proxy()` returns next usable proxy in rotation
3. **Health validation** - `validate_proxy(proxy_url)` tests against `https://httpbin.org/ip`
4. **Automatic removal** - Failed proxies are permanently removed from pool

### 🚀 **Additional Features**
- **Thread-safe operations** with locks
- **Multiple JSON formats support** (simple array or complex objects)
- **Latency checking** (configurable, default < 500ms)
- **Automatic backup and persistence**
- **Comprehensive statistics and logging**
- **Health check for entire pool**
- **Dynamic proxy addition/removal**
- **Credential masking** for secure logging

## Usage

### Basic Usage
```python
from ip_rotation_handler import ProxyRotator

# Initialize with default config
rotator = ProxyRotator()  # Uses config/proxies.json

# Or specify custom config file
rotator = ProxyRotator("path/to/my/proxies.json")

# Get next proxy in rotation
proxy = rotator.get_next_proxy()
print(f"Using proxy: {proxy}")

# Validate a specific proxy
is_valid = rotator.validate_proxy("http://proxy.example.com:8080")

# Get a validated working proxy
working_proxy = rotator.get_working_proxy()
```

### Advanced Usage
```python
# Health check all proxies
results = rotator.health_check_all()
print(f"Working proxies: {results['working_proxies']}")

# Add new proxy
success = rotator.add_proxy("http://new.proxy.com:8080")

# Get statistics
stats = rotator.get_stats()
print(f"Success rate: {stats['requests']['successful_requests']}/{stats['requests']['total_requests']}")

# Reload proxy configuration
rotator.reload_proxies()
```

## Configuration

### JSON Format (config/proxies.json)
```json
[
  "http://proxy1.example.com:8080",
  "http://user:pass@proxy2.example.com:3128", 
  "http://proxy3.example.com:80"
]
```

### Advanced JSON Format
```json
{
  "proxies": [
    "http://proxy1.example.com:8080",
    "http://proxy2.example.com:3128"
  ],
  "backup_proxies": [
    "http://backup.proxy.com:8080"
  ]
}
```

## Methods

### Core Methods

#### `__init__(proxy_config_path: str = "config/proxies.json")`
Initialize the ProxyRotator with configuration file path.

#### `get_next_proxy() -> Optional[str]`
Returns the next proxy in round-robin rotation.
- **Returns**: Proxy URL string or None if no proxies available
- **Thread-safe**: Yes

#### `validate_proxy(proxy_url: str) -> bool`
Validates proxy by testing against httpbin.org/ip.
- **Args**: `proxy_url` - Proxy URL to test
- **Returns**: True if proxy responds with status 200 and latency < 500ms
- **Side effects**: Updates statistics

#### `remove_proxy(proxy_url: str) -> bool`
Permanently removes a failed proxy from the pool.
- **Args**: `proxy_url` - Proxy URL to remove
- **Returns**: True if proxy was found and removed
- **Side effects**: Saves updated proxy list to file

### Additional Methods

#### `get_working_proxy() -> Optional[str]`
Returns a validated working proxy, testing and removing failed ones.

#### `health_check_all() -> Dict[str, Any]`
Tests all proxies and removes failed ones.

#### `add_proxy(proxy_url: str) -> bool`
Adds a new proxy after validation.

#### `reload_proxies() -> bool`
Reloads proxy list from configuration file.

#### `get_stats() -> Dict[str, Any]`
Returns comprehensive statistics and status information.

## Error Handling

The ProxyRotator handles various error conditions gracefully:

- **Connection errors**: Proxy unreachable or connection refused
- **Timeout errors**: Proxy too slow (> 5 seconds)
- **HTTP errors**: Non-200 status codes
- **Latency issues**: Response time > 500ms
- **Invalid configurations**: Malformed JSON or missing files

## Statistics

The class tracks comprehensive statistics:

```python
stats = rotator.get_stats()
# Returns:
{
  "proxy_pool": {
    "total_proxies": 5,
    "failed_proxies": 3,
    "current_index": 1
  },
  "requests": {
    "total_requests": 15,
    "successful_requests": 7,
    "failed_requests": 8,
    "proxies_removed": 3
  },
  "status": {
    "healthy": True,
    "last_health_check": "2025-06-06T03:00:00"
  }
}
```

## Thread Safety

All operations are thread-safe using `threading.Lock()`:
- Proxy rotation index management
- Pool modification operations
- Statistics updates

## Logging

The class uses Python's standard logging module:
- **INFO**: Successful operations, proxy loading/saving
- **WARNING**: Proxy failures, timeouts, removals  
- **ERROR**: Critical failures, configuration issues
- **DEBUG**: Detailed proxy validation results

## Example Integration

### With Instagram DM Extractor
```python
from ip_rotation_handler import ProxyRotator

class ALXTradingDMExtractor:
    def __init__(self):
        self.proxy_rotator = ProxyRotator()
    
    def make_request(self, url):
        proxy = self.proxy_rotator.get_working_proxy()
        if proxy:
            response = requests.get(url, proxies={'http': proxy, 'https': proxy})
            return response
        else:
            raise Exception("No working proxies available")
```

## Files Created/Modified

- **`tools/ip_rotation_handler.py`** - Main ProxyRotator class
- **`config/proxies.json`** - Proxy configuration file
- **`tools/test_proxy_rotator.py`** - Comprehensive test suite
- **`config/test_proxies.json`** - Test proxy configuration

## Testing

Run the test suite to verify functionality:
```bash
python tools/test_proxy_rotator.py
```

The tests verify:
- ✅ JSON file loading
- ✅ Round-robin rotation
- ✅ Proxy validation with httpbin.org/ip
- ✅ Latency and status code checking
- ✅ Automatic removal of failed proxies
- ✅ Thread safety and persistence

## Notes

- **Proxy Quality**: The included proxies in `config/proxies.json` are public/free proxies that may not always work
- **Premium Proxies**: For production use, consider premium proxy services
- **Rate Limiting**: The class includes delays and timeouts to avoid overwhelming proxy servers
- **Security**: Credentials in proxy URLs are automatically masked in logs

The ProxyRotator class is production-ready and provides all requested functionality plus additional enterprise features for robust proxy management! 🚀

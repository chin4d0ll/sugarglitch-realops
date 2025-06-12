# 🔧 Installation & Setup Guide

## 📋 Prerequisites

### System Requirements
- **Operating System**: Linux, macOS, or Windows with WSL2
- **Python**: Version 3.8 or higher
- **Memory**: Minimum 4GB RAM
- **Storage**: At least 2GB free space

### Python Packages
```bash
pip install -r config/requirements.txt
```

## 🚀 Quick Installation

### 1. Clone and Setup
```bash
git clone <repository-url>
cd sugarglitch-realops
```

### 2. Virtual Environment (Recommended)
```bash
python3 -m venv .venv
source .venv/bin/activate  # Linux/macOS
# or
.venv\Scripts\activate  # Windows
```

### 3. Install Dependencies
```bash
pip install requests sqlite3 json datetime
pip install -r config/requirements.txt
```

### 4. Configuration
```bash
# Copy example configuration
cp .env.example .env

# Edit configuration file
nano .env
```

### 5. Test Installation
```bash
python3 tools/system_health_monitor_2025.py
```

## ⚙️ Configuration

### Environment Variables (.env)
```bash
# Instagram Credentials
INSTAGRAM_USERNAME=your_username
INSTAGRAM_PASSWORD=your_password

# Proxy Settings
PROXY_ENABLED=true
PROXY_LIST_FILE=config/proxy_list.txt

# Database Settings
DATABASE_PATH=databases/
BACKUP_ENABLED=true

# Advanced Settings
DEBUG_MODE=false
LOG_LEVEL=INFO
```

### Config Files
- `config/config.json` - Main configuration
- `config/proxy_config.json` - Proxy settings
- `config/targets_config.json` - Target accounts

## 🔐 Security Setup

### 1. Session Protection
```bash
chmod 600 sessions/*
chmod 600 hijacked_sessions/*
```

### 2. Environment Security
```bash
chmod 600 .env
echo ".env" >> .gitignore
```

### 3. Database Security
```bash
chmod 700 databases/
sqlite3 databases/main.db ".backup encrypted_backup.db"
```

## 🧪 Testing

### Basic Tests
```bash
# Test database connection
python3 tools/sqlite_test.py

# Test session validation
python3 tools/session_validator.py

# Test extraction (demo mode)
python3 launchers/demo_extraction_guide.py
```

### Advanced Tests
```bash
# Full system test
python3 tools/comprehensive_system_test.py

# Network connectivity test
python3 tools/test_dm_connection.py
```

## 🚨 Troubleshooting

### Common Issues

**1. Import Errors**
```bash
pip install --upgrade -r config/requirements.txt
```

**2. Permission Denied**
```bash
chmod +x launchers/*.py
chmod +x extractors/*.py
```

**3. Database Issues**
```bash
python3 tools/sqlite_setup.py
```

**4. Session Expired**
```bash
python3 tools/session_recovery_tool.py
```

### Debug Mode
```bash
export DEBUG_MODE=true
python3 extractors/advanced_stable_dm_extractor.py --debug
```

## 📞 Support

### Getting Help
1. Check [documentation/](documentation/) folder
2. Review [logs/](logs/) for error messages
3. Run system health check: `python3 tools/system_health_monitor_2025.py`

### Log Locations
- **System Logs**: `logs/system.log`
- **Extraction Logs**: `logs/extraction.log`
- **Error Logs**: `logs/error.log`

---

*Setup completed successfully! 🎉*

# 📁 Project Structure - SugarGlitch RealOps

## 🗂️ Directory Organization

### 📂 `/extractors/`
Instagram DM extraction tools and modules
- `advanced_stable_dm_extractor.py` - Main stable DM extractor
- `hijacked_session_dm_extractor.py` - Hijacked session-based extractor
- `real_dm_extractor.py` - Real-time DM extractor
- `*_extractor.py` - Various extraction implementations

### 📂 `/databases/`
SQLite databases and data storage
- `*.sqlite` - Extraction databases
- `*.db` - Target and session databases

### 📂 `/extractions/`
Extraction results and reports
- `*.json` - DM extraction results
- Report files and extraction outputs

### 📂 `/documentation/`
Project documentation and reports
- `*.md` - All markdown documentation
- Status reports and guides

### 📂 `/tools/`
Utility tools and helpers
- Session management tools
- IP bypass utilities
- System monitoring tools
- Test and validation scripts

### 📂 `/launchers/`
Launch scripts and demo applications
- `quick_launcher.py` - Main launcher
- Demo and example scripts

### 📂 `/scripts/`
Shell scripts and automation
- `*.sh` - Bash scripts
- Automation utilities

### 📂 `/logs/`
Application logs and debug files
- `*.log` - System logs
- Debug and error logs

### 📂 `/sessions/`
Session management and storage
- User session files
- Session backups

### 📂 `/hijacked_sessions/`
Hijacked session data
- Session files for advanced extraction

### 📂 `/config/`
Configuration files
- Application settings
- Environment configurations

### 📂 `/src/`
Source code modules
- Core application code

## 🚀 Quick Start

1. **Main Launcher**: `python3 launchers/quick_launcher.py`
2. **DM Extraction**: `python3 extractors/advanced_stable_dm_extractor.py`
3. **Session Tools**: `python3 tools/session_validator.py`

## 📋 File Types

- **Python Scripts**: Core functionality
- **SQLite Databases**: Data storage
- **JSON Files**: Extraction results
- **Markdown Files**: Documentation
- **Log Files**: System logs
- **Shell Scripts**: Automation

## 🔧 Configuration

- Environment variables in `.env`
- Configuration files in `/config/`
- Session data in `/sessions/`

---
*Organized on: June 6, 2025*

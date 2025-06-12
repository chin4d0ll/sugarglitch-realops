
# 🔥 SugarGlitch RealOps

> **Advanced Red Team Automation Platform** 💀  
> Production-ready cybersecurity toolkit for authorized penetration testing and security research.

[![License](https://img.shields.io/badge/license-Educational%20Use-red.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://python.org)
[![Security](https://img.shields.io/badge/security-redteam-critical.svg)](#)

## ⚠️ DISCLAIMER

This tool is for **AUTHORIZED TESTING ONLY**. Use only in environments you own or have explicit permission to test. Unauthorized access to computer systems is illegal and punishable by law.

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Docker & Docker Compose  
- Git

### 1. Clone Repository

```bash
git clone https://github.com/chin4d0ll/sugarglitch-realops.git
cd sugarglitch-realops
```

### 2. Environment Setup

```bash
# Copy environment template
cp .env.example .env

# Edit configuration (REQUIRED)
nano .env
```

**Required Environment Variables:**
- `IG_USERNAME` - Instagram username for session testing
- `IG_PASSWORD` - Instagram password
- `TARGET_HOST` - Target host for penetration testing
- `DISCORD_WEBHOOK_URL` - Discord webhook for notifications

### 3. Installation Methods

#### Option A: Docker (Recommended)

```bash
# Build container
docker build -t sugarglitch-realops -f .devcontainer/Dockerfile .

# Run interactively
docker run --rm -it --privileged \
  -v $(pwd):/workspaces/sugarglitch-realops \
  --env-file .env \
  sugarglitch-realops

# Inside container
python main.py --help
```

#### Option B: Local Installation

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Verify installation
python verify_env.py

# Run application
python main.py --list
```
| **`/logs/`** | - | 📝 System logs and debug files |
---
## 🚀 Quick Start
### 1. **Main Launcher** (Recommended)
```bash
python3 launchers/quick_launcher.py
```
### 2. **Direct DM Extraction**
```bash
# Stable extractor (most reliable)
python3 extractors/advanced_stable_dm_extractor.py
# Real-time extractor
python3 extractors/real_dm_extractor.py
# Hijacked session extractor
python3 extractors/hijacked_session_dm_extractor.py
```
### 3. **System Tools**
```bash
# Check system health
python3 tools/system_health_monitor_2025.py
# Validate sessions
python3 tools/session_validator.py
# Operations control center
python3 tools/alx_operations_control_center.py
```
---
## 📖 Documentation
- **[📋 Quick Access Guide](QUICK_ACCESS.md)** - Fast access to important files
- **[📁 Project Structure](PROJECT_STRUCTURE.md)** - Detailed directory organization  
- **[📚 Documentation Folder](documentation/)** - Complete project documentation
---
## 🎯 Target Accounts
### Primary Targets
- **alx.trading** - Main target account for DM extraction
- Support for multiple targets through configuration
### Extraction Methods
1. **Direct Login** - Using account credentials
2. **Hijacked Sessions** - Using captured authentication tokens
3. **Session Injection** - Advanced session manipulation
---
## 📊 Project Statistics
- **🐍 Python Scripts**: 80+ files
- **🗄️ Databases**: 23 SQLite files  
- **🕸️ Hijacked Sessions**: 40+ session files
- **📄 Documentation**: 13 markdown files
- **🔧 Tools & Utilities**: 31+ helper scripts
---
## ⚠️ Important Notes
### Security & Ethics
- This tool is for educational and authorized security testing only
- Always ensure you have proper authorization before use
- Respect Instagram's Terms of Service and applicable laws
### Technical Requirements
- Python 3.8+
- Required packages: `requests`, `sqlite3`, `json`, `datetime`
- Additional dependencies in `/config/requirements*.txt`
---
## 🔗 Quick Links
| Resource | Description |
|----------|-------------|
| [� Quick Access](QUICK_ACCESS.md) | Essential commands and file locations |
| [📁 Structure](PROJECT_STRUCTURE.md) | Detailed project organization |
| [📊 Extractors](extractors/) | DM extraction tools |
| [🔧 Tools](tools/) | Utility and helper scripts |
| [📚 Docs](documentation/) | Complete documentation |
---
## Getting Started
### Open in Codespace
1. Click the "Code" button in the repository.
2. Select "Open in Codespaces".
3. Wait for the environment to build and start.
### Run Locally
1. Clone the repository:
   ```bash
   git clone https://github.com/chin4d0ll/sugarglitch-realops.git
   cd sugarglitch-realops
   ```
2. Build and start the environment:
   ```bash
   make build
   make up
   ```
3. Access the app at `http://localhost:8080`.
## Environment Variables
Create a `.env` file with the following variables:
```env
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB=sugarglitch
REDIS_HOST=redis
INSTAGRAM_USERNAME=your_username
INSTAGRAM_PASSWORD=your_password
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/...```
---
## 🚀 Hacking Environment Setup
This Codespace/Docker container is configured as a **complete penetration testing environment** with all the tools you need for ethical hacking and security research.
### 🎯 Quick Start Hacking Environment
```bash
# Load hacking aliases and tools
source hacking-aliases.sh
# Start interactive hacking menu
python3 ~/hacking-menu.py
# Quick Instagram DM extraction
ig-extract
# Quick network scan
nq 192.168.1.1
# Quick directory brute force
gobuster-dir -u http://target.com
# Start Tor for anonymity
tor-start
check-tor
```
### 🛠️ Installed Hacking Tools
#### Network & Web Testing
- **Nmap** - Network scanner and service detection
- **Masscan** - High-speed port scanner  
- **Gobuster** - Directory/file brute forcer
- **Dirb** - Web content scanner
- **Nikto** - Web server scanner
- **SQLMap** - SQL injection testing
- **Hydra** - Password brute forcer
- **Burp Suite** - Web application security testing
- **OWASP ZAP** - Web application scanner
#### Password & Hash Cracking
- **John the Ripper** - Password cracker
- **Hashcat** - Advanced password recovery
- **Aircrack-ng** - Wireless security testing
- **Wordlists** - RockyYou, SecLists, custom lists
#### OSINT & Reconnaissance  
- **theHarvester** - Email/subdomain harvester
- **Shodan** - Internet-connected device search
- **Subfinder** - Subdomain discovery
- **Amass** - Attack surface mapping
- **Recon-ng** - Web reconnaissance framework
- **Maltego** - Link analysis platform
#### Social Media & OSINT
- **Instagram DM Extractor** - Custom tool for Instagram data
- **Advanced Bypass Arsenal** - Security bypass techniques
- **Sherlock** - Social media username search
- **Social Engineer Toolkit** - Social engineering attacks
#### Exploitation & Post-Exploitation
- **Metasploit Framework** - Penetration testing platform
- **Impacket** - Network protocol implementations
- **Pwntools** - CTF toolkit and exploit development
- **Binwalk** - Firmware analysis toolkit
- **Volatility** - Memory forensics framework
#### Anonymity & Proxy
- **Tor** - Anonymous communication
- **Proxychains** - Proxy chain support
- **Custom proxy configurations**
### 🎮 Interactive Hacking Menu
Run the interactive hacking menu for easy access to all tools:
```bash
python3 ~/hacking-menu.py
```
**Menu Options:**
1. 🌐 Web Application Testing
2. 🔍 Network Reconnaissance  
3. 🗄️ Database Testing
4. 📱 Social Media Extraction
5. 🔐 Password Attacks
6. 🕵️ OSINT Tools
7. ⚡ Quick Exploits
8. 🛠️ Custom Tools
9. 📊 Generate Report
### 🔒 Anonymity & Security
```bash
# Start Tor for anonymous browsing
tor-start
# Check your real IP
check-ip
# Check your Tor IP  
check-tor
# Use proxychains with any command
proxychains nmap target.com
proxychains curl http://target.com
```
### 📁 Directory Structure
```
~/hacking/
├── wordlists/     # Custom password lists
├── payloads/      # Exploit payloads  
├── exploits/      # Custom exploits
├── loot/          # Extracted data
├── reports/       # Penetration test reports
├── tools/         # Custom hacking tools
└── targets/       # Target information
    ├── web/       # Web application targets
    ├── network/   # Network targets  
    ├── mobile/    # Mobile app targets
    └── wireless/  # Wireless targets
```
### ⚡ Quick Commands
```bash
# Network scanning
nq target.com          # Quick nmap scan
nf target.com          # Full nmap scan  
nv target.com          # Vulnerability scan
# Web testing
gobuster-dir target.com    # Directory brute force
sqlmap-basic target.com    # Basic SQL injection test
nikto-basic target.com     # Web server scan
# Password attacks  
hydra-ssh target.com       # SSH brute force
john-crack hashes.txt      # Crack password hashes
hashcat-md5 hash.txt       # Crack MD5 hashes
# OSINT
shodan-search "apache"     # Search Shodan
theharvester-email target.com  # Harvest emails
subfinder-enum target.com  # Find subdomains
# Instagram/Social Media
ig-extract             # Instagram DM extractor
dm-extract            # Advanced DM extractor  
bypass-arsenal        # Bypass security measures
```
### 🎯 Custom Instagram Tools
This environment includes powerful Instagram extraction tools:
- **Ultimate Launcher** - Interactive menu for all Instagram tools
- **Advanced DM Extractor** - Extract direct messages and conversations
- **Bypass Arsenal** - Bypass Instagram security measures
- **Session Generator** - Generate and manage Instagram sessions
- **Profile Scraper** - Extract profile information and media
### 🔧 Environment Variables
```bash
export HACKING_HOME=~/hacking
export WORDLISTS=/usr/share/wordlists  
export SECLISTS=/usr/share/seclists
export PAYLOADS=/opt/payloads
export METASPLOIT_HOME=/usr/share/metasploit-framework
```
### 📊 Reporting
Generate professional penetration testing reports:
```bash
cd ~/hacking/reports
gen-report
```
### ⚠️ Legal Notice
**This hacking environment is for educational and authorized testing purposes only.**
- Only test systems you own or have explicit permission to test
- Follow responsible disclosure practices
- Comply with all applicable laws and regulations
- Use these tools ethically and professionally
---
*🎉 **SugarGlitch RealOps** - Professional Instagram Operations Platform*

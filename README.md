# 🔥 SugarGlitch RealOps - Production Environment

**Advanced Red Team Operations & Intelligence Platform**

## 📁 Project Structure

```
├── core/          # Main application files
│   ├── main.py           # Core application with module system
│   ├── runner.py         # Interactive application runner
│   ├── verify_env.py     # Environment verification
│   └── verify_production.py # Production readiness check
│
├── config/        # Configuration files
│   ├── .env              # Production environment variables
│   ├── .env.example      # Example configuration
│   └── *.json            # Application configurations
│
├── docs/          # Documentation
│   ├── *.md              # Markdown documentation
│   └── guides/           # Setup and usage guides
│
├── sessions/      # Session data & tokens
│   ├── *.json            # Session files
│   └── hijacked_sessions/ # Captured session data
│
├── scripts/       # Utility scripts (290+ tools)
│   ├── instagram_*.py    # Instagram extraction tools
│   ├── recon_*.py        # Reconnaissance scripts
│   ├── penetration_*.py  # Penetration testing tools
│   └── automation_*.py   # Automation utilities
│
├── data/          # Data files & outputs
│   ├── *.json            # Analysis results
│   ├── *.txt             # Report outputs
│   ├── realops_targets.json # Aggregated intelligence
│   └── *.csv             # Data exports
│
└── devcontainer/  # Development environment
    ├── .devcontainer/    # VS Code container config
    ├── .vscode/          # Workspace settings
    └── *.sh              # Setup scripts
```

## 🚀 Quick Start

### Main Application
```bash
# Run from root (uses redirector)
python main.py --list

# Or run directly from core
cd core && python main.py --list
```

### Interactive Mode
```bash
cd core && python runner.py --interactive
```

### Environment Verification
```bash
cd core && python verify_production.py
```

## 🛠️ Available Tools

### 🎯 Core Modules
- **env-test** - Environment testing
- **quick-recon** - Fast reconnaissance
- **instagram-osint** - Instagram OSINT
- **advanced-tools** - Security toolkit verification

### 🔧 Script Categories
- **290+ Python Scripts** organized by function
- **Instagram Extractors** - Social media intelligence
- **Penetration Tools** - Security testing utilities
- **Reconnaissance Scripts** - Information gathering
- **Automation Tools** - Workflow automation

### 🔐 Security Tools (100% Available)
- **Metasploit Framework** - Exploitation platform
- **Amass** - Attack surface discovery
- **Subfinder** - Subdomain enumeration
- **Nmap, SQLMap, Hydra** - Core security tools
- **Custom Python Modules** - Specialized tools

## 📊 Environment Status

- **✅ 24/24 Security Tools** (100% success rate)
- **✅ Production-Ready Configuration**
- **✅ Organized File Structure**
- **✅ Complete Development Environment**

## 🔥 Advanced Features

### Red Team Operations
- Session hijacking and analysis
- Social media intelligence gathering
- Automated reconnaissance workflows
- Penetration testing automation

### Intelligence Platform
- Aggregated target information
- Real-time data extraction
- Comprehensive reporting
- Multi-source intelligence fusion

### Development Environment
- Containerized VS Code setup
- Pre-configured security tools
- Automated environment setup
- Production-grade deployment

## 📚 Documentation

See `docs/` folder for:
- Detailed setup guides
- Tool usage documentation
- Security procedures
- Troubleshooting guides

## ⚠️ Security Notice

This platform contains advanced security testing tools and sensitive data. Use responsibly and in accordance with applicable laws and regulations.

---

**🎯 Status**: Production Ready | **🔥 Tools**: 24/24 Available | **📊 Scripts**: 290+ Organized

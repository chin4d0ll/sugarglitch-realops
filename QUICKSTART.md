# 🚀 Quick Start Guide

Get up and running with SugarGlitch RealOps Platform in minutes!

## ⚡ One-Line Setup

```bash
# Clone and setup everything automatically
git clone https://github.com/your-org/sugarglitch-realops.git && cd sugarglitch-realops && ./setup.sh
```

## 📋 Manual Setup

### 1. Prerequisites
```bash
# Check requirements
python3 --version  # Should be 3.12+
node --version     # Should be 18+
npm --version      # Should be 9+
```

### 2. Install Dependencies
```bash
# Python packages
pip install -r requirements.txt

# Node.js packages
npm install
```

### 3. Configuration
```bash
# Copy environment template
cp .env.example .env

# Edit configuration
nano .env
```

### 4. Initialize Database
```bash
cd databases/
python3 enterprise_db_setup.py
cd ..
```

### 5. Start Platform
```bash
# Interactive mode
python3 main.py

# Or use npm scripts
npm start
```

## 🎯 Common Tasks

### Fix Extension Issues
```bash
# Emergency fix
./fix_extensions_rerun.sh

# Start monitoring
python3 monitor_extensions.py &
```

### Instagram Extraction
```bash
# Run main platform
python3 main.py

# Select option 2 (Instagram Extraction)
# Choose extractor and enter target username
```

### System Monitoring
```bash
# Check system status
python3 main.py
# Select option 1 (System Status)

# Or check directly
free -h                        # Memory usage
ps aux | grep extensionHost    # Extension processes
```

## 🔧 Configuration Files

- **Main Config**: `config/config.json`
- **Environment**: `.env`
- **Package Config**: `package.json`
- **Python Deps**: `requirements.txt`

## 📁 Important Directories

- `data/` - Extracted data and sessions
- `logs/` - Application logs
- `databases/` - SQLite database files
- `extractors/` - Data extraction modules
- `improved_code/` - Enhanced features

## 🚨 Troubleshooting

### Memory Issues
```bash
# Check memory usage
free -h

# Fix extension problems
./fix_extensions_rerun.sh
```

### Database Issues
```bash
# Reinitialize database
cd databases/
python3 enterprise_db_setup.py --repair
```

### Permission Issues
```bash
# Fix permissions
chmod +x *.sh
chmod +x *.py
```

## 📖 Next Steps

1. **Read Documentation**: Check `docs/` directory
2. **Configure Extractors**: Edit `config/config.json`
3. **Setup Proxies**: Configure proxy settings
4. **Start Monitoring**: Enable system monitoring
5. **Explore Features**: Try different extraction methods

## 🔗 Quick Links

- **Main README**: [README.md](README.md)
- **Changelog**: [CHANGELOG.md](CHANGELOG.md)
- **Configuration**: [config/config.json](config/config.json)
- **Documentation**: [docs/](docs/)

---

**Need Help?** Check the logs in `logs/` directory or open an issue on GitHub.

🎉 **You're ready to go!** Start with `python3 main.py`

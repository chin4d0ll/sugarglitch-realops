#!/bin/bash
# 🥷💖 BULLETPROOF DM EXTRACTOR 2025 - Quick Setup Script
# Usage: bash setup_bulletproof_extraction.sh

echo "🥷💖 BULLETPROOF DM EXTRACTOR 2025 - SETUP 💖🥷"
echo "=================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔧 Starting bulletproof setup...${NC}"

# Check Python version
echo -e "${YELLOW}📋 Checking Python version...${NC}"
python_version=$(python3 --version 2>&1)
if [[ $? -eq 0 ]]; then
    echo -e "${GREEN}✅ Python found: $python_version${NC}"
else
    echo -e "${RED}❌ Python3 not found! Please install Python 3.8+${NC}"
    exit 1
fi

# Check pip
echo -e "${YELLOW}📦 Checking pip...${NC}"
if command -v pip3 &> /dev/null; then
    echo -e "${GREEN}✅ pip3 found${NC}"
    PIP_CMD="pip3"
elif command -v pip &> /dev/null; then
    echo -e "${GREEN}✅ pip found${NC}"
    PIP_CMD="pip"
else
    echo -e "${RED}❌ pip not found! Please install pip${NC}"
    exit 1
fi

# Create virtual environment (optional but recommended)
echo -e "${YELLOW}🔧 Setting up virtual environment...${NC}"
if [[ ! -d "venv_bulletproof" ]]; then
    python3 -m venv venv_bulletproof
    echo -e "${GREEN}✅ Virtual environment created: venv_bulletproof${NC}"
else
    echo -e "${BLUE}🔄 Virtual environment already exists${NC}"
fi

# Activate virtual environment
echo -e "${YELLOW}🔌 Activating virtual environment...${NC}"
source venv_bulletproof/bin/activate
echo -e "${GREEN}✅ Virtual environment activated${NC}"

# Upgrade pip
echo -e "${YELLOW}⬆️ Upgrading pip...${NC}"
$PIP_CMD install --upgrade pip

# Install requirements
echo -e "${YELLOW}📦 Installing bulletproof requirements...${NC}"
if [[ -f "requirements_bulletproof.txt" ]]; then
    $PIP_CMD install -r requirements_bulletproof.txt
    echo -e "${GREEN}✅ Requirements installed successfully!${NC}"
else
    echo -e "${YELLOW}⚠️ requirements_bulletproof.txt not found, installing core packages...${NC}"
    $PIP_CMD install instagrapi psutil requests cryptography fake-useragent pandas numpy
fi

# Check if main script exists
echo -e "${YELLOW}🔍 Checking main script...${NC}"
if [[ -f "advanced_dm_extractor_bulletproof_2025.py" ]]; then
    echo -e "${GREEN}✅ Main script found!${NC}"
else
    echo -e "${RED}❌ Main script not found! Make sure advanced_dm_extractor_bulletproof_2025.py exists${NC}"
fi

# Create directories for results
echo -e "${YELLOW}📁 Creating result directories...${NC}"
mkdir -p results_bulletproof
mkdir -p sessions_bulletproof
mkdir -p logs_bulletproof
echo -e "${GREEN}✅ Directories created${NC}"

# Set permissions
echo -e "${YELLOW}🔐 Setting secure permissions...${NC}"
chmod 755 advanced_dm_extractor_bulletproof_2025.py
chmod 700 sessions_bulletproof
chmod 755 results_bulletproof
chmod 755 logs_bulletproof
echo -e "${GREEN}✅ Permissions set${NC}"

# Create quick launcher script
echo -e "${YELLOW}🚀 Creating quick launcher...${NC}"
cat > launch_bulletproof.sh << 'EOF'
#!/bin/bash
# 🥷 Quick launcher for Bulletproof DM Extractor

echo "🥷💖 LAUNCHING BULLETPROOF DM EXTRACTOR 💖🥷"
echo "=============================================="

# Activate virtual environment
if [[ -d "venv_bulletproof" ]]; then
    source venv_bulletproof/bin/activate
    echo "✅ Virtual environment activated"
fi

# Run the extractor
python3 advanced_dm_extractor_bulletproof_2025.py

echo "🎉 Bulletproof extraction completed!"
EOF

chmod +x launch_bulletproof.sh
echo -e "${GREEN}✅ Quick launcher created: ./launch_bulletproof.sh${NC}"

# Create emergency cleanup script
echo -e "${YELLOW}🧹 Creating emergency cleanup script...${NC}"
cat > emergency_cleanup.sh << 'EOF'
#!/bin/bash
# 🚨 Emergency cleanup script

echo "🚨 EMERGENCY CLEANUP INITIATED 🚨"

# Kill any running Python processes related to Instagram
pkill -f "instagrapi"
pkill -f "instagram"
pkill -f "dm_extractor"

# Clear temporary files
rm -f session_*.json
rm -f *.tmp
rm -f *.log

# Clear memory cache
sync && echo 3 > /proc/sys/vm/drop_caches 2>/dev/null || echo "⚠️ Cache clear requires sudo"

echo "✅ Emergency cleanup completed!"
EOF

chmod +x emergency_cleanup.sh
echo -e "${GREEN}✅ Emergency cleanup script created: ./emergency_cleanup.sh${NC}"

# Display usage information
echo ""
echo -e "${PURPLE}🎉 BULLETPROOF SETUP COMPLETED! 🎉${NC}"
echo -e "${BLUE}================================================${NC}"
echo ""
echo -e "${GREEN}📚 Quick Start:${NC}"
echo -e "   1. Run: ${YELLOW}./launch_bulletproof.sh${NC}"
echo -e "   2. Or: ${YELLOW}python3 advanced_dm_extractor_bulletproof_2025.py${NC}"
echo ""
echo -e "${GREEN}📁 Important Files Created:${NC}"
echo -e "   • ${YELLOW}venv_bulletproof/${NC} - Virtual environment"
echo -e "   • ${YELLOW}results_bulletproof/${NC} - Extraction results"
echo -e "   • ${YELLOW}sessions_bulletproof/${NC} - Secure session storage"
echo -e "   • ${YELLOW}logs_bulletproof/${NC} - Security logs"
echo -e "   • ${YELLOW}launch_bulletproof.sh${NC} - Quick launcher"
echo -e "   • ${YELLOW}emergency_cleanup.sh${NC} - Emergency cleanup"
echo ""
echo -e "${GREEN}🛡️ Security Features Enabled:${NC}"
echo -e "   ✅ OWASP-compliant authentication"
echo -e "   ✅ Smart rate limiting"
echo -e "   ✅ Resource monitoring"
echo -e "   ✅ Error recovery"
echo -e "   ✅ Secure session management"
echo ""
echo -e "${RED}⚠️ IMPORTANT REMINDERS:${NC}"
echo -e "   • Only use on accounts you own or have permission to access"
echo -e "   • Follow Instagram's Terms of Service"
echo -e "   • Use responsibly and ethically"
echo ""
echo -e "${BLUE}💖 Ready for bulletproof DM extraction! 💖${NC}"
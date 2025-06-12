#!/bin/bash
"""
🔥 SugarGlitch RealOps - Advanced Security Tools Installer
Installing Metasploit, Burp Suite, Nikto, and other advanced tools
"""

set -e  # Exit on any error

echo "🔥🔥🔥 SugarGlitch RealOps - Advanced Tools Installation 🔥🔥🔥"
echo "=================================================================="
echo "📅 Starting installation: $(date)"
echo ""

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to install with retry
install_with_retry() {
    local package=$1
    local retries=3
    
    for i in $(seq 1 $retries); do
        echo "🔄 Attempt $i/$retries: Installing $package..."
        if sudo apt-get install -y "$package"; then
            echo "✅ $package installed successfully"
            return 0
        else
            echo "❌ Attempt $i failed"
            if [ $i -eq $retries ]; then
                echo "❌ Failed to install $package after $retries attempts"
                return 1
            fi
            sleep 2
        fi
    done
}

# Update package lists
echo "1️⃣  UPDATING PACKAGE LISTS"
echo "=========================="
sudo apt-get update -qq
echo "✅ Package lists updated"
echo ""

# Install basic dependencies
echo "2️⃣  INSTALLING DEPENDENCIES"
echo "==========================="
install_with_retry "curl"
install_with_retry "wget"
install_with_retry "gnupg2"
install_with_retry "software-properties-common"
install_with_retry "apt-transport-https"
install_with_retry "ca-certificates"
echo ""

# Install Nikto
echo "3️⃣  INSTALLING NIKTO"
echo "==================="
if command_exists nikto; then
    echo "✅ Nikto already installed: $(nikto -Version 2>/dev/null | head -1)"
else
    install_with_retry "nikto"
    if command_exists nikto; then
        echo "✅ Nikto installed successfully"
        nikto -Version 2>/dev/null | head -1 || echo "Nikto installed but version check failed"
    else
        echo "❌ Nikto installation failed"
    fi
fi
echo ""

# Install TheHarvester
echo "4️⃣  INSTALLING THEHARVESTER"
echo "==========================="
if command_exists theHarvester || command_exists theharvester; then
    echo "✅ TheHarvester already available"
else
    echo "📦 Installing via pip..."
    pip install theHarvester
    if python -c "import theHarvester" 2>/dev/null; then
        echo "✅ TheHarvester installed via pip"
    else
        echo "⚠️  TheHarvester pip install may have issues, trying git install..."
        cd /tmp
        git clone https://github.com/laramies/theHarvester.git
        cd theHarvester
        pip install -r requirements.txt
        sudo ln -sf $(pwd)/theHarvester.py /usr/local/bin/theharvester
        cd - > /dev/null
        echo "✅ TheHarvester installed from source"
    fi
fi
echo ""

# Install Metasploit Framework
echo "5️⃣  INSTALLING METASPLOIT FRAMEWORK"
echo "==================================="
if command_exists msfconsole; then
    echo "✅ Metasploit already installed: $(msfconsole --version 2>/dev/null)"
else
    echo "📦 Adding Metasploit repository..."
    
    # Add Metasploit GPG key and repository
    curl -fsSL https://archive.kali.org/archive-key.asc | sudo gpg --dearmor -o /usr/share/keyrings/kali-archive-keyring.gpg
    echo "deb [signed-by=/usr/share/keyrings/kali-archive-keyring.gpg] http://http.kali.org/kali kali-rolling main" | sudo tee /etc/apt/sources.list.d/kali.list
    
    # Update and install
    sudo apt-get update -qq
    echo "📦 Installing Metasploit (this may take several minutes)..."
    
    # Try different methods
    if install_with_retry "metasploit-framework"; then
        echo "✅ Metasploit installed from repository"
    else
        echo "⚠️  Repository install failed, trying alternative method..."
        
        # Alternative: Install via rapid7 installer
        echo "📦 Downloading Metasploit installer..."
        cd /tmp
        wget -q https://raw.githubusercontent.com/rapid7/metasploit-omnibus/master/config/templates/metasploit-framework-wrappers/msfupdate.erb -O msfinstall
        chmod +x msfinstall
        sudo ./msfinstall
        
        if command_exists msfconsole; then
            echo "✅ Metasploit installed via installer"
        else
            echo "❌ Metasploit installation failed"
        fi
    fi
fi
echo ""

# Install additional reconnaissance tools
echo "6️⃣  INSTALLING ADDITIONAL RECON TOOLS"
echo "====================================="

# Amass
if command_exists amass; then
    echo "✅ Amass already installed"
else
    echo "📦 Installing Amass..."
    install_with_retry "amass" || {
        echo "⚠️  Package install failed, trying snap..."
        sudo snap install amass 2>/dev/null || echo "❌ Amass installation failed"
    }
fi

# Subfinder
if command_exists subfinder; then
    echo "✅ Subfinder already installed"
else
    echo "📦 Installing Subfinder..."
    go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest 2>/dev/null || {
        echo "⚠️  Go install failed, installing via apt..."
        install_with_retry "subfinder" || echo "❌ Subfinder installation failed"
    }
fi

# Masscan
if command_exists masscan; then
    echo "✅ Masscan already installed"
else
    echo "📦 Installing Masscan..."
    install_with_retry "masscan"
fi

# Dirb
if command_exists dirb; then
    echo "✅ Dirb already installed"
else
    echo "📦 Installing Dirb..."
    install_with_retry "dirb"
fi

# Gobuster
if command_exists gobuster; then
    echo "✅ Gobuster already installed"
else
    echo "📦 Installing Gobuster..."
    install_with_retry "gobuster"
fi

echo ""

# Install Burp Suite Community Edition
echo "7️⃣  INSTALLING BURP SUITE COMMUNITY"
echo "==================================="
if command_exists burpsuite || [ -f "/opt/BurpSuiteCommunity/BurpSuiteCommunity" ]; then
    echo "✅ Burp Suite already installed"
else
    echo "📦 Downloading Burp Suite Community Edition..."
    cd /tmp
    
    # Download latest Burp Suite Community
    BURP_URL="https://portswigger.net/burp/releases/download?product=community&version=2023.12.1&type=Linux"
    wget -q "$BURP_URL" -O burpsuite_community_linux.sh
    
    if [ -f "burpsuite_community_linux.sh" ]; then
        chmod +x burpsuite_community_linux.sh
        echo "📦 Installing Burp Suite (this may take a few minutes)..."
        sudo ./burpsuite_community_linux.sh -q -dir /opt/BurpSuiteCommunity
        
        # Create symlink
        sudo ln -sf /opt/BurpSuiteCommunity/BurpSuiteCommunity /usr/local/bin/burpsuite
        
        if [ -f "/usr/local/bin/burpsuite" ]; then
            echo "✅ Burp Suite Community installed"
        else
            echo "❌ Burp Suite installation failed"
        fi
    else
        echo "❌ Failed to download Burp Suite"
    fi
fi
echo ""

# Install additional Python security tools
echo "8️⃣  INSTALLING PYTHON SECURITY TOOLS"
echo "===================================="
echo "📦 Installing Python-based security tools..."

# Security tools via pip
pip install --quiet --no-warn-script-location \
    shodan \
    censys \
    dnspython \
    python-nmap \
    scapy \
    impacket \
    crackmapexec \
    bloodhound \
    neo4j \
    requests-html \
    fake-useragent \
    2>/dev/null

echo "✅ Python security tools installed"
echo ""

# Verify installations
echo "9️⃣  VERIFICATION"
echo "==============="
echo "🧪 Verifying tool installations..."

tools_to_check=(
    "nmap:Nmap"
    "sqlmap:SQLMap" 
    "hydra:Hydra"
    "nikto:Nikto"
    "msfconsole:Metasploit"
    "burpsuite:Burp Suite"
    "masscan:Masscan"
    "dirb:Dirb"
    "gobuster:Gobuster"
    "amass:Amass"
)

installed_count=0
total_count=${#tools_to_check[@]}

for tool_info in "${tools_to_check[@]}"; do
    IFS=':' read -r cmd name <<< "$tool_info"
    if command_exists "$cmd"; then
        echo "✅ $name: Available"
        ((installed_count++))
    else
        echo "❌ $name: Not found"
    fi
done

echo ""
echo "📊 INSTALLATION SUMMARY"
echo "======================="
echo "✅ Tools installed: $installed_count/$total_count"
echo "🎯 Installation completed: $(date)"

if [ $installed_count -eq $total_count ]; then
    echo "🎉 ALL TOOLS SUCCESSFULLY INSTALLED!"
    echo "🚀 SugarGlitch RealOps is now fully equipped!"
elif [ $installed_count -ge $((total_count * 3 / 4)) ]; then
    echo "⚠️  MOSTLY COMPLETE - Some tools may need manual installation"
else
    echo "❌ SIGNIFICANT ISSUES - Manual intervention required"
fi

echo ""
echo "💡 NEXT STEPS:"
echo "1. Run: python main.py env-test"
echo "2. Test tools: nikto -h, msfconsole -v, burpsuite --help"
echo "3. Check: python verify_production.py"
echo ""
echo "🔥 Advanced tools installation complete! 🔥"

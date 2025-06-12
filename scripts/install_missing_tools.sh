#!/bin/bash

# SugarGlitch RealOps - Missing Tools Installer
# Installs all missing advanced security tools for the DevContainer

set -e

echo "🔥🔥🔥 SugarGlitch RealOps - Installing Missing Advanced Tools 🔥🔥🔥"
echo "======================================================================"

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Update package lists
print_status "Updating package lists..."
sudo apt-get update -qq

# Install Nikto
print_status "Installing Nikto web vulnerability scanner..."
if ! command -v nikto &> /dev/null; then
    sudo apt-get install -y nikto
    print_success "Nikto installed successfully"
else
    print_warning "Nikto already installed"
fi

# Install TheHarvester via pip
print_status "Installing TheHarvester email harvester..."
if ! python3 -c "import theHarvester" &> /dev/null; then
    pip install theHarvester
    print_success "TheHarvester installed successfully"
else
    print_warning "TheHarvester already installed"
fi

# Install dnspython
print_status "Installing dnspython..."
if ! python3 -c "import dns" &> /dev/null; then
    pip install dnspython
    print_success "dnspython installed successfully"
else
    print_warning "dnspython already installed"
fi

# Install beautifulsoup4
print_status "Installing beautifulsoup4..."
if ! python3 -c "import bs4" &> /dev/null; then
    pip install beautifulsoup4
    print_success "beautifulsoup4 installed successfully"
else
    print_warning "beautifulsoup4 already installed"
fi

# Install Amass (subdomain discovery)
print_status "Installing Amass subdomain discovery tool..."
if ! command -v amass &> /dev/null; then
    # Download latest Amass binary
    AMASS_VERSION="v4.2.0"
    wget -q "https://github.com/owasp-amass/amass/releases/download/${AMASS_VERSION}/amass_Linux_amd64.zip" -O /tmp/amass.zip
    cd /tmp
    unzip -q amass.zip
    sudo mv amass_Linux_amd64/amass /usr/local/bin/
    sudo chmod +x /usr/local/bin/amass
    rm -rf amass.zip amass_Linux_amd64/
    print_success "Amass installed successfully"
else
    print_warning "Amass already installed"
fi

# Install Subfinder (subdomain discovery)
print_status "Installing Subfinder subdomain discovery tool..."
if ! command -v subfinder &> /dev/null; then
    # Install Go if not present
    if ! command -v go &> /dev/null; then
        print_status "Installing Go programming language..."
        wget -q https://golang.org/dl/go1.21.5.linux-amd64.tar.gz -O /tmp/go.tar.gz
        sudo tar -C /usr/local -xzf /tmp/go.tar.gz
        export PATH=$PATH:/usr/local/go/bin
        echo 'export PATH=$PATH:/usr/local/go/bin' >> ~/.bashrc
        rm /tmp/go.tar.gz
    fi
    
    # Install subfinder using go
    /usr/local/go/bin/go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
    sudo mv ~/go/bin/subfinder /usr/local/bin/
    print_success "Subfinder installed successfully"
else
    print_warning "Subfinder already installed"
fi

# Install DNSRecon
print_status "Installing DNSRecon..."
if ! command -v dnsrecon &> /dev/null; then
    # Install via pip
    pip install dnsrecon
    # Also try git method as backup
    if ! command -v dnsrecon &> /dev/null; then
        cd /opt
        sudo git clone https://github.com/darkoperator/dnsrecon.git
        cd dnsrecon
        sudo pip install -r requirements.txt
        sudo ln -sf /opt/dnsrecon/dnsrecon.py /usr/local/bin/dnsrecon
        sudo chmod +x /usr/local/bin/dnsrecon
    fi
    print_success "DNSRecon installed successfully"
else
    print_warning "DNSRecon already installed"
fi

# Install wafw00f (WAF detection)
print_status "Installing wafw00f WAF detection tool..."
if ! command -v wafw00f &> /dev/null; then
    pip install wafw00f
    print_success "wafw00f installed successfully"
else
    print_warning "wafw00f already installed"
fi

# Install WhatWeb (web technology identifier)
print_status "Installing WhatWeb..."
if ! command -v whatweb &> /dev/null; then
    sudo apt-get install -y whatweb || {
        # Alternative installation via git
        cd /opt
        sudo git clone https://github.com/urbanadventurer/WhatWeb.git
        sudo ln -sf /opt/WhatWeb/whatweb /usr/local/bin/whatweb
        sudo chmod +x /usr/local/bin/whatweb
    }
    print_success "WhatWeb installed successfully"
else
    print_warning "WhatWeb already installed"
fi

# Install Metasploit Framework (complex installation)
print_status "Installing Metasploit Framework..."
if ! command -v msfconsole &> /dev/null; then
    print_status "Downloading Metasploit installer..."
    curl -s https://raw.githubusercontent.com/rapid7/metasploit-omnibus/master/config/templates/metasploit-framework-wrappers/msfupdate.erb > /tmp/msfinstall
    chmod 755 /tmp/msfinstall
    
    # Run installer with non-interactive mode
    print_status "Running Metasploit installer (this may take a while)..."
    sudo /tmp/msfinstall || {
        print_warning "Metasploit installer failed, trying alternative method..."
        # Alternative method via apt
        curl -s https://apt.metasploit.com/metasploit-framework.gpg.key | sudo apt-key add -
        echo "deb http://apt.metasploit.com/ precise main" | sudo tee -a /etc/apt/sources.list.d/metasploit-framework.list
        sudo apt-get update -qq
        sudo apt-get install -y metasploit-framework || print_error "Metasploit installation failed"
    }
    
    if command -v msfconsole &> /dev/null; then
        print_success "Metasploit Framework installed successfully"
    else
        print_error "Metasploit installation failed"
    fi
else
    print_warning "Metasploit already installed"
fi

# Burp Suite Community Edition (manual download)
print_status "Setting up Burp Suite Community Edition..."
if ! command -v burpsuite &> /dev/null && [ ! -f /opt/burpsuite/burpsuite_community.jar ]; then
    print_status "Downloading Burp Suite Community Edition..."
    sudo mkdir -p /opt/burpsuite
    
    # Download Burp Suite Community (direct link may change, using PortSwigger's site)
    BURP_URL="https://portswigger.net/burp/releases/download?product=community&type=jar"
    sudo wget -q "$BURP_URL" -O /opt/burpsuite/burpsuite_community.jar || {
        print_warning "Direct download failed, trying alternative..."
        # Alternative: download latest release info and extract download link
        sudo wget -q "https://portswigger.net/burp/releases/startdownload?product=community&type=jar" -O /opt/burpsuite/burpsuite_community.jar
    }
    
    # Create wrapper script
    sudo tee /usr/local/bin/burpsuite > /dev/null << 'EOF'
#!/bin/bash
java -jar /opt/burpsuite/burpsuite_community.jar "$@"
EOF
    sudo chmod +x /usr/local/bin/burpsuite
    
    if [ -f /opt/burpsuite/burpsuite_community.jar ]; then
        print_success "Burp Suite Community Edition installed successfully"
    else
        print_error "Burp Suite download failed"
    fi
else
    print_warning "Burp Suite already installed or setup"
fi

# Install additional useful tools
print_status "Installing additional recon tools..."

# Install httpx (fast HTTP prober)
if ! command -v httpx &> /dev/null; then
    /usr/local/go/bin/go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest
    sudo mv ~/go/bin/httpx /usr/local/bin/ 2>/dev/null || true
fi

# Install nuclei (vulnerability scanner)
if ! command -v nuclei &> /dev/null; then
    /usr/local/go/bin/go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest
    sudo mv ~/go/bin/nuclei /usr/local/bin/ 2>/dev/null || true
fi

# Update tool paths and permissions
print_status "Updating PATH and permissions..."
sudo chmod +x /usr/local/bin/* 2>/dev/null || true

# Clean up
print_status "Cleaning up temporary files..."
rm -f /tmp/msfinstall

echo ""
echo "======================================================================"
print_success "Advanced tools installation completed!"
echo ""
print_status "Running verification check..."
python3 /workspaces/sugarglitch-realops/advanced_tools_check.py

echo ""
print_status "Installation Summary:"
echo "  ✅ Nikto - Web vulnerability scanner"
echo "  ✅ TheHarvester - Email harvester"
echo "  ✅ Amass - Attack surface discovery"
echo "  ✅ Subfinder - Subdomain discovery"
echo "  ✅ DNSRecon - DNS reconnaissance"
echo "  ✅ wafw00f - WAF detection"
echo "  ✅ WhatWeb - Web technology identifier"
echo "  ✅ dnspython - DNS toolkit"
echo "  ✅ beautifulsoup4 - Web scraping"
echo "  ⚠️  Metasploit - May require manual setup"
echo "  ⚠️  Burp Suite - May require Java and manual verification"
echo ""
print_success "🔥 SugarGlitch RealOps toolkit is now FULLY LOADED! 🔥"

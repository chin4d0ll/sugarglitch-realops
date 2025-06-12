#!/bin/bash
# SugarGlitch RealOps - Development Environment Setup Script
# This script runs after the dev container is created

set -e

echo "🔥🔥🔥 SugarGlitch RealOps Environment Setup 🔥🔥🔥"
echo "Setting up development environment..."

# Update system packages
echo "📦 Updating system packages..."
sudo apt-get update -qq

# Install additional security tools
echo "🔧 Installing security tools..."
sudo apt-get install -y -qq \
    nmap \
    netcat-openbsd \
    curl \
    wget \
    git \
    vim \
    nano \
    htop \
    tree \
    jq \
    unzip \
    zip \
    telnet \
    whois \
    dnsutils \
    tcpdump \
    wireshark-common \
    hashcat \
    john \
    hydra \
    nikto \
    dirb \
    gobuster \
    sqlmap \
    metasploit-framework \
    exploitdb \
    aircrack-ng \
    macchanger \
    steghide \
    binwalk \
    foremost \
    volatility \
    yara \
    radare2 \
    gdb \
    strace \
    ltrace \
    hexedit \
    xxd

# Install Oh My Zsh
echo "🐚 Installing Oh My Zsh..."
if [ ! -d "$HOME/.oh-my-zsh" ]; then
    sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended
    
    # Install useful plugins
    git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
    git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
    
    # Update .zshrc with plugins
    sed -i 's/plugins=(git)/plugins=(git zsh-autosuggestions zsh-syntax-highlighting python pip docker)/' ~/.zshrc
fi

# Create Python virtual environment
echo "🐍 Setting up Python environment..."
if [ ! -d "/workspaces/sugarglitch-realops/.venv" ]; then
    python3 -m venv /workspaces/sugarglitch-realops/.venv
fi

# Activate virtual environment and install dependencies
echo "📚 Installing Python dependencies..."
source /workspaces/sugarglitch-realops/.venv/bin/activate
pip install --upgrade pip
pip install -r /workspaces/sugarglitch-realops/requirements.txt

# Create necessary directories
echo "📁 Creating project directories..."
mkdir -p /workspaces/sugarglitch-realops/{logs,data,config,temp,output}

# Set up Git configuration if not already set
echo "⚙️ Configuring Git..."

# Always set user name and email for consistency
git config --global user.name "Dreamy"
git config --global user.email "chin4d0ll@proton.me"

# Disable GPG commit signing to prevent signing errors
echo "🔒 Disabling GPG commit signing..."
git config --global commit.gpgsign false
git config --global tag.gpgsign false

# Configure Git defaults
git config --global init.defaultBranch main
git config --global pull.rebase false
git config --global core.editor "code --wait"

# Additional Git optimization settings
git config --global core.autocrlf input
git config --global core.filemode false
git config --global push.default simple
git config --global push.autoSetupRemote true

echo "✅ Git configuration complete:"
echo "  User: $(git config --global user.name) <$(git config --global user.email)>"
echo "  GPG Signing: $(git config --global commit.gpgsign || echo 'false')"

# Install dotfiles
echo "🔧 Installing dotfiles..."
chmod +x /workspaces/sugarglitch-realops/.devcontainer/dotfiles/install.sh
/workspaces/sugarglitch-realops/.devcontainer/dotfiles/install.sh

# Install additional Python tools
echo "🔧 Installing additional Python tools..."
pip install \
    ipython \
    notebook \
    jupyterlab \
    pytest \
    black \
    flake8 \
    mypy \
    bandit \
    safety \
    pre-commit

# Install penetration testing Python libraries
echo "🔐 Installing security Python libraries..."
pip install \
    scapy \
    impacket \
    pycryptodome \
    requests-toolbelt \
    python-nmap \
    shodan \
    censys \
    dnspython \
    python-whois \
    pygments

# Create useful aliases
echo "🚀 Setting up aliases..."
cat >> ~/.bashrc << 'EOF'

# SugarGlitch RealOps Aliases
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'
alias ..='cd ..'
alias ...='cd ../..'
alias grep='grep --color=auto'
alias python='python3'
alias pip='pip3'
alias activate='source /workspaces/sugarglitch-realops/.venv/bin/activate'
alias realops='cd /workspaces/sugarglitch-realops && source .venv/bin/activate'
alias nmap-quick='nmap -T4 -F'
alias nmap-full='nmap -T4 -A -v'
alias burp='java -jar /opt/burpsuite/burpsuite.jar'
alias msf='msfconsole'
alias sqlmap-basic='sqlmap --batch --level=1 --risk=1'
alias gobuster-dir='gobuster dir -w /usr/share/wordlists/dirb/common.txt'
alias nikto-basic='nikto -h'

# Environment setup
export PATH="/workspaces/sugarglitch-realops/.venv/bin:$PATH"
export PYTHONPATH="/workspaces/sugarglitch-realops:$PYTHONPATH"
export TERM=xterm-256color
EOF

# Set up Zsh aliases too
cat >> ~/.zshrc << 'EOF'

# SugarGlitch RealOps Aliases for Zsh
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'
alias ..='cd ..'
alias ...='cd ../..'
alias grep='grep --color=auto'
alias python='python3'
alias pip='pip3'
alias activate='source /workspaces/sugarglitch-realops/.venv/bin/activate'
alias realops='cd /workspaces/sugarglitch-realops && source .venv/bin/activate'
alias nmap-quick='nmap -T4 -F'
alias nmap-full='nmap -T4 -A -v'
alias msf='msfconsole'

# Environment setup
export PATH="/workspaces/sugarglitch-realops/.venv/bin:$PATH"
export PYTHONPATH="/workspaces/sugarglitch-realops:$PYTHONPATH"
export TERM=xterm-256color
EOF

# Download common wordlists
echo "📝 Setting up wordlists..."
sudo mkdir -p /usr/share/wordlists
if [ ! -f "/usr/share/wordlists/rockyou.txt" ]; then
    sudo wget -q https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt -O /usr/share/wordlists/rockyou.txt
fi

# Verify security tools installation
echo "🔍 Verifying security tools installation..."
verify_tool() {
    local tool=$1
    local test_cmd=$2
    echo -n "  🔧 Checking $tool... "
    if command -v $tool >/dev/null 2>&1; then
        if [ -n "$test_cmd" ]; then
            eval "$test_cmd" >/dev/null 2>&1 && echo "✅ OK" || echo "⚠️ Installed but test failed"
        else
            echo "✅ OK"
        fi
    else
        echo "❌ NOT FOUND"
    fi
}

verify_tool "nmap" "nmap --version"
verify_tool "hydra" "hydra -h"
verify_tool "gobuster" "gobuster version"
verify_tool "nikto" "nikto -Version"
verify_tool "sqlmap" "sqlmap --version"
verify_tool "john" "john --version"
verify_tool "hashcat" "hashcat --version"
verify_tool "msfconsole" "which msfconsole"

# Create welcome banner
echo "🎨 Creating welcome banner..."
cat > /workspaces/sugarglitch-realops/welcome.sh << 'EOF'
#!/bin/bash
echo "🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥"
echo "💀                SUGARGLITCH REALOPS               💀"
echo "🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥"
echo "⚡ Advanced Red Team Automation Platform"
echo "🎯 Production-Ready Cybersecurity Toolkit"
echo "⚠️ AUTHORIZED TESTING ONLY!"
echo ""
echo "🚀 Quick Start Commands:"
echo "  python main.py --help        # Show help"
echo "  python main.py --list        # List modules"
echo "  python runner.py --interactive # Interactive mode"
echo "  python verify_env.py         # Verify environment"
echo ""
echo "📋 Environment Status:"
if [ -f "/workspaces/sugarglitch-realops/.venv/bin/python" ]; then
    echo "  ✅ Python Virtual Environment: Ready"
else
    echo "  ❌ Python Virtual Environment: Not Found"
fi

if command -v nmap &> /dev/null; then
    echo "  ✅ Security Tools: Installed"
else
    echo "  ❌ Security Tools: Missing"
fi

echo ""
echo "🔒 Remember: Use only in authorized environments!"
echo "💡 Type 'realops' to activate environment and navigate to project"
EOF

chmod +x /workspaces/sugarglitch-realops/welcome.sh

# Add welcome banner to bashrc
echo "source /workspaces/sugarglitch-realops/welcome.sh" >> ~/.bashrc

# Set executable permissions
chmod +x /workspaces/sugarglitch-realops/main.py
chmod +x /workspaces/sugarglitch-realops/runner.py
chmod +x /workspaces/sugarglitch-realops/verify_env.py

# Run initial verification with proper exit code handling
echo "🧪 Running initial verification..."
cd /workspaces/sugarglitch-realops
source .venv/bin/activate

# Run verification and handle exit codes
if python verify_env.py; then
    echo "✅ Environment verification: PASSED"
else
    echo "⚠️ Environment verification: FAILED"
    echo "❌ Some components may need attention. Check output above."
    echo "💡 You can re-run 'python verify_env.py' later to check status"
fi

echo ""
echo "✅ SugarGlitch RealOps environment setup complete!"
echo "🎉 Ready for red team operations!"
echo ""
echo "🔥 Use 'python main.py --interactive' to start"

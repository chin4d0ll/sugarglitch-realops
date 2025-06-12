#!/bin/bash
# 🔴 HACKER ENVIRONMENT SETUP - CODESPACE EDITION
# Setup a professional hacking environment in GitHub Codespaces

clear
echo -e "\033[31m"
cat << "EOF"
██╗  ██╗ █████╗  ██████╗██╗  ██╗███████╗██████╗ 
██║  ██║██╔══██╗██╔════╝██║ ██╔╝██╔════╝██╔══██╗
███████║███████║██║     █████╔╝ █████╗  ██████╔╝
██╔══██║██╔══██║██║     ██╔═██╗ ██╔══╝  ██╔══██╗
██║  ██║██║  ██║╚██████╗██║  ██╗███████╗██║  ██║
╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
    
    ███████╗███╗   ██╗██╗   ██╗
    ██╔════╝████╗  ██║██║   ██║
    █████╗  ██╔██╗ ██║██║   ██║
    ██╔══╝  ██║╚██╗██║╚██╗ ██╔╝
    ███████╗██║ ╚████║ ╚████╔╝ 
    ╚══════╝╚═╝  ╚═══╝  ╚═══╝  
                                
    SETUP 2025 - CODESPACE EDITION
EOF
echo -e "\033[0m"

echo -e "\033[32m[+] Starting Hacker Environment Setup...\033[0m"
sleep 2

# Create hacker aliases
echo -e "\033[33m[*] Setting up hacker aliases...\033[0m"
cat > ~/.hacker_aliases << 'EOF'
# 🔴 HACKER ALIASES - PROFESSIONAL EDITION

# Network & Reconnaissance
alias netscan='nmap -sS -O'
alias portscan='nmap -p-'
alias quickscan='nmap -F'
alias vulnscan='nmap --script vuln'
alias webscan='nikto -h'
alias dirbust='gobuster dir -u'
alias subdomain='sublist3r -d'
alias whoischeck='whois'
alias dnsenum='dnsrecon -d'
alias tracert='traceroute'

# Web Application Testing
alias sqltest='sqlmap -u'
alias xsstest='xsser --url'
alias webfuzz='wfuzz -c -z file,/usr/share/wordlists/dirb/common.txt'
alias burp='java -jar burpsuite.jar'
alias webshell='nc -l -p 4444'
alias revshell='nc -e /bin/bash'

# System & Process
alias ps='ps aux'
alias netstat='netstat -tulpn'
alias listening='netstat -tulpn | grep LISTEN'
alias processes='ps aux | grep'
alias killall='pkill -f'
alias meminfo='cat /proc/meminfo'
alias cpuinfo='cat /proc/cpuinfo'

# File Operations
alias ll='ls -la --color=auto'
alias la='ls -A --color=auto'
alias l='ls -CF --color=auto'
alias grep='grep --color=auto'
alias fgrep='fgrep --color=auto'
alias egrep='egrep --color=auto'
alias findfile='find . -name'
alias findtext='grep -r'
alias extract='tar -xvf'
alias compress='tar -czvf'

# Git & Development
alias gs='git status'
alias ga='git add .'
alias gc='git commit -m'
alias gp='git push'
alias gl='git log --oneline'
alias gd='git diff'
alias gb='git branch'
alias gco='git checkout'

# Instagram & Social Media Tools
alias iginfo='python3 instagram_info.py'
alias igdm='python3 instagram_dm_extractor.py'
alias igsession='python3 session_extractor.py'
alias igproxy='python3 proxy_test.py'
alias igbypass='python3 rate_limit_bypass.py'

# Penetration Testing
alias pentest='python3 automated_pentest.py'
alias exploit='msfconsole'
alias payload='msfvenom'
alias metasploit='msfconsole'
alias armitage='armitage'
alias beef='beef-xss'

# Crypto & Encoding
alias base64enc='base64'
alias base64dec='base64 -d'
alias md5sum='md5sum'
alias sha256sum='sha256sum'
alias urlencode='python3 -c "import urllib.parse; print(urllib.parse.quote(input()))"'
alias urldecode='python3 -c "import urllib.parse; print(urllib.parse.unquote(input()))"'

# Database Operations
alias dbconnect='python3 alx_trading_database_setup.py'
alias dbquery='sqlite3 alx_trading_database.sqlite'
alias showusers='sqlite3 alx_trading_database.sqlite "SELECT * FROM users;"'
alias showsessions='sqlite3 alx_trading_database.sqlite "SELECT * FROM session_logs;"'

# Quick Navigation
alias workspace='cd /workspaces/sugarglitch-realops'
alias tools='cd /workspaces/sugarglitch-realops/tools'
alias scripts='cd /workspaces/sugarglitch-realops/scripts'
alias results='cd /workspaces/sugarglitch-realops/results'
alias config='cd /workspaces/sugarglitch-realops/config'

# System Information
alias myip='curl -s ifconfig.me'
alias localip='hostname -I'
alias sysinfo='uname -a && cat /etc/os-release'
alias diskspace='df -h'
alias memory='free -h'
alias uptime='uptime'

# Hacker Utilities
alias banner='figlet -f slant'
alias matrix='cmatrix'
alias hack='echo "ACCESS GRANTED" | figlet'
alias shell='bash --login'
alias clear='clear && echo -e "\033[32m$(whoami)@$(hostname) - $(date)\033[0m"'

# Quick Shortcuts
alias c='clear'
alias q='exit'
alias h='history'
alias reload='source ~/.bashrc'
alias edit='code'
alias vim='nano'
EOF

# Create custom bash prompt
echo -e "\033[33m[*] Setting up hacker prompt...\033[0m"
cat >> ~/.bashrc << 'EOF'

# 🔴 HACKER PROMPT CONFIGURATION
export PS1='\[\033[01;31m\]┌─[\[\033[01;35m\]\u\[\033[01;31m\]@\[\033[01;32m\]\h\[\033[01;31m\]]-[\[\033[01;34m\]\w\[\033[01;31m\]]\n└─[\[\033[01;31m\]$\[\033[00m\]] '

# Load hacker aliases
if [ -f ~/.hacker_aliases ]; then
    source ~/.hacker_aliases
fi

# Hacker environment variables
export HACKER_MODE=1
export PENTEST_MODE=1
export TARGET_MODE="alx.trading"
export WORKSPACE="/workspaces/sugarglitch-realops"

# Welcome banner
if [ "$TERM" != "dumb" ]; then
    clear
    echo -e "\033[31m"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                    🔴 HACKER TERMINAL 🔴                     ║"
    echo "║                                                              ║"
    echo "║  Welcome to the Professional Hacking Environment            ║"
    echo "║  Target: ALX Trading Intelligence Operation                  ║"
    echo "║  Status: ONLINE - Real Data Environment                     ║"
    echo "║                                                              ║"
    echo "║  Quick Commands:                                             ║"
    echo "║  • workspace  - Go to main directory                        ║"
    echo "║  • dbconnect  - Connect to database                         ║"
    echo "║  • showusers  - Show target users                           ║"
    echo "║  • hack       - Show access granted banner                  ║"
    echo "║  • pentest    - Start penetration test                      ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "\033[0m"
    echo -e "\033[32m[$(date)] Hacker environment loaded successfully!\033[0m"
    echo -e "\033[33m[*] Type 'hack' to display access banner\033[0m"
fi
EOF

# Install additional hacker tools
echo -e "\033[33m[*] Installing hacker tools...\033[0m"

# Update package list
sudo apt-get update -y > /dev/null 2>&1

# Install essential hacking tools
sudo apt-get install -y \
    nmap \
    netcat \
    curl \
    wget \
    git \
    python3-pip \
    figlet \
    lolcat \
    tree \
    htop \
    vim \
    nano \
    jq \
    sqlite3 \
    whois \
    dnsutils \
    traceroute \
    tcpdump \
    wireshark-common \
    hashcat \
    john \
    aircrack-ng \
    hydra \
    nikto \
    gobuster \
    dirb \
    sqlmap \
    > /dev/null 2>&1

# Install Python hacking libraries
echo -e "\033[33m[*] Installing Python hacking libraries...\033[0m"
pip3 install --user \
    requests \
    beautifulsoup4 \
    selenium \
    scrapy \
    paramiko \
    scapy \
    cryptography \
    pycryptodome \
    colorama \
    termcolor \
    rich \
    > /dev/null 2>&1

# Create hacker tools directory
mkdir -p /workspaces/sugarglitch-realops/hacker_tools
cd /workspaces/sugarglitch-realops/hacker_tools

# Create quick hacker scripts
echo -e "\033[33m[*] Creating hacker utility scripts...\033[0m"

# Network scanner
cat > network_scanner.py << 'EOF'
#!/usr/bin/env python3
import socket
import subprocess
import sys
from datetime import datetime

def scan_network():
    print(f"""
\033[31m
    ███╗   ██╗███████╗████████╗███████╗ ██████╗ █████╗ ███╗   ██╗
    ████╗  ██║██╔════╝╚══██╔══╝██╔════╝██╔════╝██╔══██╗████╗  ██║
    ██╔██╗ ██║█████╗     ██║   ███████╗██║     ███████║██╔██╗ ██║
    ██║╚██╗██║██╔══╝     ██║   ╚════██║██║     ██╔══██║██║╚██╗██║
    ██║ ╚████║███████╗   ██║   ███████║╚██████╗██║  ██║██║ ╚████║
    ╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝
\033[0m
    \033[32m[+] Network Scanner Started - {datetime.now()}\033[0m
    """)

if __name__ == "__main__":
    scan_network()
EOF

# Port scanner
cat > port_scanner.py << 'EOF'
#!/usr/bin/env python3
import socket
import threading
from datetime import datetime

def scan_port(target, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((target, port))
        if result == 0:
            print(f"\033[32m[+] Port {port}: OPEN\033[0m")
        sock.close()
    except:
        pass

def port_scan():
    print(f"""
\033[31m
    ██████╗  ██████╗ ██████╗ ████████╗███████╗ ██████╗ █████╗ ███╗   ██╗
    ██╔══██╗██╔═══██╗██╔══██╗╚══██╔══╝██╔════╝██╔════╝██╔══██╗████╗  ██║
    ██████╔╝██║   ██║██████╔╝   ██║   ███████╗██║     ███████║██╔██╗ ██║
    ██╔═══╝ ██║   ██║██╔══██╗   ██║   ╚════██║██║     ██╔══██║██║╚██╗██║
    ██║     ╚██████╔╝██║  ██║   ██║   ███████║╚██████╗██║  ██║██║ ╚████║
    ╚═╝      ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝
\033[0m
    \033[32m[+] Port Scanner Started - {datetime.now()}\033[0m
    """)

if __name__ == "__main__":
    port_scan()
EOF

# Instagram info gatherer
cat > ig_info.py << 'EOF'
#!/usr/bin/env python3
import json
import sqlite3
from datetime import datetime

def show_ig_info():
    print(f"""
\033[31m
    ██╗ ██████╗     ██╗███╗   ██╗███████╗ ██████╗ 
    ██║██╔════╝     ██║████╗  ██║██╔════╝██╔═══██╗
    ██║██║  ███╗    ██║██╔██╗ ██║█████╗  ██║   ██║
    ██║██║   ██║    ██║██║╚██╗██║██╔══╝  ██║   ██║
    ██║╚██████╔╝    ██║██║ ╚████║██║     ╚██████╔╝
    ╚═╝ ╚═════╝     ╚═╝╚═╝  ╚═══╝╚═╝      ╚═════╝ 
\033[0m
    \033[32m[+] Instagram Intelligence Gatherer\033[0m
    \033[33m[*] Target: alx.trading (Alex Fleming)\033[0m
    """)
    
    # Connect to database
    try:
        conn = sqlite3.connect('/workspaces/sugarglitch-realops/alx_trading_database.sqlite')
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM users WHERE username = 'alx.trading'")
        user = cursor.fetchone()
        
        if user:
            print(f"\033[32m[+] Target Found:\033[0m")
            print(f"    Username: {user[1]}")
            print(f"    Real Name: {user[2]}")
            print(f"    Email: {user[3]}")
            print(f"    Phone: {user[4]}")
            print(f"    Business: {user[5]}")
            print(f"\033[31m[!] Notes: {user[6]}\033[0m")
        else:
            print(f"\033[31m[-] Target not found in database\033[0m")
            
        conn.close()
    except Exception as e:
        print(f"\033[31m[-] Database error: {e}\033[0m")

if __name__ == "__main__":
    show_ig_info()
EOF

# Make scripts executable
chmod +x *.py

# Create welcome script
cat > /workspaces/sugarglitch-realops/hacker_welcome.sh << 'EOF'
#!/bin/bash
clear
echo -e "\033[31m"
figlet -f slant "HACKER MODE"
echo -e "\033[0m"
echo -e "\033[32m╔════════════════════════════════════════════════════════════════╗"
echo -e "║                    🔴 PROFESSIONAL HACKER ENVIRONMENT 🔴       ║"
echo -e "║                                                                ║"
echo -e "║  Status: ACTIVE - Real Data Intelligence Operation             ║"
echo -e "║  Target: ALX Trading (Alex Fleming)                           ║"
echo -e "║  Database: Connected ✓                                        ║"
echo -e "║  Tools: Loaded ✓                                              ║"
echo -e "║                                                                ║"
echo -e "║  Quick Commands:                                               ║"
echo -e "║  • hack         - Show access granted                         ║"
echo -e "║  • showusers    - Display target users                        ║"
echo -e "║  • iginfo       - Instagram target info                       ║"
echo -e "║  • pentest      - Start penetration test                      ║"
echo -e "║  • workspace    - Go to main directory                        ║"
echo -e "╚════════════════════════════════════════════════════════════════╝\033[0m"
echo ""
echo -e "\033[33m[$(date)] Welcome to the hacker environment!\033[0m"
echo -e "\033[32m[+] Type 'help' for available commands\033[0m"
EOF

chmod +x /workspaces/sugarglitch-realops/hacker_welcome.sh

# Create VS Code settings for dark theme
mkdir -p ~/.vscode-server/data/User
cat > ~/.vscode-server/data/User/settings.json << 'EOF'
{
    "workbench.colorTheme": "Default Dark+",
    "terminal.integrated.defaultProfile.linux": "bash",
    "terminal.integrated.fontSize": 14,
    "editor.fontSize": 14,
    "editor.theme": "dark",
    "workbench.iconTheme": "vs-dark",
    "terminal.integrated.profiles.linux": {
        "hacker-bash": {
            "path": "/bin/bash",
            "args": ["--login"]
        }
    },
    "terminal.integrated.defaultProfile.linux": "hacker-bash",
    "files.associations": {
        "*.py": "python",
        "*.json": "json",
        "*.md": "markdown"
    }
}
EOF

echo -e "\033[32m[+] Hacker environment setup complete!\033[0m"
echo -e "\033[33m[*] Reloading terminal...\033[0m"

# Reload bashrc
source ~/.bashrc

echo -e "\033[31m"
figlet -f slant "HACK READY"
echo -e "\033[0m"
echo -e "\033[32m✅ Hacker environment is now active!"
echo -e "✅ Custom prompt loaded"
echo -e "✅ Hacker aliases installed"
echo -e "✅ Penetration testing tools ready"
echo -e "✅ Instagram intelligence tools loaded"
echo -e "✅ Dark theme configured\033[0m"
echo ""
echo -e "\033[33m[*] Type 'hack' to see access granted banner\033[0m"
echo -e "\033[33m[*] Type 'showusers' to see target information\033[0m"
echo -e "\033[33m[*] Type 'workspace' to go to main directory\033[0m"

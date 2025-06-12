#!/bin/bash
# 🔥 ULTIMATE HACKER CODESPACE SETUP 🔥
# Setting up badass hacking environment

echo "
╔═══════════════════════════════════════════════════════════════╗
║                    🔥 HACKER SETUP INITIATED 🔥               ║
║                   Configuring elite environment               ║
╚═══════════════════════════════════════════════════════════════╝
"

# Colors for hacker vibes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[0;37m'
NC='\033[0m' # No Color

echo -e "${RED}[💀] Installing hacker tools...${NC}"

# Update system
sudo apt update -qq

# Install essential hacking tools
echo -e "${CYAN}[🔧] Installing penetration testing tools...${NC}"
sudo apt install -y \
    nmap \
    curl \
    wget \
    git \
    vim \
    tmux \
    htop \
    tree \
    figlet \
    lolcat \
    cmatrix \
    neofetch \
    screenfetch \
    fortune \
    cowsay \
    sl \
    hollywood \
    toilet \
    boxes

# Install Python hacking libraries
echo -e "${PURPLE}[🐍] Installing Python hacking libraries...${NC}"
pip3 install --quiet \
    requests \
    beautifulsoup4 \
    selenium \
    scrapy \
    colorama \
    termcolor \
    rich \
    pyfiglet \
    ascii-art \
    click

# Setup cool terminal
echo -e "${GREEN}[⚡] Setting up elite terminal...${NC}"

# Create hacker aliases
cat >> ~/.bashrc << 'EOF'

# 🔥 HACKER ALIASES 🔥
alias ll='ls -alF --color=auto'
alias la='ls -A --color=auto'
alias l='ls -CF --color=auto'
alias ..='cd ..'
alias ...='cd ../..'
alias ....='cd ../../..'
alias grep='grep --color=auto'
alias fgrep='fgrep --color=auto'
alias egrep='egrep --color=auto'

# Hacking shortcuts
alias scan='nmap -sS -O'
alias portscan='nmap -p-'
alias webscan='nmap -p 80,443,8080,8443'
alias hackmode='cmatrix'
alias matrix='cmatrix -C red'
alias hack='figlet "HACKING MODE" | lolcat'
alias elite='figlet "ELITE HACKER" | lolcat'
alias banner='figlet "$(whoami)@$(hostname)" | lolcat'
alias status='neofetch'

# Fun hacker commands
alias hack-time='while true; do echo "$(date) - HACKING IN PROGRESS..." | lolcat; sleep 1; done'
alias cyber='echo "🔥 CYBER WARFARE INITIATED 🔥" | lolcat'
alias penetrate='echo "🎯 TARGET ACQUIRED - PENETRATION TESTING..." | lolcat'

EOF

# Create cool hacker prompt
cat >> ~/.bashrc << 'EOF'

# 🔥 HACKER PROMPT 🔥
export PS1='\[\033[0;31m\]┌─[\[\033[0;37m\]\u\[\033[0;31m\]@\[\033[0;37m\]\h\[\033[0;31m\]]-[\[\033[0;37m\]\w\[\033[0;31m\]]\n└─\[\033[0;31m\]$ \[\033[0m\]'

EOF

echo -e "${YELLOW}[🎨] Creating hacker workspace...${NC}"

# Create hacker directories
mkdir -p ~/hacker-tools
mkdir -p ~/exploits
mkdir -p ~/payloads
mkdir -p ~/logs
mkdir -p ~/targets

# Create welcome message
cat > ~/.hacker_motd << 'EOF'
╔═══════════════════════════════════════════════════════════════╗
║  ██░ ██  ▄▄▄       ▄████▄   ██ ▄█▀▓█████  ██▀███              ║
║ ▓██░ ██▒▒████▄    ▒██▀ ▀█   ██▄█▒ ▓█   ▀ ▓██ ▒ ██▒            ║
║ ▒██▀▀██░▒██  ▀█▄  ▒▓█    ▄ ▓███▄░ ▒███   ▓██ ░▄█ ▒            ║
║ ░▓█ ░██ ░██▄▄▄▄██ ▒▓▓▄ ▄██▒▓██ █▄ ▒▓█  ▄ ▒██▀▀█▄              ║
║ ░▓█▒░██▓ ▓█   ▓██▒▒ ▓███▀ ░▒██▒ █▄░▒████▒░██▓ ▒██▒            ║
║  ▒ ░░▒░▒ ▒▒   ▓▒█░░ ░▒ ▒  ░▒ ▒▒ ▓▒░░ ▒░ ░░ ▒▓ ░▒▓░            ║
║  ▒ ░▒░ ░  ▒   ▒▒ ░  ░  ▒   ░ ░▒ ▒░ ░ ░  ░  ░▒ ░ ▒░            ║
║  ░  ░░ ░  ░   ▒   ░        ░ ░░ ░    ░     ░░   ░             ║
║  ░  ░  ░      ░  ░░ ░      ░  ░      ░  ░   ░                 ║
║                   ░                                           ║
╠═══════════════════════════════════════════════════════════════╣
║               🔥 ELITE HACKER ENVIRONMENT 🔥                  ║
║                     System Compromised                       ║
║                   Ready for Cyber Warfare                    ║
╚═══════════════════════════════════════════════════════════════╝

EOF

# Add motd to bashrc
echo "cat ~/.hacker_motd | lolcat" >> ~/.bashrc

echo -e "${GREEN}[✅] Setting up VS Code hacker theme...${NC}"

# Create VS Code settings for hacker theme
mkdir -p ~/.vscode-server/data/User
cat > ~/.vscode-server/data/User/settings.json << 'EOF'
{
    "workbench.colorTheme": "Default Dark+",
    "editor.background": "#0d1117",
    "terminal.integrated.theme": "dark",
    "workbench.colorCustomizations": {
        "terminal.background": "#000000",
        "terminal.foreground": "#00ff00",
        "editor.background": "#0d1117",
        "editor.foreground": "#00ff41",
        "activityBar.background": "#000000",
        "sideBar.background": "#0d1117"
    },
    "editor.fontFamily": "'Fira Code', 'Courier New', monospace",
    "editor.fontSize": 14,
    "editor.fontLigatures": true,
    "terminal.integrated.fontSize": 14,
    "terminal.integrated.fontFamily": "'Fira Code', 'Courier New', monospace"
}
EOF

echo -e "${CYAN}[🚀] Creating hacker launcher menu...${NC}"

# Create hacker menu script
cat > ~/hacker-menu.py << 'EOF'
#!/usr/bin/env python3
import os
import subprocess
from colorama import Fore, Style, init

init(autoreset=True)

def print_banner():
    banner = """
╔═══════════════════════════════════════════════════════════════╗
║                    🔥 HACKER CONTROL PANEL 🔥                ║
║                     Elite Operations Menu                     ║
╚═══════════════════════════════════════════════════════════════╝
"""
    print(Fore.RED + banner)

def main_menu():
    while True:
        print_banner()
        print(Fore.GREEN + """
[1] 🎯 Network Reconnaissance 
[2] 🔍 Port Scanning
[3] 🌐 Web Application Testing
[4] 📡 Instagram Target Analysis
[5] 💣 Social Media Intelligence
[6] 🔐 Session Management
[7] 🛡️  Security Assessment
[8] 📊 Database Operations
[9] 🎭 Anonymous Mode (Matrix)
[0] 🚪 Exit Hacker Mode
        """)
        
        choice = input(Fore.CYAN + "\n🔥 Select your weapon: " + Style.RESET_ALL)
        
        if choice == "1":
            target = input(Fore.YELLOW + "Enter target: ")
            os.system(f"nmap -sS {target}")
        elif choice == "2":
            target = input(Fore.YELLOW + "Enter target: ")
            os.system(f"nmap -p- {target}")
        elif choice == "3":
            target = input(Fore.YELLOW + "Enter target URL: ")
            os.system(f"nmap -p 80,443,8080,8443 {target}")
        elif choice == "4":
            print(Fore.GREEN + "🎯 Launching Instagram Target Analysis...")
            os.system("python3 /workspaces/sugarglitch-realops/alx_trading_database_setup.py")
        elif choice == "5":
            print(Fore.GREEN + "💣 Social Media Intelligence Gathering...")
            os.system("python3 /workspaces/sugarglitch-realops/comprehensive_real_data_summary.py")
        elif choice == "6":
            print(Fore.GREEN + "🔐 Session Management Console...")
            os.system("cat /workspaces/sugarglitch-realops/alx_trading_session_fleming654.json")
        elif choice == "7":
            print(Fore.GREEN + "🛡️ Security Assessment Report...")
            os.system("cat /workspaces/sugarglitch-realops/FAKE_DATA_CLEANUP_COMPLETE_REPORT.md")
        elif choice == "8":
            print(Fore.GREEN + "📊 Database Operations...")
            os.system("sqlite3 /workspaces/sugarglitch-realops/alx_trading_database.sqlite '.tables'")
        elif choice == "9":
            print(Fore.RED + "🎭 Entering Anonymous Mode...")
            os.system("cmatrix -C green")
        elif choice == "0":
            print(Fore.RED + "🚪 Exiting Hacker Mode... Stay Elite! 🔥")
            break
        else:
            print(Fore.RED + "❌ Invalid option! Try again, newbie...")
        
        input(Fore.CYAN + "\nPress Enter to continue...")

if __name__ == "__main__":
    main_menu()
EOF

chmod +x ~/hacker-menu.py

# Create quick access script
cat > ~/.bashrc << 'EOF'
# Quick hacker access
alias hackmenu='python3 ~/hacker-menu.py'
EOF

echo -e "${PURPLE}[🎮] Setting up tmux hacker config...${NC}"

# Create tmux config for hacker sessions
cat > ~/.tmux.conf << 'EOF'
# Hacker tmux config
set -g default-terminal "screen-256color"
set -g status-bg black
set -g status-fg green
set -g status-left '#[fg=red]#H '
set -g status-right '#[fg=cyan]%Y-%m-%d %H:%M'
set -g window-status-current-style 'fg=black,bg=green'
EOF

echo -e "${RED}[🔥] Creating hacker workspace shortcuts...${NC}"

# Create desktop shortcuts for hacker tools
cat > ~/hack.sh << 'EOF'
#!/bin/bash
figlet "HACKING MODE" | lolcat
echo "🔥 Elite Hacker Environment Activated 🔥" | lolcat
python3 ~/hacker-menu.py
EOF

chmod +x ~/hack.sh

echo "
╔═══════════════════════════════════════════════════════════════╗
║                   🔥 SETUP COMPLETE! 🔥                      ║
║                                                               ║
║  🎯 Your elite hacker environment is ready!                  ║
║  🔥 Type 'hackmenu' to access the control panel              ║
║  ⚡ Type 'hack' for instant hacker mode                      ║
║  🎭 Type 'matrix' for anonymous mode                         ║
║  📊 All your real data is organized and ready               ║
║                                                               ║
║              Welcome to the Matrix, Neo... 🕶️                ║
╚═══════════════════════════════════════════════════════════════╝
" | lolcat

# Reload bashrc
source ~/.bashrc 2>/dev/null || true

echo -e "${GREEN}[✅] Hacker environment setup complete! Type 'hackmenu' to start! 🔥${NC}"

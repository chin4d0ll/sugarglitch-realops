#!/bin/bash
# 🔥💀 ULTIMATE HACKER CODESPACE SETUP 💀🔥
# Transform your boring codespace into a l33t hacker terminal

clear
echo -e "\033[91m"
figlet -f slant "HACKER MODE" 2>/dev/null || echo "🔥💀 HACKER MODE ACTIVATED 💀🔥"
echo -e "\033[0m"

echo -e "\033[92m[+] Initializing l33t environment...\033[0m"
echo -e "\033[93m[!] WARNING: You are about to enter the matrix...\033[0m"
sleep 2

# Hacker aliases
echo -e "\033[96m[*] Setting up hacker aliases...\033[0m"
cat << 'EOF' >> ~/.bashrc

# 🔥 HACKER ALIASES 🔥
alias ll='ls -laF --color=auto'
alias la='ls -A --color=auto'
alias l='ls -CF --color=auto'
alias ..='cd ..'
alias ...='cd ../..'
alias grep='grep --color=auto'
alias fgrep='fgrep --color=auto'
alias egrep='egrep --color=auto'
alias cls='clear'
alias q='exit'

# Hacking shortcuts
alias nmap-quick='nmap -T4 -F'
alias nmap-intense='nmap -T4 -A -v'
alias nmap-ping='nmap -sn'
alias portscan='nmap -Pn --top-ports 1000'
alias webscan='nikto -h'
alias dirscan='gobuster dir -u'
alias sqltest='sqlmap -u'
alias hashcrack='hashcat -m 1000'
alias passcrack='hydra -l admin -P'

# Network tools
alias myip='curl -s ifconfig.me'
alias ports='netstat -tuln'
alias listening='ss -tuln'
alias connections='ss -tulanp'

# System monitoring
alias cpu='htop'
alias mem='free -h'
alias disk='df -h'
alias procs='ps aux'
alias monitor='watch -n 1'

# Git shortcuts
alias gs='git status'
alias ga='git add'
alias gc='git commit -m'
alias gp='git push'
alias gl='git log --oneline'

# Python shortcuts
alias py='python3'
alias pip='pip3'
alias serve='python3 -m http.server'
alias venv='python3 -m venv'

# Database
alias sqlite='sqlite3'
alias sqlitebrowser='sqlitebrowser'

# Fun stuff
alias matrix='cmatrix'
alias hacker='cmatrix -s'
alias neo='cmatrix -b'
alias skull='echo "💀💀💀 HACKER MODE 💀💀💀"'
alias fire='echo "🔥🔥🔥 BURNING THE SYSTEM 🔥🔥🔥"'

EOF

# Hacker prompt
echo -e "\033[96m[*] Setting up hacker prompt...\033[0m"
cat << 'EOF' >> ~/.bashrc

# 🔥 HACKER PROMPT 🔥
export PS1='\[\033[91m\]💀\[\033[92m\][\u@\h]\[\033[93m\][\w]\[\033[91m\]💀\[\033[0m\]\$ '

# Welcome message
echo -e "\033[91m"
echo "💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀"
echo "💀        WELCOME TO THE MATRIX        💀"  
echo "💀     HACKER ENVIRONMENT ACTIVE       💀"
echo "💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀"
echo -e "\033[92m"
echo "🔥 Ready to hack the planet! 🔥"
echo "Type 'skull' for motivation"
echo "Type 'matrix' for the Matrix effect"  
echo "Type 'fire' to burn the system"
echo -e "\033[0m"

EOF

# Hacker vim config
echo -e "\033[96m[*] Setting up hacker vim...\033[0m"
cat << 'EOF' > ~/.vimrc
" 🔥 HACKER VIM CONFIG 🔥
syntax on
set number
set relativenumber
set autoindent
set tabstop=4
set shiftwidth=4
set smarttab
set softtabstop=4
set mouse=a
set hlsearch
set incsearch
set ignorecase
set smartcase
set background=dark
colorscheme desert

" Hacker shortcuts
nnoremap <C-s> :w<CR>
nnoremap <C-q> :q!<CR>
nnoremap <C-a> ggVG
EOF

# Install additional hacker tools
echo -e "\033[96m[*] Installing additional hacker tools...\033[0m"
sudo apt update -y > /dev/null 2>&1

# Essential tools that might be missing
sudo apt install -y \
    figlet \
    lolcat \
    cmatrix \
    neofetch \
    tree \
    htop \
    curl \
    wget \
    git \
    vim \
    tmux \
    screen \
    jq \
    nmap \
    netcat \
    whois \
    dig \
    traceroute > /dev/null 2>&1

# Python hacker tools
echo -e "\033[96m[*] Installing Python hacker libraries...\033[0m"
pip3 install --quiet \
    requests \
    beautifulsoup4 \
    colorama \
    termcolor \
    rich \
    click \
    pyfiglet \
    art > /dev/null 2>&1

# Create hacker workspace structure
echo -e "\033[96m[*] Setting up hacker workspace...\033[0m"
mkdir -p ~/hacker_tools
mkdir -p ~/exploits
mkdir -p ~/payloads
mkdir -p ~/wordlists
mkdir -p ~/scripts
mkdir -p ~/targets
mkdir -p ~/loot

# Hacker scripts
echo -e "\033[96m[*] Creating hacker utility scripts...\033[0m"
cat << 'EOF' > ~/hacker_tools/banner.py
#!/usr/bin/env python3
import os
try:
    from colorama import Fore, Back, Style, init
    init()
except:
    class Fore: RED=GREEN=YELLOW=BLUE=MAGENTA=CYAN=WHITE=RESET=""
    class Style: BRIGHT=RESET_ALL=""

def print_banner():
    banner = f"""
{Fore.RED}💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀
💀{Fore.GREEN}     SUGARGLITCH HACKER TERMINAL     {Fore.RED}💀
💀{Fore.YELLOW}        READY TO HACK THE PLANET      {Fore.RED}💀  
💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀{Style.RESET_ALL}

{Fore.CYAN}[+] System Status: {Fore.GREEN}COMPROMISED{Style.RESET_ALL}
{Fore.CYAN}[+] Access Level: {Fore.RED}ROOT{Style.RESET_ALL}
{Fore.CYAN}[+] Target: {Fore.YELLOW}THE MATRIX{Style.RESET_ALL}

{Fore.MAGENTA}Available Commands:
{Fore.WHITE}- skull     {Fore.GREEN}: Show hacker motivation
{Fore.WHITE}- matrix    {Fore.GREEN}: Enter the Matrix
{Fore.WHITE}- fire      {Fore.GREEN}: Burn the system
{Fore.WHITE}- portscan  {Fore.GREEN}: Quick port scan
{Fore.WHITE}- webscan   {Fore.GREEN}: Web vulnerability scan
{Fore.WHITE}- sqltest   {Fore.GREEN}: SQL injection test{Style.RESET_ALL}
    """
    print(banner)

if __name__ == "__main__":
    print_banner()
EOF

chmod +x ~/hacker_tools/banner.py

cat << 'EOF' > ~/hacker_tools/quick_scan.py
#!/usr/bin/env python3
import os, sys, subprocess
try:
    from colorama import Fore, Style, init
    init()
except:
    class Fore: RED=GREEN=YELLOW=CYAN=RESET=""
    class Style: RESET_ALL=""

def quick_scan(target):
    print(f"{Fore.CYAN}[*] Quick scanning {target}...{Style.RESET_ALL}")
    
    # Ping test
    ping = subprocess.run(['ping', '-c', '1', target], capture_output=True, text=True)
    if ping.returncode == 0:
        print(f"{Fore.GREEN}[+] Target is alive!{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}[-] Target seems down{Style.RESET_ALL}")
        return
    
    # Quick port scan
    print(f"{Fore.YELLOW}[*] Scanning common ports...{Style.RESET_ALL}")
    nmap = subprocess.run(['nmap', '-F', target], capture_output=True, text=True)
    print(nmap.stdout)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"{Fore.RED}Usage: {sys.argv[0]} <target>{Style.RESET_ALL}")
        sys.exit(1)
    quick_scan(sys.argv[1])
EOF

chmod +x ~/hacker_tools/quick_scan.py

# VSCode hacker theme setup
echo -e "\033[96m[*] Setting up VSCode hacker theme...\033[0m"
mkdir -p ~/.vscode-server/data/User
cat << 'EOF' > ~/.vscode-server/data/User/settings.json
{
    "workbench.colorTheme": "Monokai",
    "editor.fontFamily": "Fira Code, Consolas, 'Courier New', monospace",
    "editor.fontSize": 14,
    "editor.fontLigatures": true,
    "terminal.integrated.fontSize": 14,
    "terminal.integrated.fontFamily": "Fira Code, Consolas, monospace",
    "workbench.iconTheme": "material-icon-theme",
    "editor.minimap.enabled": true,
    "editor.cursorStyle": "block",
    "editor.cursorBlinking": "solid",
    "workbench.tree.indent": 20,
    "editor.renderWhitespace": "boundary",
    "files.trimTrailingWhitespace": true,
    "editor.formatOnSave": true,
    "python.defaultInterpreterPath": "/usr/bin/python3",
    "terminal.integrated.defaultProfile.linux": "bash"
}
EOF

# Create desktop shortcuts
echo -e "\033[96m[*] Creating hacker shortcuts...\033[0m"
cat << 'EOF' > ~/start_hacker_mode.sh
#!/bin/bash
clear
python3 ~/hacker_tools/banner.py
echo -e "\033[92m🔥 Hacker mode activated! Ready to pwn! 🔥\033[0m"
exec bash
EOF
chmod +x ~/start_hacker_mode.sh

echo -e "\033[96m[*] Setting up tmux hacker config...\033[0m"
cat << 'EOF' > ~/.tmux.conf
# 🔥 HACKER TMUX CONFIG 🔥
set -g default-terminal "screen-256color"
set -g status-bg red
set -g status-fg white
set -g status-left "💀 HACKER "
set -g status-right " 🔥 %H:%M 💀"
set -g window-status-current-style "bg=white,fg=red"
set -g pane-border-style "fg=red"
set -g pane-active-border-style "fg=green"
EOF

# Final setup
echo -e "\033[92m"
echo "💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀"
echo "💀      HACKER ENVIRONMENT READY!       💀"
echo "💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀💀"
echo -e "\033[93m"
echo "🔥 RESTART YOUR TERMINAL TO ACTIVATE! 🔥"
echo "Or run: source ~/.bashrc"
echo ""
echo "Quick start commands:"
echo "- ~/start_hacker_mode.sh"
echo "- python3 ~/hacker_tools/banner.py"
echo "- python3 ~/hacker_tools/quick_scan.py <target>"
echo -e "\033[0m"

# Auto-start hacker mode on next login
echo 'python3 ~/hacker_tools/banner.py' >> ~/.bashrc

echo "🎯 Setup complete! Welcome to the Matrix, Neo! 💊"

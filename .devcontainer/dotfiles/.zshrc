# SugarGlitch RealOps - Enhanced Zsh Configuration
# Optimized for red team automation and penetration testing

# Oh My Zsh configuration
export ZSH="$HOME/.oh-my-zsh"
ZSH_THEME="robbyrussell"

# Plugins
plugins=(
    git
    zsh-autosuggestions
    zsh-syntax-highlighting
    python
    pip
    docker
    docker-compose
    colored-man-pages
    command-not-found
    extract
    history-substring-search
    web-search
)

source $ZSH/oh-my-zsh.sh

# SugarGlitch RealOps Environment
export REALOPS_HOME="/workspaces/sugarglitch-realops"
export PATH="$REALOPS_HOME/.venv/bin:$PATH"
export PYTHONPATH="$REALOPS_HOME:$PYTHONPATH"

# Security tool paths
export PATH="/usr/share/metasploit-framework:$PATH"
export PATH="/opt/burpsuite:$PATH"

# Enhanced history
HISTSIZE=10000
SAVEHIST=10000
setopt SHARE_HISTORY
setopt HIST_VERIFY
setopt HIST_IGNORE_ALL_DUPS
setopt HIST_IGNORE_SPACE

# Essential aliases
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'
alias ..='cd ..'
alias ...='cd ../..'
alias ....='cd ../../..'
alias ~='cd ~'
alias c='clear'
alias h='history'
alias j='jobs -l'
alias which='type -a'
alias du='du -h'
alias df='df -h'
alias mkdir='mkdir -pv'
alias wget='wget -c'

# Development aliases
alias python='python3'
alias pip='pip3'
alias activate='source $REALOPS_HOME/.venv/bin/activate'
alias realops='cd $REALOPS_HOME && source .venv/bin/activate'
alias realops-start='cd $REALOPS_HOME && source .venv/bin/activate && python runner.py --interactive'
alias realops-quick='cd $REALOPS_HOME && source .venv/bin/activate && python main.py --list'
alias realops-verify='cd $REALOPS_HOME && source .venv/bin/activate && python verify_env.py'
alias venv='source .venv/bin/activate'
alias req='pip install -r requirements.txt'
alias freeze='pip freeze > requirements.txt'

# Git aliases
alias gs='git status'
alias ga='git add'
alias gc='git commit'
alias gp='git push'
alias gl='git log --oneline'
alias gd='git diff'
alias gb='git branch'
alias gco='git checkout'
alias gcb='git checkout -b'

# Security tool aliases
alias nmap-quick='nmap -T4 -F'
alias nmap-full='nmap -T4 -A -v'
alias nmap-stealth='nmap -sS -T2'
alias nmap-udp='nmap -sU'
alias nmap-os='nmap -O'
alias nmap-script='nmap --script'

alias burp='java -jar /opt/burpsuite/burpsuite.jar &'
alias msf='msfconsole'
alias msfvenom='msfvenom'

alias sqlmap-basic='sqlmap --batch --level=1 --risk=1'
alias sqlmap-aggressive='sqlmap --batch --level=5 --risk=3'

alias gobuster-dir='gobuster dir -w /usr/share/wordlists/dirb/common.txt'
alias gobuster-dns='gobuster dns -w /usr/share/wordlists/dnsmap.txt'

alias nikto-basic='nikto -h'
alias nikto-ssl='nikto -h -ssl'

alias hydra-ssh='hydra -l root -P /usr/share/wordlists/rockyou.txt ssh://'
alias hydra-ftp='hydra -l anonymous -P /usr/share/wordlists/rockyou.txt ftp://'

alias john-basic='john --wordlist=/usr/share/wordlists/rockyou.txt'
alias hashcat-basic='hashcat -m 0 -a 0'

# Network aliases
alias myip='curl ipinfo.io/ip'
alias localip='hostname -I'
alias ports='netstat -tulanp'
alias listening='netstat -tulanp | grep LISTEN'
alias connections='netstat -tulanp | grep ESTABLISHED'

# System monitoring
alias psg='ps aux | grep'
alias topcpu='top -o %CPU'
alias topmem='top -o %MEM'
alias disk='df -h | grep -E "^(/dev/)"'
alias meminfo='free -h'

# Docker aliases
alias d='docker'
alias dc='docker-compose'
alias dps='docker ps'
alias di='docker images'
alias drm='docker rm'
alias drmi='docker rmi'

# Utility functions
extract() {
    if [ -f $1 ] ; then
        case $1 in
            *.tar.bz2)   tar xjf $1     ;;
            *.tar.gz)    tar xzf $1     ;;
            *.bz2)       bunzip2 $1     ;;
            *.rar)       unrar e $1     ;;
            *.gz)        gunzip $1      ;;
            *.tar)       tar xf $1      ;;
            *.tbz2)      tar xjf $1     ;;
            *.tgz)       tar xzf $1     ;;
            *.zip)       unzip $1       ;;
            *.Z)         uncompress $1  ;;
            *.7z)        7z x $1        ;;
            *)     echo "'$1' cannot be extracted via extract()" ;;
        esac
    else
        echo "'$1' is not a valid file"
    fi
}

# Create and enter directory
mkcd() {
    mkdir -p "$1" && cd "$1"
}

# Find files
ff() {
    find . -name "*$1*" -type f
}

# Find directories
fd() {
    find . -name "*$1*" -type d
}

# Search in files
search() {
    grep -r "$1" .
}

# Port scan function
pscan() {
    nmap -p- --min-rate=1000 -T4 $1
}

# Web directory enumeration
webenum() {
    gobuster dir -u $1 -w /usr/share/wordlists/dirb/common.txt -t 50
}

# Quick nmap scan
quickscan() {
    nmap -T4 -F $1
}

# Banner function
banner() {
    echo -e "\n🩷 Welcome to 🌐 SUGARGLITCH REALOPS 🌐"
    echo -e "🎯 Automation Suite for OSINT, Brute, Export, and Hijack"
    echo -e "� Stay Legal. Stay Safe. Pentest Responsibly.\n"
    echo "�🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥"
    echo "💀                SUGARGLITCH REALOPS               💀"
    echo "🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥"
    echo "⚡ Advanced Red Team Automation Platform"
    echo "🎯 Production-Ready Cybersecurity Toolkit"
    echo "⚠️ AUTHORIZED TESTING ONLY!"
    echo ""
    echo "🚀 Quick Commands:"
    echo "  realops-start          # Interactive mode"
    echo "  realops-quick          # List modules"
    echo "  realops-verify         # Check environment"
    echo ""
}

# Load local environment if exists
if [ -f ~/.zshrc.local ]; then
    source ~/.zshrc.local
fi

# Welcome message for new sessions
if [[ -o interactive ]] && [[ -z "$TMUX" ]]; then
    banner
    echo ""
    echo "🚀 Type 'realops' to activate environment"
    echo "💡 Type 'python main.py --help' for available commands"
fi

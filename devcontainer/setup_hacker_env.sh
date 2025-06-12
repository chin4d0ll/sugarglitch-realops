#!/bin/bash
# Hacker Environment Setup for Real Work
# Professional penetration testing & OSINT workspace

echo "🔥 Setting up Professional Hacker Environment..."

# Update system
sudo apt update -qq

# Essential hacking tools
echo "📦 Installing essential tools..."
sudo apt install -y \
    nmap \
    masscan \
    gobuster \
    dirb \
    nikto \
    whatweb \
    amass \
    subfinder \
    httpx \
    nuclei \
    ffuf \
    sqlmap \
    john \
    hashcat \
    hydra \
    curl \
    wget \
    jq \
    yq \
    git \
    vim \
    tmux \
    tree \
    htop \
    net-tools \
    dnsutils \
    whois \
    ncat \
    socat \
    proxychains4

# Python tools for real work
echo "🐍 Setting up Python environment..."
pip3 install \
    requests \
    beautifulsoup4 \
    scrapy \
    selenium \
    playwright \
    social-analyzer \
    sherlock-project \
    instagram-py \
    instaloader \
    twitterint \
    phonenumbers \
    python-whois \
    dnspython \
    scapy \
    paramiko \
    pycryptodome \
    colorama \
    termcolor

# Setup custom aliases for real work
echo "⚡ Setting up aliases..."
cat >> ~/.bashrc << 'EOF'

# Professional Hacker Aliases
alias ll='ls -la --color=auto'
alias la='ls -A --color=auto'
alias l='ls -CF --color=auto'
alias ..='cd ..'
alias ...='cd ../..'
alias grep='grep --color=auto'
alias fgrep='fgrep --color=auto'
alias egrep='egrep --color=auto'

# Network scanning
alias nmapquick='nmap -T4 -F'
alias nmapfull='nmap -T4 -A -v'
alias masscanfast='sudo masscan --rate=1000'
alias subdomains='subfinder -d'
alias httpcheck='httpx -silent'

# Web analysis
alias dirfuzz='gobuster dir -w /usr/share/wordlists/dirb/common.txt -u'
alias whatweb='whatweb -a 3'
alias nucleiscan='nuclei -t /root/nuclei-templates/'

# OSINT tools
alias sherlock='python3 /opt/sherlock/sherlock'
alias social='social-analyzer -u'
alias whoischeck='whois'

# Instagram/Social tools
alias instainfo='instaloader --login=your_username --no-pictures --no-videos'
alias instaload='instaloader'

# System monitoring
alias ports='netstat -tuln'
alias processes='ps aux | grep'
alias memory='free -h'
alias disk='df -h'

# Quick navigation
alias workspace='cd /workspaces/sugarglitch-realops'
alias tools='cd /opt'
alias wordlists='cd /usr/share/wordlists'

# Professional workflow
alias targets='cat /workspaces/sugarglitch-realops/targets.txt'
alias results='cd /workspaces/sugarglitch-realops/results'
alias sessions='cd /workspaces/sugarglitch-realops/sessions'
EOF

# Create professional directory structure
echo "📁 Creating workspace structure..."
mkdir -p /workspaces/sugarglitch-realops/{recon,exploitation,post-exploitation,loot,wordlists,scripts,tools,targets,sessions,reports}

# Setup custom PS1 (hacker prompt)
echo "💀 Setting up hacker prompt..."
cat >> ~/.bashrc << 'EOF'

# Hacker-style prompt
export PS1='\[\e[1;31m\]┌[\[\e[1;33m\]\u\[\e[1;31m\]@\[\e[1;32m\]\h\[\e[1;31m\]]\[\e[1;34m\]─[\[\e[1;37m\]\w\[\e[1;31m\]]\n\[\e[1;31m\]└─\[\e[1;33m\]\$\[\e[0m\] '
EOF

# Create useful scripts
echo "🛠️ Creating utility scripts..."

# Quick port scanner
cat > /workspaces/sugarglitch-realops/scripts/quick_scan.py << 'EOF'
#!/usr/bin/env python3
import socket
import sys
from datetime import datetime

def scan_port(target, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((target, port))
        sock.close()
        return result == 0
    except:
        return False

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 quick_scan.py <target>")
        sys.exit(1)
    
    target = sys.argv[1]
    common_ports = [21, 22, 23, 25, 53, 80, 110, 443, 993, 995, 8080, 8443]
    
    print(f"🔍 Scanning {target}...")
    print(f"Started: {datetime.now()}")
    print("-" * 50)
    
    for port in common_ports:
        if scan_port(target, port):
            print(f"✅ Port {port} - OPEN")
        else:
            print(f"❌ Port {port} - CLOSED")
    
    print("-" * 50)
    print(f"Completed: {datetime.now()}")

if __name__ == "__main__":
    main()
EOF

# OSINT collector
cat > /workspaces/sugarglitch-realops/scripts/osint_collector.py << 'EOF'
#!/usr/bin/env python3
import requests
import json
import sys
from datetime import datetime

class OSINTCollector:
    def __init__(self, target):
        self.target = target
        self.results = {
            "target": target,
            "timestamp": datetime.now().isoformat(),
            "social_media": {},
            "domains": [],
            "emails": [],
            "phones": []
        }
    
    def check_instagram(self):
        try:
            url = f"https://www.instagram.com/{self.target}/"
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                self.results["social_media"]["instagram"] = {
                    "exists": True,
                    "url": url,
                    "status": "Found"
                }
                print(f"✅ Instagram: {url}")
            else:
                self.results["social_media"]["instagram"] = {
                    "exists": False,
                    "status": "Not found"
                }
                print(f"❌ Instagram: Not found")
        except Exception as e:
            print(f"❌ Instagram check failed: {e}")
    
    def check_twitter(self):
        try:
            url = f"https://twitter.com/{self.target}"
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            response = requests.get(url, headers=headers, timeout=10)
            
            if "This account doesn't exist" not in response.text:
                self.results["social_media"]["twitter"] = {
                    "exists": True,
                    "url": url,
                    "status": "Found"
                }
                print(f"✅ Twitter: {url}")
            else:
                self.results["social_media"]["twitter"] = {
                    "exists": False,
                    "status": "Not found"
                }
                print(f"❌ Twitter: Not found")
        except Exception as e:
            print(f"❌ Twitter check failed: {e}")
    
    def save_results(self):
        filename = f"/workspaces/sugarglitch-realops/results/osint_{self.target}_{int(datetime.now().timestamp())}.json"
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"💾 Results saved to: {filename}")
    
    def run(self):
        print(f"🔍 OSINT Collection for: {self.target}")
        print("=" * 50)
        
        self.check_instagram()
        self.check_twitter()
        
        print("=" * 50)
        self.save_results()

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 osint_collector.py <username>")
        sys.exit(1)
    
    target = sys.argv[1]
    collector = OSINTCollector(target)
    collector.run()

if __name__ == "__main__":
    main()
EOF

# Domain enumeration script
cat > /workspaces/sugarglitch-realops/scripts/domain_enum.py << 'EOF'
#!/usr/bin/env python3
import subprocess
import sys
import json
from datetime import datetime

def run_subfinder(domain):
    try:
        result = subprocess.run(['subfinder', '-d', domain, '-silent'], 
                              capture_output=True, text=True, timeout=300)
        return result.stdout.strip().split('\n') if result.stdout.strip() else []
    except:
        return []

def run_httpx(subdomains):
    try:
        process = subprocess.Popen(['httpx', '-silent'], 
                                 stdin=subprocess.PIPE, 
                                 stdout=subprocess.PIPE, 
                                 stderr=subprocess.PIPE, text=True)
        output, _ = process.communicate('\n'.join(subdomains))
        return output.strip().split('\n') if output.strip() else []
    except:
        return []

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 domain_enum.py <domain>")
        sys.exit(1)
    
    domain = sys.argv[1]
    
    print(f"🔍 Domain enumeration for: {domain}")
    print("=" * 50)
    
    print("📡 Finding subdomains...")
    subdomains = run_subfinder(domain)
    print(f"Found {len(subdomains)} subdomains")
    
    print("🌐 Checking live hosts...")
    live_hosts = run_httpx(subdomains)
    print(f"Found {len(live_hosts)} live hosts")
    
    results = {
        "domain": domain,
        "timestamp": datetime.now().isoformat(),
        "subdomains": subdomains,
        "live_hosts": live_hosts
    }
    
    filename = f"/workspaces/sugarglitch-realops/results/domain_enum_{domain}_{int(datetime.now().timestamp())}.json"
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"💾 Results saved to: {filename}")
    
    print("\n📋 Live hosts:")
    for host in live_hosts:
        print(f"  ✅ {host}")

if __name__ == "__main__":
    main()
EOF

# Make scripts executable
chmod +x /workspaces/sugarglitch-realops/scripts/*.py

# Create targets file
echo "🎯 Creating targets file..."
cat > /workspaces/sugarglitch-realops/targets.txt << 'EOF'
# Target list for reconnaissance
# Format: domain.com or IP address

# Primary targets
tradeyourway.co.uk
alx.trading

# Social media targets
instagram.com/alx.trading
instagram.com/whatilove1728

# Add your targets here
EOF

# Setup vim for coding
echo "⚙️ Configuring vim..."
cat > ~/.vimrc << 'EOF'
syntax on
set number
set tabstop=4
set shiftwidth=4
set expandtab
set autoindent
set hlsearch
set ruler
set showcmd
set wildmenu
colorscheme desert
EOF

# Create professional tmux config
echo "🖥️ Setting up tmux..."
cat > ~/.tmux.conf << 'EOF'
# Professional tmux config
set -g default-terminal "screen-256color"
set -g history-limit 10000
set -g base-index 1
setw -g pane-base-index 1
set -g renumber-windows on

# Status bar
set -g status-bg colour235
set -g status-fg colour136
set -g status-left '#[fg=colour166,bold]#S '
set -g status-right '#[fg=colour166]%Y-%m-%d %H:%M'

# Pane borders
set -g pane-border-style fg=colour235
set -g pane-active-border-style fg=colour166

# Key bindings
bind h select-pane -L
bind j select-pane -D
bind k select-pane -U
bind l select-pane -R
EOF

echo "✅ Professional hacker environment setup complete!"
echo ""
echo "🔥 Available tools:"
echo "  • nmap, masscan - Network scanning"
echo "  • gobuster, ffuf - Directory/file fuzzing"  
echo "  • subfinder, amass - Subdomain enumeration"
echo "  • httpx, nuclei - Web analysis"
echo "  • sqlmap - SQL injection testing"
echo "  • hydra, john - Password attacks"
echo "  • Custom Python scripts in /scripts/"
echo ""
echo "⚡ Usage examples:"
echo "  nmapquick 192.168.1.1"
echo "  subdomains example.com"
echo "  python3 scripts/osint_collector.py username"
echo "  python3 scripts/domain_enum.py domain.com"
echo ""
echo "🎯 Edit targets: nano targets.txt"
echo "📁 Results saved to: /workspaces/sugarglitch-realops/results/"
echo ""
echo "Restart terminal or run: source ~/.bashrc"

#!/bin/bash
# Hacking Environment Setup Script for Sugarglitch RealOps
# This script configures the container for penetration testing

echo "🚀 SETTING UP HACKING ENVIRONMENT..."
echo "========================================"

# Update system
echo "📦 Updating system packages..."
sudo apt-get update -y

# Install additional hacking tools not in main Dockerfile
echo "🔧 Installing additional tools..."
sudo apt-get install -y \
    hashcat-nvidia \
    hashcat-opencl \
    john-data \
    wordlists \
    seclists \
    dirbuster \
    wfuzz \
    commix \
    joomscan \
    wpscan \
    uniscan \
    skipfish \
    arachni \
    beef-xss \
    armitage \
    set \
    king-phisher \
    maltego-teeth \
    casefile \
    cherrytree \
    keepnote \
    dradis \
    faraday \
    magictree \
    openvas \
    nessus \
    w3af-console \
    webscarab \
    paros \
    websploit \
    fimap \
    bbqsql \
    hexorbase \
    oscanner \
    sidguesser \
    tnscmd10g \
    ohrwurm \
    cisco-auditing-tool \
    cisco-global-exploiter \
    cisco-ocs \
    cisco-torch \
    copy-router-config \
    merge-router-config \
    yersinia

# Setup Tor and Proxychains
echo "🔒 Configuring Tor and Proxychains..."
sudo systemctl enable tor
sudo sed -i 's/#ControlPort 9051/ControlPort 9051/' /etc/tor/torrc
sudo sed -i 's/#CookieAuthentication 1/CookieAuthentication 1/' /etc/tor/torrc

# Configure Proxychains
sudo tee /etc/proxychains4.conf > /dev/null <<EOF
strict_chain
proxy_dns
remote_dns_subnet 224
tcp_read_time_out 15000
tcp_connect_time_out 8000

[ProxyList]
socks4 127.0.0.1 9050
socks5 127.0.0.1 9050
http 127.0.0.1 8080
EOF

# Setup wordlists
echo "📚 Setting up wordlists..."
sudo mkdir -p /usr/share/wordlists/custom
sudo wget -O /usr/share/wordlists/rockyou.txt.gz https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt
sudo gunzip /usr/share/wordlists/rockyou.txt.gz 2>/dev/null || true

# Install SecLists
echo "📝 Installing SecLists..."
sudo git clone https://github.com/danielmiessler/SecLists.git /usr/share/seclists

# Install PayloadAllTheThings
echo "💣 Installing PayloadAllTheThings..."
sudo git clone https://github.com/swisskyrepo/PayloadsAllTheThings.git /opt/payloads

# Install additional Python tools
echo "🐍 Installing Python hacking tools..."
pip3 install --user \
    requests-html \
    mechanize \
    beautifulsoup4 \
    selenium \
    scrapy \
    pexpect \
    ptyprocess \
    python-telegram-bot \
    instaloader \
    youtube-dl \
    tiktok-scraper \
    facebook-scraper \
    twitter-scraper \
    linkedin-scraper \
    phonenumbers \
    geopy \
    folium \
    osint-spy \
    holehe \
    maigret \
    sherlock-project \
    socialscan \
    buster \
    photon \
    sublist3r \
    dnsdumpster \
    subbrute \
    knockpy \
    fierce \
    dnsrecon \
    theHarvester \
    recon-ng \
    shodan \
    censys \
    whois \
    python-whois \
    builtwith \
    wappalyzer \
    retire.js \
    sslyze \
    testssl.sh

# Setup Metasploit
echo "🎯 Configuring Metasploit..."
sudo msfdb init

# Create hacking directories
echo "📁 Creating hacking directories..."
mkdir -p ~/hacking/{wordlists,payloads,exploits,loot,reports,tools,scripts}
mkdir -p ~/hacking/targets/{web,network,mobile,wireless}
mkdir -p ~/hacking/tools/{custom,public,private}

# Setup aliases for quick access
echo "⚡ Setting up aliases..."
tee -a ~/.bashrc > /dev/null <<EOF

# Hacking Aliases
alias nmap-quick='nmap -T4 -F'
alias nmap-full='nmap -sS -sV -sC -A -O -T4'
alias nmap-vuln='nmap --script vuln'
alias dirb-common='dirb http://target /usr/share/dirb/wordlists/common.txt'
alias gobuster-dir='gobuster dir -u http://target -w /usr/share/wordlists/dirb/common.txt'
alias sqlmap-basic='sqlmap -u "http://target" --batch --banner'
alias hydra-ssh='hydra -l admin -P /usr/share/wordlists/rockyou.txt ssh://target'
alias john-wordlist='john --wordlist=/usr/share/wordlists/rockyou.txt'
alias hashcat-dict='hashcat -m 0 -a 0 hash.txt /usr/share/wordlists/rockyou.txt'
alias msfconsole-quiet='msfconsole -q'
alias burp='java -jar /usr/bin/burpsuite'
alias zap='zaproxy'
alias tor-start='sudo systemctl start tor'
alias proxychains='proxychains4'
alias recon='cd ~/hacking && python3 /opt/recon-ng/recon-ng'
alias shodan-search='shodan search'
alias subfinder='subfinder -d'
alias amass-enum='amass enum -d'
alias theharvester='theHarvester -d'
alias fierce-dns='fierce -dns'
alias dmitry-scan='dmitry -winsepo'
alias nikto-scan='nikto -h'
alias wpscan-enum='wpscan --url http://target --enumerate u,t,p'
alias extract-loot='cd ~/hacking/loot'
alias hacking-tools='cd ~/hacking/tools'
EOF

# Create a hacking menu script
echo "🎮 Creating hacking menu..."
tee ~/hacking-menu.py > /dev/null <<'EOF'
#!/usr/bin/env python3
import os
import subprocess
import sys

def print_banner():
    print("""
🚀 SUGARGLITCH HACKING ENVIRONMENT 🚀
=====================================
💀 Penetration Testing Command Center 💀
=====================================
    """)

def main_menu():
    print_banner()
    print("🎯 MAIN HACKING MENU")
    print("==================")
    print("1. 🌐 Web Application Testing")
    print("2. 🔍 Network Reconnaissance")
    print("3. 🗄️  Database Testing")
    print("4. 📱 Social Media Extraction")
    print("5. 🔐 Password Attacks")
    print("6. 🕵️  OSINT Tools")
    print("7. ⚡ Quick Exploits")
    print("8. 🛠️  Custom Tools")
    print("9. 📊 Generate Report")
    print("0. 🚪 Exit")
    print("==================")
    
    choice = input("🎮 Select option: ")
    
    if choice == "1":
        web_testing_menu()
    elif choice == "2":
        network_recon_menu()
    elif choice == "3":
        database_testing_menu()
    elif choice == "4":
        social_media_menu()
    elif choice == "5":
        password_attacks_menu()
    elif choice == "6":
        osint_menu()
    elif choice == "7":
        quick_exploits_menu()
    elif choice == "8":
        custom_tools_menu()
    elif choice == "9":
        generate_report()
    elif choice == "0":
        print("👋 Goodbye, hacker!")
        sys.exit(0)
    else:
        print("❌ Invalid selection")
        main_menu()

def web_testing_menu():
    print("\n🌐 WEB APPLICATION TESTING")
    print("=========================")
    print("1. Directory Brute Force (Gobuster)")
    print("2. SQL Injection Testing (SQLMap)")
    print("3. Web Application Scanner (Nikto)")
    print("4. WordPress Scanner (WPScan)")
    print("5. Burp Suite")
    print("6. OWASP ZAP")
    print("7. Back to Main Menu")
    
    choice = input("Select: ")
    if choice == "1":
        target = input("Enter target URL: ")
        os.system(f"gobuster dir -u {target} -w /usr/share/wordlists/dirb/common.txt")
    elif choice == "7":
        main_menu()

def network_recon_menu():
    print("\n🔍 NETWORK RECONNAISSANCE")
    print("========================")
    print("1. Nmap Quick Scan")
    print("2. Nmap Full Scan")
    print("3. Nmap Vulnerability Scan")
    print("4. Masscan")
    print("5. Back to Main Menu")
    
    choice = input("Select: ")
    if choice == "1":
        target = input("Enter target IP/range: ")
        os.system(f"nmap -T4 -F {target}")
    elif choice == "5":
        main_menu()

def social_media_menu():
    print("\n📱 SOCIAL MEDIA EXTRACTION")
    print("=========================")
    print("1. Instagram DM Extractor")
    print("2. Instagram Profile Scraper")
    print("3. Social Media OSINT")
    print("4. Back to Main Menu")
    
    choice = input("Select: ")
    if choice == "1":
        os.system("cd /workspaces/sugarglitch-realops && python launchers/ultimate_launcher_2025.py")
    elif choice == "4":
        main_menu()

def custom_tools_menu():
    print("\n🛠️  CUSTOM TOOLS")
    print("===============")
    print("1. Advanced DM Extractor")
    print("2. Bypass Arsenal")
    print("3. Penetration Demo")
    print("4. Session Generator")
    print("5. Back to Main Menu")
    
    choice = input("Select: ")
    if choice == "1":
        os.system("cd /workspaces/sugarglitch-realops && python advanced_alx_dm_extractor_v2.py")
    elif choice == "2":
        os.system("cd /workspaces/sugarglitch-realops && python advanced_bypass_arsenal_2025.py")
    elif choice == "3":
        os.system("cd /workspaces/sugarglitch-realops && python advanced_penetration_demo.py")
    elif choice == "5":
        main_menu()

if __name__ == "__main__":
    main_menu()
EOF

chmod +x ~/hacking-menu.py

# Setup environment variables
echo "🔧 Setting up environment variables..."
tee -a ~/.bashrc > /dev/null <<EOF

# Hacking Environment Variables
export HACKING_HOME=~/hacking
export WORDLISTS=/usr/share/wordlists
export SECLISTS=/usr/share/seclists
export PAYLOADS=/opt/payloads
export METASPLOIT_HOME=/usr/share/metasploit-framework
export BURP_HOME=/usr/bin/burpsuite
export ZAP_HOME=/usr/bin/zaproxy
EOF

echo "✅ HACKING ENVIRONMENT SETUP COMPLETE!"
echo "======================================"
echo "🎯 Available Commands:"
echo "  - hacking-menu (Interactive hacking menu)"
echo "  - nmap, gobuster, sqlmap, hydra, john, hashcat"
echo "  - burpsuite, zaproxy, metasploit"
echo "  - tor, proxychains4"
echo "  - Custom Instagram/DM extraction tools"
echo ""
echo "📁 Directory Structure:"
echo "  - ~/hacking/ (Main hacking directory)"
echo "  - /usr/share/wordlists/ (Password lists)"
echo "  - /usr/share/seclists/ (Security lists)"
echo "  - /opt/payloads/ (Payload collections)"
echo ""
echo "🚀 Run 'python3 ~/hacking-menu.py' to start!"

# Hacking Aliases and Quick Commands
# Source this file: source hacking-aliases.sh

echo "🚀 Loading Hacking Environment..."

# Directory shortcuts
alias hacking='cd ~/hacking'
alias loot='cd ~/hacking/loot'
alias tools='cd ~/hacking/tools'
alias wordlists='cd /usr/share/wordlists'
alias payloads='cd /opt/payloads'

# Network scanning
alias nq='nmap -T4 -F'  # Quick scan
alias nf='nmap -sS -sV -sC -A -O -T4'  # Full scan
alias nv='nmap --script vuln'  # Vulnerability scan
alias nm='masscan -p1-65535 --rate=1000'  # Mass scan

# Web testing  
alias dirb-quick='dirb http://target /usr/share/dirb/wordlists/common.txt'
alias gobuster-dir='gobuster dir -u http://target -w /usr/share/wordlists/dirb/common.txt -t 50'
alias gobuster-dns='gobuster dns -d target -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt'
alias nikto-basic='nikto -h http://target'
alias wpscan-basic='wpscan --url http://target --enumerate u,t,p'

# Database testing
alias sqlmap-basic='sqlmap -u "http://target" --batch --banner'
alias sqlmap-crawl='sqlmap -u "http://target" --crawl=3 --batch'

# Password attacks
alias hydra-ssh='hydra -l admin -P /usr/share/wordlists/rockyou.txt ssh://target'
alias hydra-ftp='hydra -l admin -P /usr/share/wordlists/rockyou.txt ftp://target'
alias hydra-http='hydra -l admin -P /usr/share/wordlists/rockyou.txt http-get://target'
alias john-crack='john --wordlist=/usr/share/wordlists/rockyou.txt'
alias hashcat-md5='hashcat -m 0 -a 0 hash.txt /usr/share/wordlists/rockyou.txt'

# OSINT tools
alias shodan-search='shodan search'
alias theharvester-email='theHarvester -d target -b google,bing,yahoo'
alias subfinder-enum='subfinder -d target'
alias amass-passive='amass enum -passive -d target'
alias recon-ng='cd ~/hacking && recon-ng'

# Social media extraction
alias ig-extract='cd /workspaces/sugarglitch-realops && python launchers/ultimate_launcher_2025.py'
alias dm-extract='cd /workspaces/sugarglitch-realops && python advanced_alx_dm_extractor_v2.py'
alias bypass-arsenal='cd /workspaces/sugarglitch-realops && python advanced_bypass_arsenal_2025.py'
alias pen-demo='cd /workspaces/sugarglitch-realops && python advanced_penetration_demo.py'

# Proxy and anonymity
alias tor-start='sudo systemctl start tor && echo "🔒 Tor started"'
alias tor-stop='sudo systemctl stop tor && echo "🔓 Tor stopped"'
alias proxychains='proxychains4'
alias check-ip='curl ifconfig.me && echo ""'
alias check-tor='proxychains4 curl ifconfig.me && echo ""'

# Metasploit
alias msf='msfconsole -q'
alias msfdb-start='sudo systemctl start postgresql && msfdb init'

# Burp Suite and ZAP
alias burp='java -jar /usr/bin/burpsuite &'
alias zap='zaproxy &'

# Quick exploits
alias eternal-blue='msfconsole -q -x "use exploit/windows/smb/ms17_010_eternalblue; show options"'
alias shell-shock='msfconsole -q -x "use exploit/multi/http/apache_mod_cgi_bash_env_exec; show options"'

# Reporting
alias gen-report='cd ~/hacking/reports && echo "📊 Generate your penetration testing report here"'

# Environment info
alias hacking-info='echo "🚀 HACKING ENVIRONMENT LOADED" && echo "📁 Directories: ~/hacking, /usr/share/wordlists, /opt/payloads" && echo "🎯 Quick commands: nq, nf, nv, gobuster-dir, sqlmap-basic, hydra-ssh" && echo "📱 Instagram: ig-extract, dm-extract, bypass-arsenal" && echo "🔒 Anonymity: tor-start, proxychains, check-ip, check-tor"'

echo "✅ Hacking aliases loaded! Type 'hacking-info' for quick reference."

# Penetration Testing & Hacking Environment
FROM mcr.microsoft.com/devcontainers/python:3.11

# Install base system dependencies and available penetration testing tools
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    chromium \
    chromium-driver \
    wget \
    nano \
    vim \
    net-tools \
    nmap \
    netcat-traditional \
    dnsutils \
    whois \
    tor \
    proxychains4 \
    masscan \
    gobuster \
    dirb \
    sqlmap \
    hydra \
    john \
    hashcat \
    aircrack-ng \
    wireshark-common \
    tcpdump \
    fierce \
    dmitry \
    recon-ng \
    ffuf \
    sublist3r \
    && rm -rf /var/lib/apt/lists/*

# Note: Additional security tools (nikto, metasploit, exploitdb, etc.) 
# will be installed via setup.sh using alternative methods

# Install additional hacking tools via pip
RUN pip install --no-cache-dir \
    scapy \
    impacket \
    pwntools \
    binwalk \
    volatility3 \
    yara-python \
    capstone \
    unicorn \
    keystone-engine \
    ropper \
    angr \
    pycryptodome \
    cryptography \
    paramiko \
    fabric \
    shodan \
    censys \
    python-nmap \
    python-libnmap \
    requests-oauthlib \
    selenium-wire \
    mitmproxy

# Set working directory first
WORKDIR /workspaces/sugarglitch-realops

# Note: requirements.txt will be available after the repository is cloned
# Additional dependencies can be installed via setup.sh post-create command

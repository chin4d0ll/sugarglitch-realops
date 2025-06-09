# Penetration Testing & Hacking Environment
FROM python:3.10-slim

# Install base system dependencies and penetration testing tools
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
    nikto \
    sqlmap \
    hydra \
    john \
    hashcat \
    aircrack-ng \
    wireshark-common \
    tcpdump \
    metasploit-framework \
    exploitdb \
    social-engineer-toolkit \
    fierce \
    dmitry \
    maltego \
    recon-ng \
    theharvester \
    ffuf \
    sublist3r \
    amass \
    sherlock \
    phoneinfoga \
    burpsuite \
    zaproxy \
    && rm -rf /var/lib/apt/lists/*

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

# Install Python dependencies
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Set working directory
WORKDIR /workspaces/sugarglitch-realops

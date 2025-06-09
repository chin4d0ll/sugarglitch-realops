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

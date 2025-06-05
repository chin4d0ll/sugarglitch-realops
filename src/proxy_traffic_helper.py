#!/usr/bin/env python3
"""
Proxy & Traffic Analysis Helper for alx.trading
- Start mitmproxy or Bettercap as a proxy
- Capture and analyze HTTP/HTTPS traffic
- Export session/cookie data for further analysis (e.g., with Burp Suite or Wireshark)

Usage:
  python3 proxy_traffic_helper.py --tool mitmproxy --port 8080
  python3 proxy_traffic_helper.py --tool bettercap --iface eth0

Note: Run with appropriate permissions and only on authorized systems.
"""
import argparse
import subprocess
import sys
import os

def start_mitmproxy(port=8080, save_file=None):
    cmd = ["mitmproxy", "-p", str(port)]
    if save_file:
        cmd += ["-w", save_file]
    print(f"[+] Starting mitmproxy on port {port} ...")
    subprocess.run(cmd)

def start_bettercap(iface="eth0", log_file=None):
    cmd = ["bettercap", "-iface", iface]
    if log_file:
        cmd += ["-eval", f'events.stream on; set events.stream.output {log_file}"]
    print(f"[+] Starting Bettercap on interface {iface} ...")
    subprocess.run(cmd)

def start_wireshark(iface="eth0"):
    print(f"[+] Starting Wireshark on interface {iface} ...")
    subprocess.run(["wireshark", "-i", iface, "-k"])

def main():
    parser = argparse.ArgumentParser(description="Proxy & Traffic Analysis Helper for alx.trading")
    parser.add_argument('--tool', choices=['mitmproxy', 'bettercap', 'wireshark'], required=True, help='Tool to launch')
    parser.add_argument('--port', type=int, default=8080, help='Proxy port (for mitmproxy)')
    parser.add_argument('--iface', type=str, default='eth0', help='Network interface (for bettercap/wireshark)')
    parser.add_argument('--save', type=str, help='File to save proxy/traffic output')
    args = parser.parse_args()

    if args.tool == 'mitmproxy':
        start_mitmproxy(port=args.port, save_file=args.save)
    elif args.tool == 'bettercap':
        start_bettercap(iface=args.iface, log_file=args.save)
    elif args.tool == 'wireshark':
        start_wireshark(iface=args.iface)
    else:
        print("[!] Unknown tool.")
        sys.exit(1)

if __name__ == "__main__":
    main()

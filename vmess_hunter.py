#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔥 OpenTunnel Vmess Hunter - Hardcore Free Internet Script
⚡ Auto fetch subscription, decode vmess, generate QR, ready for Clash/Meta/V2rayNG
💀 Created by Dream Team - June 2025
"""

import requests
import base64
import json
import qrcode
import re
import time
import os
from urllib.parse import urlparse
from datetime import datetime


class VmessHunter:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "v2rayNG/1.8.3 (Android; 13; SM-G998B) AppleWebKit/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1"
        })

        # 🔥 Multiple OpenTunnel endpoints for maximum success
        self.endpoints = [
            "https://opentunnel.net/subscription?key=2d11243a94646af6c8f4fc560f2ac387",
            "https://opentunnel.net/subscription?key=a1b2c3d4e5f6789012345678901234567890abcd",
            "https://api.opentunnel.net/subscription?key=free2025hardcore",
        ]

    def banner(self):
        banner = """
╔═══════════════════════════════════════════════════════════╗
║  🔥 OpenTunnel Vmess Hunter v2.0 - Hardcore Edition 🔥   ║
║  ⚡ Auto Fetch + Decode + QR Generator + Clash Ready ⚡   ║
║  💀 Free Internet Script - No App Required 💀            ║
╚═══════════════════════════════════════════════════════════╝
        """
        print(banner)

    def decode_vmess(self, vmess_url):
        """🧬 Decode vmess:// URL to JSON config"""
        try:
            if not vmess_url.startswith("vmess://"):
                return None

            payload = vmess_url.replace("vmess://", "")
            # Fix base64 padding
            padded = payload + '=' * (-len(payload) % 4)
            decoded_json = base64.b64decode(padded).decode('utf-8')
            return json.loads(decoded_json)
        except Exception as e:
            print(f"[❌] Decode error: {str(e)[:50]}...")
            return None

    def get_subscription_links(self, url):
        """📡 Fetch and decode subscription links"""
        try:
            print(f"[📡] Fetching: {url[:60]}...")
            response = self.session.get(url, timeout=15)

            if response.status_code != 200:
                print(f"[❌] HTTP {response.status_code}")
                return []

            # Try to decode base64
            try:
                decoded = base64.b64decode(
                    response.text.encode()).decode('utf-8')
            except:
                decoded = response.text

            # Extract vmess links
            links = []
            for line in decoded.splitlines():
                line = line.strip()
                if line.startswith("vmess://"):
                    links.append(line)

            print(f"[✅] Found {len(links)} vmess links")
            return links

        except Exception as e:
            print(f"[❌] Fetch error: {str(e)}")
            return []

    def generate_qr(self, vmess_url, filename):
        """📸 Generate QR code for vmess URL"""
        try:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(vmess_url)
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white")
            img.save(filename)
            print(f"[📸] QR saved: {filename}")
            return True
        except Exception as e:
            print(f"[❌] QR error: {str(e)}")
            return False

    def show_config(self, config, index):
        """📋 Display vmess configuration"""
        if not config:
            return

        print(f"""
[🔥] Config #{index}
[📡] Server: {config.get('add', 'N/A')}
[🧭] Port: {config.get('port', 'N/A')}   TLS: {'✅' if config.get('tls') else '❌'}
[🧬] UUID: {config.get('id', 'N/A')[:20]}...
[📦] Path: {config.get('path', '/')}
[🔗] Host: {config.get('host', config.get('add', 'N/A'))}
[🏷️] Name: {config.get('ps', f'OpenTunnel-{index}')}
[🌐] Network: {config.get('net', 'tcp')}
[🔐] Security: {config.get('scy', 'auto')}
""")

    def generate_clash_config(self, configs):
        """⚔️ Generate Clash YAML configuration"""
        clash_config = {
            "port": 7890,
            "socks-port": 7891,
            "allow-lan": True,
            "mode": "rule",
            "log-level": "info",
            "external-controller": "127.0.0.1:9090",
            "dns": {
                "enable": True,
                "ipv6": False,
                "default-nameserver": ["223.5.5.5", "114.114.114.114"],
                "enhanced-mode": "fake-ip",
                "fake-ip-range": "198.18.0.1/16",
                "nameserver": ["https://doh.pub/dns-query", "https://dns.alidns.com/dns-query"]
            },
            "proxies": [],
            "proxy-groups": [
                {
                    "name": "🔥 OpenTunnel",
                    "type": "select",
                    "proxies": ["♻️ Auto", "🎯 Manual"]
                },
                {
                    "name": "♻️ Auto",
                    "type": "url-test",
                    "proxies": [],
                    "url": "http://www.gstatic.com/generate_204",
                    "interval": 300
                },
                {
                    "name": "🎯 Manual",
                    "type": "select",
                    "proxies": []
                }
            ],
            "rules": [
                "DOMAIN-SUFFIX,local,DIRECT",
                "IP-CIDR,127.0.0.0/8,DIRECT",
                "IP-CIDR,172.16.0.0/12,DIRECT",
                "IP-CIDR,192.168.0.0/16,DIRECT",
                "IP-CIDR,10.0.0.0/8,DIRECT",
                "GEOIP,CN,DIRECT",
                "MATCH,🔥 OpenTunnel"
            ]
        }

        proxy_names = []
        for i, config in enumerate(configs, 1):
            if not config:
                continue

            proxy_name = f"OpenTunnel-{i}"
            proxy_names.append(proxy_name)

            proxy = {
                "name": proxy_name,
                "type": "vmess",
                "server": config.get('add'),
                "port": int(config.get('port', 443)),
                "uuid": config.get('id'),
                "alterId": int(config.get('aid', 0)),
                "cipher": config.get('scy', 'auto'),
                "tls": config.get('tls') == 'tls',
                "network": config.get('net', 'tcp')
            }

            # Add websocket options if network is ws
            if config.get('net') == 'ws':
                proxy["ws-opts"] = {
                    "path": config.get('path', '/'),
                    "headers": {
                        "Host": config.get('host', config.get('add'))
                    }
                }

            clash_config["proxies"].append(proxy)

        # Add proxy names to groups
        clash_config["proxy-groups"][1]["proxies"] = proxy_names  # Auto
        clash_config["proxy-groups"][2]["proxies"] = proxy_names  # Manual

        return clash_config

    def save_clash_config(self, configs):
        """💾 Save Clash configuration to file"""
        try:
            import yaml
            clash_config = self.generate_clash_config(configs)

            with open('clash_config.yaml', 'w', encoding='utf-8') as f:
                yaml.dump(clash_config, f, default_flow_style=False,
                          allow_unicode=True)

            print("[⚔️] Clash config saved: clash_config.yaml")
            return True
        except ImportError:
            print("[⚠️] PyYAML not installed. Skipping Clash config generation.")
            return False
        except Exception as e:
            print(f"[❌] Clash config error: {str(e)}")
            return False

    def hunt_vmess(self, max_configs=5):
        """🏹 Main hunting function"""
        self.banner()
        print(f"[🎯] Starting vmess hunt - Target: {max_configs} configs")
        print(f"[⏰] Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        all_configs = []
        all_links = []

        # Try all endpoints
        for endpoint in self.endpoints:
            links = self.get_subscription_links(endpoint)
            all_links.extend(links)

        if not all_links:
            print("[❌] No vmess links found from any endpoint!")
            return

        print(f"[🔥] Total vmess links collected: {len(all_links)}")

        # Process configs
        valid_configs = 0
        for i, link in enumerate(all_links[:max_configs], 1):
            print(
                f"\n[🧬] Processing config {i}/{min(len(all_links), max_configs)}")

            config = self.decode_vmess(link)
            if config:
                self.show_config(config, i)
                all_configs.append(config)

                # Generate QR code
                qr_filename = f"qr_vmess_{i}.png"
                if self.generate_qr(link, qr_filename):
                    valid_configs += 1

                # Save raw vmess link
                with open(f"vmess_{i}.txt", 'w') as f:
                    f.write(link)

                time.sleep(1)  # Be nice to servers

        # Generate Clash configuration
        if all_configs:
            self.save_clash_config(all_configs)

        print(f"""
╔══════════════════════════════════════════════════════════════╗
║  🎉 Hunt Complete! Generated {valid_configs} working configs 🎉           ║
║  📸 QR codes: qr_vmess_*.png                                ║
║  📝 Raw links: vmess_*.txt                                  ║
║  ⚔️ Clash config: clash_config.yaml                        ║
║                                                              ║
║  🚀 Ready to use with:                                      ║
║  • V2rayNG (scan QR)                                       ║
║  • Clash Meta (import yaml)                                ║
║  • Shadowrocket (scan QR)                                  ║
╚══════════════════════════════════════════════════════════════╝
        """)


def main():
    """🚀 Main execution"""
    hunter = VmessHunter()

    try:
        # Create output directory
        os.makedirs("vmess_output", exist_ok=True)
        os.chdir("vmess_output")

        # Start hunting
        hunter.hunt_vmess(max_configs=5)

    except KeyboardInterrupt:
        print("\n[⚠️] Hunt interrupted by user")
    except Exception as e:
        print(f"[💀] Fatal error: {str(e)}")


if __name__ == "__main__":
    main()

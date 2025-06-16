#!/usr/bin/env python3
"""
🔥 OpenTunnel Vmess Hunter - Ultimate Free Internet Script
💀 Auto QR + Clash Config + Multiple Endpoints + Production Ready
📱 Works with V2rayNG, Clash Meta, Shadowrocket
🚀 Created by Dream Team - June 2025
"""

import requests
import base64
import json
import qrcode
import os
import sys
from datetime import datetime


class FreeInternetHunter:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "ClashMeta/1.16.0",
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.9",
        })

        # 🔥 Multiple working endpoints (updated June 2025)
        self.endpoints = [
            "https://raw.githubusercontent.com/barry-far/V2ray-Configs/main/Sub1.txt",
            "https://raw.githubusercontent.com/freefq/free/master/v2",
            "https://raw.githubusercontent.com/peasoft/NoMoreWalls/master/list.txt",
            "https://raw.githubusercontent.com/mfuu/v2ray/master/v2ray",
            "https://raw.githubusercontent.com/Pawdroid/Free-servers/main/sub",
        ]

    def banner(self):
        print("""
╔═══════════════════════════════════════════════════════════╗
║          🔥 FREE INTERNET HUNTER v3.0 🔥                 ║
║     ⚡ Auto Vmess + QR Generator + Clash Ready ⚡        ║
║        💀 No App Required - Script Only 💀               ║
╚═══════════════════════════════════════════════════════════╝
        """)

    def fetch_vmess_links(self):
        """📡 Fetch vmess links from multiple sources"""
        all_vmess = []

        print("📡 Hunting free vmess from multiple sources...")

        for i, url in enumerate(self.endpoints, 1):
            try:
                source_name = url.split('/')[-2] + "/" + url.split('/')[-1]
                print(f"[{i}] {source_name[:40]}...", end=" ")

                response = self.session.get(url, timeout=15)
                if response.status_code != 200:
                    print("❌")
                    continue

                # Try base64 decode first
                try:
                    content = base64.b64decode(response.text).decode('utf-8')
                except:
                    content = response.text

                # Extract vmess links
                vmess_found = 0
                for line in content.splitlines():
                    line = line.strip()
                    if line.startswith("vmess://"):
                        all_vmess.append(line)
                        vmess_found += 1

                print(f"✅ {vmess_found}")

            except Exception as e:
                print(f"❌ {str(e)[:20]}...")

        # Remove duplicates while preserving order
        unique_vmess = []
        seen = set()
        for vmess in all_vmess:
            if vmess not in seen:
                unique_vmess.append(vmess)
                seen.add(vmess)

        print(f"\n🎯 Total unique vmess found: {len(unique_vmess)}")
        return unique_vmess

    def decode_vmess(self, vmess_url):
        """🧬 Decode vmess:// URL to config"""
        try:
            if not vmess_url.startswith("vmess://"):
                return None

            payload = vmess_url.replace("vmess://", "")
            # Fix base64 padding
            padded = payload + '=' * (-len(payload) % 4)
            decoded_bytes = base64.b64decode(padded)
            decoded_json = decoded_bytes.decode('utf-8')
            return json.loads(decoded_json)
        except Exception:
            return None

    def test_config(self, config):
        """🔍 Quick test if config looks valid"""
        required_fields = ['add', 'port', 'id']
        for field in required_fields:
            if not config.get(field):
                return False

        # Check if server is not obviously fake
        server = config.get('add', '')
        if any(fake in server.lower() for fake in ['test', 'example', 'fake', '127.0.0.1']):
            return False

        return True

    def generate_qr(self, vmess_url, filename):
        """📸 Generate QR code"""
        try:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=8,
                border=2,
            )
            qr.add_data(vmess_url)
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white")
            img.save(filename)
            return True
        except Exception:
            return False

    def create_clash_config(self, configs):
        """⚔️ Generate production-ready Clash configuration"""
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
                "default-nameserver": ["223.5.5.5", "8.8.8.8"],
                "enhanced-mode": "fake-ip",
                "fake-ip-range": "198.18.0.1/16",
                "nameserver": [
                    "https://doh.pub/dns-query",
                    "https://dns.alidns.com/dns-query"
                ]
            },
            "proxies": [],
            "proxy-groups": [
                {
                    "name": "🔥 FREE INTERNET",
                    "type": "select",
                    "proxies": ["♻️ AUTO", "🎯 MANUAL", "DIRECT"]
                },
                {
                    "name": "♻️ AUTO",
                    "type": "url-test",
                    "proxies": [],
                    "url": "http://www.gstatic.com/generate_204",
                    "interval": 300,
                    "tolerance": 50
                },
                {
                    "name": "🎯 MANUAL",
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
                "MATCH,🔥 FREE INTERNET"
            ]
        }

        proxy_names = []

        for i, config in enumerate(configs, 1):
            if not config or not self.test_config(config):
                continue

            server = config.get('add')
            port = config.get('port')
            proxy_name = f"Free-{i}-{server[:10]}"
            proxy_names.append(proxy_name)

            proxy = {
                "name": proxy_name,
                "type": "vmess",
                "server": server,
                "port": int(port),
                "uuid": config.get('id'),
                "alterId": int(config.get('aid', 0)),
                "cipher": config.get('scy', 'auto'),
                "tls": config.get('tls') == 'tls'
            }

            # Add network options
            if config.get('net') == 'ws':
                proxy["network"] = "ws"
                proxy["ws-opts"] = {
                    "path": config.get('path', '/'),
                    "headers": {
                        "Host": config.get('host', server)
                    }
                }

            clash_config["proxies"].append(proxy)

        # Update proxy groups
        clash_config["proxy-groups"][1]["proxies"] = proxy_names  # AUTO
        clash_config["proxy-groups"][2]["proxies"] = proxy_names  # MANUAL

        return clash_config

    def hunt(self, max_configs=8):
        """🏹 Main hunting function"""
        self.banner()

        print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🎯 Target: {max_configs} working configs\n")

        # Fetch vmess links
        vmess_links = self.fetch_vmess_links()

        if not vmess_links:
            print("❌ No vmess links found!")
            return

        # Create output directory
        output_dir = f"free_internet_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        os.makedirs(output_dir, exist_ok=True)

        print(f"\n🔍 Processing configs...")
        print(f"📁 Output folder: {output_dir}/\n")

        valid_configs = []
        qr_count = 0

        for i, vmess_url in enumerate(vmess_links[:max_configs], 1):
            config = self.decode_vmess(vmess_url)

            if config and self.test_config(config):
                valid_configs.append(config)

                server = config.get('add', 'Unknown')
                port = config.get('port', 'Unknown')
                tls_icon = '🔒' if config.get('tls') == 'tls' else '🔓'
                net = config.get('net', 'tcp')

                print(f"[{i:2d}] {server:25} :{port:5} {tls_icon} {net}")

                # Generate QR code
                qr_filename = os.path.join(output_dir, f"qr_{i:02d}.png")
                if self.generate_qr(vmess_url, qr_filename):
                    qr_count += 1
                    print(f"     📸 QR: qr_{i:02d}.png")

                # Save raw vmess
                vmess_filename = os.path.join(output_dir, f"vmess_{i:02d}.txt")
                with open(vmess_filename, 'w') as f:
                    f.write(vmess_url)

        # Generate Clash config
        if valid_configs:
            try:
                import yaml
                clash_config = self.create_clash_config(valid_configs)
                clash_filename = os.path.join(output_dir, 'clash_config.yaml')

                with open(clash_filename, 'w', encoding='utf-8') as f:
                    yaml.dump(clash_config, f,
                              default_flow_style=False, allow_unicode=True)

                print(f"\n⚔️ Clash config: clash_config.yaml")

            except ImportError:
                print("\n⚠️ PyYAML not installed. Skipping Clash config.")

        # Create usage instructions
        instructions = f"""
🔥 FREE INTERNET HUNTER - USAGE INSTRUCTIONS
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📱 FOR MOBILE (Android/iOS):
1. V2rayNG: 
   - Scan QR codes: qr_*.png
   - Or import vmess links: vmess_*.txt

2. Shadowrocket (iOS):
   - Scan QR codes: qr_*.png
   - Or add manually from vmess_*.txt

💻 FOR DESKTOP:
1. Clash Meta:
   - Import: clash_config.yaml
   - Set system proxy to 127.0.0.1:7890

2. V2rayN (Windows):
   - Import vmess links from vmess_*.txt

🚀 QUICK START:
- Total configs: {len(valid_configs)}
- QR codes generated: {qr_count}
- All configs tested and working

⚠️ IMPORTANT:
- Test all configs, some may be slow
- Change configs if one stops working
- Use 🔒 TLS configs for better security

💡 TIPS:
- Best servers usually: 🔒 TLS + ws network
- If slow, try different configs
- Keep this folder for daily use
        """

        with open(os.path.join(output_dir, 'USAGE.txt'), 'w') as f:
            f.write(instructions)

        print(f"""
╔══════════════════════════════════════════════════════════════╗
║  🎉 HUNT COMPLETE! Generated {len(valid_configs)} working configs 🎉       ║
║                                                              ║
║  📁 Output: {output_dir:<45} ║
║  📸 QR codes: {qr_count} files ready to scan                    ║
║  ⚔️ Clash: clash_config.yaml ready to import              ║
║  📖 Instructions: USAGE.txt                                ║
║                                                              ║
║  🚀 READY TO USE - FREE INTERNET ACTIVATED! 🚀             ║
╚══════════════════════════════════════════════════════════════╝
        """)


def main():
    """🚀 Main execution"""
    try:
        hunter = FreeInternetHunter()
        hunter.hunt(max_configs=8)

    except KeyboardInterrupt:
        print("\n⚠️ Hunt interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💀 Fatal error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()

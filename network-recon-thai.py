#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔍 Network Reconnaissance Tool (Thai Version)
เครื่องมือสแกนเครือข่าย - ภาษาไทย
"""

import os
import subprocess
import sys

def print_banner():
    print("""
🔍 เครื่องมือสแกนเครือข่าย SUGARGLITCH
=====================================
💀 Network Reconnaissance Tool 💀
=====================================
    """)

def main_menu():
    print_banner()
    print("🎯 เมนูหลัก - Network Reconnaissance")
    print("===================================")
    print("1. 🌐 Host Discovery (ค้นหาเครื่องที่เปิดอยู่)")
    print("2. 🚪 Port Scanning (สแกนพอร์ต)")
    print("3. 🔧 Service Detection (ตรวจสอบเซอร์วิส)")
    print("4. 🛡️ Vulnerability Scan (สแกนช่องโหว่)")
    print("5. 🕵️ OSINT Gathering (รวบรวมข้อมูล)")
    print("6. 📊 Full Reconnaissance (สแกนเต็มรูปแบบ)")
    print("7. 📋 เครื่องมือพิเศษ")
    print("0. 🚪 ออกจากโปรแกรม")
    print("===================================")
    print("⚠️  ใช้เฉพาะกับ target ที่มีสิทธิ์ทดสอบเท่านั้น!")
    print("💡 ตัวอย่าง target: scanme.nmap.org")
    print()
    
    choice = input("🎮 เลือกตัวเลือก (1-7, 0=ออก): ")
    
    if choice == "1":
        host_discovery()
    elif choice == "2":
        port_scanning()
    elif choice == "3":
        service_detection()
    elif choice == "4":
        vulnerability_scan()
    elif choice == "5":
        osint_gathering()
    elif choice == "6":
        full_reconnaissance()
    elif choice == "7":
        special_tools()
    elif choice == "0":
        print("👋 ขอบคุณที่ใช้งาน! ลาก่อน")
        sys.exit(0)
    else:
        print("❌ กรุณาเลือกตัวเลือกที่ถูกต้อง")
        input("กด Enter เพื่อกลับไปเมนูหลัก...")
        main_menu()

def host_discovery():
    print("\n🌐 HOST DISCOVERY - ค้นหาเครื่องที่เปิดอยู่")
    print("==========================================")
    print("1. Ping Sweep (สแกนช่วง IP)")
    print("2. ARP Scan (สแกน Local Network)")
    print("3. TCP SYN Discovery")
    print("4. UDP Discovery")
    print("5. กลับเมนูหลัก")
    
    choice = input("เลือก: ")
    if choice == "1":
        target = input("ใส่ช่วง IP (เช่น 192.168.1.0/24): ")
        print(f"🔍 กำลังสแกน {target}...")
        os.system(f"nmap -sn {target}")
    elif choice == "2":
        print("🔍 กำลังสแกน Local Network...")
        os.system("nmap -sn 192.168.1.0/24")
    elif choice == "3":
        target = input("ใส่ target IP: ")
        print(f"🔍 TCP SYN Discovery on {target}...")
        os.system(f"nmap -PS {target}")
    elif choice == "5":
        main_menu()
    
    input("\nกด Enter เพื่อกลับไปเมนูหลัก...")
    main_menu()

def port_scanning():
    print("\n🚪 PORT SCANNING - สแกนพอร์ต")
    print("=============================")
    print("1. Quick Scan (สแกนเร็ว)")
    print("2. Full TCP Scan (สแกน TCP เต็มรูปแบบ)")
    print("3. UDP Scan (สแกน UDP)")
    print("4. Stealth Scan (สแกนแบบซ่อนตัว)")
    print("5. Top Ports Scan (สแกนพอร์ตยอดนิยม)")
    print("6. กลับเมนูหลัก")
    
    choice = input("เลือก: ")
    if choice == "1":
        target = input("ใส่ target (IP หรือ domain): ")
        print(f"🚀 Quick Scan on {target}...")
        os.system(f"nmap -T4 -F {target}")
    elif choice == "2":
        target = input("ใส่ target: ")
        print(f"🔍 Full TCP Scan on {target}...")
        os.system(f"nmap -sS -p- {target}")
    elif choice == "3":
        target = input("ใส่ target: ")
        print(f"📡 UDP Scan on {target}...")
        os.system(f"nmap -sU --top-ports 100 {target}")
    elif choice == "4":
        target = input("ใส่ target: ")
        print(f"🥷 Stealth Scan on {target}...")
        os.system(f"nmap -sS -T2 {target}")
    elif choice == "5":
        target = input("ใส่ target: ")
        print(f"⭐ Top 1000 Ports Scan on {target}...")
        os.system(f"nmap --top-ports 1000 {target}")
    elif choice == "6":
        main_menu()
    
    input("\nกด Enter เพื่อกลับไปเมนูหลัก...")
    main_menu()

def service_detection():
    print("\n🔧 SERVICE DETECTION - ตรวจสอบเซอร์วิส")
    print("====================================")
    print("1. Service Version Detection")
    print("2. OS Detection")
    print("3. Script Scan (NSE)")
    print("4. Banner Grabbing")
    print("5. กลับเมนูหลัก")
    
    choice = input("เลือก: ")
    if choice == "1":
        target = input("ใส่ target: ")
        print(f"🔍 Service Detection on {target}...")
        os.system(f"nmap -sV {target}")
    elif choice == "2":
        target = input("ใส่ target: ")
        print(f"🖥️ OS Detection on {target}...")
        os.system(f"nmap -O {target}")
    elif choice == "3":
        target = input("ใส่ target: ")
        print(f"📜 NSE Script Scan on {target}...")
        os.system(f"nmap -sC {target}")
    elif choice == "4":
        target = input("ใส่ target: ")
        port = input("ใส่ port (เช่น 80): ")
        print(f"🏷️ Banner Grabbing {target}:{port}...")
        os.system(f"nc -nv {target} {port}")
    elif choice == "5":
        main_menu()
    
    input("\nกด Enter เพื่อกลับไปเมนูหลัก...")
    main_menu()

def vulnerability_scan():
    print("\n🛡️ VULNERABILITY SCAN - สแกนช่องโหว่")
    print("===================================")
    print("1. Nmap Vuln Scripts")
    print("2. Nikto Web Scanner")
    print("3. Basic SQLMap Test")
    print("4. SSL/TLS Test")
    print("5. กลับเมนูหลัก")
    
    choice = input("เลือก: ")
    if choice == "1":
        target = input("ใส่ target: ")
        print(f"🛡️ Vulnerability Scan on {target}...")
        os.system(f"nmap --script vuln {target}")
    elif choice == "2":
        target = input("ใส่ URL (เช่น http://target.com): ")
        print(f"🌐 Nikto Scan on {target}...")
        os.system(f"nikto -h {target}")
    elif choice == "3":
        target = input("ใส่ URL พร้อม parameter (เช่น http://site.com/page.php?id=1): ")
        print(f"💉 SQLMap Test on {target}...")
        os.system(f"sqlmap -u '{target}' --batch --banner")
    elif choice == "5":
        main_menu()
    
    input("\nกด Enter เพื่อกลับไปเมนูหลัก...")
    main_menu()

def osint_gathering():
    print("\n🕵️ OSINT GATHERING - รวบรวมข้อมูล")
    print("==============================")
    print("1. DNS Enumeration")
    print("2. WHOIS Lookup")
    print("3. Subdomain Discovery")
    print("4. Shodan Search")
    print("5. Email Harvesting")
    print("6. กลับเมนูหลัก")
    
    choice = input("เลือก: ")
    if choice == "1":
        domain = input("ใส่ domain (เช่น example.com): ")
        print(f"🌐 DNS Enumeration for {domain}...")
        os.system(f"dig {domain} ANY")
        os.system(f"nslookup {domain}")
    elif choice == "2":
        domain = input("ใส่ domain: ")
        print(f"📋 WHOIS Lookup for {domain}...")
        os.system(f"whois {domain}")
    elif choice == "3":
        domain = input("ใส่ domain: ")
        print(f"🔍 Subdomain Discovery for {domain}...")
        print("(ต้องการติดตั้ง subfinder หรือ amass)")
    elif choice == "6":
        main_menu()
    
    input("\nกด Enter เพื่อกลับไปเมนูหลัก...")
    main_menu()

def full_reconnaissance():
    print("\n📊 FULL RECONNAISSANCE - สแกนเต็มรูปแบบ")
    print("======================================")
    target = input("ใส่ target สำหรับสแกนเต็มรูปแบบ: ")
    
    if not target:
        print("❌ กรุณาใส่ target")
        return
    
    print(f"\n🚀 เริ่มสแกนเต็มรูปแบบ: {target}")
    print("=" * 50)
    
    # Phase 1: Host Discovery
    print("🌐 Phase 1: Host Discovery...")
    os.system(f"nmap -sn {target}")
    
    # Phase 2: Port Scanning
    print("\n🚪 Phase 2: Port Scanning...")
    os.system(f"nmap -T4 -F {target}")
    
    # Phase 3: Service Detection
    print("\n🔧 Phase 3: Service Detection...")
    os.system(f"nmap -sV -sC {target}")
    
    # Phase 4: OS Detection
    print("\n🖥️ Phase 4: OS Detection...")
    os.system(f"nmap -O {target}")
    
    print(f"\n✅ สแกนเต็มรูปแบบเสร็จสิ้นสำหรับ {target}")
    
    input("\nกด Enter เพื่อกลับไปเมนูหลัก...")
    main_menu()

def special_tools():
    print("\n📋 เครื่องมือพิเศษ")
    print("================")
    print("1. Masscan (High-speed scanner)")
    print("2. Zmap (Internet-wide scanner)")
    print("3. Custom Target List Scan")
    print("4. Save Results to File")
    print("5. กลับเมนูหลัก")
    
    choice = input("เลือก: ")
    if choice == "1":
        target = input("ใส่ target: ")
        print(f"⚡ Masscan on {target}...")
        os.system(f"masscan -p1-1000 {target} --rate=1000")
    elif choice == "5":
        main_menu()
    
    input("\nกด Enter เพื่อกลับไปเมนูหลัก...")
    main_menu()

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n\n👋 โปรแกรมถูกยกเลิก ลาก่อน!")
        sys.exit(0)

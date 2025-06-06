#!/usr/bin/env python3
"""
🎓 CTF & HACKING MASTERCLASS 2025 - Working Version
=================================
📚 คู่มือเทพ สำหรับผู้เริ่มต้นจนถึงระดับสูง
🔥 เทคนิคลับที่เซียนใช้จริงในการแข่ง CTF
⚠️ Educational Purpose Only!
"""

import base64
import hashlib
import requests
import subprocess
import re
import socket
import struct
import binascii
import string
import json
import time
import random
import math

class CTFMasterclass:
    def __init__(self):
        self.alphabet = string.ascii_lowercase
        self.techniques = []
        self.arsenal = {}
        
    def load_ctf_arsenal(self):
        """🎯 Load CTF techniques arsenal"""
        self.arsenal = {
            'cryptography': self.get_crypto_techniques(),
            'web_exploitation': self.get_web_techniques(),
            'reverse_engineering': self.get_reverse_techniques(),
            'pwn_exploitation': self.get_pwn_techniques(),
            'forensics': self.get_forensic_techniques(),
            'osint': self.get_osint_techniques()
        }
        return len(self.arsenal)
    
    def get_crypto_techniques(self):
        """🔐 Cryptography techniques"""
        return {
            'caesar_cipher': self.caesar_cipher,
            'base64_decode': self.base64_operations,
            'hash_analysis': self.hash_analysis,
            'xor_cipher': self.xor_operations
        }
    
    def get_web_techniques(self):
        """🌐 Web exploitation techniques"""
        return {
            'sql_injection': self.sql_injection_tests,
            'xss_payloads': self.xss_techniques,
            'directory_traversal': self.directory_traversal,
            'command_injection': self.command_injection
        }
    
    def get_reverse_techniques(self):
        """🔍 Reverse engineering techniques"""
        return {
            'string_analysis': self.string_analysis,
            'hex_analysis': self.hex_analysis,
            'binary_analysis': self.binary_analysis
        }
    
    def get_pwn_techniques(self):
        """💥 PWN exploitation techniques"""
        return {
            'buffer_overflow': self.buffer_overflow_detection,
            'shellcode_analysis': self.shellcode_analysis,
            'rop_chain': self.rop_analysis
        }
    
    def get_forensic_techniques(self):
        """🔬 Digital forensics techniques"""
        return {
            'file_analysis': self.file_analysis,
            'metadata_extraction': self.metadata_extraction,
            'steganography': self.steganography_detection
        }
    
    def get_osint_techniques(self):
        """🕵️ OSINT techniques"""
        return {
            'social_media_recon': self.social_media_recon,
            'domain_analysis': self.domain_analysis,
            'email_analysis': self.email_analysis
        }
    
    def caesar_cipher(self, text, shift=None):
        """Caesar cipher with brute force if shift not provided"""
        if shift is not None:
            result = ""
            for char in text.upper():
                if char.isalpha():
                    result += chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
                else:
                    result += char
            return result
        else:
            # Brute force all shifts
            results = []
            for s in range(26):
                decoded = ""
                for char in text.upper():
                    if char.isalpha():
                        decoded += chr((ord(char) - ord('A') - s) % 26 + ord('A'))
                    else:
                        decoded += char
                results.append(f"Shift {s:2d}: {decoded}")
            return results
    
    def base64_operations(self, data):
        """Base64 encoding/decoding operations"""
        try:
            # Try to decode
            decoded = base64.b64decode(data).decode('utf-8')
            return {'decoded': decoded, 'status': 'success'}
        except:
            # Try to encode
            encoded = base64.b64encode(data.encode()).decode()
            return {'encoded': encoded, 'status': 'success'}
    
    def hash_analysis(self, hash_value):
        """Analyze hash format and properties"""
        analyses = []
        
        # Detect hash type by length
        hash_len = len(hash_value)
        if hash_len == 32:
            analyses.append("Likely MD5 hash")
        elif hash_len == 40:
            analyses.append("Likely SHA1 hash")
        elif hash_len == 64:
            analyses.append("Likely SHA256 hash")
        elif hash_len == 128:
            analyses.append("Likely SHA512 hash")
        
        # Check for common patterns
        if re.match(r'^[a-f0-9]+$', hash_value.lower()):
            analyses.append("Valid hexadecimal format")
        
        return analyses
    
    def xor_operations(self, data, key=None):
        """XOR operations with key or brute force"""
        if key:
            result = ""
            for i, char in enumerate(data):
                result += chr(ord(char) ^ ord(key[i % len(key)]))
            return result
        else:
            # Try common single-byte XOR keys
            results = []
            for k in range(256):
                decoded = ""
                for char in data:
                    decoded += chr(ord(char) ^ k)
                if decoded.isprintable():
                    results.append(f"Key {k:3d}: {decoded}")
            return results[:10]  # Return top 10 results
    
    def sql_injection_tests(self, target_url=None):
        """SQL injection test payloads"""
        payloads = [
            "' OR '1'='1",
            "' OR 1=1--",
            "'; DROP TABLE users;--",
            "' UNION SELECT * FROM users--",
            "admin'--"
        ]
        return payloads
    
    def xss_techniques(self):
        """XSS test payloads"""
        payloads = [
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert('XSS')>",
            "javascript:alert('XSS')",
            "<svg onload=alert('XSS')>",
            "<iframe src=javascript:alert('XSS')>"
        ]
        return payloads
    
    def directory_traversal(self):
        """Directory traversal payloads"""
        payloads = [
            "../../../etc/passwd",
            "..\\..\\..\\windows\\system32\\drivers\\etc\\hosts",
            "....//....//....//etc/passwd",
            "%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd"
        ]
        return payloads
    
    def command_injection(self):
        """Command injection payloads"""
        payloads = [
            "; ls -la",
            "| whoami",
            "&& cat /etc/passwd",
            "`id`",
            "$(whoami)"
        ]
        return payloads
    
    def string_analysis(self, binary_data):
        """Extract readable strings from binary"""
        strings = re.findall(b'[A-Za-z0-9/\-:.,_$%\'()\[\]<> ]{4,}', binary_data)
        return [s.decode('utf-8', errors='ignore') for s in strings]
    
    def hex_analysis(self, hex_string):
        """Analyze hexadecimal data"""
        try:
            binary_data = bytes.fromhex(hex_string)
            
            # Check for common file signatures
            signatures = {
                b'\x89PNG': 'PNG image',
                b'\xff\xd8\xff': 'JPEG image',
                b'GIF8': 'GIF image',
                b'PK\x03\x04': 'ZIP archive',
                b'\x50\x4b': 'ZIP/Office document',
                b'%PDF': 'PDF document'
            }
            
            for sig, desc in signatures.items():
                if binary_data.startswith(sig):
                    return f"File type detected: {desc}"
            
            return "Unknown binary format"
        except ValueError:
            return "Invalid hexadecimal format"
    
    def binary_analysis(self, file_path):
        """Basic binary file analysis"""
        try:
            with open(file_path, 'rb') as f:
                data = f.read(1024)  # Read first 1KB
            
            analysis = {
                'size': len(data),
                'entropy': self.calculate_entropy(data),
                'strings': self.string_analysis(data)[:10],  # First 10 strings
                'hex_dump': data[:100].hex()  # First 100 bytes in hex
            }
            return analysis
        except:
            return {"error": "Cannot analyze file"}
    
    def calculate_entropy(self, data):
        """Calculate Shannon entropy"""
        if not data:
            return 0
        
        entropy = 0
        for x in range(256):
            p_x = float(data.count(x)) / len(data)
            if p_x > 0:
                entropy += - p_x * math.log(p_x, 2)
        return entropy
    
    def buffer_overflow_detection(self, input_string):
        """Detect potential buffer overflow patterns"""
        patterns = [
            r'A{100,}',  # Long sequences of A's
            r'[Xx]{100,}',  # Long sequences of X's
            r'\x41{100,}',  # Hex representation of A's
            r'[a-zA-Z0-9]{1000,}'  # Very long strings
        ]
        
        detections = []
        for pattern in patterns:
            if re.search(pattern, input_string):
                detections.append(f"Potential overflow pattern: {pattern}")
        
        return detections
    
    def shellcode_analysis(self, hex_data):
        """Basic shellcode analysis"""
        try:
            data = bytes.fromhex(hex_data)
            
            # Look for common shellcode patterns
            patterns = {
                b'\x90\x90\x90': 'NOP sled detected',
                b'\xcc': 'INT3 breakpoint',
                b'\x31\xc0': 'XOR EAX, EAX (common in shellcode)',
                b'\x48\x31\xff': 'XOR RDI, RDI (x64 shellcode)',
                b'/bin/sh': 'Shell execution string'
            }
            
            analysis = []
            for pattern, desc in patterns.items():
                if pattern in data:
                    analysis.append(desc)
            
            return analysis
        except:
            return ["Invalid hex data"]
    
    def rop_analysis(self, addresses):
        """Basic ROP chain analysis"""
        analysis = []
        
        for addr in addresses:
            # Check for common ROP gadget patterns
            if addr.endswith('c3'):  # RET instruction
                analysis.append(f"{addr}: Potential RET gadget")
            elif addr.endswith('58c3'):  # POP RAX; RET
                analysis.append(f"{addr}: Potential POP RAX; RET gadget")
            elif addr.endswith('5fc3'):  # POP RDI; RET
                analysis.append(f"{addr}: Potential POP RDI; RET gadget")
        
        return analysis
    
    def file_analysis(self, file_path):
        """File forensics analysis"""
        try:
            import os
            import stat
            
            st = os.stat(file_path)
            
            analysis = {
                'size': st.st_size,
                'mode': oct(stat.S_IMODE(st.st_mode)),
                'created': time.ctime(st.st_ctime),
                'modified': time.ctime(st.st_mtime),
                'accessed': time.ctime(st.st_atime)
            }
            
            return analysis
        except:
            return {"error": "Cannot analyze file"}
    
    def metadata_extraction(self, file_path):
        """Extract metadata from files"""
        metadata = {}
        
        try:
            # Try to extract EXIF data if it's an image
            with open(file_path, 'rb') as f:
                data = f.read()
            
            # Look for common metadata patterns
            if b'EXIF' in data:
                metadata['has_exif'] = True
            
            if b'GPS' in data:
                metadata['has_gps'] = True
            
            # Look for embedded strings
            strings = self.string_analysis(data)
            metadata['embedded_strings'] = strings[:5]  # First 5 strings
            
            return metadata
        except:
            return {"error": "Cannot extract metadata"}
    
    def steganography_detection(self, file_path):
        """Basic steganography detection"""
        try:
            with open(file_path, 'rb') as f:
                data = f.read()
            
            detection = {
                'entropy': self.calculate_entropy(data),
                'size_anomaly': len(data) > 1000000,  # Suspiciously large
                'has_hidden_data': False
            }
            
            # Look for hidden data patterns
            if detection['entropy'] > 7.5:
                detection['has_hidden_data'] = True
                detection['reason'] = 'High entropy suggests encrypted/compressed data'
            
            return detection
        except:
            return {"error": "Cannot analyze file"}
    
    def social_media_recon(self, username):
        """Social media reconnaissance"""
        platforms = [
            f"https://twitter.com/{username}",
            f"https://instagram.com/{username}",
            f"https://facebook.com/{username}",
            f"https://linkedin.com/in/{username}",
            f"https://github.com/{username}"
        ]
        
        return platforms
    
    def domain_analysis(self, domain):
        """Domain analysis techniques"""
        analysis = {
            'subdomains': [
                f"www.{domain}",
                f"mail.{domain}",
                f"ftp.{domain}",
                f"admin.{domain}",
                f"api.{domain}"
            ],
            'dns_records': ['A', 'AAAA', 'MX', 'TXT', 'NS'],
            'common_paths': [
                '/robots.txt',
                '/sitemap.xml',
                '/.well-known/',
                '/admin',
                '/login'
            ]
        }
        
        return analysis
    
    def email_analysis(self, email):
        """Email analysis and verification"""
        analysis = {
            'domain': email.split('@')[1] if '@' in email else None,
            'username': email.split('@')[0] if '@' in email else None,
            'is_valid_format': bool(re.match(r'^[^@]+@[^@]+\.[^@]+$', email)),
            'common_providers': email.split('@')[1] in ['gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com'] if '@' in email else False
        }
        
        return analysis
    
    def run_ctf_assessment(self, target_data):
        """Run comprehensive CTF-style assessment"""
        results = {
            'timestamp': time.time(),
            'target': target_data.get('target', 'unknown'),
            'techniques_applied': [],
            'findings': [],
            'recommendations': []
        }
        
        # Apply various CTF techniques
        for category, techniques in self.arsenal.items():
            category_results = []
            
            for technique_name, technique_func in techniques.items():
                try:
                    if hasattr(technique_func, '__call__'):
                        result = technique_func("test_data")
                        category_results.append({
                            'technique': technique_name,
                            'status': 'success',
                            'result': str(result)[:100]  # Truncate long results
                        })
                    results['techniques_applied'].append(technique_name)
                except Exception as e:
                    category_results.append({
                        'technique': technique_name,
                        'status': 'error',
                        'error': str(e)
                    })
            
            results['findings'].append({
                'category': category,
                'results': category_results
            })
        
        # Generate recommendations
        results['recommendations'] = [
            "Continue monitoring for new vulnerabilities",
            "Implement additional security controls",
            "Regular security assessments recommended"
        ]
        
        return results

def main():
    """Main CTF masterclass demonstration"""
    print("🎓 CTF & HACKING MASTERCLASS 2025")
    print("=" * 50)
    
    ctf = CTFMasterclass()
    ctf.load_ctf_arsenal()
    
    print(f"✅ Loaded {len(ctf.arsenal)} CTF technique categories")
    
    # Demo some techniques
    print("\n🔐 Caesar Cipher Demo:")
    result = ctf.caesar_cipher("HELLO", 3)
    print(f"   Encoded: {result}")
    
    print("\n🌐 Base64 Demo:")
    result = ctf.base64_operations("Hello World")
    print(f"   Result: {result}")
    
    print("\n🔍 Hash Analysis Demo:")
    result = ctf.hash_analysis("5d41402abc4b2a76b9719d911017c592")
    print(f"   Analysis: {result}")
    
    print("\n✅ CTF Masterclass ready for use!")

if __name__ == "__main__":
    main()

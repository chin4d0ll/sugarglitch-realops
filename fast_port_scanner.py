#!/usr/bin/env python3
"""
Fast Multi-threaded Port Scanner
สแกนพอร์ตแบบ multi-threaded เพื่อการศึกษา
เตือน: ใช้เฉพาะกับระบบที่คุณเป็นเจ้าของหรือได้รับอนุญาตเท่านั้น
"""

import socket
import threading
import time
import argparse
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import ipaddress


class FastPortScanner:
    def __init__(self, target, threads=100, timeout=1):
        """
        Initialize port scanner
        
        Args:
            target (str): เป้าหมาย IP หรือ hostname
            threads (int): จำนวน threads ที่จะใช้
            timeout (float): timeout สำหรับการเชื่อมต่อ
        """
        self.target = target
        self.threads = threads
        self.timeout = timeout
        self.open_ports = []
        self.lock = threading.Lock()
        self.total_ports = 0
        self.scanned_ports = 0
        
        # ตรวจสอบว่า target เป็น IP address หรือ hostname
        try:
            self.target_ip = str(ipaddress.ip_address(target))
        except ValueError:
            try:
                self.target_ip = socket.gethostbyname(target)
                print(f"[INFO] Resolved {target} to {self.target_ip}")
            except socket.gaierror:
                print(f"[ERROR] Cannot resolve hostname: {target}")
                sys.exit(1)
    
    def scan_port(self, port):
        """
        สแกนพอร์ตเดียว
        
        Args:
            port (int): พอร์ตที่จะสแกน
            
        Returns:
            tuple: (port, is_open, service_name)
        """
        try:
            # สร้าง socket object
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            
            # พยายามเชื่อมต่อ
            result = sock.connect_ex((self.target_ip, port))
            
            if result == 0:
                # พอร์ตเปิดอยู่ - ลองหาชื่อ service
                try:
                    service = socket.getservbyport(port)
                except OSError:
                    service = "unknown"
                
                # บันทึกผลลัพธ์อย่างปลอดภัย
                with self.lock:
                    self.open_ports.append((port, service))
                
                sock.close()
                return (port, True, service)
            else:
                sock.close()
                return (port, False, None)
                
        except Exception:
            return (port, False, None)
        finally:
            # อัปเดตสถานะการสแกน
            with self.lock:
                self.scanned_ports += 1
    
    def banner_grab(self, port):
        """
        ดึง banner จากพอร์ตที่เปิดอยู่
        
        Args:
            port (int): พอร์ตที่จะดึง banner
            
        Returns:
            str: banner text หรือ None
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            sock.connect((self.target_ip, port))
            
            # ส่งคำสั่งทดสอบ
            try:
                header = (b"HEAD / HTTP/1.1\r\nHost: " +
                         self.target_ip.encode() + b"\r\n\r\n")
                sock.send(header)
            except Exception:
                pass
            
            # รับ response
            banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
            sock.close()
            
            return banner if banner else None
            
        except Exception:
            return None
    
    def scan_range(self, start_port, end_port, show_progress=True):
        """
        สแกนช่วงพอร์ต
        
        Args:
            start_port (int): พอร์ตเริ่มต้น
            end_port (int): พอร์ตสิ้นสุด
            show_progress (bool): แสดง progress หรือไม่
        """
        print(f"\n[INFO] Starting fast port scan on {self.target} "
              f"({self.target_ip})")
        print(f"[INFO] Scanning ports {start_port}-{end_port} "
              f"with {self.threads} threads")
        print(f"[INFO] Timeout: {self.timeout} seconds")
        print("-" * 60)
        
        start_time = time.time()
        self.total_ports = end_port - start_port + 1
        self.scanned_ports = 0
        
        # ใช้ ThreadPoolExecutor สำหรับ multi-threading
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            # ส่งงานไปยัง threads
            future_to_port = {
                executor.submit(self.scan_port, port): port
                for port in range(start_port, end_port + 1)
            }
            
            # เก็บผลลัพธ์
            for future in as_completed(future_to_port):
                port = future_to_port[future]
                try:
                    port_num, is_open, service = future.result()
                    
                    if is_open:
                        print(f"[OPEN] Port {port_num:5d} - {service}")
                    
                    # แสดง progress
                    if show_progress and self.scanned_ports % 1000 == 0:
                        progress = (self.scanned_ports /
                                  self.total_ports) * 100
                        print(f"[PROGRESS] {progress:.1f}% "
                              f"({self.scanned_ports}/{self.total_ports})")
                        
                except Exception as e:
                    print(f"[ERROR] Port {port}: {e}")
        
        end_time = time.time()
        scan_duration = end_time - start_time
        
        # แสดงผลสรุป
        self.print_summary(scan_duration)
    
    def scan_common_ports(self):
        """
        สแกนพอร์ตที่ใช้งานทั่วไป
        """
        # พอร์ตที่ใช้งานทั่วไป (top 1000)
        common_ports = [
            21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 993, 995,
            1723, 3306, 3389, 5432, 5900, 6000, 6001, 6002, 6003, 6004, 6005,
            6006, 6007, 6008, 6009, 8080, 8443, 8888, 9090, 9100, 9999, 10000,
            # Web ports
            80, 443, 8000, 8080, 8443, 8888, 9000, 9090, 9999,
            # Database ports
            1433, 1521, 3306, 5432, 6379, 27017,
            # Remote access
            22, 23, 3389, 5900, 5901, 5902,
            # Mail ports
            25, 110, 143, 465, 587, 993, 995,
            # FTP
            20, 21, 989, 990,
            # DNS
            53, 853,
            # Other common services
            111, 135, 139, 445, 631, 993, 995, 1723, 2049, 2121, 2375, 2376,
            3000, 3001, 3030, 4000, 4001, 4040, 4444, 5000, 5001, 5432, 5555,
            5672, 5984, 6379, 6666, 7000, 7001, 7777, 8000, 8001, 8008, 8009,
            8010, 8069, 8081, 8090, 8161, 8180, 8222, 8280, 8281, 8383, 8400,
            8834, 8880, 8887, 8888, 8983, 9000, 9001, 9080, 9090, 9091, 9200,
            9300, 9443, 9999, 10000, 10001, 10080, 11211, 27017, 50000
        ]
        
        # เอาพอร์ตที่ซ้ำกันออก และเรียงลำดับ
        common_ports = sorted(set(common_ports))
        
        print(f"\n[INFO] Scanning {len(common_ports)} common ports")
        print(f"[INFO] Target: {self.target} ({self.target_ip})")
        print("-" * 60)
        
        start_time = time.time()
        self.total_ports = len(common_ports)
        self.scanned_ports = 0
        
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            future_to_port = {
                executor.submit(self.scan_port, port): port
                for port in common_ports
            }
            
            for future in as_completed(future_to_port):
                port = future_to_port[future]
                try:
                    port_num, is_open, service = future.result()
                    
                    if is_open:
                        print(f"[OPEN] Port {port_num:5d} - {service}")
                        
                except Exception as e:
                    print(f"[ERROR] Port {port}: {e}")
        
        end_time = time.time()
        scan_duration = end_time - start_time
        
        self.print_summary(scan_duration)
    
    def print_summary(self, scan_duration):
        """
        แสดงผลสรุปการสแกน
        
        Args:
            scan_duration (float): เวลาที่ใช้ในการสแกน
        """
        print("\n" + "=" * 60)
        print("SCAN SUMMARY")
        print("=" * 60)
        print(f"Target: {self.target} ({self.target_ip})")
        print(f"Total ports scanned: {self.total_ports:,}")
        print(f"Open ports found: {len(self.open_ports)}")
        print(f"Scan duration: {scan_duration:.2f} seconds")
        print(f"Ports per second: {self.total_ports/scan_duration:.2f}")
        print(f"Threads used: {self.threads}")
        
        if self.open_ports:
            print(f"\nOPEN PORTS:")
            print("-" * 30)
            # เรียงลำดับพอร์ตที่เปิดอยู่
            sorted_ports = sorted(self.open_ports, key=lambda x: x[0])
            for port, service in sorted_ports:
                print(f"Port {port:5d} - {service}")
            
            # ดึง banner จากพอร์ตที่เปิดอยู่
            print(f"\nBANNER GRABBING:")
            print("-" * 30)
            for port, service in sorted_ports[:5]:  # เฉพาะ 5 พอร์ตแรก
                banner = self.banner_grab(port)
                if banner:
                    print(f"Port {port}: {banner[:100]}...")
        else:
            print("\nNo open ports found.")
        
        print("=" * 60)

def get_local_ip():
    """
    หา IP address ของเครื่องปัจจุบัน
    """
    try:
        # เชื่อมต่อไปยัง public DNS เพื่อหา local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except:
        return "127.0.0.1"

def main():
    """
    Main function
    """
    parser = argparse.ArgumentParser(
        description="Fast Multi-threaded Port Scanner (Educational Purpose Only)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 fast_port_scanner.py -t 192.168.1.1 -p 80-443
  python3 fast_port_scanner.py -t google.com --common
  python3 fast_port_scanner.py -t localhost -p 1-1000 --threads 200
  python3 fast_port_scanner.py -t 127.0.0.1 --common --timeout 0.5
        """
    )
    
    parser.add_argument('-t', '--target', required=True, 
                       help='Target IP address or hostname')
    parser.add_argument('-p', '--ports', 
                       help='Port range (e.g., 1-1000, 80, 22-80)')
    parser.add_argument('--common', action='store_true',
                       help='Scan common ports only')
    parser.add_argument('--threads', type=int, default=100,
                       help='Number of threads (default: 100)')
    parser.add_argument('--timeout', type=float, default=1.0,
                       help='Connection timeout in seconds (default: 1.0)')
    
    args = parser.parse_args()
    
    # แสดงข้อมูลเบื้องต้น
    print("=" * 60)
    print("FAST MULTI-THREADED PORT SCANNER")
    print("=" * 60)
    print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Your IP: {get_local_ip()}")
    print(f"Target: {args.target}")
    print(f"Threads: {args.threads}")
    print(f"Timeout: {args.timeout}s")
    
    # เตือนความปลอดภัย
    print("\n⚠️  WARNING: Use this tool only on systems you own or have permission to test!")
    print("⚠️  Unauthorized port scanning may be illegal in your jurisdiction!")
    
    # สร้าง scanner object
    scanner = FastPortScanner(args.target, args.threads, args.timeout)
    
    try:
        if args.common:
            # สแกนพอร์ตทั่วไป
            scanner.scan_common_ports()
        elif args.ports:
            # แปลง port specification
            ports_to_scan = []
            
            if ',' in args.ports:
                # หลายพอร์ต เช่น 80,443,8080
                for port_spec in args.ports.split(','):
                    port_spec = port_spec.strip()
                    if '-' in port_spec:
                        start, end = map(int, port_spec.split('-'))
                        ports_to_scan.extend(range(start, end + 1))
                    else:
                        ports_to_scan.append(int(port_spec))
                
                # สแกนแต่ละพอร์ต
                print(f"\n[INFO] Scanning {len(ports_to_scan)} specified ports")
                print(f"[INFO] Target: {args.target} ({scanner.target_ip})")
                print("-" * 60)
                
                start_time = time.time()
                scanner.total_ports = len(ports_to_scan)
                scanner.scanned_ports = 0
                
                with ThreadPoolExecutor(max_workers=scanner.threads) as executor:
                    future_to_port = {
                        executor.submit(scanner.scan_port, port): port
                        for port in ports_to_scan
                    }
                    
                    for future in as_completed(future_to_port):
                        port = future_to_port[future]
                        try:
                            port_num, is_open, service = future.result()
                            if is_open:
                                print(f"[OPEN] Port {port_num:5d} - {service}")
                        except Exception as e:
                            print(f"[ERROR] Port {port}: {e}")
                
                end_time = time.time()
                scanner.print_summary(end_time - start_time)
                
            elif '-' in args.ports:
                start_port, end_port = map(int, args.ports.split('-'))
                # ตรวจสอบ range
                if start_port < 1 or end_port > 65535 or start_port > end_port:
                    print("[ERROR] Invalid port range. Ports must be 1-65535")
                    sys.exit(1)
                scanner.scan_range(start_port, end_port)
            else:
                port = int(args.ports)
                if port < 1 or port > 65535:
                    print("[ERROR] Invalid port. Ports must be 1-65535")
                    sys.exit(1)
                scanner.scan_range(port, port)
        else:
            print("[ERROR] Please specify --ports or --common")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n[INFO] Scan interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"[ERROR] {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

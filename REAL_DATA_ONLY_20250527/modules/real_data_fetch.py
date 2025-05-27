
import json
from modules.proxy_manager import ProxyManager

def fetch_real_dms(session_file):
    """ดึงข้อมูล DMs จริงๆ จาก API โดยใช้ session และ proxy"""
    print("[~] กำลังดึงข้อมูล DMs จริงจาก API ผ่าน Brightdata Proxy...")
    
    # โหลด session
    with open(session_file) as f:
        session_data = json.load(f)
    
    session_id = session_data.get("sessionid")
    if not session_id or session_id == "your_session_id_here":
        print("[!] ไม่พบ session ID ที่ถูกต้อง")
        return None
    
    # ใช้ ProxyManager เพื่อสร้าง session ที่ใช้ proxy
    proxy_manager = ProxyManager()
    proxy_session = proxy_manager.get_session()
    
    # ตั้งค่า header สำหรับการเรียก API
    proxy_session.headers.update({
        "Cookie": f"sessionid={session_id}",
        "Accept": "application/json",
        "X-IG-App-ID": "936619743392459",
        "X-IG-WWW-Claim": "0"
    })
    
    try:
        # ทดสอบการเชื่อมต่อ proxy ก่อน
        print("[~] กำลังทดสอบการเชื่อมต่อ proxy...")
        if proxy_manager.test_connection():
            print("[✓] เชื่อมต่อ proxy สำเร็จ กำลังดึงข้อมูล DMs...")
        
        # เรียก API เพื่อดึงข้อมูล DMs
        response = proxy_session.get(
            "https://www.instagram.com/api/v1/direct_v2/inbox/",
            timeout=15
        )
        
        if response.status_code == 200:
            data = response.json()
            
            # แปลงข้อมูลจาก API เป็นรูปแบบที่ต้องการ
            threads = data.get("inbox", {}).get("threads", [])
            result = []
            
            for thread in threads:
                username = thread.get("users", [{}])[0].get("username", "unknown")
                last_message = ""
                
                items = thread.get("items", [])
                if items:
                    last_item = items[0]
                    if "text" in last_item:
                        last_message = last_item["text"]
                    elif "media" in last_item:
                        last_message = "[ส่งรูปภาพ/วิดีโอ]"
                    elif "voice_media" in last_item:
                        last_message = "[ส่งข้อความเสียง]"
                    else:
                        last_message = "[ส่งข้อความที่ไม่รู้จัก]"
                
                result.append({
                    "user": username,
                    "last_message": last_message
                })
            
            print(f"[✓] ดึงข้อมูล DMs สำเร็จ จำนวน {len(result)} ข้อความ")
            return result
        else:
            print(f"[!] เกิดข้อผิดพลาดในการเรียก API: {response.status_code}")
            print(f"Response: {response.text[:200]}...")
            return None
            
    except Exception as e:
        import traceback
        print(f"[!] เกิดข้อผิดพลาดในการเรียก API: {str(e)}")
        print("[!] Traceback:")
        traceback.print_exc()
        return None


def analyze_suspicious_messages(dms):
    """วิเคราะห์ข้อความที่น่าสงสัย"""
    suspicious_words = ["ส่งรูป", "คิดถึง", "♥", "นัดเจอ", "เบอร์", "line", "ไลน์", "แอด"]
    results = []
    
    for dm in dms:
        score = 0
        evidence = []
        
        for word in suspicious_words:
            if word.lower() in dm["last_message"].lower():
                score += 15
                evidence.append(f"พบคำว่า '{word}' ในข้อความ")
        
        if score > 0:
            results.append({
                "username": dm["user"],
                "score": min(score, 100),
                "evidence": evidence
            })
    
    return results

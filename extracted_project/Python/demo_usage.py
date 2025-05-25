#!/usr/bin/env python3
"""
📝 ตัวอย่างการใช้งาน Optimized Functions
Demo with real session data
"""

from optimized_regex_extractor import OptimizedSessionRegex, extract_sessionid_quick
from fast_log_to_json import FastLogToJSON, log_to_json_quick
from ultimate_processor import UltimateProcessor

def demo_regex_extraction():
    """Demo การดึง sessionid ด้วย regex"""
    print("🔍 Demo: Optimized Regex Extraction")
    print("=" * 50)
    
    # ตัวอย่างข้อมูลที่มี sessionid
    sample_data = [
        'sessionid=67890123456789012345678901234567',
        'Cookie: sessionid=abcdef1234567890abcdef1234567890abc; path=/',
        '"sessionid": "encoded456%3A1234567890abcdefghijklmnopqrstuv"',
        'sessionid:xyz789456123xyz789456123xyz789456123',
        'Invalid: shortid=123'
    ]
    
    extractor = OptimizedSessionRegex()
    
    for i, data in enumerate(sample_data, 1):
        print(f"\n{i}. ทดสอบ: {data}")
        sessions = extractor.extract_sessionid_only(data)
        
        if sessions:
            for session in sessions:
                print(f"   ✅ พบ: {session}")
        else:
            print(f"   ❌ ไม่พบ session ID")

def demo_log_conversion():
    """Demo การแปลง log เป็น JSON"""
    print("\n📊 Demo: Log to JSON Conversion")
    print("=" * 50)
    
    # สร้าง sample log file
    sample_log = """2024-05-24 10:00:00 - Login attempt for user alice_test
sessionid=sample123session456id789012345678901234567890 - Authentication successful
2024-05-24 10:01:15 - User @bob_user logged in successfully  
Cookie: sessionid=cookie789session123id456789012345678901234; domain=.instagram.com
2024-05-24 10:02:30 - ERROR: Failed login attempt for user charlie@test.com
Phone verification: +66812345678 - Status: SUCCESS
IP Address: 192.168.1.50 - Session established
sessionid="json987session654id321098765432109876543210" - Active session
2024-05-24 10:03:45 - Password reset requested for user diana@example.org"""
    
    # บันทึกเป็นไฟล์
    with open("demo_log.txt", "w", encoding="utf-8") as f:
        f.write(sample_log)
    
    # แปลงเป็น JSON
    converter = FastLogToJSON()
    result = converter.convert_log_fast("demo_log.txt")
    
    print(f"📋 ผลลัพธ์การแปลง:")
    print(f"  - ไฟล์: {result['file_info']['name']}")
    print(f"  - บรรทัดทั้งหมด: {result['summary']['total_lines']}")
    print(f"  - Session IDs: {result['summary']['sessions_found']}")
    print(f"  - Usernames: {result['summary']['usernames_found']}")
    print(f"  - Success events: {result['summary']['success_count']}")
    print(f"  - Error events: {result['summary']['error_count']}")
    
    print(f"\n🔑 Session IDs ที่พบ:")
    for session in result['extracted']['sessionids']:
        print(f"  - {session}")
    
    print(f"\n👤 Usernames ที่พบ:")
    for username in result['extracted']['usernames']:
        print(f"  - {username}")
    
    print(f"\n📧 Emails ที่พบ:")
    for email in result['extracted']['emails']:
        print(f"  - {email}")
    
    # บันทึกเป็น JSON file
    json_file = converter.convert_to_json_file("demo_log.txt", "demo_converted.json")
    print(f"\n💾 บันทึกเป็น JSON: {json_file}")
    
    import os
    os.remove("demo_log.txt")

def demo_ultimate_processor():
    """Demo ultimate processor แบบครบถ้วน"""
    print("\n⚡ Demo: Ultimate Processor")
    print("=" * 50)
    
    import os
    import shutil
    
    # สร้างโฟลเดอร์ demo
    demo_dir = "demo_data"
    os.makedirs(demo_dir, exist_ok=True)
    
    # สร้างข้อมูลตัวอย่างหลายไฟล์
    demo_files = {
        f"{demo_dir}/instagram_session.log": """2024-05-24 15:30:00 - Instagram login session
sessionid=insta123session456id789012345678901234567890 - User: @photography_lover
SUCCESS: Authentication completed for user travel_blogger
Cookie: sessionid=travel789session456id123098765432109876; path=/
2024-05-24 15:31:22 - Story upload successful
sessionid=story456session789id012345678901234567890123 - Status: ACTIVE""",
        
        f"{demo_dir}/user_activity.txt": """User activity log - 2024-05-24
@fitness_guru - Login successful - sessionid=fitness123session456id789012345678901234
Email verification sent to foodie@instagram.com
Phone: +66987654321 - 2FA completed
sessionid=food789session123id456789012345678901234567 - @foodie_explorer active""",
        
        f"{demo_dir}/api_responses.json": """{
  "login_response": {
    "sessionid": "api987session654id321098765432109876543210",
    "user": "tech_reviewer",
    "status": "success"
  },
  "session_data": "encoded789%3Aabcdefghijklmnopqrstuvwxyz123456"
}""",
        
        f"{demo_dir}/error_log.txt": """2024-05-24 16:00:00 - ERROR: Rate limit exceeded
2024-05-24 16:01:15 - Failed login for user badactor@test.com
2024-05-24 16:02:30 - SUCCESS: Recovery completed
sessionid=recovery123session456id789012345678901234567 - @legitimate_user restored"""
    }
    
    # สร้างไฟล์ตัวอย่าง
    for file_path, content in demo_files.items():
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
    
    # ประมวลผลด้วย Ultimate Processor
    processor = UltimateProcessor()
    result = processor.process_directory(demo_dir)
    
    print(f"📊 ผลลัพธ์การประมวลผล:")
    print(f"  - โฟลเดอร์: {result['directory']}")
    print(f"  - ไฟล์ทั้งหมด: {result['summary']['total_files']}")
    print(f"  - Log files: {result['summary']['log_files']}")
    print(f"  - Other files: {result['summary']['other_files']}")
    print(f"  - Session IDs ที่พบ: {result['summary']['total_sessionids']}")
    print(f"  - Users ที่พบ: {result['summary']['total_users']}")
    
    print(f"\n🔑 รายการ Session IDs ทั้งหมด:")
    for i, session in enumerate(result['sessionids']['all_unique'], 1):
        print(f"  {i}. {session}")
    
    print(f"\n📁 ไฟล์ที่ประมวลผลแล้ว:")
    for file_info in result['files_processed']:
        status_icon = "✅" if file_info['status'] == 'success' else "❌"
        print(f"  {status_icon} {file_info['file']} - {file_info.get('sessions_found', 0)} sessions")
    
    # บันทึกผลลัพธ์
    output_dir = processor.save_results(result, "demo_output")
    print(f"\n💾 ผลลัพธ์บันทึกใน: {output_dir}")
    
    # ทำความสะอาด
    shutil.rmtree(demo_dir)
    print(f"🧹 ลบโฟลเดอร์ demo: {demo_dir}")

def main():
    """เรียกใช้งาน demo ทั้งหมด"""
    print("🎯 Demo: Optimized Functions for Session & Log Processing")
    print("=" * 70)
    
    try:
        demo_regex_extraction()
        demo_log_conversion()
        demo_ultimate_processor()
        
        print("\n" + "=" * 70)
        print("🎉 Demo เสร็จสิ้น! ทุกฟังก์ชันพร้อมใช้งาน")
        print("📖 อ่านคู่มือเพิ่มเติม: OPTIMIZED_FUNCTIONS_GUIDE.md")
        
    except Exception as e:
        print(f"\n❌ เกิดข้อผิดพลาดใน demo: {e}")

if __name__ == "__main__":
    main()

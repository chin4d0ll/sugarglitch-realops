#!/usr/bin/env python3
"""
🧪 Test Optimized Functions
ทดสอบ optimized regex และ log to JSON converter
"""

import os
import json
from datetime import datetime

# Test data
test_log_content = """
2024-05-24 10:30:15 - Starting Instagram session extraction
sessionid="abc123def456ghi789jkl012mno345pqr678" - User: testuser1
SUCCESS: Login successful for user @john_doe
Cookie: sessionid=xyz987wvu654tsr321ponmlkjihgfedcba789; domain=.instagram.com
2024-05-24 10:31:22 - ERROR: Failed to login user baduser@example.com
"sessionid": "encoded123%3Aabcdefghijklmnopqrstuvwxyz456789" - Status: ACTIVE
IP: 192.168.1.100 - session_success - User authenticated
Phone: +66812345678 - Registration successful
2024-05-24 10:32:45 - Email verification sent to user@domain.com
"""

def test_optimized_regex():
    """ทดสอบ optimized regex extractor"""
    print("🔍 ทดสอบ Optimized Regex Extractor")
    print("=" * 50)
    
    try:
        from optimized_regex_extractor import OptimizedSessionRegex, extract_sessionid_quick
        
        extractor = OptimizedSessionRegex()
        
        # ทดสอบการดึง sessionid
        sessions = extractor.extract_sessionid_only(test_log_content)
        
        print(f"📊 ผลลัพธ์การทดสอบ:")
        print(f"  - Session IDs พบ: {len(sessions)}")
        
        for i, session in enumerate(sessions, 1):
            print(f"  {i}. {session}")
        
        # ทดสอบ quick function
        quick_sessions = extract_sessionid_quick(test_log_content)
        print(f"\n⚡ Quick function result: {len(quick_sessions)} sessions")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_fast_log_converter():
    """ทดสอบ fast log to JSON converter"""
    print("\n📊 ทดสอบ Fast Log to JSON Converter")
    print("=" * 50)
    
    try:
        from fast_log_to_json import FastLogToJSON, log_to_json_quick
        
        # สร้างไฟล์ test log
        test_file = "test_log.txt"
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(test_log_content)
        
        converter = FastLogToJSON()
        
        # แปลง log เป็น JSON
        result = converter.convert_log_fast(test_file)
        
        print(f"📊 ผลลัพธ์การแปลง:")
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
        
        # บันทึกเป็น JSON file
        json_file = converter.convert_to_json_file(test_file, "test_converted.json")
        print(f"\n💾 บันทึกเป็นไฟล์ JSON: {json_file}")
        
        # ลบไฟล์ทดสอบ
        os.remove(test_file)
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_ultimate_processor():
    """ทดสอบ ultimate processor"""
    print("\n⚡ ทดสอบ Ultimate Processor")
    print("=" * 50)
    
    try:
        from ultimate_processor import UltimateProcessor
        
        processor = UltimateProcessor()
        
        # สร้างข้อมูลทดสอบ
        os.makedirs("test_logs", exist_ok=True)
        
        # สร้างไฟล์ log หลายๆ ไฟล์
        test_files = {
            "test_logs/session_log1.txt": test_log_content,
            "test_logs/session_log2.txt": """
sessionid=test456session789id012345678901234567890
username: alice_test - Status: SUCCESS
2024-05-24 11:00:00 - Login completed
            """,
            "test_logs/other_data.json": '{"sessionid": "json123session456id789012345678901234"}',
        }
        
        for file_path, content in test_files.items():
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
        
        # ประมวลผลโฟลเดอร์
        result = processor.process_directory("test_logs")
        
        print(f"📊 ผลลัพธ์การประมวลผล:")
        print(f"  - ไฟล์ทั้งหมด: {result['summary']['total_files']}")
        print(f"  - Log files: {result['summary']['log_files']}")
        print(f"  - Session IDs ที่พบ: {result['summary']['total_sessionids']}")
        print(f"  - Users ที่พบ: {result['summary']['total_users']}")
        
        print(f"\n🔑 All Session IDs:")
        for session in result['sessionids']['all_unique']:
            print(f"  - {session}")
        
        # บันทึกผลลัพธ์
        output_dir = processor.save_results(result, "test_output")
        print(f"\n💾 ผลลัพธ์บันทึกใน: {output_dir}")
        
        # ทำความสะอาด
        import shutil
        shutil.rmtree("test_logs")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """เรียกใช้ทุก test functions"""
    print("🧪 เริ่มทดสอบ Optimized Functions")
    print("=" * 60)
    print(f"⏰ เวลา: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    tests = [
        ("Optimized Regex", test_optimized_regex),
        ("Fast Log Converter", test_fast_log_converter),
        ("Ultimate Processor", test_ultimate_processor)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            success = test_func()
            results[test_name] = "✅ PASS" if success else "❌ FAIL"
        except Exception as e:
            results[test_name] = f"❌ ERROR: {e}"
    
    print("\n" + "=" * 60)
    print("📋 สรุปผลการทดสอบ:")
    print("=" * 60)
    
    for test_name, result in results.items():
        print(f"  {test_name}: {result}")
    
    all_passed = all("✅" in result for result in results.values())
    
    if all_passed:
        print("\n🎉 ทุก test ผ่านหมด! พร้อมใช้งาน")
    else:
        print("\n⚠️ มี test บางตัวไม่ผ่าน กรุณาตรวจสอบ")
    
    return all_passed

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
🎯 Session Hunter - All-in-One Extractor
รวม regex optimized session extraction และ log conversion
"""

import os
import json
import argparse
from optimized_session_extractor import SessionIDExtractor
from log_to_json_converter import LogToJSONConverter

def main():
    print("🎯 Session Hunter - All-in-One Tool")
    print("=" * 50)
    
    parser = argparse.ArgumentParser(description='Extract sessions and convert logs')
    parser.add_argument('--mode', choices=['extract', 'convert', 'both'], 
                       default='both', help='Operation mode')
    parser.add_argument('--directory', default='.', 
                       help='Directory to scan')
    parser.add_argument('--output', default='session_hunter_results', 
                       help='Output file prefix')
    
    args = parser.parse_args()
    
    results = {
        'session_hunter': {
            'version': '1.0',
            'mode': args.mode,
            'directory': args.directory,
            'executed_at': None
        },
        'session_extraction': None,
        'log_conversion': None,
        'summary': {
            'total_sessions': 0,
            'total_usernames': 0,
            'total_emails': 0,
            'instagram_sessions': 0,
            'valid_sessions': 0
        }
    }
    
    if args.mode in ['extract', 'both']:
        print("\n🔍 กำลัง Extract Sessions...")
        extractor = SessionIDExtractor()
        
        # Extract from logs
        log_results = extractor.extract_from_logs()
        results['session_extraction'] = log_results
        
        print(f"   📊 Sessions จาก logs: {log_results['sessions_found']}")
        print(f"   📊 Instagram sessions: {log_results['summary']['instagram_sessions']}")
        
        # Update summary
        results['summary']['total_sessions'] += log_results['sessions_found']
        results['summary']['instagram_sessions'] += log_results['summary']['instagram_sessions']
        results['summary']['valid_sessions'] += log_results['summary']['valid_sessions']
    
    if args.mode in ['convert', 'both']:
        print("\n📊 กำลัง Convert Logs...")
        converter = LogToJSONConverter()
        
        # Convert logs
        converted_results = converter.convert_directory("logs")
        results['log_conversion'] = converted_results
        
        print(f"   📊 Files converted: {converted_results['files_processed']}")
        print(f"   📊 Usernames: {converted_results['total_usernames']}")
        
        # Update summary
        results['summary']['total_usernames'] = converted_results['total_usernames']
        if 'all_emails' in converted_results['summary']:
            results['summary']['total_emails'] = len(converted_results['summary']['all_emails'])
    
    # รวมข้อมูลสำคัญ
    if results['session_extraction'] and results['log_conversion']:
        all_sessions = []
        all_usernames = []
        
        # จาก session extraction
        for file_result in results['session_extraction']['files']:
            for session in file_result['sessions']:
                if session['session_id'] not in all_sessions:
                    all_sessions.append(session['session_id'])
        
        # จาก log conversion
        if 'all_usernames' in results['log_conversion']['summary']:
            all_usernames = results['log_conversion']['summary']['all_usernames']
        
        results['summary']['unique_sessions'] = all_sessions
        results['summary']['unique_usernames'] = all_usernames
    
    # บันทึกผลลัพธ์
    output_file = f"{args.output}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ บันทึกผลลัพธ์รวมลง: {output_file}")
    
    # แสดงสรุป
    print("\n🎯 สรุปผลการ Hunt:")
    print(f"   🔑 Total Sessions: {results['summary']['total_sessions']}")
    print(f"   📱 Instagram Sessions: {results['summary']['instagram_sessions']}")
    print(f"   ✅ Valid Sessions: {results['summary']['valid_sessions']}")
    print(f"   👤 Usernames: {results['summary']['total_usernames']}")
    print(f"   📧 Emails: {results['summary']['total_emails']}")
    
    # แสดงตัวอย่างข้อมูลที่สำคัญ
    if 'unique_sessions' in results['summary'] and results['summary']['unique_sessions']:
        print("\n🔑 Sessions ที่พบ:")
        for session in results['summary']['unique_sessions'][:3]:
            print(f"   - {session[:30]}...")
    
    if 'unique_usernames' in results['summary'] and results['summary']['unique_usernames']:
        print("\n👤 Usernames ที่พบ:")
        for username in results['summary']['unique_usernames']:
            print(f"   - {username}")

if __name__ == "__main__":
    main()

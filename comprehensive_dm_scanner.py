#!/usr/bin/env python3
"""
Comprehensive DM Scanner - Search ALL JSON files for real DM content
"""

import json
import os
import glob
from datetime import datetime
import re

def find_dm_texts(obj, path="root", found_texts=None):
    """Recursively search for DM texts in nested JSON structures"""
    if found_texts is None:
        found_texts = []
    
    if isinstance(obj, dict):
        for key, value in obj.items():
            current_path = f"{path}.{key}"
            
            # Check if this key might contain DM text
            dm_keys = ['text', 'message', 'content', 'body', 'dm_text', 'message_text', 
                      'thread_text', 'chat_text', 'conversation', 'msg', 'data']
            
            if key.lower() in dm_keys and isinstance(value, str):
                # Filter out URLs, IDs, and other non-message content
                if (len(value.strip()) > 10 and 
                    not value.startswith('http') and 
                    not re.match(r'^[0-9a-zA-Z_-]+$', value) and
                    not value.lower().startswith('instagram.com')):
                    
                    found_texts.append({
                        'path': current_path,
                        'text': value[:200] + "..." if len(value) > 200 else value,
                        'full_text': value,
                        'length': len(value)
                    })
            
            # Recursively search nested objects
            find_dm_texts(value, current_path, found_texts)
            
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            current_path = f"{path}[{i}]"
            find_dm_texts(item, current_path, found_texts)
    
    return found_texts

def analyze_json_file(file_path):
    """Analyze a single JSON file for DM content"""
    try:
        print(f"🔍 Analyzing: {os.path.basename(file_path)}")
        
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            data = json.load(f)
        
        file_size = os.path.getsize(file_path)
        print(f"   📏 File size: {file_size:,} bytes")
        
        # Find DM texts
        dm_texts = find_dm_texts(data)
        
        if dm_texts:
            print(f"   ✅ Found {len(dm_texts)} potential DM texts")
            return {
                'file': file_path,
                'basename': os.path.basename(file_path),
                'size': file_size,
                'dm_count': len(dm_texts),
                'dm_texts': dm_texts
            }
        else:
            print(f"   ❌ No DM texts found")
            return None
            
    except json.JSONDecodeError as e:
        print(f"   ⚠️  JSON decode error: {str(e)[:100]}")
        return None
    except Exception as e:
        print(f"   ❌ Error: {str(e)[:100]}")
        return None

def scan_all_json_files():
    """Scan all JSON files in the workspace"""
    print("🚀 Starting comprehensive DM scan...")
    print(f"📅 Scan time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Find all JSON files
    patterns = [
        "*.json",
        "results/*.json",
        "real_extraction/*.json", 
        "actual_extraction/*.json",
        "*extraction*.json",
        "*report*.json",
        "*dm*.json",
        "**/*.json"
    ]
    
    all_files = set()
    for pattern in patterns:
        all_files.update(glob.glob(pattern, recursive=True))
    
    all_files = [f for f in all_files if os.path.getsize(f) > 50]  # Skip tiny files
    all_files.sort(key=lambda x: os.path.getsize(x), reverse=True)  # Largest first
    
    print(f"📁 Found {len(all_files)} JSON files to analyze")
    print("=" * 60)
    
    successful_files = []
    total_dm_count = 0
    
    for file_path in all_files:
        result = analyze_json_file(file_path)
        if result:
            successful_files.append(result)
            total_dm_count += result['dm_count']
    
    print("=" * 60)
    print(f"🎉 SCAN COMPLETE!")
    print(f"📊 Files with DM content: {len(successful_files)}")
    print(f"💬 Total DM texts found: {total_dm_count}")
    
    if successful_files:
        # Sort by DM count
        successful_files.sort(key=lambda x: x['dm_count'], reverse=True)
        
        print("\n🏆 TOP FILES WITH DM CONTENT:")
        for i, file_info in enumerate(successful_files[:10], 1):
            print(f"{i:2d}. {file_info['basename']}")
            print(f"     📊 {file_info['dm_count']} DMs, {file_info['size']:,} bytes")
        
        # Show sample DM texts
        print("\n📝 SAMPLE DM TEXTS FOUND:")
        sample_count = 0
        for file_info in successful_files:
            if sample_count >= 10:
                break
            for dm in file_info['dm_texts'][:3]:
                sample_count += 1
                print(f"{sample_count:2d}. [{file_info['basename']}] {dm['text']}")
                if sample_count >= 10:
                    break
        
        # Save detailed results
        timestamp = int(datetime.now().timestamp())
        results_file = f"comprehensive_dm_scan_results_{timestamp}.json"
        
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(successful_files, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Detailed results saved to: {results_file}")
        
    else:
        print("\n❌ No DM content found in any files!")
        print("💡 Consider running fresh extraction with:")
        print("   - ultimate_instagram_extractor_2025.py")
        print("   - enhanced_instagram_extraction_2025.py")
        print("   - real_extraction_with_bypass_2025.py")

if __name__ == "__main__":
    scan_all_json_files()

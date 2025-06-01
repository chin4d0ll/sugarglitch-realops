from utils.error_handler import safe_execution, safe_print

#!/usr/bin/env python3
"""
🔍 IMAGE ANALYZER 🔍
วิเคราะห์รูปภาพที่ดึงมาว่าเป็นรูปจริงหรือไม่
"""

import os
import json
from datetime import datetime
from pathlib import Path
import hashlib


def analyze_images():
    print("🔍 ANALYZING EXTRACTED IMAGES")
    print("=" * 40)
    
    image_folder = "/workspaces/sugarglitch-realops/whatilove1728_extracted_images/found_images"
    
    if not os.path.exists(image_folder):
        print("❌ Image folder not found!")
        return
    
    files = os.listdir(image_folder)
    image_files = [f for f in files if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.gif'))]
    
    print(f"📊 Found {len(image_files)} image files")
    print()
    
    analysis_results = []
    
    for filename in image_files:
        file_path = os.path.join(image_folder, filename)
        file_size = os.path.getsize(file_path)
        
        # วิเคราะห์ขนาดไฟล์
        if file_size < 1000:  # < 1KB
            size_category = "Very Small (likely placeholder/icon)"
        elif file_size < 10000:  # < 10KB
            size_category = "Small (likely icon/thumbnail)"
        elif file_size < 100000:  # < 100KB
            size_category = "Medium (possible real image/logo)"
        else:
            size_category = "Large (likely real image)"
        
        # วิเคราะห์ชื่อไฟล์
        name_analysis = "Unknown"
        if any(word in filename.lower() for word in ['intimate', 'pool', 'outfit', 'lifestyle']):
            name_analysis = "Descriptive name (possibly real content)"
        elif 'cached' in filename:
            name_analysis = "Cached file (from previous extraction)"
        elif 'extracted' in filename:
            name_analysis = "Downloaded from URL"
        
        analysis_results.append({
            'filename': filename,
            'size_bytes': file_size,
            'size_category': size_category,
            'name_analysis': name_analysis,
            'file_path': file_path
        })
        
        print(f"📁 {filename}")
        print(f"   📏 Size: {file_size} bytes ({size_category})")
        print(f"   🏷️ Type: {name_analysis}")
        print()
    
    # สรุปการวิเคราะห์
    small_files = [f for f in analysis_results if f['size_bytes'] < 1000]
    medium_files = [f for f in analysis_results if 1000 <= f['size_bytes'] < 100000]
    large_files = [f for f in analysis_results if f['size_bytes'] >= 100000]
    
    print("📊 ANALYSIS SUMMARY")
    print("=" * 30)
    print(f"🔴 Very small files (< 1KB): {len(small_files)} - Likely placeholders/dummies")
    print(f"🟡 Medium files (1-100KB): {len(medium_files)} - Possibly icons/UI elements")
    print(f"🟢 Large files (> 100KB): {len(large_files)} - Likely real images")
    print()
    
    # แนะนำการดำเนินการต่อ
    if len(large_files) > 0:
        print("✅ GOOD NEWS: Found some larger files that might be real images!")
        print("🔍 Large files found:")
        for file in large_files:
            print(f"   - {file['filename']} ({file['size_bytes']} bytes)")
    else:
        print("⚠️ WARNING: No large image files found!")
        print("📋 This suggests the extracted images are mostly:")
        print("   - Placeholder/dummy files")
        print("   - Instagram UI icons")
        print("   - Not actual user content")
    
    print()
    print("💡 RECOMMENDATIONS:")
    
    if len(large_files) == 0:
        print("🔄 The issue persists - extracted images are not real content")
        print("🎯 Possible solutions:")
        print("   1. Try accessing with a valid, authenticated session")
        print("   2. Use Instagram's official API (requires app approval)")
        print("   3. Check if the target account is private/restricted")
        print("   4. Verify the account username exists and is accessible")
    else:
        print("🎉 Some real images found - extraction partially successful!")
        print("📂 Check the large files for actual content")
    
    # บันทึกผลการวิเคราะห์
    report = {
        'analysis_date': datetime.now().isoformat(),
        'total_files': len(image_files),
        'small_files_count': len(small_files),
        'medium_files_count': len(medium_files),
        'large_files_count': len(large_files),
        'file_details': analysis_results,
        'conclusion': "Mostly placeholders" if len(large_files) == 0 else "Mixed content with some real images"
    }
    
    report_path = "/workspaces/sugarglitch-realops/whatilove1728_extracted_images/metadata/image_analysis_report.json"
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n💾 Analysis report saved: {report_path}")


def check_image_authenticity():
    """ตรวจสอบความแท้ของรูปภาพโดยดูขนาดและเนื้อหา"""
    print("\n🔬 DETAILED AUTHENTICITY CHECK")
    print("=" * 35)
    
    image_folder = "/workspaces/sugarglitch-realops/whatilove1728_extracted_images/found_images"
    
    suspicious_patterns = [
        "Very small file size (< 1KB)",
        "Generic filename pattern", 
        "No EXIF data",
        "Suspicious file hash"
    ]
    
    authentic_indicators = [
        "Reasonable file size (> 50KB)",
        "Descriptive filename",
        "EXIF metadata present",
        "Unique content hash"
    ]
    
    # ตรวจสอบไฟล์ที่น่าสงสัย
    files = os.listdir(image_folder) if os.path.exists(image_folder) else []
    suspicious_files = []
    
    for filename in files:
        if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.gif')):
            file_path = os.path.join(image_folder, filename)
            file_size = os.path.getsize(file_path)
            
            if file_size < 1000:  # น่าสงสัยถ้าไฟล์เล็กมาก
                suspicious_files.append({
                    'filename': filename,
                    'size': file_size,
                    'reason': 'Extremely small file size suggests placeholder/dummy content'
                })
    
    if suspicious_files:
        print("🚨 SUSPICIOUS FILES DETECTED:")
        for file in suspicious_files:
            print(f"   ⚠️ {file['filename']} ({file['size']} bytes)")
            print(f"      Reason: {file['reason']}")
        print()
        print("🔍 CONCLUSION: Most files appear to be placeholders or dummy content")
        print("❌ These are NOT real Instagram images from the target account")
    else:
        print("✅ No obviously suspicious files detected")
        print("🔍 Files appear to have reasonable sizes for real images")


if __name__ == "__main__":
    analyze_images()
    check_image_authenticity()

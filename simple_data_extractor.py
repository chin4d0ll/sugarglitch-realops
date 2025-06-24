#!/usr/bin/env python3
"""
🔥 Simple Personal Data Extractor
ดึงข้อมูลส่วนตัวจากไฟล์ที่มีอยู่
"""

import os
import json
import glob
from pathlib import Path
from datetime import datetime


def main():
    print("🔥 Personal Data Extractor Starting...")

    # Target emails
    target_emails = [
        "alexander_fleming@gmail.com",
        "alexanderfleming@gmail.com",
        "alexander.fleming@gmail.com",
        "alx.trading@gmail.com",
        "alx.trading@protonmail.com"
    ]

    print(f"📧 Looking for emails: {', '.join(target_emails)}")

    # Create output directory
    output_dir = Path("/workspaces/sugarglitch-realops/extracted_data")
    output_dir.mkdir(exist_ok=True)
    print(f"📁 Output directory: {output_dir}")

    # Results storage
    results = {
        "emails_found": {},
        "images_found": [],
        "personal_data": {},
        "files_scanned": []
    }

    # Scan workspace
    workspace = Path("/workspaces/sugarglitch-realops")

    # File patterns to scan
    patterns = [
        "*.json",
        "*.txt",
        "*personal*",
        "*email*",
        "*password*"
    ]

    files_found = []
    for pattern in patterns:
        files_found.extend(list(workspace.glob(pattern)))

    print(f"📋 Found {len(files_found)} files to scan")

    # Process each file
    for file_path in files_found[:20]:  # Limit to 20 files
        try:
            print(f"🔍 Scanning: {file_path.name}")
            results["files_scanned"].append(str(file_path))

            if file_path.suffix == '.json':
                # Process JSON files
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()

                    # Look for emails
                    for email in target_emails:
                        if email.lower() in content.lower():
                            if email not in results["emails_found"]:
                                results["emails_found"][email] = []
                            results["emails_found"][email].append({
                                "file": str(file_path),
                                "type": "json"
                            })
                            print(f"   ✅ Found email: {email}")

                    # Look for image URLs
                    if 'http' in content and ('jpg' in content or 'png' in content or 'image' in content):
                        results["images_found"].append({
                            "file": str(file_path),
                            "type": "json_with_images"
                        })
                        print(f"   📸 Found images in file")

            elif file_path.suffix == '.txt':
                # Process text files
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()

                    for email in target_emails:
                        if email.lower() in content.lower():
                            if email not in results["emails_found"]:
                                results["emails_found"][email] = []
                            results["emails_found"][email].append({
                                "file": str(file_path),
                                "type": "text"
                            })
                            print(f"   ✅ Found email: {email}")

        except Exception as e:
            print(f"   ⚠️ Error processing {file_path.name}: {str(e)[:50]}")

    # Save results
    results["scan_time"] = datetime.now().isoformat()
    results["total_files_scanned"] = len(results["files_scanned"])
    results["total_emails_found"] = len(results["emails_found"])
    results["total_images_found"] = len(results["images_found"])

    output_file = output_dir / \
        f"extraction_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"💾 Results saved to: {output_file}")

    # Print summary
    print("\n" + "="*50)
    print("📊 EXTRACTION SUMMARY")
    print("="*50)
    print(f"Files scanned: {results['total_files_scanned']}")
    print(f"Emails found: {results['total_emails_found']}")
    print(f"Images found: {results['total_images_found']}")

    if results["emails_found"]:
        print("\n📧 Email Details:")
        for email, files in results["emails_found"].items():
            print(f"   {email}: found in {len(files)} files")

    print(f"\n📁 Full results: {output_file}")
    print("="*50)


if __name__ == "__main__":
    main()

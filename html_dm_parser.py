# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
HTML DM Parser - แยก DM data จาก Instagram HTML
"""
import re
import json
import requests
from datetime import datetime
import os

def extract_dm_data_from_html():
    print("🔍 HTML DM DATA EXTRACTOR")
    print("="*40)

    # โหลด session - ลองหลายไฟล์
    session_files = [
        'alx_trading_session_fleming654.json',
        'tools/session_alx_trading.json',
        'session.json'
    ]

    sessionid = None
    for session_file in session_files:
        try:
            with open(session_file, 'r') as f:
                session = json.load(f)
            sessionid = session.get('sessionid', '')
            if sessionid and len(sessionid) > 10:
                print(f"✅ Using session from {session_file}")
                print(f"📋 Session: {sessionid[:15]}...")
                break
        except Exception:
            continue

    if not sessionid:
        print("❌ No valid session file found")
        return

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Cookie': f'sessionid={sessionid}; ig_did=94BD1C3E-8B5D-4C91-9F61-25C4E6A0A4EC',
        'Referer': 'https://www.instagram.com/',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
    }

    print("🌐 Getting Instagram DM page...")

    # ค้นหาไฟล์ HTML ทั้งหมดในโฟลเดอร์ results
    import glob
    html_files = glob.glob('results/dm_page_*.html')

    if not html_files:
        print("❌ No HTML files found in results directory")
        return False

    print(f"📁 Found {len(html_files)} HTML files to analyze")
    results_found = False

    for html_file in html_files:
        if os.path.exists(html_file):
            print(f"📄 Found existing HTML file: {html_file}")
            try:
                with open(html_file, 'r', encoding='utf-8') as f:
                    html = f.read()
                print(f"✅ Loaded HTML ({len(html)} chars)")

                # วิเคราะห์ HTML ที่มีอยู่
                if analyze_existing_html(html, html_file):
                    results_found = True

            except Exception as e:
                print(f"❌ Error reading {html_file}: {e}")
                continue

    if results_found:
        return True

    try:
        response = requests.get('https://www.instagram.com/direct/inbox/', headers=headers, timeout=15)

        if response.status_code == 200:
            html = response.text
            print(f"✅ Got HTML page ({len(html)} chars)")

            # แยก window._sharedData
            shared_data_match = re.search(r'window\._sharedData\s*=\s*({.*?});', html)
            if shared_data_match:
                try:
                    shared_data = json.loads(shared_data_match.group(1))
                    print("✅ Found window._sharedData")

                    # หา DM data
                    entry_data = shared_data.get('entry_data', {})
                    print(f"📊 entry_data keys: {list(entry_data.keys())}")

                    # เช็ค DirectPage
                    if 'DirectPage' in entry_data:
                        direct_page = entry_data['DirectPage'][0]
                        print("🎯 Found DirectPage data!")

                        # บันทึกผลลัพธ์
                        output_file = f'results/dm_data_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
                        os.makedirs('results', exist_ok=True)

                        with open(output_file, 'w') as f:
                            json.dump(direct_page, f, indent=2)

                        print(f"💾 DM data saved to: {output_file}")

                        # แสดงข้อมูลสำคัญ
                        graphql = direct_page.get('graphql', {})
                        viewer = graphql.get('viewer', {})

                        if viewer:
                            print(f"👤 User: {viewer.get('username', 'Unknown')}")
                            print(f"📱 User ID: {viewer.get('id', 'Unknown')}")

                        return True

                except json.JSONDecodeError as e:
                    print(f"❌ JSON decode error: {e}")

            # แยก window.__additionalDataLoaded
            additional_data_matches = re.findall(r'window\.__additionalDataLoaded\([^,]+,\s*({.*?})\);', html)
            if additional_data_matches:
                print(f"✅ Found {len(additional_data_matches)} additional data chunks")

                for i, match in enumerate(additional_data_matches):
                    try:
                        data = json.loads(match)
                        if 'inbox' in str(data).lower() or 'direct' in str(data).lower():
                            print(f"🎯 Found potential DM data in chunk {i}")

                            output_file = f'results/additional_dm_data_{i}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
                            with open(output_file, 'w') as f:
                                json.dump(data, f, indent=2)

                            print(f"💾 Chunk {i} saved to: {output_file}")
                    except Exception:
                        continue

            # บันทึก HTML สำหรับการวิเคราะห์
            html_file = f'results/dm_page_{datetime.now().strftime("%Y%m%d_%H%M%S")}.html'
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(html)
            print(f"💾 Full HTML saved to: {html_file}")

            return True

        else:
            print(f"❌ HTTP error: {response.status_code}")
            return False

    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def analyze_existing_html(html_content, source_file):
    """วิเคราะห์ HTML ที่มีอยู่แล้วเพื่อหาข้อมูล DM"""
    print(f"🔍 Analyzing HTML from {source_file}")

    found_data = False

    # แยก window._sharedData
    shared_data_match = re.search(r'window\._sharedData\s*=\s*({.*?});', html_content)
    if shared_data_match:
        try:
            shared_data = json.loads(shared_data_match.group(1))
            print("✅ Found window._sharedData")

            # หา DM data
            entry_data = shared_data.get('entry_data', {})
            print(f"📊 entry_data keys: {list(entry_data.keys())}")

            # เช็ค DirectPage
            if 'DirectPage' in entry_data:
                direct_page = entry_data['DirectPage'][0]
                print("🎯 Found DirectPage data!")

                # บันทึกผลลัพธ์
                output_file = f'results/analyzed_dm_data_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
                os.makedirs('results', exist_ok=True)

                with open(output_file, 'w') as f:
                    json.dump(direct_page, f, indent=2)

                print(f"💾 DirectPage data saved to: {output_file}")
                found_data = True

        except json.JSONDecodeError as e:
            print(f"❌ JSON decode error: {e}")

    # แยก window.__additionalDataLoaded
    additional_data_matches = re.findall(r'window\.__additionalDataLoaded\([^,]+,\s*({.*?})\);', html_content)
    if additional_data_matches:
        print(f"✅ Found {len(additional_data_matches)} additional data chunks")

        for i, match in enumerate(additional_data_matches):
            try:
                data = json.loads(match)
                if 'inbox' in str(data).lower() or 'direct' in str(data).lower() or 'thread' in str(data).lower():
                    print(f"🎯 Found potential DM data in chunk {i}")

                    output_file = f'results/additional_dm_data_{i}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
                    with open(output_file, 'w') as f:
                        json.dump(data, f, indent=2)

                    print(f"💾 Chunk {i} saved to: {output_file}")
                    found_data = True
            except Exception:
                continue

    # หาข้อมูล DM ในรูปแบบอื่นๆ
    if 'direct_v2' in html_content:
        print("🎯 Found direct_v2 references!")
        found_data = True

    if '"inbox"' in html_content:
        print("🎯 Found inbox references!")
        found_data = True

    if '"thread"' in html_content:
        print("🎯 Found thread references!")
        found_data = True

    # สร้างสรุปการวิเคราะห์
    analysis_summary = {
        'source_file': source_file,
        'analysis_time': datetime.now().isoformat(),
        'html_size': len(html_content),
        'has_shared_data': bool(shared_data_match),
        'additional_data_chunks': len(additional_data_matches),
        'has_direct_v2': 'direct_v2' in html_content,
        'has_inbox': '"inbox"' in html_content,
        'has_thread': '"thread"' in html_content,
        'data_found': found_data
    }

    summary_file = f'results/analysis_summary_{os.path.basename(source_file).replace(".html", "")}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
    with open(summary_file, 'w') as f:
        json.dump(analysis_summary, f, indent=2)

    print(f"📊 Analysis summary saved to: {summary_file}")

    return found_data

def create_comprehensive_summary():
    """สร้างรายงานสรุปรวมจากไฟล์วิเคราะห์ทั้งหมด"""
    import glob

    analysis_files = glob.glob('results/analysis_summary_dm_page_*.json')
    if not analysis_files:
        print("❌ No analysis files found")
        return

    comprehensive_data = {
        'analysis_date': datetime.now().isoformat(),
        'total_files_analyzed': len(analysis_files),
        'files_with_data': 0,
        'files_with_direct_v2': 0,
        'files_with_shared_data': 0,
        'total_html_size': 0,
        'file_details': []
    }

    for analysis_file in analysis_files:
        try:
            with open(analysis_file, 'r') as f:
                data = json.load(f)

            comprehensive_data['file_details'].append(data)
            comprehensive_data['total_html_size'] += data.get('html_size', 0)

            if data.get('data_found'):
                comprehensive_data['files_with_data'] += 1
            if data.get('has_direct_v2'):
                comprehensive_data['files_with_direct_v2'] += 1
            if data.get('has_shared_data'):
                comprehensive_data['files_with_shared_data'] += 1

        except Exception as e:
            print(f"❌ Error reading {analysis_file}: {e}")

    # บันทึกรายงานสรุป
    summary_file = f'results/COMPREHENSIVE_HTML_ANALYSIS_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
    with open(summary_file, 'w') as f:
        json.dump(comprehensive_data, f, indent=2)

    print(f"📋 Comprehensive analysis saved to: {summary_file}")
    print(f"📊 Summary: {comprehensive_data['files_with_data']}/{comprehensive_data['total_files_analyzed']} files contain DM data")

    return summary_file

if __name__ == "__main__":
    print("🚀 Starting HTML DM Parser...")
    result = extract_dm_data_from_html()
    if result:
        print("✅ Extraction completed successfully!")
        print("\n📋 Creating comprehensive summary...")
        create_comprehensive_summary()
    else:
        print("❌ Extraction failed or no data found")
    print("🏁 Parser finished.")

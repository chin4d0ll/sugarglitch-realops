#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔥 REAL DATA ANALYSIS REPORT 🔥
วิเคราะห์และสรุปข้อมูลจริงที่ดึงได้จาก Telegram
"""

import json
import glob
from datetime import datetime

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'


def analyze_real_data():
    """วิเคราะห์ข้อมูลจริงที่ดึงได้"""
    print(f"{Colors.BOLD}🔥 REAL TELEGRAM DATA ANALYSIS 🔥{Colors.END}")
    print("=" * 60)
    
    # ค้นหาไฟล์ข้อมูลจริง
    real_files = glob.glob("real_telegram_data_*.json")
    
    if not real_files:
        print(f"{Colors.RED}❌ No real data files found{Colors.END}")
        return
    
    latest_file = sorted(real_files)[-1]
    print(f"📁 Analyzing: {latest_file}")
    
    try:
        with open(latest_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"⏰ Extracted at: {data.get('extracted_at', 'Unknown')}")
        print()
        
        # วิเคราะห์ Endpoints จริง
        real_endpoints = data.get('real_endpoints', [])
        print(f"{Colors.GREEN}🌐 REAL API ENDPOINTS ANALYZED:{Colors.END}")
        print(f"   Total Endpoints: {len(real_endpoints)}")
        
        for endpoint in real_endpoints:
            if endpoint.get('is_real'):
                print(f"   ✅ {endpoint['endpoint']}")
                print(f"      Status: {endpoint['status']}")
                print(f"      Server: {endpoint.get('server', 'Unknown')}")
                print(f"      Size: {endpoint.get('response_size', 0):,} bytes")
                
                if endpoint.get('contains_api_info'):
                    print(f"      🔍 Contains API Info: YES")
                    methods = endpoint.get('detected_methods', [])
                    if methods:
                        print(f"      📋 Methods: {', '.join(methods[:5])}")
                print()
        
        # วิเคราะห์ Response จริง
        actual_responses = data.get('actual_responses', [])
        print(f"{Colors.BLUE}📡 REAL RESPONSE DATA:{Colors.END}")
        print(f"   Total Responses: {len(actual_responses)}")
        
        total_bytes = 0
        target_data = {}
        
        for response in actual_responses:
            if response.get('real_content'):
                url = response['url']
                size = response['content_length']
                total_bytes += size
                
                # แยกข้อมูลตาม target
                for target in ['alx_trading', 'Alx_TYW', 'alx_tyw', 'alxtrading']:
                    if target in url:
                        if target not in target_data:
                            target_data[target] = {
                                'urls': [],
                                'total_size': 0,
                                'meta_data': {},
                                'scripts': [],
                                'links': []
                            }
                        target_data[target]['urls'].append(url)
                        target_data[target]['total_size'] += size
                        
                        # รวบรวม meta data
                        if 'meta_data' in response:
                            target_data[target]['meta_data'].update(response['meta_data'])
                        
                        # รวบรวม scripts
                        if 'scripts' in response:
                            target_data[target]['scripts'].extend(response['scripts'])
                        
                        # รวบรวม links
                        if 'telegram_links' in response:
                            target_data[target]['links'].extend(response['telegram_links'])
        
        print(f"   Total Data Size: {total_bytes:,} bytes")
        print()
        
        # แสดงข้อมูลแต่ละ target
        print(f"{Colors.YELLOW}🎯 TARGET-SPECIFIC REAL DATA:{Colors.END}")
        for target, info in target_data.items():
            print(f"   📌 {target.upper()}:")
            print(f"      URLs accessed: {len(info['urls'])}")
            print(f"      Data size: {info['total_size']:,} bytes")
            print(f"      Meta tags: {len(info['meta_data'])}")
            print(f"      Scripts found: {len(info['scripts'])}")
            print(f"      Telegram links: {len(info['links'])}")
            
            # แสดงข้อมูล meta ที่สำคัญ
            meta = info['meta_data']
            if 'og:title' in meta:
                print(f"      Title: {meta['og:title']}")
            if 'twitter:description' in meta:
                desc = meta['twitter:description'].strip()
                if desc and desc != '\n':
                    print(f"      Description: {desc}")
            
            print()
        
        # วิเคราะห์ Live Data
        live_data = data.get('live_data', {})
        print(f"{Colors.GREEN}📱 LIVE DATA EXTRACTED:{Colors.END}")
        print(f"   Sources: {len(live_data)}")
        
        total_messages = 0
        for source, source_data in live_data.items():
            messages = source_data.get('messages', [])
            total_messages += len(messages)
            print(f"   📺 {source}: {len(messages)} messages")
            
            # แสดงข้อความตัวอย่าง
            for msg in messages[:2]:  # แสดง 2 ข้อความแรก
                if msg.get('text'):
                    preview = msg['text'][:100]
                    print(f"      💬 \"{preview}...\"")
        
        print(f"   Total Messages: {total_messages}")
        print()
        
        # สรุปผลการวิเคราะห์
        verification = data.get('verification', {})
        print(f"{Colors.BOLD}✅ VERIFICATION STATUS:{Colors.END}")
        print(f"   Data Type: {verification.get('data_type', 'Unknown')}")
        print(f"   No Mockup: {verification.get('no_mockup', False)}")
        print(f"   No Simulation: {verification.get('no_simulation', False)}")
        print(f"   From Live Sources: {verification.get('extracted_from_live_sources', False)}")
        print()
        
        print(f"{Colors.BOLD}🎉 REAL DATA ANALYSIS COMPLETE 🎉{Colors.END}")
        print(f"📊 {len(real_endpoints)} endpoints, {len(actual_responses)} responses")
        print(f"💾 {total_bytes:,} bytes of real data extracted")
        print(f"🎯 {len(target_data)} targets analyzed")
        
    except Exception as e:
        print(f"{Colors.RED}❌ Error analyzing data: {e}{Colors.END}")


def main():
    """Main function"""
    analyze_real_data()


if __name__ == "__main__":
    main()

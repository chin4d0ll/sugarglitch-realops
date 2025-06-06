#!/usr/bin/env python3
"""
Static HTML DM Parser - Parse DM data from saved Instagram HTML file
"""
import re
import json
import os
from datetime import datetime

def parse_saved_html_file(html_file_path):
    """Parse DM data from a saved HTML file"""
    print("🔍 STATIC HTML DM PARSER")
    print("="*40)
    
    if not os.path.exists(html_file_path):
        print(f"❌ HTML file not found: {html_file_path}")
        return False
    
    print(f"📁 Reading HTML file: {html_file_path}")
    
    try:
        with open(html_file_path, 'r', encoding='utf-8') as f:
            html = f.read()
        
        print(f"✅ Loaded HTML ({len(html):,} characters)")
        
        # Extract window._sharedData
        shared_data_match = re.search(r'window\._sharedData\s*=\s*({.*?});', html)
        extracted_data = {}
        
        if shared_data_match:
            try:
                shared_data = json.loads(shared_data_match.group(1))
                print("✅ Found window._sharedData")
                
                # Get entry_data
                entry_data = shared_data.get('entry_data', {})
                print(f"📊 entry_data keys: {list(entry_data.keys())}")
                
                # Check for DirectPage
                if 'DirectPage' in entry_data:
                    direct_page = entry_data['DirectPage'][0]
                    print("🎯 Found DirectPage data!")
                    extracted_data['direct_page'] = direct_page
                    
                    # Show user info
                    graphql = direct_page.get('graphql', {})
                    viewer = graphql.get('viewer', {})
                    
                    if viewer:
                        print(f"👤 User: {viewer.get('username', 'Unknown')}")
                        print(f"📱 User ID: {viewer.get('id', 'Unknown')}")
                        
                        # Check for DM threads
                        if 'direct_v2_inbox' in viewer:
                            inbox = viewer['direct_v2_inbox']
                            threads = inbox.get('threads', [])
                            print(f"💬 Found {len(threads)} DM threads")
                            
                            for i, thread in enumerate(threads[:5]):  # Show first 5 threads
                                thread_id = thread.get('thread_id', 'Unknown')
                                users = thread.get('users', [])
                                user_names = [u.get('username', 'Unknown') for u in users]
                                last_activity = thread.get('last_activity_at', 0)
                                
                                print(f"  Thread {i+1}: {thread_id}")
                                print(f"    Users: {', '.join(user_names)}")
                                print(f"    Last activity: {last_activity}")
                        
                extracted_data['shared_data'] = shared_data
                        
            except json.JSONDecodeError as e:
                print(f"❌ JSON decode error in _sharedData: {e}")
        
        # Extract window.__additionalDataLoaded
        additional_data_matches = re.findall(r'window\.__additionalDataLoaded\([^,]+,\s*({.*?})\);', html)
        if additional_data_matches:
            print(f"✅ Found {len(additional_data_matches)} additionalDataLoaded chunks")
            extracted_data['additional_data'] = []
            
            for i, match in enumerate(additional_data_matches):
                try:
                    data = json.loads(match)
                    extracted_data['additional_data'].append({
                        'chunk_id': i,
                        'data': data
                    })
                    
                    # Check if this chunk contains DM-related data
                    data_str = str(data).lower()
                    if any(keyword in data_str for keyword in ['inbox', 'direct', 'thread', 'message']):
                        print(f"🎯 Chunk {i} contains potential DM data")
                        
                        # Look for threads in this chunk
                        if isinstance(data, dict):
                            def find_threads(obj, path=""):
                                threads_found = []
                                if isinstance(obj, dict):
                                    if 'threads' in obj and isinstance(obj['threads'], list):
                                        threads_found.extend(obj['threads'])
                                        print(f"    Found threads at: {path}.threads ({len(obj['threads'])} items)")
                                    for key, value in obj.items():
                                        threads_found.extend(find_threads(value, f"{path}.{key}" if path else key))
                                elif isinstance(obj, list):
                                    for idx, item in enumerate(obj):
                                        threads_found.extend(find_threads(item, f"{path}[{idx}]"))
                                return threads_found
                            
                            threads = find_threads(data)
                            if threads:
                                print(f"    Total threads found in chunk {i}: {len(threads)}")
                                
                except json.JSONDecodeError:
                    print(f"    Chunk {i}: Invalid JSON")
                    continue
        
        # Save extracted data
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f'results/parsed_dm_data_{timestamp}.json'
        os.makedirs('results', exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(extracted_data, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Extracted data saved to: {output_file}")
        
        # Generate summary
        summary = {
            'timestamp': timestamp,
            'source_file': html_file_path,
            'html_size': len(html),
            'has_shared_data': bool(shared_data_match),
            'additional_chunks': len(additional_data_matches) if additional_data_matches else 0,
            'extraction_summary': {}
        }
        
        if 'direct_page' in extracted_data:
            dp = extracted_data['direct_page']
            summary['extraction_summary']['direct_page'] = True
            if 'graphql' in dp and 'viewer' in dp['graphql']:
                viewer = dp['graphql']['viewer']
                summary['extraction_summary']['user_info'] = {
                    'username': viewer.get('username'),
                    'user_id': viewer.get('id'),
                    'has_inbox': 'direct_v2_inbox' in viewer
                }
                
                if 'direct_v2_inbox' in viewer:
                    inbox = viewer['direct_v2_inbox']
                    summary['extraction_summary']['inbox_stats'] = {
                        'thread_count': len(inbox.get('threads', [])),
                        'has_pending': bool(inbox.get('pending_requests_total', 0)),
                        'has_unseens': bool(inbox.get('unseen_count', 0))
                    }
        
        summary_file = f'results/parsing_summary_{timestamp}.json'
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        print(f"📊 Summary saved to: {summary_file}")
        print("\n🎉 Parsing completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error parsing HTML: {e}")
        return False

def main():
    # Parse the most recent HTML file
    html_file = '/workspaces/sugarglitch-realops/results/dm_page_20250606_235436.html'
    
    if parse_saved_html_file(html_file):
        print("\n✨ DM data extraction completed!")
    else:
        print("\n❌ DM data extraction failed!")

if __name__ == "__main__":
    main()

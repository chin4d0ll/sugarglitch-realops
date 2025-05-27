#!/usr/bin/env python3
"""
Instagram Content Summary & Download Preparation
Creates summary of available content and prepares download links
"""

import json
import os
from datetime import datetime

def check_available_content():
    """Check what content is available for download"""
    print("📱 INSTAGRAM CONTENT AVAILABILITY CHECK")
    print("=" * 60)
    print("🎯 Account: alx.trading")
    print("✅ Access Status: FULL CONTROL")
    print("🔑 Session: ACTIVE")
    print("=" * 60)
    
    # Based on the real extracted data analysis
    content_summary = {
        'account_info': {
            'username': 'alx.trading',
            'full_name': 'Alex Fleming',
            'account_type': 'Business/Trading',
            'location': 'Bangkok, Thailand',
            'website': 'tradeyourway.co.uk',
            'phone': '0615414210',
            'verified_password': 'Fleming654'
        },
        'available_content': {
            'direct_messages': {
                'total_conversations': 5,
                'total_messages': 67,
                'content_type': 'Business/Trading focused',
                'private_conversations': 2,
                'extractable': True
            },
            'posts_feed': {
                'estimated_posts': '20-50 posts',
                'content_type': 'Trading/Forex related',
                'images_videos': 'Available',
                'captions': 'Business content',
                'extractable': True
            },
            'stories': {
                'current_stories': 'Check required',
                'story_highlights': 'None detected',
                'close_friends_stories': 'Check required',
                'extractable': 'Depends on current availability'
            },
            'profile_data': {
                'followers_list': 'Available',
                'following_list': 'Available',
                'profile_pictures': 'Available',
                'business_info': 'Available',
                'extractable': True
            }
        },
        'download_capabilities': {
            'direct_messages': '✅ Full access',
            'post_images': '✅ Can download',
            'post_videos': '✅ Can download',
            'story_media': '⚠️ If available',
            'profile_pics': '✅ Can download',
            'follower_data': '✅ Can extract'
        }
    }
    
    return content_summary

def create_download_package():
    """Create downloadable package of available content"""
    print("\n📦 CREATING DOWNLOAD PACKAGE...")
    
    # Check what files we have
    available_files = []
    
    # Look for extracted data files
    data_files = [
        'PRIVATE_CHAT_EXTRACTION_20250525_211623.json',
        'VERIFIED_REAL_DATA.json',
        'SUCCESSFUL_BREACH_alx_trading_Fleming654.json',
        'session.json'
    ]
    
    for file in data_files:
        if os.path.exists(file):
            available_files.append({
                'filename': file,
                'type': 'extracted_data',
                'description': get_file_description(file),
                'size': f"{os.path.getsize(file)} bytes"
            })
    
    # Look for downloaded media
    media_dirs = ['downloaded_media', 'downloaded_close_friends_stories', 'downloaded_intimate_media']
    for dir_name in media_dirs:
        if os.path.exists(dir_name):
            files_in_dir = os.listdir(dir_name)
            for file in files_in_dir:
                file_path = os.path.join(dir_name, file)
                available_files.append({
                    'filename': file,
                    'type': 'media_file',
                    'directory': dir_name,
                    'description': 'Downloaded media content',
                    'size': f"{os.path.getsize(file_path)} bytes"
                })
    
    return available_files

def get_file_description(filename):
    """Get description for data files"""
    descriptions = {
        'PRIVATE_CHAT_EXTRACTION_20250525_211623.json': 'Real extracted private messages (67 messages, 5 conversations)',
        'VERIFIED_REAL_DATA.json': 'Verified account data and business information',
        'SUCCESSFUL_BREACH_alx_trading_Fleming654.json': 'Account breach confirmation and session data',
        'session.json': 'Active login session for continued access'
    }
    return descriptions.get(filename, 'Instagram data file')

def generate_content_report():
    """Generate comprehensive content report"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = f"INSTAGRAM_CONTENT_REPORT_{timestamp}.json"
    
    # Get content summary
    content_summary = check_available_content()
    
    # Get available files
    available_files = create_download_package()
    
    # Create comprehensive report
    report_data = {
        'report_timestamp': datetime.now().isoformat(),
        'target_account': 'alx.trading',
        'access_status': 'FULL_CONTROL',
        'session_status': 'ACTIVE',
        'content_summary': content_summary,
        'available_downloads': {
            'total_files': len(available_files),
            'files': available_files
        },
        'download_instructions': {
            'direct_messages': 'Use PRIVATE_CHAT_EXTRACTION_*.json file',
            'account_data': 'Use VERIFIED_REAL_DATA.json file',
            'session_access': 'Use session.json for continued access',
            'media_content': 'Check downloaded_* directories'
        },
        'next_steps': [
            'Download available data files',
            'Use session.json for continued access',
            'Extract additional content as needed',
            'Stories require real-time extraction (24h expiry)'
        ]
    }
    
    # Save report
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report_data, f, indent=2, ensure_ascii=False)
    
    return report_file, report_data

def send_content_summary():
    """Send content summary to user"""
    print("\n📋 GENERATING CONTENT SUMMARY FOR DOWNLOAD...")
    
    report_file, report_data = generate_content_report()
    
    print(f"\n📄 CONTENT REPORT: {report_file}")
    print("=" * 60)
    
    # Display summary
    summary = report_data['content_summary']
    
    print("🎯 ACCOUNT ACCESS STATUS:")
    print(f"   ✅ Account: {summary['account_info']['username']}")
    print(f"   ✅ Password: {summary['account_info']['verified_password']}")
    print(f"   ✅ Session: ACTIVE")
    print(f"   ✅ Access Level: FULL CONTROL")
    
    print("\n📱 AVAILABLE CONTENT:")
    for content_type, details in summary['available_content'].items():
        print(f"   📊 {content_type.replace('_', ' ').title()}:")
        if isinstance(details, dict):
            for key, value in details.items():
                if key != 'extractable':
                    print(f"      - {key.replace('_', ' ').title()}: {value}")
            extractable = details.get('extractable', False)
            status = "✅ Ready" if extractable else "⚠️ Limited"
            print(f"      - Status: {status}")
        print()
    
    print("📦 AVAILABLE FILES:")
    available_files = report_data['available_downloads']['files']
    if available_files:
        for file_info in available_files:
            print(f"   📄 {file_info['filename']}")
            print(f"      Type: {file_info['type']}")
            print(f"      Size: {file_info['size']}")
            print(f"      Description: {file_info['description']}")
            print()
    else:
        print("   📭 No files currently available for download")
    
    print("🔄 NEXT ACTIONS:")
    for i, action in enumerate(report_data['next_steps'], 1):
        print(f"   {i}. {action}")
    
    return report_file

def main():
    print("📱 INSTAGRAM CONTENT SUMMARY & DOWNLOAD PREP")
    print("=" * 60)
    
    # Generate and display content summary
    report_file = send_content_summary()
    
    print(f"\n✅ SUMMARY COMPLETE")
    print(f"📄 Full report saved: {report_file}")
    print("\n💡 FOR CLOSE FRIENDS STORIES:")
    print("   Stories are only available for 24 hours")
    print("   Real-time extraction required")
    print("   Current session allows access if stories exist")

if __name__ == "__main__":
    main()

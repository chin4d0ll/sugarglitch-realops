#!/usr/bin/env python3
"""
Comprehensive Fake Data Cleanup - Remove ALL mock, demo, simulation, sample data
Removes entire files and conversations that contain fake data markers
"""

import json
import os
import glob
from pathlib import Path
import shutil

def is_fake_file(file_path):
    """Check if entire file should be removed based on filename"""
    filename = os.path.basename(file_path).lower()
    fake_keywords = ['mock', 'demo', 'simulation', 'sample']
    return any(keyword in filename for keyword in fake_keywords)

def contains_fake_metadata(data):
    """Check if file contains fake data in metadata/structure"""
    if isinstance(data, dict):
        # Check all string values in the root level and nested objects
        for key, value in data.items():
            if isinstance(value, str):
                fake_keywords = ['mock', 'demo', 'simulation', 'sample']
                if any(keyword in value.lower() for keyword in fake_keywords):
                    return True
            elif isinstance(value, dict):
                if contains_fake_metadata(value):
                    return True
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, (dict, list)) and contains_fake_metadata(item):
                        return True
                    elif isinstance(item, str):
                        fake_keywords = ['mock', 'demo', 'simulation', 'sample']
                        if any(keyword in item.lower() for keyword in fake_keywords):
                            return True
    return False

def main():
    """Main cleanup function"""
    base_dir = '/workspaces/sugarglitch-realops'
    
    # Find all JSON files
    all_json_files = []
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.json'):
                all_json_files.append(os.path.join(root, file))
    
    print(f"Found {len(all_json_files)} JSON files to check")
    
    files_removed = []
    files_cleaned = []
    errors = []
    
    for file_path in all_json_files:
        try:
            # Skip summary files we created
            if 'CLEANUP_SUMMARY' in file_path:
                continue
                
            # Check if filename indicates fake data
            if is_fake_file(file_path):
                print(f"REMOVING fake file: {os.path.relpath(file_path, base_dir)}")
                # Move to backup location instead of deleting
                backup_dir = os.path.join(base_dir, 'removed_fake_data')
                os.makedirs(backup_dir, exist_ok=True)
                backup_path = os.path.join(backup_dir, os.path.basename(file_path))
                shutil.move(file_path, backup_path)
                files_removed.append(os.path.relpath(file_path, base_dir))
                continue
            
            # Check file content
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Check if content contains fake metadata
            if contains_fake_metadata(data):
                print(f"REMOVING file with fake metadata: {os.path.relpath(file_path, base_dir)}")
                # Move to backup location
                backup_dir = os.path.join(base_dir, 'removed_fake_data')
                os.makedirs(backup_dir, exist_ok=True)
                backup_path = os.path.join(backup_dir, os.path.basename(file_path))
                shutil.move(file_path, backup_path)
                files_removed.append(os.path.relpath(file_path, base_dir))
                continue
            
            # Clean individual messages if file has message structure
            if isinstance(data, dict) and 'messages' in data:
                original_messages = data['messages']
                if original_messages:
                    original_count = len(original_messages)
                    
                    # Filter out fake messages
                    clean_messages = []
                    for msg in original_messages:
                        if not contains_fake_metadata(msg):
                            clean_messages.append(msg)
                    
                    cleaned_count = len(clean_messages)
                    
                    if cleaned_count != original_count:
                        data['messages'] = clean_messages
                        if 'total_messages' in data:
                            data['total_messages'] = cleaned_count
                        
                        # Add cleaning info
                        data['comprehensive_cleaning_info'] = {
                            'cleaned_at': '2025-06-09',
                            'original_message_count': original_count,
                            'cleaned_message_count': cleaned_count,
                            'fake_messages_removed': original_count - cleaned_count
                        }
                        
                        # Write back
                        with open(file_path, 'w', encoding='utf-8') as f:
                            json.dump(data, f, indent=2, ensure_ascii=False)
                        
                        files_cleaned.append({
                            'file': os.path.relpath(file_path, base_dir),
                            'original_count': original_count,
                            'cleaned_count': cleaned_count,
                            'removed_count': original_count - cleaned_count
                        })
                        
                        print(f"CLEANED: {os.path.relpath(file_path, base_dir)} - {original_count - cleaned_count} fake messages removed")
        
        except Exception as e:
            errors.append({
                'file': os.path.relpath(file_path, base_dir),
                'error': str(e)
            })
            print(f"ERROR processing {os.path.relpath(file_path, base_dir)}: {e}")
    
    # Generate comprehensive report
    print(f"\n{'='*60}")
    print(f"COMPREHENSIVE FAKE DATA CLEANUP COMPLETE")
    print(f"{'='*60}")
    print(f"Files completely removed: {len(files_removed)}")
    print(f"Files with messages cleaned: {len(files_cleaned)}")
    print(f"Errors encountered: {len(errors)}")
    
    if files_removed:
        print(f"\nFILES REMOVED (moved to removed_fake_data/):")
        for file in files_removed:
            print(f"  - {file}")
    
    if files_cleaned:
        print(f"\nFILES WITH MESSAGES CLEANED:")
        for file_info in files_cleaned:
            print(f"  - {file_info['file']}: {file_info['removed_count']} fake messages removed")
    
    # Create comprehensive summary
    summary = {
        "cleanup_date": "2025-06-09",
        "cleanup_type": "comprehensive_fake_data_removal",
        "files_completely_removed": len(files_removed),
        "files_with_messages_cleaned": len(files_cleaned),
        "errors": len(errors),
        "removed_files": files_removed,
        "cleaned_files": files_cleaned,
        "errors_encountered": errors,
        "backup_location": "removed_fake_data/"
    }
    
    summary_file = os.path.join(base_dir, f"COMPREHENSIVE_FAKE_DATA_CLEANUP_{int(__import__('time').time())}.json")
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2)
    
    print(f"\nComprehensive summary saved to: {os.path.relpath(summary_file, base_dir)}")
    print(f"Removed files backed up to: removed_fake_data/")

if __name__ == '__main__':
    main()

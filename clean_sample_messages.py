#!/usr/bin/env python3
"""
Clean Sample Messages from DM Extraction Files
Removes all DM messages containing "sample" from JSON files
"""

import json
import os
import glob
from pathlib import Path
import re

def contains_fake_data(obj):
    """Check if an object contains fake/mock/demo/simulation data"""
    fake_keywords = ['sample', 'mock', 'simulation', 'demo']
    
    if isinstance(obj, dict):
        for key, value in obj.items():
            if isinstance(value, str) and any(keyword in value.lower() for keyword in fake_keywords):
                return True
            if contains_fake_data(value):
                return True
    elif isinstance(obj, list):
        for item in obj:
            if contains_fake_data(item):
                return True
    elif isinstance(obj, str):
        return any(keyword in obj.lower() for keyword in fake_keywords)
    return False

def clean_messages_from_file(file_path):
    """Clean sample messages from a single JSON file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        original_count = 0
        cleaned_count = 0
        
        if isinstance(data, dict) and 'messages' in data:
            original_messages = data['messages']
            original_count = len(original_messages)
            
            # Filter out messages with fake data (sample, mock, demo, simulation)
            clean_messages = []
            for msg in original_messages:
                if not contains_fake_data(msg):
                    clean_messages.append(msg)
            
            data['messages'] = clean_messages
            cleaned_count = len(clean_messages)
            
            # Update total count if it exists
            if 'total_messages' in data:
                data['total_messages'] = cleaned_count
            
            # Add cleaning metadata
            data['cleaning_info'] = {
                'cleaned_at': '2025-06-09',
                'original_message_count': original_count,
                'cleaned_message_count': cleaned_count,
                'fake_messages_removed': original_count - cleaned_count,
                'removed_types': ['sample', 'mock', 'demo', 'simulation']
            }
            
            # Write back to file
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            return original_count, cleaned_count
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return 0, 0
    
    return 0, 0

def main():
    """Main cleaning function"""
    base_dir = '/workspaces/sugarglitch-realops'
    
    # Find all JSON files that might contain DM extractions
    patterns = [
        '**/ultra_fast_dm_extraction_*.json',
        '**/dm_extraction_*.json',
        '**/browser_dm_extraction_*.json',
        '**/mobile_dm_extraction_*.json',
        '**/ultimate_dm_extraction_*.json',
        '**/advanced_dm_extraction_*.json',
        '**/mock_dm_extraction_*.json',
        '**/demo_extraction_*.json',
        '**/simulation_*.json',
        '**/*dm*extraction*.json',
        '**/*mock*.json',
        '**/*demo*.json',
        '**/*simulation*.json'
    ]
    
    files_to_clean = set()
    
    for pattern in patterns:
        for file_path in glob.glob(os.path.join(base_dir, pattern), recursive=True):
            files_to_clean.add(file_path)
    
    print(f"Found {len(files_to_clean)} potential DM extraction files to check")
    
    total_original = 0
    total_cleaned = 0
    files_processed = 0
    
    for file_path in sorted(files_to_clean):
        print(f"\nProcessing: {os.path.relpath(file_path, base_dir)}")
        
        original, cleaned = clean_messages_from_file(file_path)
        
        if original > 0:
            files_processed += 1
            total_original += original
            total_cleaned += cleaned
            removed = original - cleaned
            
            print(f"  Original messages: {original}")
            print(f"  Cleaned messages: {cleaned}")
            print(f"  Sample messages removed: {removed}")
        else:
            print("  No messages found or file is empty")
    
    print(f"\n{'='*50}")
    print(f"CLEANING SUMMARY:")
    print(f"Files processed: {files_processed}")
    print(f"Total original messages: {total_original}")
    print(f"Total cleaned messages: {total_cleaned}")
    print(f"Total sample messages removed: {total_original - total_cleaned}")
    
    # Create a cleaned data summary file
    summary = {
        "cleaning_date": "2025-01-17",
        "files_processed": files_processed,
        "total_original_messages": total_original,
        "total_cleaned_messages": total_cleaned,
        "sample_messages_removed": total_original - total_cleaned,
        "cleaned_files": [os.path.relpath(f, base_dir) for f in sorted(files_to_clean) if os.path.exists(f)]
    }
    
    summary_file = os.path.join(base_dir, f"SAMPLE_CLEANUP_SUMMARY_{int(__import__('time').time())}.json")
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2)
    
    print(f"Summary saved to: {os.path.relpath(summary_file, base_dir)}")

if __name__ == '__main__':
    main()

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
import asyncio
import aiohttp
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

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

async def fetch(session, url):
    try:
        async with session.get(url) as response:
            response.raise_for_status()
            logging.info(f"✅ Success: {url}")
            return await response.json()
    except Exception as e:
        logging.error(f"❌ Error fetching {url}: {e}")
        return None

async def batch_iter(data, batch_size):
    """Split list into batches to reduce memory load"""
    for i in range(0, len(data), batch_size):
        yield data[i:i + batch_size]

async def main():
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
    
    logging.info(f"Found {len(files_to_clean)} potential DM extraction files to check")
    
    total_original = 0
    total_cleaned = 0
    files_processed = 0
    
    async with aiohttp.ClientSession() as session:
        for file_path in sorted(files_to_clean):
            logging.info(f"\nProcessing: {os.path.relpath(file_path, base_dir)}")
            
            original, cleaned = clean_messages_from_file(file_path)
            
            if original > 0:
                files_processed += 1
                total_original += original
                total_cleaned += cleaned
                removed = original - cleaned
                
                logging.info(f"  Original messages: {original}")
                logging.info(f"  Cleaned messages: {cleaned}")
                logging.info(f"  Sample messages removed: {removed}")
            else:
                logging.info("  No messages found or file is empty")
    
    logging.info(f"\n{'='*50}")
    logging.info(f"CLEANING SUMMARY:")
    logging.info(f"Files processed: {files_processed}")
    logging.info(f"Total original messages: {total_original}")
    logging.info(f"Total cleaned messages: {total_cleaned}")
    logging.info(f"Total fake messages removed: {total_original - total_cleaned}")
    logging.info(f"Removed types: sample, mock, demo, simulation")
    
    # Create a cleaned data summary file
    summary = {
        "cleaning_date": "2025-06-09",
        "files_processed": files_processed,
        "total_original_messages": total_original,
        "total_cleaned_messages": total_cleaned,
        "fake_messages_removed": total_original - total_cleaned,
        "removed_types": ["sample", "mock", "demo", "simulation"],
        "cleaned_files": [os.path.relpath(f, base_dir) for f in sorted(files_to_clean) if os.path.exists(f)]
    }
    
    summary_file = os.path.join(base_dir, f"FAKE_DATA_CLEANUP_SUMMARY_{int(__import__('time').time())}.json")
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2)
    
    logging.info(f"Summary saved to: {os.path.relpath(summary_file, base_dir)}")

if __name__ == '__main__':
    asyncio.run(main())

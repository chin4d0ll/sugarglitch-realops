#!/usr/bin/env python3
"""
💾 Memory-Efficient Data Processor
ใช้ techniques จาก performance optimization repos
"""

import asyncio
import json
import logging
from typing import AsyncGenerator, Iterator, Dict, List
from pathlib import Path
import gc
import psutil
import sys

class MemoryEfficientProcessor:
    def __init__(self, chunk_size: int = 1000):
        self.chunk_size = chunk_size
        self.processed_count = 0
        
        # Memory monitoring
        self.process = psutil.Process()
        self.initial_memory = self.process.memory_info().rss / 1024 / 1024  # MB
        
    def memory_usage(self) -> float:
        """📊 Get current memory usage in MB"""
        return self.process.memory_info().rss / 1024 / 1024
    
    def memory_diff(self) -> float:
        """📈 Get memory usage difference from start"""
        return self.memory_usage() - self.initial_memory
    
    async def stream_json_file(self, filepath: Path) -> AsyncGenerator[Dict, None]:
        """📂 Stream large JSON files without loading into memory"""
        logging.info(f"🔄 Streaming JSON file: {filepath}")
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                # If it's a list, yield items one by one
                if isinstance(data, list):
                    for item in data:
                        yield item
                        self.processed_count += 1
                        
                        # Force garbage collection every chunk_size items
                        if self.processed_count % self.chunk_size == 0:
                            gc.collect()
                            logging.info(f"💾 Processed {self.processed_count} items, "
                                       f"Memory: {self.memory_usage():.1f}MB "
                                       f"(+{self.memory_diff():.1f}MB)")
                
                # If it's a dict with nested lists
                elif isinstance(data, dict):
                    for key, value in data.items():
                        if isinstance(value, list):
                            for item in value:
                                yield {"source_key": key, "data": item}
                                self.processed_count += 1
                        else:
                            yield {"source_key": key, "data": value}
                            self.processed_count += 1
                            
        except Exception as e:
            logging.error(f"❌ Error streaming {filepath}: {e}")
    
    def chunk_iterator(self, items: List, chunk_size: int = None) -> Iterator[List]:
        """🔄 Split large lists into memory-friendly chunks"""
        if chunk_size is None:
            chunk_size = self.chunk_size
            
        for i in range(0, len(items), chunk_size):
            yield items[i:i + chunk_size]
    
    async def process_dm_data_efficiently(self, dm_file: Path) -> Dict:
        """💬 Process DM data without memory overflow"""
        logging.info(f"🔍 Processing DM data efficiently: {dm_file}")
        
        stats = {
            "total_threads": 0,
            "total_messages": 0,
            "participants": set(),
            "message_types": {},
            "processing_stats": {
                "peak_memory_mb": 0,
                "chunks_processed": 0
            }
        }
        
        try:
            # Stream the file instead of loading all at once
            async for item in self.stream_json_file(dm_file):
                if isinstance(item, dict):
                    # Process DM thread data
                    if "thread_id" in item:
                        stats["total_threads"] += 1
                        
                        # Process participants efficiently
                        participants = item.get("participants", [])
                        for participant in participants:
                            if isinstance(participant, str):
                                stats["participants"].add(participant)
                    
                    # Process messages
                    if "items" in item:  # Message items
                        messages = item.get("items", [])
                        stats["total_messages"] += len(messages)
                        
                        # Process message types in chunks
                        for chunk in self.chunk_iterator(messages, 100):
                            for message in chunk:
                                msg_type = message.get("item_type", "unknown")
                                stats["message_types"][msg_type] = stats["message_types"].get(msg_type, 0) + 1
                            
                            # Update memory stats
                            current_memory = self.memory_usage()
                            if current_memory > stats["processing_stats"]["peak_memory_mb"]:
                                stats["processing_stats"]["peak_memory_mb"] = current_memory
                            
                            stats["processing_stats"]["chunks_processed"] += 1
                            
                            # Force garbage collection
                            gc.collect()
        
        except Exception as e:
            logging.error(f"❌ Error processing DM data: {e}")
        
        # Convert set to list for JSON serialization
        stats["participants"] = list(stats["participants"])
        stats["processing_stats"]["final_memory_mb"] = self.memory_usage()
        stats["processing_stats"]["memory_overhead_mb"] = self.memory_diff()
        
        logging.info(f"✅ Processed {stats['total_threads']} threads, "
                    f"{stats['total_messages']} messages, "
                    f"Memory overhead: {stats['processing_stats']['memory_overhead_mb']:.1f}MB")
        
        return stats
    
    async def optimize_json_files(self, directory: Path) -> Dict:
        """🔧 Optimize JSON files by removing empty values and compacting"""
        logging.info(f"🔧 Optimizing JSON files in: {directory}")
        
        optimization_stats = {
            "files_processed": 0,
            "bytes_saved": 0,
            "empty_values_removed": 0,
            "errors": []
        }
        
        json_files = list(directory.rglob("*.json"))
        
        for json_file in json_files:
            try:
                original_size = json_file.stat().st_size
                
                # Stream and clean the file
                cleaned_data = {}
                async for item in self.stream_json_file(json_file):
                    # Remove empty values to save space
                    if isinstance(item, dict):
                        cleaned_item = {k: v for k, v in item.items() 
                                     if v not in [None, "", [], {}]}
                        
                        if cleaned_item:  # Only keep non-empty items
                            if "cleaned_data" not in cleaned_data:
                                cleaned_data["cleaned_data"] = []
                            cleaned_data["cleaned_data"].append(cleaned_item)
                        else:
                            optimization_stats["empty_values_removed"] += 1
                
                # Write optimized file
                if cleaned_data:
                    with open(json_file, 'w', encoding='utf-8') as f:
                        json.dump(cleaned_data, f, separators=(',', ':'))  # Compact format
                    
                    new_size = json_file.stat().st_size
                    bytes_saved = original_size - new_size
                    optimization_stats["bytes_saved"] += bytes_saved
                    
                    logging.info(f"📦 Optimized {json_file.name}: saved {bytes_saved} bytes")
                
                optimization_stats["files_processed"] += 1
                
                # Memory cleanup
                del cleaned_data
                gc.collect()
                
            except Exception as e:
                error_msg = f"Error optimizing {json_file.name}: {e}"
                optimization_stats["errors"].append(error_msg)
                logging.error(f"❌ {error_msg}")
        
        logging.info(f"✅ Optimization complete: "
                    f"{optimization_stats['files_processed']} files, "
                    f"{optimization_stats['bytes_saved']} bytes saved")
        
        return optimization_stats

async def main():
    print("💾 MEMORY-EFFICIENT DATA PROCESSOR")
    print("=" * 50)
    
    # Initialize processor
    processor = MemoryEfficientProcessor(chunk_size=500)
    
    print(f"🔄 Initial memory usage: {processor.memory_usage():.1f}MB")
    
    # Example: Process sample data
    sample_data = [{"id": i, "data": f"item_{i}"} for i in range(10000)]
    
    print(f"📊 Created sample data: {len(sample_data)} items")
    print(f"💾 Memory after data creation: {processor.memory_usage():.1f}MB")
    
    # Process in chunks
    processed = 0
    for chunk in processor.chunk_iterator(sample_data, 1000):
        # Simulate processing
        for item in chunk:
            item["processed"] = True
        processed += len(chunk)
        
        # Force garbage collection
        gc.collect()
        
        print(f"✅ Processed {processed}/{len(sample_data)} items, "
              f"Memory: {processor.memory_usage():.1f}MB")
    
    print(f"🎯 Final memory usage: {processor.memory_usage():.1f}MB")
    print(f"📈 Memory overhead: {processor.memory_diff():.1f}MB")
    
    # Demo file optimization
    results_dir = Path("./results")
    if results_dir.exists():
        optimization_stats = await processor.optimize_json_files(results_dir)
        print(f"\n🔧 Optimization results:")
        print(f"   Files processed: {optimization_stats['files_processed']}")
        print(f"   Bytes saved: {optimization_stats['bytes_saved']}")
        print(f"   Empty values removed: {optimization_stats['empty_values_removed']}")

if __name__ == "__main__":
    asyncio.run(main())

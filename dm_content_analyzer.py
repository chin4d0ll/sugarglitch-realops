#!/usr/bin/env python3
"""
DM Content Analyzer
Analyzes all extraction results to find and extract actual DM message content
"""

import os
import sys
import json
import re
import logging
import time
from datetime import datetime
from typing import Dict, List, Any, Set, Tuple
import glob
from collections import defaultdict

class DMContentAnalyzer:
    def __init__(self):
        self.setup_logging()
        self.timestamp = str(int(time.time()))
        
        # Directories to search for extraction results
        self.search_dirs = [
            "results",
            ".",  # Root directory
            "logs",
            "config"
        ]
        
        # File patterns to search
        self.file_patterns = [
            "*.json",
            "*dm*.json",
            "*extraction*.json",
            "*report*.json",
            "*messages*.json",
            "*conversation*.json",
            "*thread*.json",
            "*chat*.json"
        ]
        
        # Patterns that indicate actual message content
        self.message_indicators = [
            'text', 'message', 'content', 'body', 'msg',
            'item_text', 'message_text', 'text_content',
            'chat_message', 'dm_text', 'conversation_text'
        ]
        
        # Patterns to exclude (not real messages)
        self.exclude_patterns = [
            r'^https?://',  # URLs
            r'^\d+$',  # Just numbers
            r'^[A-Z_]+$',  # All caps constants
            r'instagram\.com',
            r'facebook\.com',
            r'thread_id',
            r'user_id',
            r'session_id',
            r'api_key',
            r'token',
            r'timestamp',
            r'created_at',
            r'updated_at',
            r'profile_pic',
            r'^\d{4}-\d{2}-\d{2}',  # Dates
            r'^\d{1,2}:\d{2}',  # Times
            r'application/json',
            r'text/html',
            r'utf-8',
            r'gzip',
            r'deflate'
        ]
        
        self.logger.info("🔍 DM Content Analyzer Initialized")

    def setup_logging(self):
        """Setup logging"""
        log_dir = "logs"
        os.makedirs(log_dir, exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(f'{log_dir}/dm_content_analysis_{int(time.time())}.log'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)

    def find_extraction_files(self) -> List[str]:
        """Find all extraction result files"""
        files = []
        
        for search_dir in self.search_dirs:
            if not os.path.exists(search_dir):
                continue
                
            self.logger.info(f"🔍 Searching directory: {search_dir}")
            
            for pattern in self.file_patterns:
                pattern_path = os.path.join(search_dir, "**", pattern)
                matching_files = glob.glob(pattern_path, recursive=True)
                files.extend(matching_files)
        
        # Remove duplicates and sort
        files = sorted(list(set(files)))
        
        self.logger.info(f"📁 Found {len(files)} files to analyze")
        return files

    def load_and_parse_file(self, file_path: str) -> Dict[str, Any]:
        """Load and parse a JSON file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data
        except json.JSONDecodeError:
            # Try to load as text and look for JSON within it
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Look for JSON patterns in text
                json_patterns = [
                    r'\{.*?\}',
                    r'\[.*?\]'
                ]
                
                for pattern in json_patterns:
                    matches = re.findall(pattern, content, re.DOTALL)
                    for match in matches:
                        try:
                            return json.loads(match)
                        except:
                            continue
                
                return {'raw_content': content}
            except:
                return {}
        except Exception as e:
            self.logger.debug(f"Error loading {file_path}: {str(e)}")
            return {}

    def extract_text_content(self, data: Any, path: str = "") -> List[Tuple[str, str]]:
        """Recursively extract text content from data structure"""
        text_content = []
        
        try:
            if isinstance(data, dict):
                for key, value in data.items():
                    current_path = f"{path}.{key}" if path else key
                    
                    # Check if this key indicates message content
                    if any(indicator in key.lower() for indicator in self.message_indicators):
                        if isinstance(value, str) and self.is_likely_message(value):
                            text_content.append((current_path, value.strip()))
                    
                    # Recursively process nested data
                    if isinstance(value, (dict, list)):
                        nested_content = self.extract_text_content(value, current_path)
                        text_content.extend(nested_content)
                    elif isinstance(value, str) and len(value) > 10:
                        # Check if any string value looks like a message
                        if self.is_likely_message(value):
                            text_content.append((current_path, value.strip()))
            
            elif isinstance(data, list):
                for i, item in enumerate(data):
                    current_path = f"{path}[{i}]" if path else f"[{i}]"
                    nested_content = self.extract_text_content(item, current_path)
                    text_content.extend(nested_content)
            
            elif isinstance(data, str) and len(data) > 10:
                if self.is_likely_message(data):
                    text_content.append((path, data.strip()))
        
        except Exception as e:
            self.logger.debug(f"Error extracting text content: {str(e)}")
        
        return text_content

    def is_likely_message(self, text: str) -> bool:
        """Determine if text is likely a real message"""
        if not text or len(text.strip()) < 3:
            return False
        
        text_lower = text.lower().strip()
        
        # Check exclude patterns
        for pattern in self.exclude_patterns:
            if re.search(pattern, text_lower):
                return False
        
        # Check for common non-message content
        non_message_indicators = [
            'application/', 'text/', 'image/', 'video/',
            'http://', 'https://',
            'www.instagram.com', 'instagram.com',
            'api.instagram.com',
            '<!doctype', '<html', '<head', '<body',
            'window.', 'document.',
            'function(', 'var ', 'const ', 'let ',
            '{"', '"}', '[{', '}]',
            'null', 'true', 'false',
            'undefined', 'object',
            'array', 'string', 'number',
            'sessionid=', 'csrftoken=',
            'user-agent:', 'content-type:',
            'accept:', 'authorization:',
            'x-ig-', 'x-csrf-', 'x-asbd-'
        ]
        
        for indicator in non_message_indicators:
            if indicator in text_lower:
                return False
        
        # Must contain some letters
        if not re.search(r'[a-zA-Z]', text):
            return False
        
        # Should be reasonable message length
        if len(text) > 2000:  # Very long text is probably not a message
            return False
        
        # Check if it looks like natural language
        word_count = len(text.split())
        if word_count >= 2:  # At least 2 words
            return True
        
        # Single word messages are possible but should be meaningful
        if word_count == 1 and len(text) >= 3:
            # Exclude single technical terms
            technical_terms = [
                'json', 'html', 'xml', 'css', 'javascript',
                'api', 'url', 'uri', 'http', 'https',
                'get', 'post', 'put', 'delete',
                'true', 'false', 'null', 'undefined'
            ]
            if text_lower not in technical_terms:
                return True
        
        return False

    def analyze_file(self, file_path: str) -> Dict[str, Any]:
        """Analyze a single file for DM content"""
        self.logger.info(f"📄 Analyzing: {os.path.basename(file_path)}")
        
        analysis_result = {
            'file_path': file_path,
            'file_name': os.path.basename(file_path),
            'file_size': 0,
            'load_success': False,
            'message_content': [],
            'potential_messages': 0,
            'analysis_timestamp': datetime.now().isoformat()
        }
        
        try:
            # Get file size
            analysis_result['file_size'] = os.path.getsize(file_path)
            
            # Load file data
            data = self.load_and_parse_file(file_path)
            
            if data:
                analysis_result['load_success'] = True
                
                # Extract text content
                text_content = self.extract_text_content(data)
                
                # Process and deduplicate content
                seen_messages = set()
                unique_messages = []
                
                for path, text in text_content:
                    if text not in seen_messages:
                        seen_messages.add(text)
                        unique_messages.append({
                            'path': path,
                            'text': text,
                            'length': len(text),
                            'word_count': len(text.split())
                        })
                
                analysis_result['message_content'] = unique_messages
                analysis_result['potential_messages'] = len(unique_messages)
                
                if unique_messages:
                    self.logger.info(f"✅ Found {len(unique_messages)} potential messages in {os.path.basename(file_path)}")
                    
                    # Show sample messages
                    for i, msg in enumerate(unique_messages[:3]):
                        preview = msg['text'][:100] + ('...' if len(msg['text']) > 100 else '')
                        self.logger.info(f"   📝 Sample {i+1}: {preview}")
            
        except Exception as e:
            self.logger.error(f"❌ Error analyzing {file_path}: {str(e)}")
        
        return analysis_result

    def run_comprehensive_analysis(self) -> Dict[str, Any]:
        """Run comprehensive analysis of all extraction files"""
        self.logger.info("🚀 Starting Comprehensive DM Content Analysis")
        
        # Find all extraction files
        files = self.find_extraction_files()
        
        if not files:
            self.logger.warning("⚠️ No extraction files found")
            return {'success': False, 'files_analyzed': 0, 'total_messages': 0}
        
        all_results = []
        total_messages = 0
        successful_files = 0
        
        # Analyze each file
        for file_path in files:
            result = self.analyze_file(file_path)
            all_results.append(result)
            
            if result['load_success']:
                successful_files += 1
                total_messages += result['potential_messages']
        
        # Create comprehensive summary
        summary = {
            'analysis_timestamp': datetime.now().isoformat(),
            'total_files_found': len(files),
            'files_successfully_analyzed': successful_files,
            'files_with_potential_messages': len([r for r in all_results if r['potential_messages'] > 0]),
            'total_potential_messages': total_messages,
            'file_analyses': all_results,
            'success': total_messages > 0
        }
        
        # Save detailed results
        self.save_analysis_results(summary)
        
        # Print summary
        self.print_analysis_summary(summary)
        
        return summary

    def save_analysis_results(self, summary: Dict[str, Any]):
        """Save analysis results"""
        try:
            results_dir = "results/dm_content_analysis"
            os.makedirs(results_dir, exist_ok=True)
            
            # Save comprehensive summary
            summary_file = f"{results_dir}/dm_content_analysis_{self.timestamp}.json"
            with open(summary_file, 'w', encoding='utf-8') as f:
                json.dump(summary, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"💾 Analysis results saved: {summary_file}")
            
            # Save extracted messages separately
            all_messages = []
            for file_analysis in summary['file_analyses']:
                for msg in file_analysis.get('message_content', []):
                    all_messages.append({
                        'source_file': file_analysis['file_name'],
                        'text': msg['text'],
                        'path': msg['path'],
                        'length': msg['length'],
                        'word_count': msg['word_count']
                    })
            
            if all_messages:
                messages_file = f"{results_dir}/extracted_messages_{self.timestamp}.json"
                with open(messages_file, 'w', encoding='utf-8') as f:
                    json.dump(all_messages, f, indent=2, ensure_ascii=False)
                
                self.logger.info(f"💾 Extracted messages saved: {messages_file}")
                
                # Also save as readable text
                text_file = f"{results_dir}/extracted_messages_{self.timestamp}.txt"
                with open(text_file, 'w', encoding='utf-8') as f:
                    f.write("EXTRACTED DM MESSAGES\n")
                    f.write("=" * 50 + "\n\n")
                    
                    for i, msg in enumerate(all_messages, 1):
                        f.write(f"Message {i}:\n")
                        f.write(f"Source: {msg['source_file']}\n")
                        f.write(f"Path: {msg['path']}\n")
                        f.write(f"Text: {msg['text']}\n")
                        f.write("-" * 30 + "\n\n")
                
                self.logger.info(f"💾 Readable messages saved: {text_file}")
            
        except Exception as e:
            self.logger.error(f"❌ Error saving analysis results: {str(e)}")

    def print_analysis_summary(self, summary: Dict[str, Any]):
        """Print analysis summary"""
        print("\n" + "="*70)
        print("🔍 DM CONTENT ANALYSIS SUMMARY")
        print("="*70)
        
        print(f"📁 Total Files Found: {summary['total_files_found']}")
        print(f"✅ Files Successfully Analyzed: {summary['files_successfully_analyzed']}")
        print(f"📨 Files with Potential Messages: {summary['files_with_potential_messages']}")
        print(f"💬 Total Potential Messages: {summary['total_potential_messages']}")
        
        if summary['total_potential_messages'] > 0:
            print(f"\n🎉 SUCCESS: Found {summary['total_potential_messages']} potential DM messages!")
            print("\nTop Files with Messages:")
            
            # Sort files by message count
            files_with_messages = [
                f for f in summary['file_analyses'] 
                if f['potential_messages'] > 0
            ]
            files_with_messages.sort(key=lambda x: x['potential_messages'], reverse=True)
            
            for i, file_info in enumerate(files_with_messages[:10], 1):
                print(f"{i:2d}. {file_info['file_name']}: {file_info['potential_messages']} messages")
            
            print("\nSample Messages Found:")
            message_count = 0
            for file_info in files_with_messages:
                for msg in file_info.get('message_content', []):
                    if message_count >= 10:  # Show max 10 samples
                        break
                    message_count += 1
                    preview = msg['text'][:100] + ('...' if len(msg['text']) > 100 else '')
                    print(f"{message_count:2d}. {preview}")
                if message_count >= 10:
                    break
            
        else:
            print("\n❌ No potential DM messages found in any files")
            print("\nThis could mean:")
            print("- Sessions are expired and no real DM data was extracted")
            print("- DM data is in a different format than expected")
            print("- Files contain only metadata/configuration data")
            print("- Real message content is encrypted or encoded")
        
        print("="*70)

def main():
    """Main execution function"""
    print("🔍 DM Content Analyzer")
    print("="*60)
    
    analyzer = DMContentAnalyzer()
    
    try:
        summary = analyzer.run_comprehensive_analysis()
        
        if summary['success']:
            print(f"\n✅ Analysis completed successfully!")
            print(f"Found {summary['total_potential_messages']} potential DM messages across {summary['files_with_potential_messages']} files")
        else:
            print(f"\n⚠️ Analysis completed but no DM messages found")
            print("Check the detailed analysis results for more information")
            
    except Exception as e:
        print(f"❌ Analysis failed: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

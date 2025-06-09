# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
Comprehensive DM Extraction Analysis 2025
=========================================
Analyzes all extraction attempts and creates a final comprehensive report.
"""

import json
import os
import glob
from datetime import datetime
from pathlib import Path

class DMExtractionAnalyzer:
    def __init__(self):
        self.results_dir = Path('/workspaces/sugarglitch-realops/results')
        self.all_extractions = []
        self.all_messages = []
        self.analysis = {}

    def find_all_extraction_files(self):
        """Find all extraction result files"""
        extraction_files = []

        # Search in results directory
        if self.results_dir.exists():
            for file_path in self.results_dir.rglob('*.json'):
                extraction_files.append(file_path)

        # Search in root directory for extraction files
        root_files = glob.glob('/workspaces/sugarglitch-realops/*extraction*.json')
        root_files.extend(glob.glob('/workspaces/sugarglitch-realops/*dm*.json'))
        root_files.extend(glob.glob('/workspaces/sugarglitch-realops/*trading*.json'))
        root_files.extend(glob.glob('/workspaces/sugarglitch-realops/*report*.json'))

        for file_path in root_files:
            extraction_files.append(Path(file_path))

        return sorted(list(set(extraction_files)))  # Remove duplicates and sort

    def analyze_extraction_file(self, file_path):
        """Analyze a single extraction file"""
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)

            extraction_info = {
                'file_path': str(file_path),
                'file_name': file_path.name,
                'file_size': file_path.stat().st_size,
                'modified_time': datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
                'extraction_method': data.get('extraction_method', 'unknown'),
                'total_messages': 0,
                'messages': [],
                'has_real_content': False,
                'analysis': {}
            }

            # Extract messages from various formats
            messages = []
            if 'extracted_messages' in data:
                messages = data['extracted_messages']
            elif 'messages' in data:
                messages = data['messages']
            elif 'dm_content' in data:
                messages = data['dm_content']
            elif 'results' in data and isinstance(data['results'], list):
                messages = data['results']

            extraction_info['total_messages'] = len(messages)
            extraction_info['messages'] = messages

            # Analyze message content
            real_messages = []
            metadata_messages = []

            for msg in messages:
                text = ''
                if isinstance(msg, dict):
                    text = msg.get('text', msg.get('message', msg.get('content', '')))
                elif isinstance(msg, str):
                    text = msg

                if text and len(text.strip()) > 1:
                    if self.is_likely_real_message(text):
                        real_messages.append({
                            'text': text,
                            'source': msg.get('source', 'unknown') if isinstance(msg, dict) else 'direct'
                        })
                    else:
                        metadata_messages.append({
                            'text': text,
                            'source': msg.get('source', 'unknown') if isinstance(msg, dict) else 'direct'
                        })

            extraction_info['has_real_content'] = len(real_messages) > 0
            extraction_info['analysis'] = {
                'real_messages': real_messages,
                'metadata_messages': metadata_messages,
                'real_count': len(real_messages),
                'metadata_count': len(metadata_messages)
            }

            return extraction_info

        except Exception as e:
            return {
                'file_path': str(file_path),
                'file_name': file_path.name,
                'error': str(e),
                'total_messages': 0,
                'has_real_content': False
            }

    def is_likely_real_message(self, text):
        """Determine if text is likely a real DM message"""
        if not text or len(text) < 2:
            return False

        text_lower = text.lower().strip()

        # Obvious metadata/technical patterns
        metadata_indicators = [
            'null', 'undefined', 'true', 'false', '{}', '[]',
            'application/json', 'text/html', 'content-type',
            'csrf_token', 'session_id', 'user_id', 'device_id',
            'instagram.com', 'facebook.com', 'api.instagram',
            'bearer ', 'oauth ', 'token ', 'authorization',
            '{"', '[{', '}]', '{"error"', '"status"',
            'http/1.1', 'content-type', 'user-agent',
            'window.', 'document.', 'function(', 'var ',
            'const ', 'let ', 'return ', 'typeof ',
            '</div>', '<span>', '<p>', '<html>', '<!doctype',
            'undefined_0_', '_js_', '__typename', '__',
            'error_code', 'status_code', 'response_code',
            'graphql', 'mutation', 'subscription', 'query',
            'x-ig-', 'x-fb-', 'x-pigeon-', 'x-bloks-',
            'multipart/form-data', 'boundary=',
            'pk_', 'item_id', 'thread_id', 'media_id'
        ]

        for indicator in metadata_indicators:
            if indicator in text_lower:
                return False

        # JSON-like structures
        if (text.startswith('{') and text.endswith('}')) or \
           (text.startswith('[') and text.endswith(']')):
            return False

        # Very short or very long unlikely to be real messages
        if len(text) < 3 or len(text) > 2000:
            return False

        # Real message characteristics
        has_spaces = ' ' in text
        has_letters = any(c.isalpha() for c in text)
        reasonable_length = 3 <= len(text) <= 500

        return has_spaces and has_letters and reasonable_length

    def generate_comprehensive_analysis(self):
        """Generate comprehensive analysis of all extractions"""
        extraction_files = self.find_all_extraction_files()

        print(f"🔍 Found {len(extraction_files)} extraction files to analyze...")

        all_real_messages = []
        all_metadata = []
        method_stats = {}

        for file_path in extraction_files:
            print(f"📁 Analyzing: {file_path.name}")
            extraction_info = self.analyze_extraction_file(file_path)
            self.all_extractions.append(extraction_info)

            if extraction_info.get('analysis'):
                real_msgs = extraction_info['analysis']['real_messages']
                meta_msgs = extraction_info['analysis']['metadata_messages']

                all_real_messages.extend(real_msgs)
                all_metadata.extend(meta_msgs)

                method = extraction_info.get('extraction_method', 'unknown')
                if method not in method_stats:
                    method_stats[method] = {'files': 0, 'real_messages': 0, 'metadata': 0}

                method_stats[method]['files'] += 1
                method_stats[method]['real_messages'] += len(real_msgs)
                method_stats[method]['metadata'] += len(meta_msgs)

        # Remove duplicate messages
        unique_real_messages = []
        seen_texts = set()
        for msg in all_real_messages:
            if msg['text'] not in seen_texts:
                unique_real_messages.append(msg)
                seen_texts.add(msg['text'])

        self.analysis = {
            'total_extraction_files': len(extraction_files),
            'total_raw_messages': len(all_real_messages) + len(all_metadata),
            'total_real_messages': len(all_real_messages),
            'unique_real_messages': len(unique_real_messages),
            'total_metadata_entries': len(all_metadata),
            'method_statistics': method_stats,
            'real_messages': unique_real_messages,
            'extraction_files': [e for e in self.all_extractions if e.get('total_messages', 0) > 0]
        }

        return self.analysis

    def display_results(self):
        """Display analysis results"""
        print("\n" + "="*80)
        print("🎯 COMPREHENSIVE INSTAGRAM DM EXTRACTION ANALYSIS")
        print("="*80)

        analysis = self.analysis

        print(f"📊 OVERALL STATISTICS:")
        print(f"   📁 Total extraction files: {analysis['total_extraction_files']}")
        print(f"   📝 Total raw messages found: {analysis['total_raw_messages']}")
        print(f"   💬 Real DM messages: {analysis['total_real_messages']}")
        print(f"   🔤 Unique real messages: {analysis['unique_real_messages']}")
        print(f"   📋 Metadata entries: {analysis['total_metadata_entries']}")

        print(f"\n🔧 EXTRACTION METHOD BREAKDOWN:")
        for method, stats in analysis['method_statistics'].items():
            print(f"   {method}: {stats['files']} files, {stats['real_messages']} real messages, {stats['metadata']} metadata")

        print(f"\n💬 REAL DM CONTENT FOUND:")
        if analysis['unique_real_messages']:
            print(f"   ✅ SUCCESS! Found {len(analysis['unique_real_messages'])} unique real messages:")
            for i, msg in enumerate(analysis['unique_real_messages'][:10]):  # Show first 10
                print(f"   {i+1}. [{msg['source']}] {msg['text'][:80]}...")
            if len(analysis['unique_real_messages']) > 10:
                print(f"   ... and {len(analysis['unique_real_messages']) - 10} more messages")
        else:
            print("   ❌ NO REAL DM CONTENT FOUND")
            print("   📋 All extracted data appears to be metadata/configuration")

        print(f"\n📁 EXTRACTION FILES WITH CONTENT:")
        for extraction in analysis['extraction_files'][:10]:  # Show first 10
            real_count = extraction.get('analysis', {}).get('real_count', 0)
            meta_count = extraction.get('analysis', {}).get('metadata_count', 0)
            status = "✅ REAL CONTENT" if real_count > 0 else "📋 METADATA ONLY"
            print(f"   {status} - {extraction['file_name']} ({real_count} real, {meta_count} metadata)")

        print("="*80)

    def save_final_report(self):
        """Save final comprehensive report"""
        timestamp = int(datetime.now().timestamp())
        report_file = f'/workspaces/sugarglitch-realops/FINAL_DM_EXTRACTION_ANALYSIS_{timestamp}.json'

        final_report = {
            'analysis_timestamp': timestamp,
            'analysis_date': datetime.now().isoformat(),
            'comprehensive_analysis': self.analysis,
            'all_extractions': self.all_extractions,
            'final_verdict': {
                'real_dm_content_found': self.analysis['unique_real_messages'] > 0,
                'total_unique_real_messages': self.analysis['unique_real_messages'],
                'extraction_success': 'SUCCESS' if self.analysis['unique_real_messages'] > 0 else 'METADATA_ONLY',
                'recommendation': 'Real DM content extracted successfully' if self.analysis['unique_real_messages'] > 0
                                else 'Only metadata/config data extracted - need fresh sessions or different approach'
            }
        }

        with open(report_file, 'w') as f:
            json.dump(final_report, f, indent = 2)

        print(f"\n📊 Final analysis saved to: {report_file}")
        return report_file

def main():
    """Main function"""
    analyzer = DMExtractionAnalyzer()

    print("🚀 Starting comprehensive DM extraction analysis...")
    analysis = analyzer.generate_comprehensive_analysis()
    analyzer.display_results()
    report_file = analyzer.save_final_report()

    print(f"\n🎉 Analysis complete! Report saved to: {report_file}")

if __name__ == "__main__":
    main()

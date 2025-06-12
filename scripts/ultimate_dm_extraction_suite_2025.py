# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
Ultimate Instagram DM Extraction Suite 2025
===========================================
Combines browser automation, WebSocket interception, mobile API emulation,
and advanced bypass techniques for comprehensive DM content extraction.
"""

import asyncio
import subprocess
import json
import time
import logging
from datetime import datetime
from pathlib import Path
import concurrent.futures

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/workspaces/sugarglitch-realops/logs/ultimate_dm_extraction.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class UltimateDMExtractionSuite:
    def __init__(self):
        self.results = {}
        self.start_time = time.time()

    def run_script(self, script_path, script_name):
        """Run a single extraction script"""
        try:
            logger.info(f"Starting {script_name}...")

            if script_name == "Browser Automation":
                # Run browser script (async)
                result = subprocess.run(
                    ['python3', script_path],
                    capture_output=True,
                    text=True,
                    timeout=300,  # 5 minutes timeout
                    cwd='/workspaces/sugarglitch-realops'
                )
            elif script_name == "WebSocket Interceptor":
                # Run WebSocket script (async)
                result = subprocess.run(
                    ['python3', script_path],
                    capture_output=True,
                    text=True,
                    timeout=120,  # 2 minutes timeout
                    cwd='/workspaces/sugarglitch-realops'
                )
            else:
                # Run other scripts (sync)
                result = subprocess.run(
                    ['python3', script_path],
                    capture_output=True,
                    text=True,
                    timeout=180,  # 3 minutes timeout
                    cwd='/workspaces/sugarglitch-realops'
                )

            if result.returncode == 0:
                logger.info(f"✅ {script_name} completed successfully")
                self.results[script_name] = {
                    'status': 'success',
                    'output': result.stdout,
                    'error': result.stderr
                }
            else:
                logger.warning(f"⚠️ {script_name} completed with warnings")
                self.results[script_name] = {
                    'status': 'warning',
                    'output': result.stdout,
                    'error': result.stderr
                }

        except subprocess.TimeoutExpired:
            logger.error(f"❌ {script_name} timed out")
            self.results[script_name] = {
                'status': 'timeout',
                'output': '',
                'error': 'Script execution timed out'
            }
        except Exception as e:
            logger.error(f"❌ {script_name} failed: {e}")
            self.results[script_name] = {
                'status': 'error',
                'output': '',
                'error': str(e)
            }

    def collect_all_results(self):
        """Collect results from all extraction methods"""
        results_dir = Path('/workspaces/sugarglitch-realops/results')
        all_messages = []
        result_files = []

        if results_dir.exists():
            # Find recent result files
            for file_path in results_dir.rglob('*.json'):
                if file_path.stat().st_mtime > self.start_time - 3600:  # Files from last hour
                    try:
                        with open(file_path, 'r') as f:
                            data = json.load(f)

                        result_files.append({
                            'file': str(file_path),
                            'method': data.get('extraction_method', 'unknown'),
                            'message_count': data.get('total_messages', 0),
                            'timestamp': data.get('timestamp', 0)
                        })

                        # Extract messages
                        if 'extracted_messages' in data:
                            for msg in data['extracted_messages']:
                                msg['extraction_file'] = str(file_path)
                                all_messages.append(msg)
                        elif 'messages' in data:
                            for msg in data['messages']:
                                msg['extraction_file'] = str(file_path)
                                all_messages.append(msg)

                    except Exception as e:
                        logger.debug(f"Error reading {file_path}: {e}")

        return all_messages, result_files

    def analyze_extraction_results(self, all_messages):
        """Analyze and categorize extraction results"""
        analysis = {
            'total_messages': len(all_messages),
            'by_method': {},
            'unique_texts': set(),
            'potential_real_messages': [],
            'metadata_entries': [],
            'analysis_summary': {}
        }

        for msg in all_messages:
            method = msg.get('source', 'unknown')
            if method not in analysis['by_method']:
                analysis['by_method'][method] = 0
            analysis['by_method'][method] += 1

            text = msg.get('text', '')
            if text:
                analysis['unique_texts'].add(text)

                # Categorize message type
                if self.is_likely_real_message(text):
                    analysis['potential_real_messages'].append(msg)
                else:
                    analysis['metadata_entries'].append(msg)

        # Convert set to list for JSON serialization
        analysis['unique_texts'] = list(analysis['unique_texts'])

        # Generate summary
        analysis['analysis_summary'] = {
            'total_extractions': len(all_messages),
            'unique_text_count': len(analysis['unique_texts']),
            'potential_real_messages': len(analysis['potential_real_messages']),
            'metadata_entries': len(analysis['metadata_entries']),
            'extraction_methods_used': list(analysis['by_method'].keys()),
            'success_rate': 'High' if analysis['potential_real_messages'] else 'Low'
        }

        return analysis

    def is_likely_real_message(self, text):
        """Determine if text is likely a real DM message vs metadata"""
        if not text or len(text) < 2:
            return False

        # Common metadata patterns
        metadata_patterns = [
            'null', 'undefined', 'true', 'false',
            'application/json', 'text/html',
            'csrf_token', 'session_id', 'user_id',
            'instagram.com', 'facebook.com',
            'Bearer ', 'OAuth ', 'Token ',
            '{"', '[{', '}]', '{"error"',
            'HTTP/1.1', 'Content-Type',
            'window.', 'document.', 'function(',
            'var ', 'const ', 'let ',
            '</div>', '<span>', '<p>',
            'undefined_0_', '_js_', '__',
            'error_code', 'status_code'
        ]

        text_lower = text.lower()
        for pattern in metadata_patterns:
            if pattern.lower() in text_lower:
                return False

        # Characteristics of real messages
        if (3 <= len(text) <= 1000 and
            not text.startswith('{') and
            not text.startswith('[') and
            not text.endswith('}') and
            not text.endswith(']') and
            ' ' in text):  # Contains spaces (natural language)
            return True

        return False

    def run_all_extractions(self):
        """Run all extraction methods"""
        extraction_scripts = [
            ('/workspaces/sugarglitch-realops/browser_dm_extractor_2025.py', 'Browser Automation'),
            ('/workspaces/sugarglitch-realops/websocket_dm_interceptor_2025.py', 'WebSocket Interceptor'),
            ('/workspaces/sugarglitch-realops/mobile_dm_extractor_2025.py', 'Mobile API Emulation'),
            ('/workspaces/sugarglitch-realops/enhanced_instagram_extraction_2025.py', 'Enhanced Extraction'),
            ('/workspaces/sugarglitch-realops/real_extraction_with_bypass_2025.py', 'Bypass Arsenal'),
        ]

        logger.info("🚀 Starting Ultimate Instagram DM Extraction Suite...")
        logger.info(f"📋 Running {len(extraction_scripts)} extraction methods")

        # Run scripts sequentially to avoid conflicts
        for script_path, script_name in extraction_scripts:
            if Path(script_path).exists():
                self.run_script(script_path, script_name)
                time.sleep(5)  # Delay between methods
            else:
                logger.warning(f"Script not found: {script_path}")
                self.results[script_name] = {
                    'status': 'not_found',
                    'output': '',
                    'error': 'Script file not found'
                }

    def generate_comprehensive_report(self):
        """Generate comprehensive extraction report"""
        try:
            all_messages, result_files = self.collect_all_results()
            analysis = self.analyze_extraction_results(all_messages)

            timestamp = int(time.time())
            report_file = f'/workspaces/sugarglitch-realops/ULTIMATE_DM_EXTRACTION_REPORT_{timestamp}.json'

            report = {
                'extraction_suite': 'Ultimate Instagram DM Extraction Suite 2025',
                'timestamp': timestamp,
                'execution_time': datetime.now().isoformat(),
                'total_runtime_seconds': time.time() - self.start_time,
                'extraction_results': self.results,
                'message_analysis': analysis,
                'result_files': result_files,
                'summary': {
                    'methods_executed': len(self.results),
                    'successful_methods': len([r for r in self.results.values() if r['status'] == 'success']),
                    'total_messages_found': analysis['total_messages'],
                    'potential_real_messages': len(analysis['potential_real_messages']),
                    'unique_text_extractions': len(analysis['unique_texts']),
                    'overall_success': analysis['potential_real_messages'] > 0
                }
            }

            with open(report_file, 'w') as f:
                json.dump(report, f, indent=2)

            logger.info(f"📊 Comprehensive report saved to: {report_file}")

            # Display summary
            self.display_extraction_summary(report)

            return report_file

        except Exception as e:
            logger.error(f"Error generating report: {e}")
            return None

    def display_extraction_summary(self, report):
        """Display extraction summary to console"""
        print("\n" + "="*80)
        print("🎯 ULTIMATE INSTAGRAM DM EXTRACTION SUMMARY")
        print("="*80)

        summary = report['summary']
        analysis = report['message_analysis']

        print(f"⏱️  Total Runtime: {report['total_runtime_seconds']:.2f} seconds")
        print(f"🔧 Methods Executed: {summary['methods_executed']}")
        print(f"✅ Successful Methods: {summary['successful_methods']}")
        print(f"📬 Total Messages Found: {summary['total_messages_found']}")
        print(f"💬 Potential Real Messages: {summary['potential_real_messages']}")
        print(f"🔤 Unique Text Extractions: {summary['unique_text_extractions']}")
        print(f"🎯 Overall Success: {'YES' if summary['overall_success'] else 'NO'}")

        print("\n📋 EXTRACTION METHOD BREAKDOWN:")
        for method, result in report['extraction_results'].items():
            status_emoji = {
                'success': '✅',
                'warning': '⚠️',
                'timeout': '⏰',
                'error': '❌',
                'not_found': '🔍'
            }.get(result['status'], '❓')
            print(f"  {status_emoji} {method}: {result['status'].upper()}")

        if analysis['potential_real_messages']:
            print("\n💬 POTENTIAL REAL MESSAGES FOUND:")
            for i, msg in enumerate(analysis['potential_real_messages'][:5]):  # Show first 5
                print(f"  {i+1}. {msg.get('text', 'N/A')[:80]}...")
        else:
            print("\n⚠️  NO REAL DM CONTENT EXTRACTED - Only metadata/config data found")

        print("\n📁 RESULT FILES GENERATED:")
        for file_info in report['result_files'][-5:]:  # Show last 5 files
            print(f"  📄 {Path(file_info['file']).name} ({file_info['method']}) - {file_info['message_count']} messages")

        print("="*80)

def main():
    """Main execution function"""
    suite = UltimateDMExtractionSuite()

    try:
        # Run all extraction methods
        suite.run_all_extractions()

        # Generate comprehensive report
        report_file = suite.generate_comprehensive_report()

        if report_file:
            print(f"\n🎉 Ultimate DM extraction completed!")
            print(f"📊 Full report: {report_file}")
        else:
            print("❌ Failed to generate comprehensive report")

    except KeyboardInterrupt:
        logger.info("Extraction interrupted by user")
    except Exception as e:
        logger.error(f"Ultimate extraction suite error: {e}")

if __name__ == "__main__":
    main()

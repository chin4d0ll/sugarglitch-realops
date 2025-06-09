# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
#!/usr/bin/env python3
"""
Comprehensive Session Data Analyzer for HTML Files
Extracts session data, user identifiers, and database schema information.
"""

import json
import re
import os
import sqlite3
from datetime import datetime
import logging
from pathlib import Path

# Set up logging
logging.basicConfig(level = logging.INFO)
logger = logging.getLogger(__name__)

class SessionDataAnalyzer:
    def __init__(self):
        self.results = {
            "analysis_timestamp": datetime.now().isoformat(),
            "session_data": {},
            "user_identifiers": {},
            "csrf_tokens": {},
            "api_keys": {},
            "database_schemas": {},
            "extracted_cookies": {},
            "deferred_cookies": {},
            "instagram_config": {},
            "api_endpoints": []
        }

    def extract_json_data(self, html_content, key_pattern):
        """Extract JSON data based on pattern"""
        matches = re.finditer(key_pattern, html_content, re.IGNORECASE)
        extracted = {}

        for match in matches:
            try:
                # Find the JSON data after the key
                start_pos = match.end()
                json_start = html_content.find('{', start_pos)
                if json_start == -1:
                    continue

                # Find matching closing brace
                brace_count = 0
                json_end = json_start
                for i, char in enumerate(html_content[json_start:], json_start):
                    if char == '{':
                        brace_count += 1
                    elif char == '}':
                        brace_count -= 1
                        if brace_count == 0:
                            json_end = i + 1
                            break

                json_str = html_content[json_start:json_end]
                data = json.loads(json_str)
                extracted[match.group(0)] = data

            except Exception as e:
                logger.debug(f"Failed to parse JSON for {match.group(0)}: {e}")

        return extracted

    def analyze_html_file(self, file_path):
        """Analyze a single HTML file for session data"""
        logger.info(f"Analyzing {file_path}")

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            logger.error(f"Failed to read {file_path}: {e}")
            return {}

        file_results = {
            "file_path": file_path,
            "file_size": len(content),
            "analysis_time": datetime.now().isoformat()
        }

        # Extract CSRF tokens
        csrf_matches = re.findall(r'"csrf_token":"([^"]*)"', content)
        if csrf_matches:
            file_results["csrf_tokens"] = csrf_matches

        # Extract X-IG-App-ID
        app_id_matches = re.findall(r'"X-IG-App-ID":"([^"]*)"', content)
        if app_id_matches:
            file_results["x_ig_app_ids"] = app_id_matches

        # Extract User IDs
        user_id_matches = re.findall(r'"USER_ID":"([^"]*)"', content)
        if user_id_matches:
            file_results["user_ids"] = user_id_matches

        # Extract Account IDs
        account_id_matches = re.findall(r'"ACCOUNT_ID":"([^"]*)"', content)
        if account_id_matches:
            file_results["account_ids"] = account_id_matches

        # Extract session cookies (_js_ig_did, _js_datr)
        ig_did_matches = re.findall(r'"_js_ig_did":\{"value":"([^"]*)"', content)
        if ig_did_matches:
            file_results["ig_device_ids"] = ig_did_matches

        datr_matches = re.findall(r'"_js_datr":\{"value":"([^"]*)"', content)
        if datr_matches:
            file_results["datr_tokens"] = datr_matches

        # Extract Instagram Security Config
        security_config = self.extract_json_data(content, r'"InstagramSecurityConfig"')
        if security_config:
            file_results["security_config"] = security_config

        # Extract Current User Data
        user_data = self.extract_json_data(content, r'"CurrentUserInitialData"')
        if user_data:
            file_results["current_user_data"] = user_data

        # Extract RelayAPI Config
        relay_config = self.extract_json_data(content, r'"RelayAPIConfigDefaults"')
        if relay_config:
            file_results["relay_api_config"] = relay_config

        # Extract PolarisViewer data
        viewer_data = self.extract_json_data(content, r'"PolarisViewer"')
        if viewer_data:
            file_results["polaris_viewer"] = viewer_data

        # Extract Cookie Config
        cookie_config = self.extract_json_data(content, r'"CookieCoreConfig"')
        if cookie_config:
            file_results["cookie_config"] = cookie_config

        # Extract Direct V2 API endpoints
        direct_v2_matches = re.findall(r'"path":"([^"]*direct_v2[^"]*)"', content)
        if direct_v2_matches:
            file_results["direct_v2_endpoints"] = direct_v2_matches

        # Extract WebLoom Config for Direct messaging
        webloom_matches = re.findall(r'"DirectInboxPage":[0-9.]+', content)
        if webloom_matches:
            file_results["direct_inbox_metrics"] = webloom_matches

        thread_matches = re.findall(r'"DirectThreadPage":[0-9.]+', content)
        if thread_matches:
            file_results["direct_thread_metrics"] = thread_matches

        return file_results

    def analyze_database_schema(self, db_path):
        """Analyze SQLite database schema"""
        logger.info(f"Analyzing database {db_path}")

        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            # Get table names
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()

            schema_info = {
                "database_path": db_path,
                "tables": {},
                "analysis_time": datetime.now().isoformat()
            }

            for table in tables:
                table_name = table[0]

                # Get table schema
                cursor.execute(f"PRAGMA table_info({table_name});")
                columns = cursor.fetchall()

                # Get row count
                cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
                row_count = cursor.fetchone()[0]

                # Get sample data if available
                sample_data = []
                if row_count > 0:
                    cursor.execute(f"SELECT * FROM {table_name} LIMIT 3;")
                    sample_data = cursor.fetchall()

                schema_info["tables"][table_name] = {
                    "columns": [{"name": col[1], "type": col[2], "not_null": col[3], "primary_key": col[5]} for col in columns],
                    "row_count": row_count,
                    "sample_data": sample_data
                }

            conn.close()
            return schema_info

        except Exception as e:
            logger.error(f"Failed to analyze database {db_path}: {e}")
            return {"error": str(e), "database_path": db_path}

    def run_analysis(self, results_dir="results", workspace_dir="."):
        """Run comprehensive analysis"""
        logger.info("Starting comprehensive session data analysis")

        # Analyze HTML files
        html_files = []
        if os.path.exists(results_dir):
            html_files = [os.path.join(results_dir, f) for f in os.listdir(results_dir) if f.endswith('.html')]

        for html_file in html_files:
            file_data = self.analyze_html_file(html_file)
            if file_data:
                self.results["session_data"][os.path.basename(html_file)] = file_data

        # Analyze SQLite databases
        sqlite_files = []
        for root, dirs, files in os.walk(workspace_dir):
            for file in files:
                if file.endswith('.sqlite'):
                    sqlite_files.append(os.path.join(root, file))

        for db_file in sqlite_files:
            db_data = self.analyze_database_schema(db_file)
            if db_data:
                self.results["database_schemas"][os.path.basename(db_file)] = db_data

        # Generate summary
        self.generate_summary()

        return self.results

    def generate_summary(self):
        """Generate analysis summary"""
        summary = {
            "total_html_files": len(self.results["session_data"]),
            "total_databases": len(self.results["database_schemas"]),
            "unique_csrf_tokens": set(),
            "unique_app_ids": set(),
            "unique_user_ids": set(),
            "unique_device_ids": set(),
            "direct_v2_endpoints": set(),
            "session_identifiers_found": False
        }

        # Collect unique identifiers
        for file_name, file_data in self.results["session_data"].items():
            if "csrf_tokens" in file_data:
                summary["unique_csrf_tokens"].update(file_data["csrf_tokens"])
            if "x_ig_app_ids" in file_data:
                summary["unique_app_ids"].update(file_data["x_ig_app_ids"])
            if "user_ids" in file_data:
                summary["unique_user_ids"].update(file_data["user_ids"])
            if "ig_device_ids" in file_data:
                summary["unique_device_ids"].update(file_data["ig_device_ids"])
            if "direct_v2_endpoints" in file_data:
                summary["direct_v2_endpoints"].update(file_data["direct_v2_endpoints"])

            # Check if session identifiers found
            if any(key in file_data for key in ["csrf_tokens", "ig_device_ids", "datr_tokens"]):
                summary["session_identifiers_found"] = True

        # Convert sets to lists for JSON serialization
        summary["unique_csrf_tokens"] = list(summary["unique_csrf_tokens"])
        summary["unique_app_ids"] = list(summary["unique_app_ids"])
        summary["unique_user_ids"] = list(summary["unique_user_ids"])
        summary["unique_device_ids"] = list(summary["unique_device_ids"])
        summary["direct_v2_endpoints"] = list(summary["direct_v2_endpoints"])

        self.results["summary"] = summary

    def save_results(self, output_file="comprehensive_session_analysis.json"):
        """Save analysis results to file"""
        with open(output_file, 'w') as f:
            json.dump(self.results, f, indent = 2)
        logger.info(f"Analysis results saved to {output_file}")

def main():
    analyzer = SessionDataAnalyzer()
    results = analyzer.run_analysis()

    # Save detailed results
    analyzer.save_results()

    # Print summary
    print("\n" + "="*60)
    print("COMPREHENSIVE SESSION DATA ANALYSIS SUMMARY")
    print("="*60)

    summary = results["summary"]
    print(f"HTML Files Analyzed: {summary['total_html_files']}")
    print(f"Databases Analyzed: {summary['total_databases']}")
    print(f"Session Identifiers Found: {'Yes' if summary['session_identifiers_found'] else 'No'}")

    if summary["unique_csrf_tokens"]:
        print(f"\nCSRF Tokens Found ({len(summary['unique_csrf_tokens'])}):")
        for token in summary["unique_csrf_tokens"]:
            print(f"  - {token}")

    if summary["unique_app_ids"]:
        print(f"\nInstagram App IDs ({len(summary['unique_app_ids'])}):")
        for app_id in summary["unique_app_ids"]:
            print(f"  - {app_id}")

    if summary["unique_device_ids"]:
        print(f"\nDevice IDs ({len(summary['unique_device_ids'])}):")
        for device_id in summary["unique_device_ids"]:
            print(f"  - {device_id}")

    if summary["direct_v2_endpoints"]:
        print(f"\nDirect V2 Endpoints ({len(summary['direct_v2_endpoints'])}):")
        for endpoint in summary["direct_v2_endpoints"]:
            print(f"  - {endpoint}")

    # Show database schemas
    if results["database_schemas"]:
        print(f"\nDatabase Schemas Found:")
        for db_name, db_info in results["database_schemas"].items():
            if "tables" in db_info:
                print(f"\n{db_name}:")
                for table_name, table_info in db_info["tables"].items():
                    print(f"  Table: {table_name} ({table_info['row_count']} rows)")
                    for col in table_info["columns"]:
                        pk_marker = " (PK)" if col["primary_key"] else ""
                        print(f"    - {col['name']}: {col['type']}{pk_marker}")

    print("\n" + "="*60)
    print("Analysis complete! Full details saved to comprehensive_session_analysis.json")

if __name__ == "__main__":
    main()

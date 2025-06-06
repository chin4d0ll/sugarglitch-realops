#!/usr/bin/env python3
"""
Database Consolidation and Analysis Tool
Analyzes and consolidates all database files in the workspace
"""

import sqlite3
import json
import os
from pathlib import Path
from datetime import datetime
import logging
from typing import Dict, List, Any
import pandas as pd

# Import our error handling utilities
import sys
sys.path.append('/workspaces/sugarglitch-realops')
from utils.error_handler import safe_execution, safe_print

class DatabaseAnalyzer:
    def __init__(self):
        self.root_dir = Path("/workspaces/sugarglitch-realops")
        self.analysis_dir = self.root_dir / "database_analysis"
        self.consolidated_db = self.root_dir / "consolidated_intelligence.db"
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    @safe_execution
    def find_database_files(self):
        """Find all database files in the workspace"""
        db_files = []
        
        # Find .db files
        db_files.extend(list(self.root_dir.glob("*.db")))
        
        # Find SQLite files
        db_files.extend(list(self.root_dir.glob("*.sqlite")))
        db_files.extend(list(self.root_dir.glob("*.sqlite3")))
        
        # Remove duplicates and filter out lock files
        unique_dbs = []
        for db_file in db_files:
            if not any(suffix in db_file.name for suffix in ['-shm', '-wal', 'lock']):
                unique_dbs.append(db_file)
        
        safe_print(f"🔍 Found {len(unique_dbs)} database files:")
        for db in unique_dbs:
            safe_print(f"   - {db.name}")
            
        return unique_dbs

    @safe_execution
    def analyze_database_structure(self, db_path: Path):
        """Analyze the structure of a single database"""
        safe_print(f"📊 Analyzing {db_path.name}...")
        
        try:
            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()
            
            # Get all tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            
            db_analysis = {
                "database_name": db_path.name,
                "file_size": db_path.stat().st_size,
                "tables": {},
                "total_records": 0,
                "analysis_timestamp": datetime.now().isoformat()
            }
            
            for table_name in [t[0] for t in tables]:
                try:
                    # Get table info
                    cursor.execute(f"PRAGMA table_info({table_name})")
                    columns = cursor.fetchall()
                    
                    # Get record count
                    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                    record_count = cursor.fetchone()[0]
                    
                    # Get sample data (first 3 rows)
                    cursor.execute(f"SELECT * FROM {table_name} LIMIT 3")
                    sample_data = cursor.fetchall()
                    
                    db_analysis["tables"][table_name] = {
                        "columns": [{"name": col[1], "type": col[2]} for col in columns],
                        "record_count": record_count,
                        "sample_data": sample_data[:3] if sample_data else []
                    }
                    
                    db_analysis["total_records"] += record_count
                    
                except Exception as e:
                    safe_print(f"⚠️ Error analyzing table {table_name}: {e}")
            
            conn.close()
            safe_print(f"✅ {db_path.name}: {len(tables)} tables, {db_analysis['total_records']} total records")
            return db_analysis
            
        except Exception as e:
            safe_print(f"❌ Error analyzing {db_path.name}: {e}")
            return None

    @safe_execution
    def create_consolidated_database(self, db_analyses: List[Dict]):
        """Create a consolidated database with all intelligence data"""
        safe_print("🔄 Creating consolidated intelligence database...")
        
        # Remove existing consolidated DB if exists
        if self.consolidated_db.exists():
            self.consolidated_db.unlink()
        
        conn = sqlite3.connect(str(self.consolidated_db))
        cursor = conn.cursor()
        
        # Create metadata table
        cursor.execute('''
            CREATE TABLE database_metadata (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_database TEXT,
                table_name TEXT,
                record_count INTEGER,
                analysis_timestamp TEXT
            )
        ''')
        
        # Create unified intelligence table
        cursor.execute('''
            CREATE TABLE unified_intelligence (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_database TEXT,
                source_table TEXT,
                data_type TEXT,
                target_identifier TEXT,
                extracted_data TEXT,
                timestamp TEXT,
                confidence_score REAL
            )
        ''')
        
        # Create session management table
        cursor.execute('''
            CREATE TABLE session_tracking (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT UNIQUE,
                platform TEXT,
                target TEXT,
                status TEXT,
                created_timestamp TEXT,
                last_updated TEXT
            )
        ''')
        
        # Insert metadata for each analyzed database
        for analysis in db_analyses:
            if analysis:
                for table_name, table_info in analysis["tables"].items():
                    cursor.execute('''
                        INSERT INTO database_metadata 
                        (source_database, table_name, record_count, analysis_timestamp)
                        VALUES (?, ?, ?, ?)
                    ''', (
                        analysis["database_name"],
                        table_name,
                        table_info["record_count"],
                        analysis["analysis_timestamp"]
                    ))
        
        conn.commit()
        conn.close()
        
        safe_print(f"✅ Consolidated database created: {self.consolidated_db.name}")
        return True

    @safe_execution
    def export_database_summary(self, db_analyses: List[Dict]):
        """Export comprehensive database summary"""
        safe_print("📄 Creating database summary report...")
        
        self.analysis_dir.mkdir(exist_ok=True)
        
        # Create summary statistics
        summary = {
            "analysis_timestamp": datetime.now().isoformat(),
            "total_databases": len([a for a in db_analyses if a]),
            "total_tables": 0,
            "total_records": 0,
            "databases": [],
            "table_distribution": {},
            "data_types_found": set()
        }
        
        for analysis in db_analyses:
            if analysis:
                summary["total_tables"] += len(analysis["tables"])
                summary["total_records"] += analysis["total_records"]
                summary["databases"].append({
                    "name": analysis["database_name"],
                    "tables": len(analysis["tables"]),
                    "records": analysis["total_records"],
                    "size_bytes": analysis["file_size"]
                })
                
                # Analyze table types
                for table_name, table_info in analysis["tables"].items():
                    if table_info["record_count"] > 0:
                        category = self._categorize_table(table_name)
                        summary["table_distribution"][category] = summary["table_distribution"].get(category, 0) + 1
                        
                        # Collect data types
                        for col in table_info["columns"]:
                            summary["data_types_found"].add(col["type"])
        
        # Convert set to list for JSON serialization
        summary["data_types_found"] = list(summary["data_types_found"])
        
        # Save detailed analysis
        detailed_report = self.analysis_dir / f"database_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(detailed_report, 'w') as f:
            json.dump(db_analyses, f, indent=2, default=str)
        
        # Save summary report
        summary_report = self.analysis_dir / f"database_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(summary_report, 'w') as f:
            json.dump(summary, f, indent=2, default=str)
        
        # Create human-readable report
        readable_report = self.analysis_dir / f"database_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        self._create_readable_report(summary, readable_report)
        
        safe_print(f"✅ Database analysis reports created in {self.analysis_dir.name}/")
        return summary

    def _categorize_table(self, table_name: str) -> str:
        """Categorize table based on name patterns"""
        table_lower = table_name.lower()
        
        if any(word in table_lower for word in ['session', 'auth', 'login']):
            return "authentication"
        elif any(word in table_lower for word in ['intelligence', 'data', 'extraction']):
            return "intelligence"
        elif any(word in table_lower for word in ['target', 'profile', 'user']):
            return "targets"
        elif any(word in table_lower for word in ['message', 'chat', 'conversation']):
            return "communications"
        elif any(word in table_lower for word in ['image', 'media', 'file']):
            return "media"
        else:
            return "other"

    def _create_readable_report(self, summary: Dict, report_path: Path):
        """Create human-readable markdown report"""
        content = f"""# Database Analysis Report

**Generated:** {summary['analysis_timestamp']}

## Summary Statistics

- **Total Databases:** {summary['total_databases']}
- **Total Tables:** {summary['total_tables']}
- **Total Records:** {summary['total_records']:,}

## Database Breakdown

| Database | Tables | Records | Size |
|----------|--------|---------|------|
"""
        
        for db in summary['databases']:
            size_mb = db['size_bytes'] / (1024 * 1024)
            content += f"| {db['name']} | {db['tables']} | {db['records']:,} | {size_mb:.2f} MB |\n"
        
        content += f"""

## Table Categories

"""
        for category, count in summary['table_distribution'].items():
            content += f"- **{category.title()}:** {count} tables\n"
        
        content += f"""

## Data Types Found

{', '.join(summary['data_types_found'])}

## Recommendations

1. **Consolidation**: Consider merging similar tables across databases
2. **Optimization**: Some databases may benefit from indexing
3. **Cleanup**: Review empty or duplicate tables
4. **Backup**: Ensure regular backups of critical intelligence data

---
*Generated by Sugarglitch RealOps Database Analyzer*
"""
        
        with open(report_path, 'w') as f:
            f.write(content)

    @safe_execution
    def run_complete_analysis(self):
        """Run complete database analysis pipeline"""
        safe_print("🔍 Starting comprehensive database analysis...")
        safe_print("="*60)
        
        # Step 1: Find all databases
        db_files = self.find_database_files()
        if not db_files:
            safe_print("❌ No database files found!")
            return False
        
        # Step 2: Analyze each database
        safe_print("\n📊 Analyzing database structures...")
        db_analyses = []
        for db_file in db_files:
            analysis = self.analyze_database_structure(db_file)
            if analysis:
                db_analyses.append(analysis)
        
        # Step 3: Create consolidated database
        safe_print("\n🔄 Creating consolidated database...")
        self.create_consolidated_database(db_analyses)
        
        # Step 4: Export comprehensive summary
        safe_print("\n📄 Generating analysis reports...")
        summary = self.export_database_summary(db_analyses)
        
        safe_print("="*60)
        safe_print("🎉 Database analysis completed!")
        safe_print(f"📊 Analyzed {len(db_analyses)} databases")
        safe_print(f"📁 Reports saved in {self.analysis_dir.name}/")
        safe_print(f"🗃️ Consolidated DB: {self.consolidated_db.name}")
        safe_print("="*60)
        
        return summary


def main():
    """Main execution function"""
    safe_print("🗃️ Sugarglitch RealOps - Database Analysis Tool")
    safe_print("="*60)
    safe_print("This tool analyzes and consolidates all database files")
    safe_print("while preserving ALL existing data")
    safe_print("="*60)
    
    analyzer = DatabaseAnalyzer()
    results = analyzer.run_complete_analysis()
    
    if results:
        safe_print("\n✅ Database analysis completed successfully!")
        safe_print("📁 Check the database_analysis/ directory for detailed reports")
    else:
        safe_print("\n⚠️ Database analysis encountered issues. Check the logs.")


if __name__ == "__main__":
    main()
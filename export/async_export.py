#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📊 ASYNC EXPORT MODULE
High-performance async data export with streaming and memory optimization
"""

import asyncio
import aiofiles
import json
import csv
import time
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, AsyncGenerator
from dataclasses import dataclass
from io import StringIO
import zipfile
import logging

# Rich imports
try:
    from rich.console import Console
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

console = Console() if RICH_AVAILABLE else None


@dataclass
class ExportConfig:
    """⚙️ Export configuration"""
    chunk_size: int = 1000
    compress: bool = True
    include_metadata: bool = True
    pretty_json: bool = True
    memory_limit_mb: int = 100
    temp_dir: Path = Path("temp")
    backup_enabled: bool = True


@dataclass
class ExportMetadata:
    """📝 Export metadata tracking"""
    export_id: str
    start_time: datetime
    end_time: Optional[datetime] = None
    total_records: int = 0
    file_size_bytes: int = 0
    export_format: str = ""
    compression_ratio: float = 0.0
    success: bool = False
    error_message: str = ""


class AsyncDataExporter:
    """🚀 High-performance async data exporter"""

    def __init__(self, config: Optional[ExportConfig] = None):
        self.config = config or ExportConfig()
        self.exports: Dict[str, ExportMetadata] = {}
        self.active_exports = 0

        # Ensure temp directory exists
        self.config.temp_dir.mkdir(exist_ok=True)

    async def export_json_streaming(
        self,
        data_generator: AsyncGenerator[Dict[str, Any], None],
        output_path: Path,
        indent: Optional[int] = 2
    ) -> ExportMetadata:
        """Stream export to JSON with memory optimization"""

        export_id = f"json_{int(time.time())}"
        metadata = ExportMetadata(
            export_id=export_id,
            start_time=datetime.now(),
            export_format="JSON"
        )
        self.exports[export_id] = metadata

        try:
            self.active_exports += 1

            # Create backup if enabled
            if self.config.backup_enabled and output_path.exists():
                timestamp = int(time.time())
                backup_path = output_path.with_suffix(
                    f".backup_{timestamp}.json")
                await self._copy_file(output_path, backup_path)

            # Open output file
            mode = 'wt' if self.config.compress else 'w'

            async with aiofiles.open(
                output_path, mode=mode, encoding='utf-8'
            ) as f:

                # Write JSON opening
                await f.write('[\n' if indent else '[')

                record_count = 0
                first_record = True

                # Process data in chunks
                async for record in data_generator:

                    # Add comma separator
                    if not first_record:
                        await f.write(',\n' if indent else ',')
                    first_record = False

                    # Serialize record
                    if indent:
                        json_str = json.dumps(
                            record, indent=indent, ensure_ascii=False)
                        # Indent all lines except first
                        lines = json_str.split('\n')
                        indented = lines[0] + '\n' + \
                            '\n'.join(f'  {line}' for line in lines[1:])
                        await f.write(indented)
                    else:
                        json_str = json.dumps(
                            record, ensure_ascii=False, separators=(',', ':'))
                        await f.write(json_str)

                    record_count += 1

                    # Memory management - flush periodically
                    if record_count % self.config.chunk_size == 0:
                        await f.flush()
                        await asyncio.sleep(0)  # Yield control

                # Write JSON closing
                await f.write('\n]' if indent else ']')

            # Update metadata
            metadata.total_records = record_count
            metadata.file_size_bytes = output_path.stat().st_size
            metadata.end_time = datetime.now()
            metadata.success = True

            # Calculate compression ratio
            if self.config.compress:
                # Estimate uncompressed size for ratio calculation
                with open(output_path, 'rb') as compressed:
                    compressed_size = len(compressed.read())
                estimated_uncompressed = compressed_size * 3  # Rough estimate
                metadata.compression_ratio = compressed_size / estimated_uncompressed

        except Exception as e:
            metadata.error_message = str(e)
            metadata.end_time = datetime.now()
            logging.error(f"JSON export failed: {e}")

        finally:
            self.active_exports -= 1

        return metadata

    async def export_csv_streaming(
        self,
        data_generator: AsyncGenerator[Dict[str, Any], None],
        output_path: Path,
        fieldnames: Optional[List[str]] = None
    ) -> ExportMetadata:
        """Stream export to CSV with automatic field detection"""

        export_id = f"csv_{int(time.time())}"
        metadata = ExportMetadata(
            export_id=export_id,
            start_time=datetime.now(),
            export_format="CSV"
        )
        self.exports[export_id] = metadata

        try:
            self.active_exports += 1

            # Use temporary file for field detection if needed
            temp_records = []
            detected_fieldnames = fieldnames

            if not detected_fieldnames:
                # Collect first few records to detect fields
                sample_count = 0
                async for record in data_generator:
                    temp_records.append(record)
                    sample_count += 1
                    if sample_count >= 10:  # Sample first 10 records
                        break

                # Extract all unique field names
                all_fields = set()
                for record in temp_records:
                    all_fields.update(record.keys())
                detected_fieldnames = sorted(all_fields)

            # Open output file
            async with aiofiles.open(output_path, mode='w', encoding='utf-8', newline='') as f:

                # Create CSV writer using StringIO buffer
                buffer = StringIO()
                writer = csv.DictWriter(buffer, fieldnames=detected_fieldnames)

                # Write header
                writer.writeheader()
                await f.write(buffer.getvalue())
                buffer.seek(0)
                buffer.truncate(0)

                record_count = 0

                # Write temp records first
                for record in temp_records:
                    writer.writerow(record)
                    record_count += 1

                    # Flush buffer periodically
                    if record_count % 100 == 0:
                        await f.write(buffer.getvalue())
                        buffer.seek(0)
                        buffer.truncate(0)
                        await asyncio.sleep(0)

                # Continue with remaining data
                async for record in data_generator:
                    writer.writerow(record)
                    record_count += 1

                    # Flush buffer periodically
                    if record_count % 100 == 0:
                        await f.write(buffer.getvalue())
                        buffer.seek(0)
                        buffer.truncate(0)
                        await asyncio.sleep(0)

                # Write final buffer content
                if buffer.tell() > 0:
                    await f.write(buffer.getvalue())

            # Update metadata
            metadata.total_records = record_count
            metadata.file_size_bytes = output_path.stat().st_size
            metadata.end_time = datetime.now()
            metadata.success = True

        except Exception as e:
            metadata.error_message = str(e)
            metadata.end_time = datetime.now()
            logging.error(f"CSV export failed: {e}")

        finally:
            self.active_exports -= 1

        return metadata

    async def export_sqlite_streaming(
        self,
        data_generator: AsyncGenerator[Dict[str, Any], None],
        output_path: Path,
        table_name: str = "data"
    ) -> ExportMetadata:
        """Stream export to SQLite database"""

        export_id = f"sqlite_{int(time.time())}"
        metadata = ExportMetadata(
            export_id=export_id,
            start_time=datetime.now(),
            export_format="SQLite"
        )
        self.exports[export_id] = metadata

        try:
            self.active_exports += 1

            # Remove existing database
            if output_path.exists():
                output_path.unlink()

            # Connect to SQLite
            conn = sqlite3.connect(str(output_path))
            cursor = conn.cursor()

            # Collect sample records to create schema
            sample_records = []
            sample_count = 0
            async for record in data_generator:
                sample_records.append(record)
                sample_count += 1
                if sample_count >= 5:  # Sample for schema detection
                    break

            # Create table schema from sample
            if sample_records:
                all_fields = set()
                for record in sample_records:
                    all_fields.update(record.keys())

                # Create table
                fields_def = ", ".join(
                    f'"{field}" TEXT' for field in sorted(all_fields))
                create_sql = f'CREATE TABLE "{table_name}" ({fields_def})'
                cursor.execute(create_sql)

                # Prepare insert statement
                placeholders = ", ".join("?" for _ in all_fields)
                insert_sql = f'INSERT INTO "{table_name}" VALUES ({placeholders})'

                record_count = 0

                # Insert sample records
                for record in sample_records:
                    values = [record.get(field, None)
                              for field in sorted(all_fields)]
                    cursor.execute(insert_sql, values)
                    record_count += 1

                # Insert remaining records
                batch = []
                async for record in data_generator:
                    values = [record.get(field, None)
                              for field in sorted(all_fields)]
                    batch.append(values)
                    record_count += 1

                    # Execute batch inserts
                    if len(batch) >= self.config.chunk_size:
                        cursor.executemany(insert_sql, batch)
                        conn.commit()
                        batch.clear()
                        await asyncio.sleep(0)  # Yield control

                # Insert final batch
                if batch:
                    cursor.executemany(insert_sql, batch)
                    conn.commit()

                # Update metadata
                metadata.total_records = record_count

            conn.close()
            metadata.file_size_bytes = output_path.stat().st_size
            metadata.end_time = datetime.now()
            metadata.success = True

        except Exception as e:
            metadata.error_message = str(e)
            metadata.end_time = datetime.now()
            logging.error(f"SQLite export failed: {e}")

        finally:
            self.active_exports -= 1

        return metadata

    async def export_xml_streaming(
        self,
        data_generator: AsyncGenerator[Dict[str, Any], None],
        output_path: Path,
        root_element: str = "data",
        record_element: str = "record"
    ) -> ExportMetadata:
        """Stream export to XML format"""

        export_id = f"xml_{int(time.time())}"
        metadata = ExportMetadata(
            export_id=export_id,
            start_time=datetime.now(),
            export_format="XML"
        )
        self.exports[export_id] = metadata

        try:
            self.active_exports += 1

            async with aiofiles.open(output_path, mode='w', encoding='utf-8') as f:

                # Write XML header and root opening
                await f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
                await f.write(f'<{root_element}>\n')

                record_count = 0

                async for record in data_generator:
                    # Convert record to XML
                    await f.write(f'  <{record_element}>\n')

                    for key, value in record.items():
                        # Escape XML characters
                        safe_key = str(key).replace('&', '&amp;').replace(
                            '<', '&lt;').replace('>', '&gt;')
                        safe_value = str(value).replace('&', '&amp;').replace(
                            '<', '&lt;').replace('>', '&gt;')
                        await f.write(f'    <{safe_key}>{safe_value}</{safe_key}>\n')

                    await f.write(f'  </{record_element}>\n')
                    record_count += 1

                    # Yield control periodically
                    if record_count % self.config.chunk_size == 0:
                        await f.flush()
                        await asyncio.sleep(0)

                # Write root closing
                await f.write(f'</{root_element}>\n')

            # Update metadata
            metadata.total_records = record_count
            metadata.file_size_bytes = output_path.stat().st_size
            metadata.end_time = datetime.now()
            metadata.success = True

        except Exception as e:
            metadata.error_message = str(e)
            metadata.end_time = datetime.now()
            logging.error(f"XML export failed: {e}")

        finally:
            self.active_exports -= 1

        return metadata

    async def export_html_report(
        self,
        data: Dict[str, Any],
        output_path: Path,
        template_name: str = "default"
    ) -> ExportMetadata:
        """Export data as HTML report"""

        export_id = f"html_{int(time.time())}"
        metadata = ExportMetadata(
            export_id=export_id,
            start_time=datetime.now(),
            export_format="HTML"
        )
        self.exports[export_id] = metadata

        try:
            self.active_exports += 1

            # Generate HTML content
            html_content = await self._generate_html_report(data, template_name)

            async with aiofiles.open(output_path, mode='w', encoding='utf-8') as f:
                await f.write(html_content)

            # Update metadata
            metadata.total_records = 1  # Single report
            metadata.file_size_bytes = output_path.stat().st_size
            metadata.end_time = datetime.now()
            metadata.success = True

        except Exception as e:
            metadata.error_message = str(e)
            metadata.end_time = datetime.now()
            logging.error(f"HTML export failed: {e}")

        finally:
            self.active_exports -= 1

        return metadata

    async def _generate_html_report(self, data: Dict[str, Any], template_name: str) -> str:
        """Generate HTML report from data"""

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SugarGlitch RealOps Report</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; background: #0a0a0a; color: #fff; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; border-radius: 10px; text-align: center; margin-bottom: 30px; }}
        .header h1 {{ margin: 0; font-size: 2.5em; color: white; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); }}
        .header p {{ margin: 10px 0 0 0; opacity: 0.9; font-size: 1.1em; }}
        .section {{ background: #1a1a1a; border-radius: 10px; padding: 25px; margin-bottom: 20px; border-left: 4px solid #667eea; }}
        .section h2 {{ margin-top: 0; color: #667eea; border-bottom: 2px solid #333; padding-bottom: 10px; }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }}
        .card {{ background: #2a2a2a; border-radius: 8px; padding: 20px; border-left: 3px solid #764ba2; }}
        .card h3 {{ margin-top: 0; color: #764ba2; }}
        .stats {{ display: flex; justify-content: space-around; flex-wrap: wrap; }}
        .stat {{ text-align: center; margin: 10px; }}
        .stat-value {{ font-size: 2em; font-weight: bold; color: #667eea; }}
        .stat-label {{ color: #888; margin-top: 5px; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 15px; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #333; }}
        th {{ background: #333; color: #667eea; font-weight: bold; }}
        tr:hover {{ background: #333; }}
        .success {{ color: #4CAF50; }}
        .error {{ color: #f44336; }}
        .warning {{ color: #ff9800; }}
        .footer {{ text-align: center; margin-top: 40px; padding: 20px; color: #666; border-top: 1px solid #333; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔥 SugarGlitch RealOps Report</h1>
            <p>Generated on {timestamp}</p>
        </div>
"""

        # Add data sections
        for section_name, section_data in data.items():
            html += f'        <div class="section">\n'
            html += f'            <h2>{section_name.replace("_", " ").title()}</h2>\n'

            if isinstance(section_data, dict):
                html += '            <div class="grid">\n'
                for key, value in section_data.items():
                    html += f'                <div class="card">\n'
                    html += f'                    <h3>{key.replace("_", " ").title()}</h3>\n'
                    html += f'                    <p>{value}</p>\n'
                    html += f'                </div>\n'
                html += '            </div>\n'
            elif isinstance(section_data, list):
                if section_data and isinstance(section_data[0], dict):
                    # Table format
                    html += '            <table>\n'
                    headers = section_data[0].keys()
                    html += '                <tr>\n'
                    for header in headers:
                        html += f'                    <th>{header.replace("_", " ").title()}</th>\n'
                    html += '                </tr>\n'

                    for row in section_data:
                        html += '                <tr>\n'
                        for header in headers:
                            value = row.get(header, '')
                            html += f'                    <td>{value}</td>\n'
                        html += '                </tr>\n'
                    html += '            </table>\n'
                else:
                    # List format
                    html += '            <ul>\n'
                    for item in section_data:
                        html += f'                <li>{item}</li>\n'
                    html += '            </ul>\n'
            else:
                html += f'            <p>{section_data}</p>\n'

            html += '        </div>\n'

        html += """
        <div class="footer">
            <p>🚀 Generated by SugarGlitch RealOps v2.0 - Advanced RedTeam Automation Suite</p>
        </div>
    </div>
</body>
</html>
"""

        return html

    async def _copy_file(self, source: Path, destination: Path) -> None:
        """Async file copy"""
        async with aiofiles.open(source, 'rb') as src:
            async with aiofiles.open(destination, 'wb') as dst:
                while chunk := await src.read(self.config.chunk_size):
                    await dst.write(chunk)

    async def create_archive(
        self,
        file_paths: List[Path],
        archive_path: Path,
        compression: str = "zip"
    ) -> ExportMetadata:
        """Create compressed archive of multiple files"""

        export_id = f"archive_{int(time.time())}"
        metadata = ExportMetadata(
            export_id=export_id,
            start_time=datetime.now(),
            export_format=compression.upper()
        )
        self.exports[export_id] = metadata

        try:
            self.active_exports += 1

            if compression.lower() == "zip":
                with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    for file_path in file_paths:
                        if file_path.exists():
                            zipf.write(file_path, file_path.name)
                            await asyncio.sleep(0)  # Yield control

            metadata.total_records = len(file_paths)
            metadata.file_size_bytes = archive_path.stat().st_size
            metadata.end_time = datetime.now()
            metadata.success = True

        except Exception as e:
            metadata.error_message = str(e)
            metadata.end_time = datetime.now()
            logging.error(f"Archive creation failed: {e}")

        finally:
            self.active_exports -= 1

        return metadata

    def get_export_stats(self) -> Dict[str, Any]:
        """Get export statistics"""
        total_exports = len(self.exports)
        successful_exports = sum(
            1 for exp in self.exports.values() if exp.success)

        return {
            "total_exports": total_exports,
            "successful_exports": successful_exports,
            "failed_exports": total_exports - successful_exports,
            "active_exports": self.active_exports,
            "success_rate": (successful_exports / max(total_exports, 1)) * 100
        }

    async def cleanup_temp_files(self) -> int:
        """Clean up temporary files"""
        cleaned = 0
        temp_pattern = self.config.temp_dir.glob("temp_*")

        for temp_file in temp_pattern:
            try:
                if temp_file.is_file():
                    temp_file.unlink()
                    cleaned += 1
                await asyncio.sleep(0)
            except Exception as e:
                logging.warning(f"Failed to clean temp file {temp_file}: {e}")

        return cleaned


# Utility functions for common export patterns
async def export_list_to_json(
    data_list: List[Dict[str, Any]],
    output_path: Path,
    chunk_size: int = 1000
) -> ExportMetadata:
    """Quick export of list to JSON"""

    async def data_generator():
        for item in data_list:
            yield item

    exporter = AsyncDataExporter(ExportConfig(chunk_size=chunk_size))
    return await exporter.export_json_streaming(data_generator(), output_path)


async def export_list_to_csv(
    data_list: List[Dict[str, Any]],
    output_path: Path,
    fieldnames: Optional[List[str]] = None
) -> ExportMetadata:
    """Quick export of list to CSV"""

    async def data_generator():
        for item in data_list:
            yield item

    exporter = AsyncDataExporter()
    return await exporter.export_csv_streaming(data_generator(), output_path, fieldnames)


# Export main components
__all__ = [
    'AsyncDataExporter',
    'ExportConfig',
    'ExportMetadata',
    'export_list_to_json',
    'export_list_to_csv'
]

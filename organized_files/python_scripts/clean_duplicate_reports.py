import os
import re
import json
from pathlib import Path

REPORT_DIRS = [
    'COMPLETE_SENSITIVE_REPORTS',
    'SENSITIVE_REPORTS',
    'results',
    'export',
    'data/extractions/extraction_reports'
]

# Patterns for report files (adjust as needed)
REPORT_PATTERNS = [
    re.compile(r'^rapid_intel_.*\.json$'),
    re.compile(r'^rapid_intel_.*\.md$'),
    re.compile(r'^rapid_intel_.*\.html$'),
    re.compile(r'^rapid_intel_.*\.pdf$'),
]

def is_report_file(filename):
    return any(p.match(filename) for p in REPORT_PATTERNS)

def get_latest_report(files):
    # Return the most recently modified file
    if not files:
        return None
    return max(files, key=lambda f: f.stat().st_mtime)

def clean_reports():
    for report_dir in REPORT_DIRS:
        dir_path = Path(report_dir)
        if not dir_path.exists() or not dir_path.is_dir():
            continue
        # Group files by base name (without extension)
        report_files = [f for f in dir_path.iterdir() if f.is_file() and is_report_file(f.name)]
        base_map = {}
        for f in report_files:
            base = re.sub(r'\.[^.]+$', '', f.name)
            base_map.setdefault(base, []).append(f)
        for base, files in base_map.items():
            if len(files) > 1:
                latest = get_latest_report(files)
                for f in files:
                    if f != latest:
                        print(f"Deleting duplicate: {f}")
                        f.unlink()

def main():
    clean_reports()
    print("Duplicate report cleanup complete.")

if __name__ == "__main__":
    main()

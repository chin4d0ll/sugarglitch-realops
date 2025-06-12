# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
import json
import sys
from pathlib import Path

def extract_dm_texts(report_path):
    with open(report_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    results = []
    # Walk through all successful_extractions
    def find_texts(obj, path=None):
        if path is None:
            path = []
        if isinstance(obj, dict):
            for k, v in obj.items():
                if k in ('text', 'message', 'messages', 'body') and isinstance(v, str):
                    results.append({'path': path + [k], 'text': v})
                else:
                    find_texts(v, path + [k])
        elif isinstance(obj, list):
            for i, v in enumerate(obj):
                find_texts(v, path + [str(i)])

    # Find all successful_extractions
    found = False
    for section in data.values():
        if isinstance(section, dict) and 'successful_extractions' in section:
            se = section['successful_extractions']
            if isinstance(se, list):
                for extraction in se:
                    if 'data' in extraction:
                        find_texts(extraction['data'], path=['data'])
                        found = True
    if not found and 'successful_extractions' in data:
        se = data['successful_extractions']
        if isinstance(se, list):
            for extraction in se:
                if 'data' in extraction:
                    find_texts(extraction['data'], path=['data'])

    return results

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extract_dm_texts_from_report.py <report.json>")
        sys.exit(1)
    report_path = sys.argv[1]
    results = extract_dm_texts(report_path)
    if not results:
        print("No DM text/message found.")
    else:
        for item in results:
            print(f"Path: {'/'.join(item['path'])}\nText: {item['text']}\n{'-'*40}")

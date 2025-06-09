# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
import matplotlib.pyplot as plt
from datetime import datetime
from collections import Counter

def generate_dm_timeline(dms: dict, output_png: str):
    """
    Parses DM JSON, counts messages per day, plots a line chart, and saves as PNG.
    Args:
        dms (dict): DM data, expects a list of messages under dms['messages'] or dms['conversations']
        output_png (str): Output PNG file path
    """
    # Try to find the list of messages
    messages = []
    if 'messages' in dms:
        messages = dms['messages']
    elif 'conversations' in dms:
        # If conversations, flatten all messages
        for conv in dms['conversations']:
            messages.extend(conv.get('messages', []))
    else:
        raise ValueError('No messages or conversations found in dms dict')

    # Extract date from each message (assume 'timestamp' in ms or s, or 'created_at' as ISO)
    dates = []
    for msg in messages:
        if 'created_at' in msg and msg['created_at']:
            try:
                dt = datetime.fromisoformat(msg['created_at'])
                dates.append(dt.date())
            except Exception:
                pass
        elif 'timestamp' in msg and msg['timestamp']:
            ts = msg['timestamp']
            # Heuristic: if ts > 10^12, it's in microseconds; if > 10^9, milliseconds; else seconds
            if ts > 1e12:
                ts = ts / 1_000_000  # microseconds to seconds
            elif ts > 1e10:
                ts = ts / 1_000  # milliseconds to seconds
            try:
                dt = datetime.fromtimestamp(ts)
                dates.append(dt.date())
            except Exception:
                pass
    if not dates:
        raise ValueError('No valid message dates found')

    # Count messages per day
    counter = Counter(dates)
    sorted_dates = sorted(counter)
    counts = [counter[d] for d in sorted_dates]

    # Plot
    plt.figure(figsize=(10, 5))
    plt.plot(sorted_dates, counts)
    plt.xlabel('Date')
    plt.ylabel('Message Count')
    plt.title('DM Timeline')
    plt.tight_layout()
    plt.savefig(output_png)
    plt.close()

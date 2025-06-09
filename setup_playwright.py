# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
import asyncio
from playwright.async_api import async_playwright
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, date
from collections import defaultdict
import json

def generate_dm_timeline(dms: dict, output_png: str):
    """
    Generate a timeline chart of DM messages per day.

    Args:
        dms (dict): Dictionary containing DM data with messages
        output_png (str): Path to save the output PNG chart
    """
    # Dictionary to count messages per day
    daily_counts = defaultdict(int)

    # Parse DMs to extract message dates
    try:
        # Handle different possible DM data structures
        messages = []

        if 'conversations' in dms:
            # Format: {"conversations": [{"messages": [...]}]}
            for conversation in dms['conversations']:
                if 'messages' in conversation:
                    messages.extend(conversation['messages'])
        elif 'messages' in dms:
            # Format: {"messages": [...]}
            messages = dms['messages']
        elif isinstance(dms, list):
            # Format: [{"timestamp": ..., ...}, ...]
            messages = dms
        else:
            # Try to find messages in any nested structure
            for key, value in dms.items():
                if isinstance(value, list) and value:
                    # Check if this looks like a message list
                    if any('timestamp' in item or 'created_at' in item or 'date' in item
                           for item in value if isinstance(item, dict)):
                        messages.extend(value)

        # Count messages per day
        for message in messages:
            if isinstance(message, dict):
                # Try different timestamp field names
                timestamp = None
                for field in ['timestamp', 'created_at', 'date', 'time']:
                    if field in message:
                        timestamp = message[field]
                        break

                if timestamp:
                    try:
                        # Handle different timestamp formats
                        if isinstance(timestamp, (int, float)):
                            # Unix timestamp (handle both seconds and milliseconds)
                            if timestamp > 1e10:  # Likely milliseconds
                                timestamp = timestamp / 1000
                            dt = datetime.fromtimestamp(timestamp)
                        elif isinstance(timestamp, str):
                            # ISO format string
                            if 'T' in timestamp:
                                dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                            else:
                                # Try to parse various date formats
                                for fmt in ['%Y-%m-%d', '%Y-%m-%d %H:%M:%S', '%m/%d/%Y']:
                                    try:
                                        dt = datetime.strptime(timestamp, fmt)
                                        break
                                    except ValueError:
                                        continue
                                else:
                                    continue  # Skip if no format matches
                        else:
                            continue  # Skip if timestamp type is unexpected

                        # Get date (without time) for grouping
                        message_date = dt.date()
                        daily_counts[message_date] += 1

                    except (ValueError, TypeError, OSError):
                        # Skip invalid timestamps
                        continue

        if not daily_counts:
            print("Warning: No valid timestamps found in DM data")
            # Create empty chart with message
            plt.figure(figsize=(10, 6))
            plt.text(0.5, 0.5, 'No message data found',
                    horizontalalignment='center', verticalalignment='center',
                    transform = plt.gca().transAxes, fontsize = 14)
            plt.title('DM Timeline - No Data Available')
            plt.savefig(output_png, dpi = 300, bbox_inches='tight')
            plt.close()
            return

        # Sort dates for proper timeline
        sorted_dates = sorted(daily_counts.keys())
        counts = [daily_counts[date] for date in sorted_dates]

        # Create the line chart
        plt.figure(figsize=(12, 6))
        plt.plot(sorted_dates, counts, marker='o', linewidth = 2, markersize = 4)

        # Format the chart
        plt.title('DM Messages Timeline', fontsize = 16, fontweight='bold')
        plt.xlabel('Date', fontsize = 12)
        plt.ylabel('Number of Messages', fontsize = 12)
        plt.grid(True, alpha = 0.3)

        # Format x-axis dates
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval = max(1, len(sorted_dates)//10)))
        plt.xticks(rotation = 45)

        # Add some statistics as text
        total_messages = sum(counts)
        total_days = len(sorted_dates)
        avg_messages = total_messages / total_days if total_days > 0 else 0

        stats_text = f'Total Messages: {total_messages}\nTotal Days: {total_days}\nAvg Messages/Day: {avg_messages:.1f}'
        plt.text(0.02, 0.98, stats_text, transform = plt.gca().transAxes,
                verticalalignment='top', bbox = dict(boxstyle='round', facecolor='white', alpha = 0.8))

        # Adjust layout and save
        plt.tight_layout()
        plt.savefig(output_png, dpi = 300, bbox_inches='tight')
        plt.close()

        print(f"✅ DM timeline chart saved to: {output_png}")
        print(f"📊 Statistics: {total_messages} messages across {total_days} days")

    except Exception as e:
        print(f"❌ Error generating DM timeline: {e}")
        # Create error chart
        plt.figure(figsize=(10, 6))
        plt.text(0.5, 0.5, f'Error generating chart:\n{str(e)}',
                horizontalalignment='center', verticalalignment='center',
                transform = plt.gca().transAxes, fontsize = 12)
        plt.title('DM Timeline - Error')
        plt.savefig(output_png, dpi = 300, bbox_inches='tight')
        plt.close()

def verify_playwright_installation():
    async def run():
        print("Installing Playwright and setting up Chromium...")
        # Launch Playwright
        async with async_playwright() as p:
            # Launch a headless browser
            print("Launching headless Chromium browser...")
            browser = await p.chromium.launch(headless = True)
            context = await browser.new_context()
            page = await context.new_page()

            # Navigate to a test page
            await page.goto("https://example.com")
            print("Page title:", await page.title())

            # Close the browser
            await browser.close()
            print("Playwright setup and verification complete.")

    asyncio.run(run())

if __name__ == "__main__":
    verify_playwright_installation()

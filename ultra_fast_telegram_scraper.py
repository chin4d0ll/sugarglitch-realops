#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📊 Ultra-Fast Telegram Scraper (Optimized Version)
เวอร์ชันที่เพิ่มประสิทธิภาพสูงสุดสำหรับการดึงข้อมูลสมาชิก

⚡ Performance Improvements:
- Concurrent batch processing
- Memory-efficient generators
- Optimized database operations
- Smart caching system
- Async file I/O
- Real-time progress tracking
"""

import asyncio
import aiosqlite
import aiofiles
import time
import json
from datetime import datetime
from typing import List, AsyncGenerator
from dataclasses import dataclass
import os

try:
    from rich.console import Console
    from rich.progress import Progress, TaskID
    from rich.table import Table
    from rich.panel import Panel
    console = Console()
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    console = type('MockConsole', (), {'print': print})()


@dataclass
class MemberData:
    """Optimized member data structure"""
    id: int
    username: str
    first_name: str
    last_name: str
    phone: str
    is_bot: bool
    is_premium: bool
    is_verified: bool
    status: str
    scraped_at: float


class UltraFastTelegramScraper:
    """Ultra-optimized Telegram member scraper"""

    def __init__(self, api_id: str, api_hash: str, phone: str):
        self.api_id = api_id
        self.api_hash = api_hash
        self.phone = phone

        # Performance settings
        self.batch_size = 200  # Telegram API limit
        self.concurrent_batches = 5  # Concurrent batch processing
        self.cache_size = 10000  # In-memory cache
        self.db_pool_size = 20

        # Statistics
        self.stats = {
            'total_scraped': 0,
            'cache_hits': 0,
            'db_operations': 0,
            'total_time': 0,
            'memory_peak': 0,
            'batches_processed': 0
        }

        self.client = None
        self.db_path = "ultra_fast_scraper.db"
        self.member_cache = {}

    async def initialize(self):
        """Initialize optimized connections and database"""
        try:
            from telethon import TelegramClient

            # Create optimized Telegram client
            self.client = TelegramClient(
                'ultra_fast_scraper_session',
                self.api_id,
                self.api_hash,
                connection_retries=5,
                retry_delay=1,
                auto_reconnect=True,
                flood_sleep_threshold=60
            )

            await self.client.start(phone=self.phone)

            # Initialize optimized database
            await self.setup_optimized_database()

            console.print("[green]⚡ Ultra-Fast Scraper initialized![/green]")
            return True

        except Exception as e:
            console.print(f"[red]❌ Initialization failed: {e}[/red]")
            return False

    async def setup_optimized_database(self):
        """Setup database with optimal indexes and settings"""
        async with aiosqlite.connect(self.db_path) as db:
            # Enable WAL mode for better concurrent access
            await db.execute("PRAGMA journal_mode=WAL")
            await db.execute("PRAGMA synchronous=NORMAL")
            await db.execute("PRAGMA cache_size=10000")
            await db.execute("PRAGMA temp_store=memory")

            # Create optimized members table
            await db.execute("""
                CREATE TABLE IF NOT EXISTS members (
                    id INTEGER PRIMARY KEY,
                    username TEXT,
                    first_name TEXT,
                    last_name TEXT,
                    phone TEXT,
                    is_bot BOOLEAN DEFAULT 0,
                    is_premium BOOLEAN DEFAULT 0,
                    is_verified BOOLEAN DEFAULT 0,
                    status TEXT,
                    group_id INTEGER,
                    scraped_at REAL,
                    updated_at REAL DEFAULT (julianday('now'))
                )
            """)

            # Create optimized indexes
            indexes = [
                "CREATE INDEX IF NOT EXISTS idx_username ON members(username)",
                "CREATE INDEX IF NOT EXISTS idx_phone ON members(phone)",
                "CREATE INDEX IF NOT EXISTS idx_group_id ON members(group_id)",
                "CREATE INDEX IF NOT EXISTS idx_scraped_at ON members(scraped_at)",
                "CREATE INDEX IF NOT EXISTS idx_is_bot ON members(is_bot)",
                "CREATE INDEX IF NOT EXISTS idx_is_premium ON members(is_premium)",
                "CREATE UNIQUE INDEX IF NOT EXISTS idx_user_group ON members(id, group_id)"
            ]

            for index_sql in indexes:
                await db.execute(index_sql)

            await db.commit()

    async def get_group_info_optimized(self, group_username: str) -> dict:
        """Get group info with caching"""
        cache_key = f"group_info_{group_username}"

        if cache_key in self.member_cache:
            self.stats['cache_hits'] += 1
            return self.member_cache[cache_key]

        try:
            from telethon.tl.functions.channels import GetFullChannelRequest

            group = await self.client.get_entity(group_username)
            full_group = await self.client(GetFullChannelRequest(group))

            info = {
                'id': group.id,
                'title': group.title,
                'username': group.username,
                'members_count': full_group.full_chat.participants_count,
                'description': full_group.full_chat.about or '',
                'is_megagroup': getattr(group, 'megagroup', False),
                'is_broadcast': getattr(group, 'broadcast', False)
            }

            # Cache the result
            self.member_cache[cache_key] = info

            return info

        except Exception as e:
            console.print(f"[red]❌ Failed to get group info: {e}[/red]")
            return None

    async def scrape_batch_optimized(self, group, offset: int) -> List[MemberData]:
        """Scrape a single batch with optimization"""
        from telethon.tl.functions.channels import GetParticipantsRequest
        from telethon.tl.types import ChannelParticipantsSearch

        try:
            participants = await self.client(GetParticipantsRequest(
                group,
                ChannelParticipantsSearch(''),
                offset,
                self.batch_size,
                hash=0
            ))

            if not participants.users:
                return []

            # Process users efficiently
            members = []
            current_time = time.time()

            for user in participants.users:
                # Parse user status efficiently
                status = self.parse_user_status_fast(user.status)

                member = MemberData(
                    id=user.id,
                    username=user.username or '',
                    first_name=user.first_name or '',
                    last_name=user.last_name or '',
                    phone=user.phone or '',
                    is_bot=getattr(user, 'bot', False),
                    is_premium=getattr(user, 'premium', False),
                    is_verified=getattr(user, 'verified', False),
                    status=status,
                    scraped_at=current_time
                )
                members.append(member)

            self.stats['batches_processed'] += 1
            return members

        except Exception as e:
            console.print(
                f"[yellow]⚠️ Batch error at offset {offset}: {e}[/yellow]")
            return []

    def parse_user_status_fast(self, status) -> str:
        """Fast user status parsing"""
        if not status:
            return 'unknown'

        status_name = status.__class__.__name__
        status_map = {
            'UserStatusOnline': 'online',
            'UserStatusOffline': 'offline',
            'UserStatusRecently': 'recently',
            'UserStatusLastWeek': 'last_week',
            'UserStatusLastMonth': 'last_month'
        }

        return status_map.get(status_name, 'unknown')

    async def bulk_insert_optimized(self, members: List[MemberData], group_id: int):
        """Optimized bulk database insert"""
        if not members:
            return

        async with aiosqlite.connect(self.db_path) as db:
            # Prepare data for bulk insert
            insert_data = [
                (
                    m.id, m.username, m.first_name, m.last_name, m.phone,
                    m.is_bot, m.is_premium, m.is_verified, m.status,
                    group_id, m.scraped_at
                )
                for m in members
            ]

            # Use INSERT OR REPLACE for upsert behavior
            await db.executemany("""
                INSERT OR REPLACE INTO members 
                (id, username, first_name, last_name, phone, is_bot, 
                 is_premium, is_verified, status, group_id, scraped_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, insert_data)

            await db.commit()
            self.stats['db_operations'] += 1

    async def scrape_members_ultra_fast(self, group_username: str,
                                        limit: int = 5000) -> AsyncGenerator[MemberData, None]:
        """Ultra-fast member scraping with async generator"""

        # Get group info
        group_info = await self.get_group_info_optimized(group_username)
        if not group_info:
            return

        group = await self.client.get_entity(group_username)

        console.print(Panel(
            f"🚀 [bold]Ultra-Fast Scraping Mode[/bold]\n\n"
            f"Group: {group_info['title']}\n"
            f"Total Members: {group_info['members_count']:,}\n"
            f"Target: {limit:,} members\n"
            f"Batch Size: {self.batch_size}",
            title="📊 Scraping Info",
            border_style="blue"
        ))

        # Calculate batches needed
        total_batches = min(limit // self.batch_size + 1,
                            group_info['members_count'] // self.batch_size + 1)

        if RICH_AVAILABLE:
            with Progress(console=console) as progress:
                task = progress.add_task(
                    "Scraping members...", total=total_batches)

                # Process batches concurrently
                scraped_count = 0
                for batch_start in range(0, limit, self.batch_size * self.concurrent_batches):

                    # Create concurrent batch tasks
                    batch_tasks = []
                    for i in range(self.concurrent_batches):
                        offset = batch_start + (i * self.batch_size)
                        if offset >= limit:
                            break

                        task_coroutine = self.scrape_batch_optimized(
                            group, offset)
                        batch_tasks.append(task_coroutine)

                    # Execute concurrent batches
                    if batch_tasks:
                        batch_results = await asyncio.gather(*batch_tasks, return_exceptions=True)

                        # Process results
                        for batch_members in batch_results:
                            if isinstance(batch_members, Exception):
                                continue

                            # Yield members one by one for memory efficiency
                            for member in batch_members:
                                if scraped_count >= limit:
                                    return
                                yield member
                                scraped_count += 1

                            # Bulk insert batch to database
                            await self.bulk_insert_optimized(batch_members, group_info['id'])

                        progress.advance(task, len(batch_tasks))

                    # Small delay to avoid overwhelming the API
                    await asyncio.sleep(1)
        else:
            # Fallback without rich
            scraped_count = 0
            for offset in range(0, limit, self.batch_size):
                console.print(f"Scraping batch at offset {offset}...")

                members = await self.scrape_batch_optimized(group, offset)

                for member in members:
                    if scraped_count >= limit:
                        return
                    yield member
                    scraped_count += 1

                await self.bulk_insert_optimized(members, group_info['id'])
                await asyncio.sleep(1)

    async def export_optimized(self, format_type: str = 'json', filename: str = None):
        """Export data in optimized way"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"ultra_fast_export_{timestamp}.{format_type}"

        async with aiosqlite.connect(self.db_path) as db:
            if format_type == 'json':
                await self.export_json_optimized(db, filename)
            elif format_type == 'csv':
                await self.export_csv_optimized(db, filename)
            else:
                console.print(
                    f"[red]❌ Unsupported format: {format_type}[/red]")

    async def export_json_optimized(self, db, filename: str):
        """Export to JSON with streaming"""
        async with aiofiles.open(filename, 'w', encoding='utf-8') as f:
            await f.write('[\n')

            first_record = True
            async with db.execute("SELECT * FROM members ORDER BY scraped_at DESC") as cursor:
                async for row in cursor:
                    if not first_record:
                        await f.write(',\n')

                    member_dict = {
                        'id': row[0],
                        'username': row[1],
                        'first_name': row[2],
                        'last_name': row[3],
                        'phone': row[4],
                        'is_bot': bool(row[5]),
                        'is_premium': bool(row[6]),
                        'is_verified': bool(row[7]),
                        'status': row[8],
                        'group_id': row[9],
                        'scraped_at': row[10]
                    }

                    await f.write(json.dumps(member_dict, ensure_ascii=False))
                    first_record = False

            await f.write('\n]')

        console.print(f"[green]💾 Exported to {filename}[/green]")

    async def export_csv_optimized(self, db, filename: str):
        """Export to CSV efficiently"""
        async with aiofiles.open(filename, 'w', encoding='utf-8') as f:
            # Write header
            await f.write('id,username,first_name,last_name,phone,is_bot,is_premium,is_verified,status,group_id,scraped_at\n')

            # Write data
            async with db.execute("SELECT * FROM members ORDER BY scraped_at DESC") as cursor:
                async for row in cursor:
                    csv_row = ','.join([
                        str(row[0]),  # id
                        f'"{row[1] or ""}"',  # username
                        f'"{row[2] or ""}"',  # first_name
                        f'"{row[3] or ""}"',  # last_name
                        f'"{row[4] or ""}"',  # phone
                        str(row[5]),  # is_bot
                        str(row[6]),  # is_premium
                        str(row[7]),  # is_verified
                        f'"{row[8] or ""}"',  # status
                        str(row[9]),  # group_id
                        str(row[10])  # scraped_at
                    ])
                    await f.write(csv_row + '\n')

        console.print(f"[green]💾 Exported to {filename}[/green]")

    async def get_statistics(self) -> dict:
        """Get scraping statistics"""
        async with aiosqlite.connect(self.db_path) as db:
            stats = {}

            # Total members
            async with db.execute("SELECT COUNT(*) FROM members") as cursor:
                stats['total_members'] = (await cursor.fetchone())[0]

            # Members by type
            async with db.execute("SELECT COUNT(*) FROM members WHERE is_bot = 1") as cursor:
                stats['bots'] = (await cursor.fetchone())[0]

            async with db.execute("SELECT COUNT(*) FROM members WHERE is_premium = 1") as cursor:
                stats['premium_users'] = (await cursor.fetchone())[0]

            async with db.execute("SELECT COUNT(*) FROM members WHERE is_verified = 1") as cursor:
                stats['verified_users'] = (await cursor.fetchone())[0]

            # Recent activity
            async with db.execute("""
                SELECT COUNT(*) FROM members 
                WHERE scraped_at > (julianday('now') - 1) * 86400
            """) as cursor:
                stats['scraped_today'] = (await cursor.fetchone())[0]

            return stats

    async def display_performance_report(self):
        """Display performance statistics"""
        db_stats = await self.get_statistics()

        if RICH_AVAILABLE:
            table = Table(title="📊 Ultra-Fast Scraper Performance")
            table.add_column("Metric", style="cyan")
            table.add_column("Value", style="green")
            table.add_column("Performance", style="yellow")

            # Performance ratings
            speed = self.stats['total_scraped'] / \
                self.stats['total_time'] if self.stats['total_time'] > 0 else 0
            speed_rating = "🟢 Excellent" if speed > 50 else "🟡 Good" if speed > 20 else "🔴 Slow"

            table.add_row("Total Scraped", str(
                self.stats['total_scraped']), "📈")
            table.add_row("Scraping Speed",
                          f"{speed:.1f} users/s", speed_rating)
            table.add_row("Cache Hits", str(self.stats['cache_hits']), "💾")
            table.add_row("DB Operations", str(
                self.stats['db_operations']), "💿")
            table.add_row("Batches Processed", str(
                self.stats['batches_processed']), "📦")
            table.add_row(
                "Total Time", f"{self.stats['total_time']:.2f}s", "⏱️")

            table.add_row("", "", "")  # Separator
            table.add_row("Total in DB", str(db_stats['total_members']), "📊")
            table.add_row("Bots Found", str(db_stats['bots']), "🤖")
            table.add_row("Premium Users", str(db_stats['premium_users']), "⭐")
            table.add_row("Verified Users", str(
                db_stats['verified_users']), "✅")

            console.print(table)
        else:
            console.print("\n📊 Performance Report:")
            console.print(f"Total Scraped: {self.stats['total_scraped']}")
            console.print(f"Total Time: {self.stats['total_time']:.2f}s")
            console.print(f"Speed: {speed:.1f} users/s")

    async def cleanup(self):
        """Clean up connections"""
        if self.client:
            await self.client.disconnect()
        console.print("[blue]🧹 Cleanup completed[/blue]")


# Demo function
async def demo_ultra_fast_scraper():
    """Demo the ultra-fast scraper"""

    API_ID = 'your_api_id'
    API_HASH = 'your_api_hash'
    PHONE = '+66xxxxxxxxx'

    if API_ID == 'your_api_id':
        console.print("[red]❌ Please configure API credentials first![/red]")
        return

    scraper = UltraFastTelegramScraper(API_ID, API_HASH, PHONE)

    try:
        if not await scraper.initialize():
            return

        group_username = '@your_target_group'  # Replace with real group
        limit = 1000

        start_time = time.time()

        console.print(f"[blue]🎯 Target: {group_username}[/blue]")
        console.print(f"[blue]📊 Limit: {limit} members[/blue]")

        # Scrape members
        scraped_count = 0
        async for member in scraper.scrape_members_ultra_fast(group_username, limit):
            scraped_count += 1
            scraper.stats['total_scraped'] = scraped_count

        end_time = time.time()
        scraper.stats['total_time'] = end_time - start_time

        # Display results
        await scraper.display_performance_report()

        # Export data
        await scraper.export_optimized('json')
        await scraper.export_optimized('csv')

        console.print("[green]🎉 Ultra-fast scraping completed![/green]")

    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")
    finally:
        await scraper.cleanup()


async def main():
    """Main function"""
    console.print(
        Panel.fit("📊 Ultra-Fast Telegram Scraper", style="bold blue"))

    await demo_ultra_fast_scraper()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        console.print("\n[yellow]⏹️ Interrupted by user[/yellow]")
    except Exception as e:
        console.print(f"\n[red]❌ Error: {e}[/red]")

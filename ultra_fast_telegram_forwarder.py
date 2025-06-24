#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔄 Ultra-Fast Telegram Forwarder (Optimized Version)
เวอร์ชันที่เพิ่มประสิทธิภาพสูงสุดสำหรับการ Forward ข้อความ

⚡ Performance Improvements:
- Async batch forwarding
- Smart rate limiting with adaptive backoff
- Memory-efficient message queuing
- Database logging with connection pooling
- Real-time progress tracking
- Error resilience with retry logic
"""

import asyncio
import aiosqlite
import aiofiles
import time
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional, AsyncGenerator
from dataclasses import dataclass, asdict
from enum import Enum
import random

try:
    from rich.console import Console
    from rich.progress import Progress, BarColumn, TextColumn, TimeElapsedColumn
    from rich.table import Table
    from rich.panel import Panel
    from rich.live import Live
    from rich.layout import Layout
    console = Console()
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    console = type('MockConsole', (), {'print': print})()


class ForwardStatus(Enum):
    """Forward status enumeration"""
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"
    RATE_LIMITED = "rate_limited"
    FILTERED = "filtered"


@dataclass
class ForwardTask:
    """Optimized forward task structure"""
    id: str
    source_chat: str
    target_chat: str
    message_id: int
    scheduled_at: float
    priority: int = 1
    retry_count: int = 0
    status: ForwardStatus = ForwardStatus.PENDING
    error_message: str = ""
    forwarded_at: Optional[float] = None


@dataclass
class ForwardStats:
    """Forward statistics tracking"""
    total_tasks: int = 0
    completed: int = 0
    failed: int = 0
    rate_limited: int = 0
    filtered: int = 0
    start_time: float = 0
    current_rate: float = 0
    estimated_completion: Optional[float] = None


class UltraFastTelegramForwarder:
    """Ultra-optimized Telegram message forwarder"""

    def __init__(self, api_id: str, api_hash: str, phone: str):
        self.api_id = api_id
        self.api_hash = api_hash
        self.phone = phone

        # Performance settings
        self.max_concurrent_forwards = 10  # Concurrent forward operations
        self.base_delay = 1.0  # Base delay between forwards
        self.max_delay = 30.0  # Maximum delay for rate limiting
        self.batch_size = 50  # Batch processing size
        self.retry_limit = 3  # Maximum retry attempts

        # Adaptive rate limiting
        self.current_delay = self.base_delay
        self.success_streak = 0
        self.rate_limit_cooldown = 0

        # State management
        self.client = None
        self.db_path = "ultra_fast_forwarder.db"
        self.task_queue = asyncio.Queue()
        self.stats = ForwardStats()
        self.is_running = False

        # Cache for chat entities
        self.chat_cache = {}
        self.user_cache = {}

    async def initialize(self):
        """Initialize optimized connections and database"""
        try:
            from telethon import TelegramClient

            # Create optimized Telegram client
            self.client = TelegramClient(
                'ultra_fast_forwarder_session',
                self.api_id,
                self.api_hash,
                connection_retries=5,
                retry_delay=2,
                auto_reconnect=True,
                flood_sleep_threshold=60,
                request_retries=3
            )

            await self.client.start(phone=self.phone)

            # Initialize optimized database
            await self.setup_optimized_database()

            console.print("[green]⚡ Ultra-Fast Forwarder initialized![/green]")
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
            await db.execute("PRAGMA cache_size=20000")
            await db.execute("PRAGMA temp_store=memory")
            await db.execute("PRAGMA mmap_size=268435456")  # 256MB

            # Create forward tasks table
            await db.execute("""
                CREATE TABLE IF NOT EXISTS forward_tasks (
                    id TEXT PRIMARY KEY,
                    source_chat TEXT NOT NULL,
                    target_chat TEXT NOT NULL,
                    message_id INTEGER NOT NULL,
                    scheduled_at REAL NOT NULL,
                    priority INTEGER DEFAULT 1,
                    retry_count INTEGER DEFAULT 0,
                    status TEXT DEFAULT 'pending',
                    error_message TEXT,
                    forwarded_at REAL,
                    created_at REAL DEFAULT (julianday('now')),
                    updated_at REAL DEFAULT (julianday('now'))
                )
            """)

            # Create forward logs table
            await db.execute("""
                CREATE TABLE IF NOT EXISTS forward_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task_id TEXT NOT NULL,
                    source_chat TEXT NOT NULL,
                    target_chat TEXT NOT NULL,
                    message_id INTEGER NOT NULL,
                    success BOOLEAN NOT NULL,
                    response_time REAL,
                    error_message TEXT,
                    timestamp REAL DEFAULT (julianday('now')),
                    FOREIGN KEY (task_id) REFERENCES forward_tasks (id)
                )
            """)

            # Create performance-optimized indexes
            indexes = [
                "CREATE INDEX IF NOT EXISTS idx_task_status ON forward_tasks(status)",
                "CREATE INDEX IF NOT EXISTS idx_task_scheduled ON forward_tasks(scheduled_at)",
                "CREATE INDEX IF NOT EXISTS idx_task_priority ON forward_tasks(priority DESC)",
                "CREATE INDEX IF NOT EXISTS idx_task_source ON forward_tasks(source_chat)",
                "CREATE INDEX IF NOT EXISTS idx_task_target ON forward_tasks(target_chat)",
                "CREATE INDEX IF NOT EXISTS idx_log_timestamp ON forward_logs(timestamp)",
                "CREATE INDEX IF NOT EXISTS idx_log_success ON forward_logs(success)",
                "CREATE INDEX IF NOT EXISTS idx_log_task ON forward_logs(task_id)"
            ]

            for index_sql in indexes:
                await db.execute(index_sql)

            await db.commit()

    async def get_chat_entity_cached(self, chat_identifier: str):
        """Get chat entity with caching"""
        if chat_identifier in self.chat_cache:
            return self.chat_cache[chat_identifier]

        try:
            entity = await self.client.get_entity(chat_identifier)
            self.chat_cache[chat_identifier] = entity
            return entity
        except Exception as e:
            console.print(
                f"[red]❌ Failed to get chat {chat_identifier}: {e}[/red]")
            return None

    async def add_forward_task(self, source_chat: str, target_chat: str,
                               message_id: int, priority: int = 1,
                               delay_seconds: int = 0) -> str:
        """Add a forward task to the queue"""
        task_id = f"task_{int(time.time() * 1000)}_{random.randint(1000, 9999)}"
        scheduled_at = time.time() + delay_seconds

        task = ForwardTask(
            id=task_id,
            source_chat=source_chat,
            target_chat=target_chat,
            message_id=message_id,
            scheduled_at=scheduled_at,
            priority=priority
        )

        # Save to database
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                INSERT INTO forward_tasks 
                (id, source_chat, target_chat, message_id, scheduled_at, priority)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (task_id, source_chat, target_chat, message_id, scheduled_at, priority))
            await db.commit()

        # Add to queue
        await self.task_queue.put(task)
        self.stats.total_tasks += 1

        return task_id

    async def add_bulk_forward_tasks(self, tasks: List[Dict]) -> List[str]:
        """Add multiple forward tasks efficiently"""
        task_ids = []
        db_data = []

        for task_data in tasks:
            task_id = f"bulk_{int(time.time() * 1000)}_{random.randint(1000, 9999)}"
            scheduled_at = time.time() + task_data.get('delay_seconds', 0)

            task = ForwardTask(
                id=task_id,
                source_chat=task_data['source_chat'],
                target_chat=task_data['target_chat'],
                message_id=task_data['message_id'],
                scheduled_at=scheduled_at,
                priority=task_data.get('priority', 1)
            )

            db_data.append((
                task_id, task_data['source_chat'], task_data['target_chat'],
                task_data['message_id'], scheduled_at, task_data.get(
                    'priority', 1)
            ))

            await self.task_queue.put(task)
            task_ids.append(task_id)

        # Bulk insert to database
        async with aiosqlite.connect(self.db_path) as db:
            await db.executemany("""
                INSERT INTO forward_tasks 
                (id, source_chat, target_chat, message_id, scheduled_at, priority)
                VALUES (?, ?, ?, ?, ?, ?)
            """, db_data)
            await db.commit()

        self.stats.total_tasks += len(task_ids)
        console.print(
            f"[green]📦 Added {len(task_ids)} bulk forward tasks[/green]")

        return task_ids

    async def forward_single_message(self, task: ForwardTask) -> bool:
        """Forward a single message with optimization"""
        try:
            # Check if it's time to process
            if time.time() < task.scheduled_at:
                await asyncio.sleep(task.scheduled_at - time.time())

            # Get chat entities
            source_entity = await self.get_chat_entity_cached(task.source_chat)
            target_entity = await self.get_chat_entity_cached(task.target_chat)

            if not source_entity or not target_entity:
                raise Exception("Failed to get chat entities")

            # Adaptive rate limiting
            if self.rate_limit_cooldown > time.time():
                await asyncio.sleep(self.rate_limit_cooldown - time.time())

            start_time = time.time()

            # Forward the message
            await self.client.forward_messages(
                entity=target_entity,
                messages=task.message_id,
                from_peer=source_entity
            )

            response_time = time.time() - start_time

            # Update success statistics
            self.success_streak += 1
            # Decrease delay on success
            self.current_delay = max(self.base_delay * 0.9, 0.5)

            # Log success
            await self.log_forward_result(task, True, response_time)

            # Update task status
            task.status = ForwardStatus.SUCCESS
            task.forwarded_at = time.time()
            await self.update_task_status(task)

            self.stats.completed += 1

            return True

        except Exception as e:
            error_msg = str(e).lower()

            # Handle different types of errors
            if "flood" in error_msg or "too many requests" in error_msg:
                await self.handle_rate_limit(task, e)
                return False

            elif "chat_write_forbidden" in error_msg or "forbidden" in error_msg:
                task.status = ForwardStatus.FILTERED
                task.error_message = str(e)
                await self.update_task_status(task)
                self.stats.filtered += 1
                return False

            else:
                # Generic error handling with retry
                return await self.handle_forward_error(task, e)

    async def handle_rate_limit(self, task: ForwardTask, error: Exception):
        """Handle rate limiting intelligently"""
        self.success_streak = 0
        self.current_delay = min(self.current_delay * 2, self.max_delay)
        self.rate_limit_cooldown = time.time() + self.current_delay

        # Extract wait time from error if available
        error_str = str(error)
        if "seconds" in error_str:
            import re
            wait_match = re.search(r'(\d+)\s*seconds?', error_str)
            if wait_match:
                wait_time = int(wait_match.group(1))
                self.rate_limit_cooldown = time.time() + wait_time + 5

        task.status = ForwardStatus.RATE_LIMITED
        task.error_message = str(error)
        task.scheduled_at = self.rate_limit_cooldown + random.uniform(1, 5)

        await self.update_task_status(task)
        await self.task_queue.put(task)  # Re-queue the task

        self.stats.rate_limited += 1

        console.print(
            f"[yellow]⏳ Rate limited, waiting {self.current_delay:.1f}s[/yellow]")

    async def handle_forward_error(self, task: ForwardTask, error: Exception) -> bool:
        """Handle generic forward errors with retry logic"""
        task.retry_count += 1

        if task.retry_count <= self.retry_limit:
            # Exponential backoff for retries
            retry_delay = (2 ** task.retry_count) + random.uniform(1, 3)
            task.scheduled_at = time.time() + retry_delay
            task.status = ForwardStatus.PENDING
            task.error_message = f"Retry {task.retry_count}/{self.retry_limit}: {str(error)}"

            await self.update_task_status(task)
            await self.task_queue.put(task)  # Re-queue for retry

            console.print(
                f"[yellow]🔄 Retrying task {task.id} in {retry_delay:.1f}s[/yellow]")
            return False
        else:
            # Max retries exceeded
            task.status = ForwardStatus.FAILED
            task.error_message = f"Max retries exceeded: {str(error)}"

            await self.update_task_status(task)
            await self.log_forward_result(task, False, 0, str(error))

            self.stats.failed += 1
            return False

    async def log_forward_result(self, task: ForwardTask, success: bool,
                                 response_time: float, error_message: str = ""):
        """Log forward result to database"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                INSERT INTO forward_logs 
                (task_id, source_chat, target_chat, message_id, success, 
                 response_time, error_message)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (task.id, task.source_chat, task.target_chat, task.message_id,
                  success, response_time, error_message))
            await db.commit()

    async def update_task_status(self, task: ForwardTask):
        """Update task status in database"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                UPDATE forward_tasks 
                SET status = ?, error_message = ?, forwarded_at = ?, 
                    retry_count = ?, scheduled_at = ?, updated_at = julianday('now')
                WHERE id = ?
            """, (task.status.value, task.error_message, task.forwarded_at,
                  task.retry_count, task.scheduled_at, task.id))
            await db.commit()

    async def worker_coroutine(self, worker_id: int):
        """Worker coroutine for concurrent processing"""
        while self.is_running:
            try:
                # Get task from queue with timeout
                task = await asyncio.wait_for(self.task_queue.get(), timeout=5.0)

                # Process the task
                success = await self.forward_single_message(task)

                # Mark task as done
                self.task_queue.task_done()

                # Adaptive delay between operations
                if success:
                    await asyncio.sleep(self.current_delay)
                else:
                    await asyncio.sleep(self.current_delay * 2)

            except asyncio.TimeoutError:
                # No tasks available, continue
                continue
            except Exception as e:
                console.print(f"[red]❌ Worker {worker_id} error: {e}[/red]")
                await asyncio.sleep(5)

    async def start_processing(self, num_workers: int = None):
        """Start processing forward tasks with multiple workers"""
        if num_workers is None:
            num_workers = self.max_concurrent_forwards

        self.is_running = True
        self.stats.start_time = time.time()

        console.print(
            f"[blue]🚀 Starting {num_workers} forward workers...[/blue]")

        # Create worker tasks
        workers = []
        for i in range(num_workers):
            worker = asyncio.create_task(self.worker_coroutine(i))
            workers.append(worker)

        try:
            if RICH_AVAILABLE:
                await self.run_with_rich_progress(workers)
            else:
                await self.run_with_simple_progress(workers)
        finally:
            # Stop workers
            self.is_running = False

            # Cancel remaining worker tasks
            for worker in workers:
                worker.cancel()

            # Wait for workers to finish
            await asyncio.gather(*workers, return_exceptions=True)

    async def run_with_rich_progress(self, workers):
        """Run with rich progress display"""
        layout = Layout()
        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="progress"),
            Layout(name="stats", size=10)
        )

        with Live(layout, refresh_per_second=2, console=console) as live:
            # Progress bar
            with Progress(
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                TextColumn("({task.completed}/{task.total})"),
                TimeElapsedColumn()
            ) as progress:

                task_progress = progress.add_task(
                    "Forwarding messages...",
                    total=self.stats.total_tasks
                )

                layout["progress"].update(progress)

                while self.is_running and not self.task_queue.empty():
                    # Update progress
                    completed = self.stats.completed + self.stats.failed + self.stats.filtered
                    progress.update(task_progress, completed=completed)

                    # Update header
                    layout["header"].update(Panel(
                        f"🔄 Ultra-Fast Telegram Forwarder | "
                        f"Queue: {self.task_queue.qsize()} | "
                        f"Rate: {self.calculate_current_rate():.1f}/min",
                        style="bold blue"
                    ))

                    # Update stats
                    layout["stats"].update(self.create_stats_table())

                    await asyncio.sleep(1)

    async def run_with_simple_progress(self, workers):
        """Run with simple text progress"""
        while self.is_running and not self.task_queue.empty():
            completed = self.stats.completed + self.stats.failed + self.stats.filtered
            rate = self.calculate_current_rate()

            console.print(
                f"Progress: {completed}/{self.stats.total_tasks} | "
                f"Queue: {self.task_queue.qsize()} | "
                f"Rate: {rate:.1f}/min | "
                f"Success: {self.stats.completed} | "
                f"Failed: {self.stats.failed}"
            )

            await asyncio.sleep(5)

    def calculate_current_rate(self) -> float:
        """Calculate current forwarding rate per minute"""
        if self.stats.start_time == 0:
            return 0.0

        elapsed = time.time() - self.stats.start_time
        if elapsed == 0:
            return 0.0

        completed = self.stats.completed + self.stats.failed + self.stats.filtered
        return (completed / elapsed) * 60  # Per minute

    def create_stats_table(self) -> Table:
        """Create statistics table"""
        table = Table(title="📊 Forward Statistics")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        table.add_column("Percentage", style="yellow")

        total_processed = self.stats.completed + \
            self.stats.failed + self.stats.filtered

        if total_processed > 0:
            success_rate = (self.stats.completed / total_processed) * 100
            fail_rate = (self.stats.failed / total_processed) * 100
            filter_rate = (self.stats.filtered / total_processed) * 100
        else:
            success_rate = fail_rate = filter_rate = 0

        table.add_row("Total Tasks", str(self.stats.total_tasks), "")
        table.add_row("Completed", str(self.stats.completed),
                      f"{success_rate:.1f}%")
        table.add_row("Failed", str(self.stats.failed), f"{fail_rate:.1f}%")
        table.add_row("Filtered", str(self.stats.filtered),
                      f"{filter_rate:.1f}%")
        table.add_row("Rate Limited", str(self.stats.rate_limited), "")
        table.add_row("Queue Size", str(self.task_queue.qsize()), "")
        table.add_row("Current Rate",
                      f"{self.calculate_current_rate():.1f}/min", "")
        table.add_row("Current Delay", f"{self.current_delay:.1f}s", "")

        return table

    async def export_results(self, filename: str = None):
        """Export forwarding results"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"forward_results_{timestamp}.json"

        async with aiosqlite.connect(self.db_path) as db:
            # Get all tasks
            tasks = []
            async with db.execute("""
                SELECT * FROM forward_tasks ORDER BY created_at DESC
            """) as cursor:
                async for row in cursor:
                    task_data = {
                        'id': row[0],
                        'source_chat': row[1],
                        'target_chat': row[2],
                        'message_id': row[3],
                        'scheduled_at': row[4],
                        'priority': row[5],
                        'retry_count': row[6],
                        'status': row[7],
                        'error_message': row[8],
                        'forwarded_at': row[9],
                        'created_at': row[10],
                        'updated_at': row[11]
                    }
                    tasks.append(task_data)

            # Get logs
            logs = []
            async with db.execute("""
                SELECT * FROM forward_logs ORDER BY timestamp DESC LIMIT 1000
            """) as cursor:
                async for row in cursor:
                    log_data = {
                        'id': row[0],
                        'task_id': row[1],
                        'source_chat': row[2],
                        'target_chat': row[3],
                        'message_id': row[4],
                        'success': bool(row[5]),
                        'response_time': row[6],
                        'error_message': row[7],
                        'timestamp': row[8]
                    }
                    logs.append(log_data)

        # Create export data
        export_data = {
            'summary': asdict(self.stats),
            'tasks': tasks,
            'logs': logs,
            'exported_at': time.time(),
            'performance_metrics': {
                'current_rate_per_minute': self.calculate_current_rate(),
                'current_delay': self.current_delay,
                'success_streak': self.success_streak,
                'rate_limit_cooldown': self.rate_limit_cooldown
            }
        }

        # Write to file
        async with aiofiles.open(filename, 'w', encoding='utf-8') as f:
            await f.write(json.dumps(export_data, indent=2, ensure_ascii=False))

        console.print(f"[green]💾 Results exported to {filename}[/green]")

    async def cleanup(self):
        """Clean up connections and resources"""
        self.is_running = False

        if self.client:
            await self.client.disconnect()

        console.print("[blue]🧹 Cleanup completed[/blue]")


# Demo function
async def demo_ultra_fast_forwarder():
    """Demo the ultra-fast forwarder"""

    API_ID = 'your_api_id'
    API_HASH = 'your_api_hash'
    PHONE = '+66xxxxxxxxx'

    if API_ID == 'your_api_id':
        console.print("[red]❌ Please configure API credentials first![/red]")
        return

    forwarder = UltraFastTelegramForwarder(API_ID, API_HASH, PHONE)

    try:
        if not await forwarder.initialize():
            return

        # Example: Add some forward tasks
        source_chat = '@source_channel'
        target_chat = '@target_channel'

        # Add individual tasks
        await forwarder.add_forward_task(source_chat, target_chat, 12345, priority=1)
        await forwarder.add_forward_task(source_chat, target_chat, 12346, priority=2)

        # Add bulk tasks
        bulk_tasks = [
            {
                'source_chat': source_chat,
                'target_chat': target_chat,
                'message_id': 12347 + i,
                'priority': 1,
                'delay_seconds': i * 2
            }
            for i in range(10)
        ]

        await forwarder.add_bulk_forward_tasks(bulk_tasks)

        console.print(
            f"[blue]📋 Total tasks queued: {forwarder.stats.total_tasks}[/blue]")

        # Start processing
        await forwarder.start_processing(num_workers=5)

        # Export results
        await forwarder.export_results()

        console.print("[green]🎉 Forward processing completed![/green]")

    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")
    finally:
        await forwarder.cleanup()


async def main():
    """Main function"""
    console.print(
        Panel.fit("🔄 Ultra-Fast Telegram Forwarder", style="bold blue"))

    await demo_ultra_fast_forwarder()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        console.print("\n[yellow]⏹️ Interrupted by user[/yellow]")
    except Exception as e:
        console.print(f"\n[red]❌ Error: {e}[/red]")

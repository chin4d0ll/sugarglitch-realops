#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 ASYNC CORE ENGINE - SugarGlitch RealOps v2.0
High-performance async foundation for all operations
"""

import asyncio
import aiohttp
import aiofiles
import time
import logging
from typing import Any, Dict, List, Optional, Union, Callable, AsyncGenerator
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
import json
import weakref
from contextlib import asynccontextmanager
import signal
import ssl
from concurrent.futures import ThreadPoolExecutor
from functools import wraps, partial
import traceback

# Rich imports for UI
try:
    from rich.console import Console
    from rich.progress import Progress, TaskID, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
    from rich.table import Table
    from rich.panel import Panel
    from rich.live import Live
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

console = Console() if RICH_AVAILABLE else None


@dataclass
class AsyncConfig:
    """🔧 Async performance configuration"""
    max_concurrent_requests: int = 50
    max_concurrent_tasks: int = 100
    request_timeout: int = 30
    connect_timeout: int = 10
    pool_limit: int = 100
    pool_limit_per_host: int = 30
    rate_limit_calls: int = 100
    rate_limit_period: int = 60
    retry_attempts: int = 3
    retry_backoff: float = 1.5
    chunk_size: int = 8192
    memory_limit_mb: int = 512
    enable_compression: bool = True
    enable_keepalive: bool = True
    ssl_verify: bool = False


@dataclass
class RequestMetrics:
    """📊 Request performance metrics"""
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    rate_limited: int = 0
    timeouts: int = 0
    start_time: float = field(default_factory=time.time)
    total_bytes: int = 0
    avg_response_time: float = 0.0
    requests_per_second: float = 0.0


class AsyncRateLimiter:
    """⏱️ High-performance async rate limiter with token bucket"""
    
    def __init__(self, calls: int, period: int):
        self.calls = calls
        self.period = period
        self.tokens = calls
        self.last_update = time.time()
        self._lock = asyncio.Lock()
        
    async def acquire(self) -> None:
        """Acquire rate limit token"""
        async with self._lock:
            now = time.time()
            # Add tokens based on elapsed time
            elapsed = now - self.last_update
            self.tokens = min(self.calls, self.tokens + elapsed * (self.calls / self.period))
            self.last_update = now
            
            if self.tokens >= 1:
                self.tokens -= 1
                return
            
            # Wait for next token
            wait_time = (1 - self.tokens) * (self.period / self.calls)
            await asyncio.sleep(wait_time)
            self.tokens = 0


class AsyncSessionManager:
    """🔗 Advanced async HTTP session manager with connection pooling"""
    
    def __init__(self, config: AsyncConfig):
        self.config = config
        self.session: Optional[aiohttp.ClientSession] = None
        self.rate_limiter = AsyncRateLimiter(config.rate_limit_calls, config.rate_limit_period)
        self.semaphore = asyncio.Semaphore(config.max_concurrent_requests)
        self.metrics = RequestMetrics()
        self._closed = False
        
    async def __aenter__(self):
        await self.start()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
        
    async def start(self) -> None:
        """Initialize async session with optimized settings"""
        if self.session and not self.session.closed:
            return
            
        # SSL context for performance
        ssl_context = ssl.create_default_context()
        if not self.config.ssl_verify:
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
            
        # Connection settings
        connector = aiohttp.TCPConnector(
            limit=self.config.pool_limit,
            limit_per_host=self.config.pool_limit_per_host,
            ssl=ssl_context,
            enable_cleanup_closed=True,
            keepalive_timeout=30,
            ttl_dns_cache=300
        )
        
        # Timeout settings
        timeout = aiohttp.ClientTimeout(
            total=self.config.request_timeout,
            connect=self.config.connect_timeout
        )
        
        # Session with compression
        self.session = aiohttp.ClientSession(
            connector=connector,
            timeout=timeout,
            headers={
                'Accept-Encoding': 'gzip, deflate, br' if self.config.enable_compression else None,
                'Connection': 'keep-alive' if self.config.enable_keepalive else 'close'
            }
        )
        
    async def close(self) -> None:
        """Gracefully close session"""
        if self.session and not self.session.closed:
            await self.session.close()
            # Wait for connections to close
            await asyncio.sleep(0.1)
        self._closed = True
        
    async def request(
        self, 
        method: str, 
        url: str, 
        headers: Optional[Dict] = None,
        data: Optional[Union[str, bytes, Dict]] = None,
        json_data: Optional[Dict] = None,
        **kwargs
    ) -> Optional[aiohttp.ClientResponse]:
        """Make optimized async HTTP request with rate limiting"""
        if self._closed or not self.session:
            await self.start()
            
        await self.rate_limiter.acquire()
        
        async with self.semaphore:
            start_time = time.time()
            
            try:
                self.metrics.total_requests += 1
                
                async with self.session.request(
                    method, 
                    url, 
                    headers=headers,
                    data=data,
                    json=json_data,
                    **kwargs
                ) as response:
                    # Update metrics
                    response_time = time.time() - start_time
                    self.metrics.avg_response_time = (
                        (self.metrics.avg_response_time * (self.metrics.total_requests - 1) + response_time) 
                        / self.metrics.total_requests
                    )
                    
                    if response.status == 200:
                        self.metrics.successful_requests += 1
                    elif response.status == 429:
                        self.metrics.rate_limited += 1
                    else:
                        self.metrics.failed_requests += 1
                        
                    return response
                    
            except asyncio.TimeoutError:
                self.metrics.timeouts += 1
                self.metrics.failed_requests += 1
                return None
            except Exception as e:
                self.metrics.failed_requests += 1
                logging.debug(f"Request failed: {e}")
                return None


class AsyncFileManager:
    """📁 High-performance async file operations"""
    
    def __init__(self, chunk_size: int = 8192):
        self.chunk_size = chunk_size
        
    @asynccontextmanager
    async def open_file(self, filepath: Path, mode: str = 'r', encoding: str = 'utf-8'):
        """Async context manager for file operations"""
        async with aiofiles.open(filepath, mode=mode, encoding=encoding) as f:
            yield f
            
    async def write_json_streaming(self, filepath: Path, data: AsyncGenerator, indent: int = 2) -> None:
        """Stream write large JSON data to avoid memory issues"""
        async with self.open_file(filepath, 'w') as f:
            await f.write('[\n')
            
            first_item = True
            async for item in data:
                if not first_item:
                    await f.write(',\n')
                first_item = False
                
                json_str = json.dumps(item, indent=indent, ensure_ascii=False)
                await f.write(json_str)
                
            await f.write('\n]')
            
    async def read_lines_streaming(self, filepath: Path) -> AsyncGenerator[str, None]:
        """Stream read file lines to avoid loading entire file in memory"""
        async with self.open_file(filepath, 'r') as f:
            async for line in f:
                yield line.strip()


class AsyncTaskManager:
    """🎯 Advanced async task orchestration with progress tracking"""
    
    def __init__(self, max_concurrent: int = 100):
        self.max_concurrent = max_concurrent
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.tasks: List[asyncio.Task] = []
        self.completed_tasks = 0
        self.failed_tasks = 0
        self.progress: Optional[Progress] = None
        self.task_id: Optional[TaskID] = None
        
    async def __aenter__(self):
        if RICH_AVAILABLE:
            self.progress = Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                TimeElapsedColumn(),
                console=console
            )
            self.progress.__enter__()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.wait_all()
        if self.progress:
            self.progress.__exit__(exc_type, exc_val, exc_tb)
            
    async def add_task(self, coro, description: str = "Processing...") -> None:
        """Add async task with concurrency control"""
        if self.progress and not self.task_id:
            self.task_id = self.progress.add_task(description, total=None)
            
        async def controlled_task():
            async with self.semaphore:
                try:
                    result = await coro
                    self.completed_tasks += 1
                    if self.progress and self.task_id:
                        self.progress.update(self.task_id, advance=1)
                    return result
                except Exception as e:
                    self.failed_tasks += 1
                    logging.debug(f"Task failed: {e}")
                    raise
                    
        task = asyncio.create_task(controlled_task())
        self.tasks.append(task)
        
    async def add_batch(self, coros: List, description: str = "Batch processing...") -> None:
        """Add batch of coroutines efficiently"""
        if self.progress:
            self.task_id = self.progress.add_task(description, total=len(coros))
            
        for coro in coros:
            await self.add_task(coro, description)
            
    async def wait_all(self) -> List[Any]:
        """Wait for all tasks to complete"""
        if not self.tasks:
            return []
            
        results = []
        for task in asyncio.as_completed(self.tasks):
            try:
                result = await task
                results.append(result)
            except Exception as e:
                logging.warning(f"Task failed: {e}")
                results.append(None)
                
        self.tasks.clear()
        return results


class AsyncLogger:
    """📝 High-performance async logging system"""
    
    def __init__(self, log_file: Optional[Path] = None, level: int = logging.INFO):
        self.log_file = log_file
        self.level = level
        self.logger = self._setup_logger()
        self._log_queue = asyncio.Queue()
        self._log_task: Optional[asyncio.Task] = None
        
    def _setup_logger(self) -> logging.Logger:
        """Setup optimized logger"""
        logger = logging.getLogger("AsyncCore")
        logger.setLevel(self.level)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(self.level)
        
        # File handler if specified
        if self.log_file:
            file_handler = logging.FileHandler(self.log_file)
            file_handler.setLevel(self.level)
            logger.addHandler(file_handler)
            
        logger.addHandler(console_handler)
        return logger
        
    async def start_logging(self) -> None:
        """Start async log processing"""
        if self._log_task:
            return
            
        self._log_task = asyncio.create_task(self._log_processor())
        
    async def stop_logging(self) -> None:
        """Stop async log processing"""
        if self._log_task:
            await self._log_queue.put(None)  # Sentinel
            await self._log_task
            self._log_task = None
            
    async def _log_processor(self) -> None:
        """Process log messages asynchronously"""
        while True:
            log_item = await self._log_queue.get()
            if log_item is None:  # Sentinel to stop
                break
                
            level, message, extra = log_item
            self.logger.log(level, message, extra=extra or {})
            
    async def log(self, level: int, message: str, **kwargs) -> None:
        """Queue async log message"""
        await self._log_queue.put((level, message, kwargs))
        
    async def info(self, message: str, **kwargs) -> None:
        await self.log(logging.INFO, message, **kwargs)
        
    async def warning(self, message: str, **kwargs) -> None:
        await self.log(logging.WARNING, message, **kwargs)
        
    async def error(self, message: str, **kwargs) -> None:
        await self.log(logging.ERROR, message, **kwargs)


class AsyncCoreEngine:
    """🚀 Main async engine coordinating all components"""
    
    def __init__(self, config: Optional[AsyncConfig] = None):
        self.config = config or AsyncConfig()
        self.session_manager: Optional[AsyncSessionManager] = None
        self.file_manager = AsyncFileManager(self.config.chunk_size)
        self.task_manager: Optional[AsyncTaskManager] = None
        self.logger: Optional[AsyncLogger] = None
        self._shutdown_event = asyncio.Event()
        
    async def __aenter__(self):
        await self.initialize()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.shutdown()
        
    async def initialize(self) -> None:
        """Initialize all async components"""
        # Setup signal handlers for graceful shutdown
        loop = asyncio.get_event_loop()
        for sig in [signal.SIGTERM, signal.SIGINT]:
            loop.add_signal_handler(sig, self._signal_handler)
            
        # Initialize components
        self.session_manager = AsyncSessionManager(self.config)
        await self.session_manager.start()
        
        self.task_manager = AsyncTaskManager(self.config.max_concurrent_tasks)
        
        # Setup logging
        log_file = Path("logs/async_core.log")
        log_file.parent.mkdir(exist_ok=True)
        self.logger = AsyncLogger(log_file)
        await self.logger.start_logging()
        
        await self.logger.info("🚀 AsyncCoreEngine initialized")
        
    def _signal_handler(self):
        """Handle shutdown signals"""
        self._shutdown_event.set()
        
    async def shutdown(self) -> None:
        """Graceful shutdown of all components"""
        await self.logger.info("🔄 Shutting down AsyncCoreEngine...")
        
        # Cancel all pending tasks
        if self.task_manager:
            for task in self.task_manager.tasks:
                if not task.done():
                    task.cancel()
                    
        # Close session manager
        if self.session_manager:
            await self.session_manager.close()
            
        # Stop logging
        if self.logger:
            await self.logger.stop_logging()
            
        await asyncio.sleep(0.1)  # Allow cleanup
        
    async def get_performance_stats(self) -> Dict[str, Any]:
        """Get comprehensive performance statistics"""
        if not self.session_manager:
            return {}
            
        metrics = self.session_manager.metrics
        elapsed_time = time.time() - metrics.start_time
        
        return {
            "uptime_seconds": elapsed_time,
            "total_requests": metrics.total_requests,
            "successful_requests": metrics.successful_requests,
            "failed_requests": metrics.failed_requests,
            "success_rate": metrics.successful_requests / max(metrics.total_requests, 1) * 100,
            "requests_per_second": metrics.total_requests / max(elapsed_time, 1),
            "avg_response_time": metrics.avg_response_time,
            "rate_limited": metrics.rate_limited,
            "timeouts": metrics.timeouts,
            "total_bytes": metrics.total_bytes
        }
        
    async def display_performance_report(self) -> None:
        """Display beautiful performance report"""
        stats = await self.get_performance_stats()
        
        if RICH_AVAILABLE and console:
            table = Table(title="🚀 Async Performance Report")
            table.add_column("Metric", style="cyan")
            table.add_column("Value", style="green")
            
            for key, value in stats.items():
                if isinstance(value, float):
                    table.add_row(key.replace("_", " ").title(), f"{value:.2f}")
                else:
                    table.add_row(key.replace("_", " ").title(), str(value))
                    
            console.print(table)
        else:
            print("\n🚀 Async Performance Report:")
            for key, value in stats.items():
                print(f"  {key.replace('_', ' ').title()}: {value}")


# Utility decorators for async optimization
def async_retry(max_attempts: int = 3, backoff: float = 1.5):
    """Decorator for async retry logic"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(max_attempts):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        wait_time = backoff ** attempt
                        await asyncio.sleep(wait_time)
                    else:
                        break
                        
            raise last_exception
        return wrapper
    return decorator


def async_timeout(seconds: int):
    """Decorator for async timeout"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            return await asyncio.wait_for(func(*args, **kwargs), timeout=seconds)
        return wrapper
    return decorator


# Export main components
__all__ = [
    'AsyncConfig',
    'AsyncCoreEngine', 
    'AsyncSessionManager',
    'AsyncTaskManager',
    'AsyncFileManager',
    'AsyncLogger',
    'async_retry',
    'async_timeout'
]

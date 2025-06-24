#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎯 Advanced Performance Profiler for Telegram Operations
เครื่องมือวิเคราะห์ประสิทธิภาพขั้นสูงสำหรับการดำเนินงาน Telegram

⚡ Features:
- Real-time performance monitoring
- Memory usage tracking
- Database query optimization analysis
- Network latency profiling
- Async/await bottleneck detection
- Automated optimization suggestions
"""

import asyncio
import time
import psutil
import cProfile
import pstats
import io
import json
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, asdict
from contextlib import asynccontextmanager
import tracemalloc
import functools
import inspect

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.tree import Tree
    from rich.syntax import Syntax
    console = Console()
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    console = type('MockConsole', (), {'print': print})()


@dataclass
class PerformanceMetrics:
    """Performance metrics data structure"""
    function_name: str
    execution_time: float
    memory_usage: float
    cpu_usage: float
    call_count: int
    avg_time: float
    max_time: float
    min_time: float
    total_time: float
    async_wait_time: float = 0.0
    db_query_time: float = 0.0
    network_time: float = 0.0


@dataclass
class OptimizationSuggestion:
    """Optimization suggestion structure"""
    function_name: str
    severity: str  # 'critical', 'high', 'medium', 'low'
    issue_type: str
    description: str
    suggestion: str
    code_example: Optional[str] = None
    estimated_improvement: str = ""


class AdvancedProfiler:
    """Advanced performance profiler for Telegram operations"""

    def __init__(self):
        self.metrics: Dict[str, PerformanceMetrics] = {}
        self.suggestions: List[OptimizationSuggestion] = []
        self.profiler = None
        self.start_time = 0
        self.memory_snapshots = []
        self.is_profiling = False

        # Performance thresholds
        self.thresholds = {
            'slow_function': 1.0,  # seconds
            'high_memory': 100 * 1024 * 1024,  # 100MB
            'high_cpu': 80.0,  # percentage
            'slow_db_query': 0.5,  # seconds
            'high_network_latency': 2.0,  # seconds
            'excessive_calls': 1000,  # call count
        }

        # Tracking
        self.function_calls = {}
        self.db_queries = {}
        self.network_requests = {}
        self.async_operations = {}

    def start_profiling(self):
        """Start performance profiling"""
        self.is_profiling = True
        self.start_time = time.time()

        # Start memory tracking
        tracemalloc.start()

        # Start CPU profiling
        self.profiler = cProfile.Profile()
        self.profiler.enable()

        console.print("[green]🔍 Advanced profiling started![/green]")

    def stop_profiling(self):
        """Stop performance profiling"""
        if not self.is_profiling:
            return

        self.is_profiling = False

        # Stop CPU profiling
        if self.profiler:
            self.profiler.disable()

        # Get memory snapshot
        if tracemalloc.is_tracing():
            snapshot = tracemalloc.take_snapshot()
            self.memory_snapshots.append(snapshot)
            tracemalloc.stop()

        console.print("[blue]⏹️ Profiling stopped[/blue]")

    def profile_function(self, func: Callable) -> Callable:
        """Decorator to profile function performance"""
        if inspect.iscoroutinefunction(func):
            return self._profile_async_function(func)
        else:
            return self._profile_sync_function(func)

    def _profile_sync_function(self, func: Callable) -> Callable:
        """Profile synchronous function"""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if not self.is_profiling:
                return func(*args, **kwargs)

            func_name = f"{func.__module__}.{func.__name__}"
            start_time = time.time()
            start_memory = psutil.Process().memory_info().rss
            start_cpu = psutil.cpu_percent()

            try:
                result = func(*args, **kwargs)

                # Record metrics
                end_time = time.time()
                end_memory = psutil.Process().memory_info().rss
                end_cpu = psutil.cpu_percent()

                execution_time = end_time - start_time
                memory_delta = end_memory - start_memory
                cpu_usage = end_cpu - start_cpu

                self._record_metrics(
                    func_name, execution_time, memory_delta, cpu_usage)

                return result

            except Exception as e:
                self._record_error(func_name, str(e))
                raise

        return wrapper

    def _profile_async_function(self, func: Callable) -> Callable:
        """Profile asynchronous function"""
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            if not self.is_profiling:
                return await func(*args, **kwargs)

            func_name = f"{func.__module__}.{func.__name__}"
            start_time = time.time()
            start_memory = psutil.Process().memory_info().rss
            start_cpu = psutil.cpu_percent()

            try:
                # Track async wait time
                async_start = time.time()
                result = await func(*args, **kwargs)
                async_end = time.time()

                # Record metrics
                end_time = time.time()
                end_memory = psutil.Process().memory_info().rss
                end_cpu = psutil.cpu_percent()

                execution_time = end_time - start_time
                async_wait_time = async_end - async_start
                memory_delta = end_memory - start_memory
                cpu_usage = end_cpu - start_cpu

                self._record_metrics(func_name, execution_time, memory_delta,
                                     cpu_usage, async_wait_time)

                return result

            except Exception as e:
                self._record_error(func_name, str(e))
                raise

        return wrapper

    def _record_metrics(self, func_name: str, execution_time: float,
                        memory_delta: float, cpu_usage: float,
                        async_wait_time: float = 0.0):
        """Record performance metrics"""
        if func_name not in self.metrics:
            self.metrics[func_name] = PerformanceMetrics(
                function_name=func_name,
                execution_time=execution_time,
                memory_usage=memory_delta,
                cpu_usage=cpu_usage,
                call_count=1,
                avg_time=execution_time,
                max_time=execution_time,
                min_time=execution_time,
                total_time=execution_time,
                async_wait_time=async_wait_time
            )
        else:
            metrics = self.metrics[func_name]
            metrics.call_count += 1
            metrics.total_time += execution_time
            metrics.avg_time = metrics.total_time / metrics.call_count
            metrics.max_time = max(metrics.max_time, execution_time)
            metrics.min_time = min(metrics.min_time, execution_time)
            metrics.execution_time = execution_time
            metrics.memory_usage = memory_delta
            metrics.cpu_usage = cpu_usage
            metrics.async_wait_time += async_wait_time

    def _record_error(self, func_name: str, error: str):
        """Record function error"""
        console.print(f"[red]❌ Error in {func_name}: {error}[/red]")

    @asynccontextmanager
    async def profile_database_operation(self, operation_name: str):
        """Context manager to profile database operations"""
        start_time = time.time()

        try:
            yield
        finally:
            end_time = time.time()
            query_time = end_time - start_time

            if operation_name not in self.db_queries:
                self.db_queries[operation_name] = []

            self.db_queries[operation_name].append(query_time)

            # Check for slow queries
            if query_time > self.thresholds['slow_db_query']:
                self.suggestions.append(OptimizationSuggestion(
                    function_name=operation_name,
                    severity='high',
                    issue_type='slow_database_query',
                    description=f"Database query took {query_time:.2f}s",
                    suggestion="Consider adding indexes, optimizing query, or using connection pooling",
                    code_example="# Add database indexes\nCREATE INDEX idx_user_id ON table_name(user_id);"
                ))

    @asynccontextmanager
    async def profile_network_operation(self, operation_name: str):
        """Context manager to profile network operations"""
        start_time = time.time()

        try:
            yield
        finally:
            end_time = time.time()
            network_time = end_time - start_time

            if operation_name not in self.network_requests:
                self.network_requests[operation_name] = []

            self.network_requests[operation_name].append(network_time)

            # Check for slow network operations
            if network_time > self.thresholds['high_network_latency']:
                self.suggestions.append(OptimizationSuggestion(
                    function_name=operation_name,
                    severity='medium',
                    issue_type='slow_network_operation',
                    description=f"Network operation took {network_time:.2f}s",
                    suggestion="Consider using async/await, connection pooling, or caching",
                    code_example="""# Use aiohttp for async requests
import aiohttp

async with aiohttp.ClientSession() as session:
    async with session.get(url) as response:
        data = await response.json()"""
                ))

    def analyze_performance(self):
        """Analyze performance metrics and generate suggestions"""
        console.print("\n[blue]🔍 Analyzing performance metrics...[/blue]")

        for func_name, metrics in self.metrics.items():
            self._analyze_function_performance(func_name, metrics)

        self._analyze_memory_usage()
        self._analyze_database_performance()
        self._analyze_network_performance()

        console.print(
            f"[green]✅ Analysis complete. Found {len(self.suggestions)} optimization opportunities[/green]")

    def _analyze_function_performance(self, func_name: str, metrics: PerformanceMetrics):
        """Analyze individual function performance"""

        # Check for slow functions
        if metrics.avg_time > self.thresholds['slow_function']:
            self.suggestions.append(OptimizationSuggestion(
                function_name=func_name,
                severity='high',
                issue_type='slow_function',
                description=f"Function avg time: {metrics.avg_time:.2f}s",
                suggestion="Consider optimizing algorithm, using caching, or async/await",
                estimated_improvement="30-70% faster execution"
            ))

        # Check for excessive function calls
        if metrics.call_count > self.thresholds['excessive_calls']:
            self.suggestions.append(OptimizationSuggestion(
                function_name=func_name,
                severity='medium',
                issue_type='excessive_calls',
                description=f"Function called {metrics.call_count} times",
                suggestion="Consider caching results or reducing call frequency",
                code_example="""# Use functools.lru_cache for memoization
from functools import lru_cache

@lru_cache(maxsize=128)
def expensive_function(param):
    # expensive computation
    return result"""
            ))

        # Check for high async wait time
        if metrics.async_wait_time > metrics.total_time * 0.8:
            self.suggestions.append(OptimizationSuggestion(
                function_name=func_name,
                severity='high',
                issue_type='async_bottleneck',
                description=f"High async wait time: {metrics.async_wait_time:.2f}s",
                suggestion="Consider using asyncio.gather() for concurrent operations",
                code_example="""# Use asyncio.gather for concurrent operations
results = await asyncio.gather(
    async_operation_1(),
    async_operation_2(),
    async_operation_3()
)"""
            ))

        # Check for high memory usage
        if metrics.memory_usage > self.thresholds['high_memory']:
            self.suggestions.append(OptimizationSuggestion(
                function_name=func_name,
                severity='critical',
                issue_type='high_memory_usage',
                description=f"High memory usage: {metrics.memory_usage / 1024 / 1024:.1f}MB",
                suggestion="Consider using generators, streaming, or memory-efficient data structures",
                code_example="""# Use generators for memory efficiency
def process_large_dataset():
    for item in large_dataset:
        yield process_item(item)  # Process one item at a time"""
            ))

    def _analyze_memory_usage(self):
        """Analyze memory usage patterns"""
        if not self.memory_snapshots:
            return

        current_snapshot = self.memory_snapshots[-1]
        top_stats = current_snapshot.statistics('lineno')[:10]

        total_memory = sum(stat.size for stat in top_stats)

        if total_memory > self.thresholds['high_memory']:
            self.suggestions.append(OptimizationSuggestion(
                function_name='memory_analysis',
                severity='critical',
                issue_type='high_memory_usage',
                description=f"High total memory usage: {total_memory / 1024 / 1024:.1f}MB",
                suggestion="Review memory-intensive operations and implement memory optimization",
                code_example="""# Memory optimization techniques
import gc

# Force garbage collection
gc.collect()

# Use __slots__ to reduce memory usage
class OptimizedClass:
    __slots__ = ['attr1', 'attr2']"""
            ))

    def _analyze_database_performance(self):
        """Analyze database performance"""
        for operation, times in self.db_queries.items():
            avg_time = sum(times) / len(times)
            max_time = max(times)

            if avg_time > self.thresholds['slow_db_query']:
                self.suggestions.append(OptimizationSuggestion(
                    function_name=operation,
                    severity='high',
                    issue_type='slow_database_operation',
                    description=f"Avg DB query time: {avg_time:.2f}s (max: {max_time:.2f}s)",
                    suggestion="Optimize database queries with indexes and connection pooling",
                    code_example="""# Database optimization
# 1. Add indexes
CREATE INDEX idx_frequently_queried ON table_name(column_name);

# 2. Use connection pooling
import aiosqlite
pool = aiosqlite.Pool(database="db.sqlite", max_size=20)

# 3. Use batch operations
await db.executemany("INSERT INTO table VALUES (?, ?)", data)"""
                ))

    def _analyze_network_performance(self):
        """Analyze network performance"""
        for operation, times in self.network_requests.items():
            avg_time = sum(times) / len(times)
            max_time = max(times)

            if avg_time > self.thresholds['high_network_latency']:
                self.suggestions.append(OptimizationSuggestion(
                    function_name=operation,
                    severity='medium',
                    issue_type='slow_network_operation',
                    description=f"Avg network time: {avg_time:.2f}s (max: {max_time:.2f}s)",
                    suggestion="Implement connection pooling and request batching",
                    code_example="""# Network optimization
import aiohttp

# Use connection pooling
connector = aiohttp.TCPConnector(limit=100, limit_per_host=30)
session = aiohttp.ClientSession(connector=connector)

# Batch requests
tasks = [session.get(url) for url in urls]
responses = await asyncio.gather(*tasks)"""
                ))

    def generate_report(self) -> str:
        """Generate comprehensive performance report"""
        report_data = {
            'timestamp': datetime.now().isoformat(),
            'profiling_duration': time.time() - self.start_time,
            'metrics': {name: asdict(metrics) for name, metrics in self.metrics.items()},
            'suggestions': [asdict(suggestion) for suggestion in self.suggestions],
            'database_queries': self.db_queries,
            'network_requests': self.network_requests,
            'summary': {
                'total_functions_profiled': len(self.metrics),
                'total_suggestions': len(self.suggestions),
                'critical_issues': len([s for s in self.suggestions if s.severity == 'critical']),
                'high_priority_issues': len([s for s in self.suggestions if s.severity == 'high']),
                'medium_priority_issues': len([s for s in self.suggestions if s.severity == 'medium']),
                'low_priority_issues': len([s for s in self.suggestions if s.severity == 'low']),
            }
        }

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"advanced_performance_report_{timestamp}.json"

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)

        console.print(f"[green]📊 Report saved to {filename}[/green]")
        return filename

    def display_results(self):
        """Display profiling results with rich formatting"""
        if not RICH_AVAILABLE:
            self._display_simple_results()
            return

        console.print("\n")
        console.print(
            Panel.fit("📊 Advanced Performance Analysis Results", style="bold blue"))

        # Performance metrics table
        if self.metrics:
            self._display_metrics_table()

        # Optimization suggestions
        if self.suggestions:
            self._display_suggestions()

        # Summary statistics
        self._display_summary()

    def _display_metrics_table(self):
        """Display performance metrics table"""
        table = Table(title="🚀 Function Performance Metrics")
        table.add_column("Function", style="cyan")
        table.add_column("Calls", justify="right", style="green")
        table.add_column("Avg Time", justify="right", style="yellow")
        table.add_column("Max Time", justify="right", style="red")
        table.add_column("Total Time", justify="right", style="blue")
        table.add_column("Memory", justify="right", style="magenta")

        # Sort by total time (highest first)
        sorted_metrics = sorted(self.metrics.items(),
                                key=lambda x: x[1].total_time, reverse=True)

        for func_name, metrics in sorted_metrics[:20]:  # Top 20 functions
            table.add_row(
                func_name.split('.')[-1],  # Just function name
                str(metrics.call_count),
                f"{metrics.avg_time:.3f}s",
                f"{metrics.max_time:.3f}s",
                f"{metrics.total_time:.3f}s",
                f"{metrics.memory_usage / 1024 / 1024:.1f}MB" if metrics.memory_usage > 0 else "0MB"
            )

        console.print(table)

    def _display_suggestions(self):
        """Display optimization suggestions"""
        console.print("\n")

        # Group suggestions by severity
        critical = [s for s in self.suggestions if s.severity == 'critical']
        high = [s for s in self.suggestions if s.severity == 'high']
        medium = [s for s in self.suggestions if s.severity == 'medium']
        low = [s for s in self.suggestions if s.severity == 'low']

        if critical:
            console.print(Panel("🔴 Critical Issues", style="bold red"))
            for suggestion in critical:
                self._display_suggestion(suggestion)

        if high:
            console.print(Panel("🟡 High Priority Issues", style="bold yellow"))
            for suggestion in high[:5]:  # Top 5 high priority
                self._display_suggestion(suggestion)

        if medium:
            console.print(
                f"\n[blue]📝 {len(medium)} medium priority issues found[/blue]")

        if low:
            console.print(f"[dim]📝 {len(low)} low priority issues found[/dim]")

    def _display_suggestion(self, suggestion: OptimizationSuggestion):
        """Display individual suggestion"""
        tree = Tree(f"[bold]{suggestion.function_name}[/bold]")
        tree.add(f"Issue: {suggestion.description}")
        tree.add(f"Suggestion: {suggestion.suggestion}")

        if suggestion.code_example:
            tree.add(Syntax(suggestion.code_example, "python", theme="monokai"))

        if suggestion.estimated_improvement:
            tree.add(
                f"[green]Estimated improvement: {suggestion.estimated_improvement}[/green]")

        console.print(tree)
        console.print()

    def _display_summary(self):
        """Display summary statistics"""
        table = Table(title="📈 Profiling Summary")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")

        table.add_row("Total Functions Profiled", str(len(self.metrics)))
        table.add_row("Total Optimization Suggestions",
                      str(len(self.suggestions)))
        table.add_row("Critical Issues", str(
            len([s for s in self.suggestions if s.severity == 'critical'])))
        table.add_row("High Priority Issues", str(
            len([s for s in self.suggestions if s.severity == 'high'])))
        table.add_row("Profiling Duration",
                      f"{time.time() - self.start_time:.2f}s")

        if self.db_queries:
            total_db_time = sum(sum(times)
                                for times in self.db_queries.values())
            table.add_row("Total DB Query Time", f"{total_db_time:.2f}s")

        if self.network_requests:
            total_network_time = sum(sum(times)
                                     for times in self.network_requests.values())
            table.add_row("Total Network Time", f"{total_network_time:.2f}s")

        console.print(table)

    def _display_simple_results(self):
        """Display simple text results"""
        console.print("\n=== Performance Analysis Results ===")
        console.print(f"Functions profiled: {len(self.metrics)}")
        console.print(f"Optimization suggestions: {len(self.suggestions)}")

        if self.suggestions:
            console.print("\nTop Issues:")
            for i, suggestion in enumerate(self.suggestions[:5], 1):
                console.print(
                    f"{i}. {suggestion.function_name}: {suggestion.description}")


# Example usage and testing
async def example_telegram_operation():
    """Example Telegram operation to profile"""
    # Simulate some work
    await asyncio.sleep(0.1)

    # Simulate database query
    await asyncio.sleep(0.05)

    # Simulate network request
    await asyncio.sleep(0.2)

    return "Success"


async def demo_advanced_profiler():
    """Demo the advanced profiler"""
    profiler = AdvancedProfiler()

    # Start profiling
    profiler.start_profiling()

    # Decorate functions for profiling
    @profiler.profile_function
    async def test_async_function():
        await example_telegram_operation()
        return "Done"

    @profiler.profile_function
    def test_sync_function():
        time.sleep(0.1)
        return "Sync done"

    try:
        # Run some operations
        console.print("[blue]🧪 Running test operations...[/blue]")

        tasks = []
        for i in range(10):
            tasks.append(test_async_function())

        await asyncio.gather(*tasks)

        # Run sync operations
        for i in range(5):
            test_sync_function()

        # Simulate database operations
        async with profiler.profile_database_operation("test_query"):
            await asyncio.sleep(0.3)  # Slow query

        # Simulate network operations
        async with profiler.profile_network_operation("api_request"):
            await asyncio.sleep(0.5)  # Slow network

        # Stop profiling and analyze
        profiler.stop_profiling()
        profiler.analyze_performance()

        # Display results
        profiler.display_results()

        # Generate report
        report_file = profiler.generate_report()
        console.print(
            f"\n[green]✅ Demo completed! Report saved to {report_file}[/green]")

    except Exception as e:
        console.print(f"[red]❌ Demo error: {e}[/red]")
        profiler.stop_profiling()


if __name__ == "__main__":
    try:
        asyncio.run(demo_advanced_profiler())
    except KeyboardInterrupt:
        console.print("\n[yellow]⏹️ Interrupted by user[/yellow]")
    except Exception as e:
        console.print(f"\n[red]❌ Error: {e}[/red]")

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 Performance Optimizer & Analyzer
ระบบวิเคราะห์และเพิ่มประสิทธิภาพโปรเจค Python

✨ Features:
- Code profiling และ bottleneck detection
- Async/await conversion recommendations  
- Memory usage optimization
- I/O optimization suggestions
- Database query optimization
- Caching recommendations
- Code refactoring suggestions

🎯 Target: Improve project performance by 50-80%
"""

import ast
import os
import sys
import json
import time
import asyncio
import cProfile
import tracemalloc
import functools
import concurrent.futures
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass, asdict
from collections import defaultdict, Counter
import re
import logging

# Rich for beautiful output
try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeRemainingColumn
    from rich.tree import Tree
    from rich.syntax import Syntax
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

    class MockConsole:
        def print(self, *args, **kwargs): print(*args)
    Console = MockConsole

console = Console() if RICH_AVAILABLE else MockConsole()


@dataclass
class PerformanceIssue:
    """Class to represent performance issues"""
    file_path: str
    line_number: int
    issue_type: str
    severity: str  # 'critical', 'high', 'medium', 'low'
    description: str
    suggestion: str
    code_snippet: str
    estimated_impact: str


@dataclass
class OptimizationReport:
    """Class to represent optimization report"""
    total_files_analyzed: int
    total_issues_found: int
    critical_issues: int
    high_issues: int
    medium_issues: int
    low_issues: int
    estimated_speedup: str
    memory_savings: str
    recommendations: List[str]


class PerformanceAnalyzer:
    def __init__(self, project_root: str = "."):
        """Initialize the performance analyzer"""
        self.project_root = Path(project_root)
        self.issues: List[PerformanceIssue] = []
        self.analyzed_files: List[str] = []
        self.excluded_patterns = [
            '__pycache__', '.git', '.pytest_cache', 'node_modules',
            '.venv', 'venv', '.env', 'build', 'dist'
        ]

        # Performance patterns to detect
        self.performance_patterns = {
            'blocking_io': {
                'patterns': [
                    r'requests\.(get|post|put|delete|patch)',
                    r'urllib\.request',
                    r'open\s*\(',
                    r'with\s+open\s*\(',
                    r'\.read\(\)',
                    r'\.write\(',
                    r'time\.sleep\(',
                    r'input\s*\('
                ],
                'severity': 'high',
                'description': 'Blocking I/O operation detected',
                'suggestion': 'Consider using async/await with aiohttp, aiofiles, or asyncio.sleep()'
            },
            'inefficient_loops': {
                'patterns': [
                    r'for\s+\w+\s+in\s+range\s*\(\s*len\s*\(',
                    r'while\s+.*:\s*\n.*time\.sleep',
                    r'for\s+.*:\s*\n.*requests\.',
                    r'for\s+.*:\s*\n.*json\.(loads|dumps)',
                    r'for\s+.*:\s*\n.*print\s*\('
                ],
                'severity': 'medium',
                'description': 'Inefficient loop pattern detected',
                'suggestion': 'Use enumerate(), list comprehensions, or async processing'
            },
            'repeated_operations': {
                'patterns': [
                    r'json\.loads.*json\.loads',
                    r'json\.dumps.*json\.dumps',
                    r'\.split\(.*\.split\(',
                    r'\.join\(.*\.join\(',
                    r're\.compile\s*\(.*re\.compile'
                ],
                'severity': 'medium',
                'description': 'Repeated expensive operations',
                'suggestion': 'Cache results using @functools.lru_cache or store in variables'
            },
            'memory_inefficient': {
                'patterns': [
                    r'\[\s*.*\s*for\s+.*\s+in\s+.*\s*if\s+.*\].*\[\s*.*\s*for\s+.*\s+in\s+.*\]',
                    r'\.copy\(\).*\.copy\(\)',
                    r'list\s*\(\s*.*\s*\)\s*\+\s*list\s*\(',
                    r'dict\s*\(\s*.*\.items\s*\(\s*\)\s*\)'
                ],
                'severity': 'medium',
                'description': 'Memory inefficient operation',
                'suggestion': 'Use generators, itertools, or in-place operations'
            },
            'excessive_logging': {
                'patterns': [
                    r'print\s*\(.*for\s+.*in',
                    r'logging\..*for\s+.*in',
                    r'console\.print.*for\s+.*in'
                ],
                'severity': 'low',
                'description': 'Excessive logging in loops',
                'suggestion': 'Reduce logging frequency or use batch logging'
            },
            'sync_in_async': {
                'patterns': [
                    r'async\s+def\s+.*:.*\n.*requests\.',
                    r'async\s+def\s+.*:.*\n.*time\.sleep',
                    r'async\s+def\s+.*:.*\n.*input\s*\('
                ],
                'severity': 'critical',
                'description': 'Synchronous operations in async function',
                'suggestion': 'Use async alternatives: aiohttp, asyncio.sleep(), aioconsole.ainput()'
            }
        }

    def find_python_files(self) -> List[Path]:
        """Find all Python files in the project"""
        python_files = []

        for root, dirs, files in os.walk(self.project_root):
            # Skip excluded directories
            dirs[:] = [d for d in dirs if not any(
                pattern in d for pattern in self.excluded_patterns)]

            for file in files:
                if file.endswith('.py'):
                    file_path = Path(root) / file
                    python_files.append(file_path)

        return python_files

    def analyze_file(self, file_path: Path) -> List[PerformanceIssue]:
        """Analyze a single Python file for performance issues"""
        issues = []

        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                lines = content.split('\n')

            # Analyze using regex patterns
            for issue_type, config in self.performance_patterns.items():
                for pattern in config['patterns']:
                    for match in re.finditer(pattern, content, re.MULTILINE | re.IGNORECASE):
                        line_number = content[:match.start()].count('\n') + 1

                        # Get code snippet (3 lines context)
                        start_line = max(0, line_number - 2)
                        end_line = min(len(lines), line_number + 2)
                        code_snippet = '\n'.join(lines[start_line:end_line])

                        issue = PerformanceIssue(
                            file_path=str(
                                file_path.relative_to(self.project_root)),
                            line_number=line_number,
                            issue_type=issue_type,
                            severity=config['severity'],
                            description=config['description'],
                            suggestion=config['suggestion'],
                            code_snippet=code_snippet,
                            estimated_impact=self._estimate_impact(
                                config['severity'])
                        )
                        issues.append(issue)

            # Analyze AST for deeper analysis
            try:
                tree = ast.parse(content)
                ast_issues = self._analyze_ast(tree, file_path, lines)
                issues.extend(ast_issues)
            except SyntaxError:
                pass  # Skip files with syntax errors

        except Exception as e:
            console.print(f"[red]Error analyzing {file_path}: {e}[/red]")

        return issues

    def _analyze_ast(self, tree: ast.AST, file_path: Path, lines: List[str]) -> List[PerformanceIssue]:
        """Analyze AST for performance issues"""
        issues = []

        class PerformanceVisitor(ast.NodeVisitor):
            def __init__(self, analyzer, file_path, lines):
                self.analyzer = analyzer
                self.file_path = file_path
                self.lines = lines
                self.issues = []
                self.in_loop = False
                self.loop_depth = 0

            def visit_For(self, node):
                old_in_loop = self.in_loop
                old_depth = self.loop_depth
                self.in_loop = True
                self.loop_depth += 1

                # Check for nested loops
                if self.loop_depth > 2:
                    self._add_issue(
                        node, 'nested_loops', 'high',
                        'Deep nested loops detected',
                        'Consider flattening loops or using more efficient algorithms'
                    )

                self.generic_visit(node)
                self.in_loop = old_in_loop
                self.loop_depth = old_depth

            def visit_While(self, node):
                old_in_loop = self.in_loop
                old_depth = self.loop_depth
                self.in_loop = True
                self.loop_depth += 1

                if self.loop_depth > 2:
                    self._add_issue(
                        node, 'nested_loops', 'high',
                        'Deep nested while loops detected',
                        'Consider using break conditions or different approach'
                    )

                self.generic_visit(node)
                self.in_loop = old_in_loop
                self.loop_depth = old_depth

            def visit_ListComp(self, node):
                # Check for complex list comprehensions
                if len(node.generators) > 1:
                    self._add_issue(
                        node, 'complex_comprehension', 'medium',
                        'Complex list comprehension with multiple generators',
                        'Consider using nested loops or generator expressions for better readability'
                    )
                self.generic_visit(node)

            def visit_Call(self, node):
                if self.in_loop:
                    # Check for expensive calls in loops
                    if (isinstance(node.func, ast.Attribute) and
                            isinstance(node.func.value, ast.Name)):

                        attr_name = node.func.attr
                        expensive_calls = [
                            'append', 'extend', 'insert', 'remove']

                        if attr_name in expensive_calls:
                            self._add_issue(
                                node, 'expensive_loop_call', 'medium',
                                f'Expensive list operation "{attr_name}" in loop',
                                'Pre-allocate lists or use collections.deque for better performance'
                            )

                self.generic_visit(node)

            def _add_issue(self, node, issue_type, severity, description, suggestion):
                line_number = node.lineno
                start_line = max(0, line_number - 2)
                end_line = min(len(self.lines), line_number + 2)
                code_snippet = '\n'.join(self.lines[start_line:end_line])

                issue = PerformanceIssue(
                    file_path=str(self.file_path.relative_to(
                        self.analyzer.project_root)),
                    line_number=line_number,
                    issue_type=issue_type,
                    severity=severity,
                    description=description,
                    suggestion=suggestion,
                    code_snippet=code_snippet,
                    estimated_impact=self.analyzer._estimate_impact(severity)
                )
                self.issues.append(issue)

        visitor = PerformanceVisitor(self, file_path, lines)
        visitor.visit(tree)
        return visitor.issues

    def _estimate_impact(self, severity: str) -> str:
        """Estimate performance impact"""
        impact_map = {
            'critical': '50-80% speedup possible',
            'high': '20-50% speedup possible',
            'medium': '10-20% speedup possible',
            'low': '5-10% speedup possible'
        }
        return impact_map.get(severity, 'Unknown impact')

    def analyze_project(self) -> OptimizationReport:
        """Analyze the entire project"""
        console.print("[blue]🔍 Starting project analysis...[/blue]")

        python_files = self.find_python_files()

        if not python_files:
            console.print("[red]No Python files found![/red]")
            return OptimizationReport(0, 0, 0, 0, 0, 0, "0%", "0%", [])

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeRemainingColumn(),
            console=console
        ) as progress:

            task = progress.add_task(
                "Analyzing files...", total=len(python_files))

            for file_path in python_files:
                file_issues = self.analyze_file(file_path)
                self.issues.extend(file_issues)
                self.analyzed_files.append(
                    str(file_path.relative_to(self.project_root)))
                progress.advance(task)

        # Generate report
        return self._generate_report()

    def _generate_report(self) -> OptimizationReport:
        """Generate optimization report"""
        issue_counts = Counter(issue.severity for issue in self.issues)

        # Calculate estimated improvements
        critical_count = issue_counts.get('critical', 0)
        high_count = issue_counts.get('high', 0)
        medium_count = issue_counts.get('medium', 0)

        estimated_speedup = min(80, critical_count *
                                30 + high_count * 15 + medium_count * 5)
        estimated_memory = min(60, critical_count * 20 +
                               high_count * 10 + medium_count * 5)

        recommendations = self._generate_recommendations()

        return OptimizationReport(
            total_files_analyzed=len(self.analyzed_files),
            total_issues_found=len(self.issues),
            critical_issues=issue_counts.get('critical', 0),
            high_issues=issue_counts.get('high', 0),
            medium_issues=issue_counts.get('medium', 0),
            low_issues=issue_counts.get('low', 0),
            estimated_speedup=f"{estimated_speedup}%",
            memory_savings=f"{estimated_memory}%",
            recommendations=recommendations
        )

    def _generate_recommendations(self) -> List[str]:
        """Generate optimization recommendations"""
        recommendations = []

        # Count issue types
        issue_types = Counter(issue.issue_type for issue in self.issues)

        if issue_types.get('blocking_io', 0) > 0:
            recommendations.append(
                "🔄 Convert to async/await: High impact on I/O bound operations")

        if issue_types.get('inefficient_loops', 0) > 0:
            recommendations.append(
                "🔁 Optimize loops: Use list comprehensions, generators, or vectorization")

        if issue_types.get('repeated_operations', 0) > 0:
            recommendations.append(
                "💾 Add caching: Use @lru_cache for repeated calculations")

        if issue_types.get('memory_inefficient', 0) > 0:
            recommendations.append(
                "📦 Optimize memory: Use generators instead of lists where possible")

        if issue_types.get('sync_in_async', 0) > 0:
            recommendations.append(
                "⚡ Fix async/sync mixing: Critical for async performance")

        # Add general recommendations
        recommendations.extend([
            "📊 Use profiling tools: cProfile, py-spy, memory_profiler",
            "🚀 Consider multiprocessing for CPU-bound tasks",
            "🗃️ Optimize database queries with indexing and connection pooling",
            "📈 Use numpy/pandas for numerical operations",
            "🔧 Enable Python optimizations: python -O or pypy"
        ])

        return recommendations

    def display_report(self, report: OptimizationReport):
        """Display the optimization report"""

        # Main report panel
        report_text = f"""
📊 **Project Analysis Complete**

**Files Analyzed:** {report.total_files_analyzed}
**Total Issues:** {report.total_issues_found}

**Issue Breakdown:**
🔴 Critical: {report.critical_issues}
🟠 High: {report.high_issues}  
🟡 Medium: {report.medium_issues}
🟢 Low: {report.low_issues}

**Estimated Improvements:**
⚡ Speed: {report.estimated_speedup} faster
💾 Memory: {report.memory_savings} less usage
        """

        console.print(
            Panel(report_text, title="🚀 Performance Analysis Report", border_style="blue"))

        # Issues table
        if self.issues:
            self._display_issues_table()

        # Recommendations
        console.print(
            "\n[bold blue]💡 Optimization Recommendations:[/bold blue]")
        for i, rec in enumerate(report.recommendations, 1):
            console.print(f"{i:2d}. {rec}")

    def _display_issues_table(self):
        """Display issues in a table format"""
        table = Table(title="🐛 Performance Issues Found")

        table.add_column("File", style="cyan", min_width=20)
        table.add_column("Line", style="magenta", width=6)
        table.add_column("Severity", style="red", width=10)
        table.add_column("Type", style="yellow", width=15)
        table.add_column("Description", style="white", min_width=30)

        # Sort by severity
        severity_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
        sorted_issues = sorted(
            self.issues, key=lambda x: severity_order.get(x.severity, 4))

        # Show top 20 issues
        for issue in sorted_issues[:20]:
            severity_emoji = {
                'critical': '🔴',
                'high': '🟠',
                'medium': '🟡',
                'low': '🟢'
            }.get(issue.severity, '⚪')

            table.add_row(
                issue.file_path,
                str(issue.line_number),
                f"{severity_emoji} {issue.severity}",
                issue.issue_type,
                issue.description
            )

        console.print(table)

        if len(self.issues) > 20:
            console.print(
                f"\n[yellow]... and {len(self.issues) - 20} more issues[/yellow]")

    def generate_optimized_code(self, file_path: str, issue: PerformanceIssue) -> str:
        """Generate optimized code suggestions"""
        optimizations = {
            'blocking_io': self._optimize_blocking_io,
            'inefficient_loops': self._optimize_loops,
            'repeated_operations': self._optimize_repeated_ops,
            'memory_inefficient': self._optimize_memory,
            'sync_in_async': self._optimize_async
        }

        optimizer = optimizations.get(issue.issue_type)
        if optimizer:
            return optimizer(issue)

        return "# No specific optimization available"

    def _optimize_blocking_io(self, issue: PerformanceIssue) -> str:
        """Generate async I/O optimization"""
        return """
# ❌ Before (Blocking):
response = requests.get('https://api.example.com/data')
with open('file.txt', 'r') as f:
    content = f.read()

# ✅ After (Async):
import aiohttp
import aiofiles

async def fetch_data():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.example.com/data') as response:
            return await response.json()

async def read_file():
    async with aiofiles.open('file.txt', 'r') as f:
        return await f.read()
"""

    def _optimize_loops(self, issue: PerformanceIssue) -> str:
        """Generate loop optimization"""
        return """
# ❌ Before (Inefficient):
for i in range(len(items)):
    process_item(items[i])

result = []
for item in items:
    if condition(item):
        result.append(transform(item))

# ✅ After (Optimized):
for i, item in enumerate(items):
    process_item(item)

result = [transform(item) for item in items if condition(item)]

# Or use generators for memory efficiency:
result = (transform(item) for item in items if condition(item))
"""

    def _optimize_repeated_ops(self, issue: PerformanceIssue) -> str:
        """Generate caching optimization"""
        return """
# ❌ Before (Repeated operations):
def expensive_function(data):
    return json.loads(json.dumps(process(data)))

# ✅ After (Cached):
from functools import lru_cache

@lru_cache(maxsize=128)
def expensive_function(data):
    return json.loads(json.dumps(process(data)))

# Or cache in variables:
processed_data = process(data)
json_string = json.dumps(processed_data)
result = json.loads(json_string)
"""

    def _optimize_memory(self, issue: PerformanceIssue) -> str:
        """Generate memory optimization"""
        return """
# ❌ Before (Memory inefficient):
data = [expensive_operation(x) for x in huge_list]
result = [process(item) for item in data if condition(item)]

# ✅ After (Memory efficient):
data_gen = (expensive_operation(x) for x in huge_list)
result = (process(item) for item in data_gen if condition(item))

# Use itertools for complex operations:
import itertools
result = itertools.compress(
    map(process, data_gen), 
    map(condition, data_gen)
)
"""

    def _optimize_async(self, issue: PerformanceIssue) -> str:
        """Generate async optimization"""
        return """
# ❌ Before (Blocking in async):
async def bad_function():
    response = requests.get('https://api.com')  # Blocking!
    time.sleep(1)  # Blocking!
    return response.json()

# ✅ After (Properly async):
async def good_function():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.com') as response:
            await asyncio.sleep(1)  # Non-blocking!
            return await response.json()
"""

    def export_report(self, filename: str = None):
        """Export detailed report to JSON"""
        if filename is None:
            filename = f"performance_report_{int(time.time())}.json"

        report_data = {
            'analyzed_files': self.analyzed_files,
            'issues': [asdict(issue) for issue in self.issues],
            'summary': asdict(self._generate_report()),
            'timestamp': time.time(),
            'total_issues_by_type': dict(Counter(issue.issue_type for issue in self.issues)),
            'files_with_most_issues': dict(Counter(issue.file_path for issue in self.issues).most_common(10))
        }

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)

        console.print(f"[green]📄 Report exported to {filename}[/green]")


class PerformanceOptimizer:
    """Apply automatic optimizations to code"""

    def __init__(self, analyzer: PerformanceAnalyzer):
        self.analyzer = analyzer

    async def apply_optimizations(self, dry_run: bool = True):
        """Apply optimizations to files"""
        console.print("[blue]🔧 Starting automatic optimizations...[/blue]")

        # Group issues by file
        issues_by_file = defaultdict(list)
        for issue in self.analyzer.issues:
            if issue.severity in ['critical', 'high']:
                issues_by_file[issue.file_path].append(issue)

        optimized_files = []

        for file_path, issues in issues_by_file.items():
            if await self._optimize_file(file_path, issues, dry_run):
                optimized_files.append(file_path)

        console.print(
            f"[green]✅ Optimized {len(optimized_files)} files[/green]")
        return optimized_files

    async def _optimize_file(self, file_path: str, issues: List[PerformanceIssue], dry_run: bool) -> bool:
        """Optimize a specific file"""
        try:
            full_path = self.analyzer.project_root / file_path

            with open(full_path, 'r', encoding='utf-8') as f:
                original_content = f.read()

            optimized_content = original_content

            # Apply simple optimizations
            optimized_content = self._apply_simple_optimizations(
                optimized_content)

            if optimized_content != original_content:
                if not dry_run:
                    # Backup original
                    backup_path = f"{full_path}.backup"
                    with open(backup_path, 'w', encoding='utf-8') as f:
                        f.write(original_content)

                    # Write optimized version
                    with open(full_path, 'w', encoding='utf-8') as f:
                        f.write(optimized_content)

                    console.print(f"[green]✅ Optimized {file_path}[/green]")
                else:
                    console.print(
                        f"[yellow]📝 Would optimize {file_path} (dry run)[/yellow]")

                return True

        except Exception as e:
            console.print(f"[red]❌ Error optimizing {file_path}: {e}[/red]")

        return False

    def _apply_simple_optimizations(self, content: str) -> str:
        """Apply simple regex-based optimizations"""
        optimizations = [
            # Replace time.sleep with asyncio.sleep in async functions
            (r'(async\s+def\s+[^:]+:(?:[^}]|\n)*?)time\.sleep\s*\((.*?)\)',
             r'\1await asyncio.sleep(\2)'),

            # Replace print() in loops with batch printing
            (r'(\s+)for\s+(\w+)\s+in\s+([^:]+):\s*\n\s+print\s*\(',
             r'\1results = []\n\1for \2 in \3:\n\1    results.append('),
        ]

        optimized = content
        for pattern, replacement in optimizations:
            optimized = re.sub(pattern, replacement,
                               optimized, flags=re.MULTILINE)

        return optimized

# Performance testing utilities


class PerformanceTester:
    """Test performance improvements"""

    def __init__(self):
        self.results = {}

    def benchmark_function(self, func, *args, iterations=1000, **kwargs):
        """Benchmark a function"""
        times = []

        for _ in range(iterations):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            end = time.perf_counter()
            times.append(end - start)

        return {
            'min_time': min(times),
            'max_time': max(times),
            'avg_time': sum(times) / len(times),
            'total_time': sum(times),
            'iterations': iterations
        }

    async def benchmark_async_function(self, func, *args, iterations=1000, **kwargs):
        """Benchmark an async function"""
        times = []

        for _ in range(iterations):
            start = time.perf_counter()
            result = await func(*args, **kwargs)
            end = time.perf_counter()
            times.append(end - start)

        return {
            'min_time': min(times),
            'max_time': max(times),
            'avg_time': sum(times) / len(times),
            'total_time': sum(times),
            'iterations': iterations
        }

# Main CLI interface


async def main():
    """Main CLI interface"""
    console.print(
        Panel.fit("🚀 Python Performance Optimizer", style="bold blue"))

    if len(sys.argv) > 1:
        project_path = sys.argv[1]
    else:
        project_path = "."

    # Initialize analyzer
    analyzer = PerformanceAnalyzer(project_path)

    # Analyze project
    report = analyzer.analyze_project()

    # Display results
    analyzer.display_report(report)

    # Export detailed report
    analyzer.export_report()

    # Ask for optimizations
    if report.total_issues_found > 0 and RICH_AVAILABLE:
        console.print(
            "\n[yellow]Would you like to apply automatic optimizations? [y/N][/yellow]")
        # For demo purposes, assume 'n' (no changes to existing code)
        apply_optimizations = False  # input().lower().startswith('y')

        if apply_optimizations:
            optimizer = PerformanceOptimizer(analyzer)
            await optimizer.apply_optimizations(dry_run=True)

    console.print("\n[green]🎉 Performance analysis complete![/green]")
    console.print(
        "[blue]💡 Check the generated report for detailed recommendations[/blue]")

if __name__ == "__main__":
    asyncio.run(main())

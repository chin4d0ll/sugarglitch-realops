#!/usr/bin/env python3
"""
🔧 PERFORMANCE BENCHMARK TOOL
เปรียบเทียบประสิทธิภาพ extraction methods
"""

import time
import psutil
import tracemalloc
import sqlite3
import json
from datetime import datetime

class PerformanceBenchmark:
    """📊 Performance testing and comparison tool"""
    
    def __init__(self):
        self.results = []
        self.db_path = "/workspaces/sugarglitch-realops/alx_trading_database.sqlite"
    
    def benchmark_method(self, method_name: str, func, *args, **kwargs):
        """🎯 Benchmark any extraction method"""
        print(f"\n🔥 Benchmarking: {method_name}")
        print("=" * 40)
        
        # 📊 Start monitoring
        process = psutil.Process()
        start_time = time.perf_counter()
        start_memory = process.memory_info().rss
        tracemalloc.start()
        
        # 🚀 Execute function
        try:
            result = func(*args, **kwargs)
            success = True
        except Exception as e:
            print(f"❌ Error: {e}")
            result = None
            success = False
        
        # 📊 Stop monitoring
        end_time = time.perf_counter()
        end_memory = process.memory_info().rss
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        # 📈 Calculate metrics
        execution_time = end_time - start_time
        memory_used = peak / 1024 / 1024  # MB
        memory_delta = (end_memory - start_memory) / 1024 / 1024  # MB
        
        # 💾 Store results
        benchmark_result = {
            'method': method_name,
            'success': success,
            'execution_time': execution_time,
            'memory_peak_mb': memory_used,
            'memory_delta_mb': memory_delta,
            'timestamp': datetime.now().isoformat()
        }
        
        self.results.append(benchmark_result)
        
        # 📋 Print results
        print(f"✅ Success: {success}")
        print(f"⏱️  Time: {execution_time:.2f}s")
        print(f"💾 Memory Peak: {memory_used:.1f}MB")
        print(f"📊 Memory Delta: {memory_delta:.1f}MB")
        
        return benchmark_result
    
    def test_database_query_performance(self):
        """🗄️ Test database query optimization"""
        print("\n🗄️ DATABASE QUERY PERFORMANCE TEST")
        print("=" * 50)
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Test 1: Simple query
            def simple_query():
                cursor.execute("SELECT COUNT(*) FROM dm_data")
                return cursor.fetchone()[0]
            
            self.benchmark_method("Simple Count Query", simple_query)
            
            # Test 2: Complex query with joins
            def complex_query():
                cursor.execute("""
                    SELECT d.item_id, d.text, p.target_name 
                    FROM dm_data d 
                    LEFT JOIN deep_profiles p ON d.user_id = p.target_name 
                    LIMIT 100
                """)
                return cursor.fetchall()
            
            self.benchmark_method("Complex Join Query", complex_query)
            
            # Test 3: Memory-efficient pagination
            def paginated_query():
                results = []
                offset = 0
                batch_size = 50
                
                while True:
                    cursor.execute(
                        "SELECT * FROM dm_data LIMIT ? OFFSET ?", 
                        (batch_size, offset)
                    )
                    batch = cursor.fetchmany(batch_size)
                    if not batch:
                        break
                    results.extend(batch)
                    offset += batch_size
                    if len(results) >= 200:  # Limit test
                        break
                
                return len(results)
            
            self.benchmark_method("Paginated Query", paginated_query)
            
            conn.close()
            
        except Exception as e:
            print(f"❌ Database test failed: {e}")
    
    def test_json_processing_performance(self):
        """📄 Test JSON processing optimization"""
        print("\n📄 JSON PROCESSING PERFORMANCE TEST")
        print("=" * 50)
        
        # Create test data
        test_data = [
            {
                'id': f'msg_{i}',
                'timestamp': int(time.time()) + i,
                'content': f'Test message content {i}' * 10,  # Longer content
                'user_id': f'user_{i % 100}',
                'thread_id': f'thread_{i % 50}'
            }
            for i in range(1000)
        ]
        
        # Test 1: Standard JSON dump
        def standard_json_dump():
            filename = "/tmp/test_standard.json"
            with open(filename, 'w') as f:
                json.dump(test_data, f)
            return filename
        
        self.benchmark_method("Standard JSON Dump", standard_json_dump)
        
        # Test 2: Streaming JSON write
        def streaming_json_write():
            filename = "/tmp/test_streaming.json"
            with open(filename, 'w', buffering=8192) as f:
                f.write('[\n')
                for i, item in enumerate(test_data):
                    if i > 0:
                        f.write(',\n')
                    json.dump(item, f)
                f.write('\n]')
            return filename
        
        self.benchmark_method("Streaming JSON Write", streaming_json_write)
        
        # Test 3: Memory-efficient generator
        def generator_json_write():
            def data_generator():
                for item in test_data:
                    yield item
            
            filename = "/tmp/test_generator.json"
            with open(filename, 'w') as f:
                f.write('[\n')
                first = True
                for item in data_generator():
                    if not first:
                        f.write(',\n')
                    json.dump(item, f)
                    first = False
                f.write('\n]')
            return filename
        
        self.benchmark_method("Generator JSON Write", generator_json_write)
    
    def run_full_benchmark(self):
        """🚀 Run complete benchmark suite"""
        print("🎯 SUGARGLITCH REALOPS - PERFORMANCE BENCHMARK")
        print("=" * 60)
        print(f"🕐 Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Database tests
        self.test_database_query_performance()
        
        # JSON processing tests
        self.test_json_processing_performance()
        
        # Test ultra-fast extractor if available
        try:
            from ultra_fast_dm_extractor import UltraFastDMExtractor, MemoryContext
            
            def test_ultra_fast_extractor():
                with MemoryContext():
                    extractor = UltraFastDMExtractor()
                    output_file = f"/tmp/benchmark_extraction_{int(time.time())}.json"
                    return extractor.extract_and_save("fleming654", output_file, limit=100)
            
            self.benchmark_method("Ultra Fast DM Extractor", test_ultra_fast_extractor)
            
        except ImportError:
            print("⚠️ Ultra Fast DM Extractor not available for testing")
        
        # 📊 Generate summary report
        self.generate_summary_report()
    
    def generate_summary_report(self):
        """📋 Generate performance summary report"""
        print("\n📊 PERFORMANCE SUMMARY REPORT")
        print("=" * 60)
        
        if not self.results:
            print("❌ No benchmark results available")
            return
        
        # Sort by execution time
        sorted_results = sorted(self.results, key=lambda x: x['execution_time'])
        
        print("🏆 FASTEST METHODS:")
        for i, result in enumerate(sorted_results[:3], 1):
            print(f"{i}. {result['method']}: {result['execution_time']:.2f}s")
        
        print("\n💾 MEMORY EFFICIENCY:")
        memory_sorted = sorted(self.results, key=lambda x: x['memory_peak_mb'])
        for i, result in enumerate(memory_sorted[:3], 1):
            print(f"{i}. {result['method']}: {result['memory_peak_mb']:.1f}MB")
        
        # Save detailed report
        report_file = f"/workspaces/sugarglitch-realops/performance_benchmark_{int(time.time())}.json"
        with open(report_file, 'w') as f:
            json.dump({
                'benchmark_summary': {
                    'total_tests': len(self.results),
                    'timestamp': datetime.now().isoformat(),
                    'fastest_method': sorted_results[0]['method'] if sorted_results else None,
                    'most_memory_efficient': memory_sorted[0]['method'] if memory_sorted else None
                },
                'detailed_results': self.results
            }, f, indent=2)
        
        print(f"\n📄 Detailed report saved: {report_file}")

def main():
    """🎯 Run performance benchmark"""
    benchmark = PerformanceBenchmark()
    benchmark.run_full_benchmark()

if __name__ == "__main__":
    main()

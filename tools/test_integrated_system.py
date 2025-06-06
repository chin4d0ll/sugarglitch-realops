#!/usr/bin/env python3
"""
Comprehensive Test Suite for Integrated DM Extraction System
Tests all components: proxy rotation, block recovery, and DM extraction
"""

import os
import sys
import json
import time
import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime

# Add the tools directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'tools'))

try:
    from integrated_dm_extractor import IntegratedDMExtractor
    from ip_rotation_handler import ProxyRotator
    from instagram_block_recovery import InstagramBlockRecovery, renew_session
    from extract_alx_trading_dms import ALXTradingDMExtractor
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure all required modules are available")
    sys.exit(1)


class TestIntegratedDMExtractor(unittest.TestCase):
    """Test cases for the integrated DM extraction system"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_session_file = "test_session.json"
        self.test_proxy_config = "test_proxies.json"
        self.test_output_dir = "test_results"
        
        # Create test session file
        test_session = {
            "cookies": {
                "sessionid": "test_session_id",
                "ds_user_id": "test_user_id",
                "csrftoken": "test_csrf_token"
            },
            "headers": {
                "User-Agent": "Instagram Test Agent",
                "X-CSRFToken": "test_csrf_token"
            }
        }
        
        with open(self.test_session_file, 'w') as f:
            json.dump(test_session, f)
        
        # Create test proxy config
        test_proxies = [
            "http://proxy1.example.com:8080",
            "http://proxy2.example.com:8080",
            "http://proxy3.example.com:8080"
        ]
        
        with open(self.test_proxy_config, 'w') as f:
            json.dump(test_proxies, f)
        
        # Create test output directory
        os.makedirs(self.test_output_dir, exist_ok=True)
        os.makedirs("logs", exist_ok=True)
    
    def tearDown(self):
        """Clean up test fixtures"""
        # Remove test files
        for file in [self.test_session_file, self.test_proxy_config]:
            if os.path.exists(file):
                os.remove(file)
        
        # Remove test output directory
        if os.path.exists(self.test_output_dir):
            import shutil
            shutil.rmtree(self.test_output_dir)
    
    def test_integrated_extractor_initialization(self):
        """Test that integrated extractor initializes correctly"""
        extractor = IntegratedDMExtractor(
            session_file=self.test_session_file,
            proxy_config=self.test_proxy_config,
            output_dir=self.test_output_dir
        )
        
        # Check that all components are initialized
        self.assertIsInstance(extractor.proxy_rotator, ProxyRotator)
        self.assertIsInstance(extractor.block_recovery, InstagramBlockRecovery)
        self.assertIsInstance(extractor.dm_extractor, ALXTradingDMExtractor)
        
        # Check configuration
        self.assertEqual(extractor.session_file, self.test_session_file)
        self.assertEqual(extractor.proxy_config, self.test_proxy_config)
        self.assertEqual(extractor.output_dir, self.test_output_dir)
    
    def test_health_check(self):
        """Test the system health check functionality"""
        extractor = IntegratedDMExtractor(
            session_file=self.test_session_file,
            proxy_config=self.test_proxy_config,
            output_dir=self.test_output_dir
        )
        
        health = extractor.run_health_check()
        
        # Check health check structure
        self.assertIn("timestamp", health)
        self.assertIn("session_file", health)
        self.assertIn("proxy_config", health)
        self.assertIn("proxy_count", health)
        self.assertIn("components", health)
        self.assertIn("overall_status", health)
        
        # Check that files exist
        self.assertTrue(health["session_file"])
        self.assertTrue(health["proxy_config"])
        self.assertEqual(health["proxy_count"], 3)  # Our test proxies
    
    def test_proxy_status(self):
        """Test proxy status reporting"""
        extractor = IntegratedDMExtractor(
            session_file=self.test_session_file,
            proxy_config=self.test_proxy_config,
            output_dir=self.test_output_dir
        )
        
        status = extractor.get_proxy_status()
        
        # Check status structure
        self.assertIn("total_proxies", status)
        self.assertIn("failed_proxies", status)
        self.assertIn("current_proxy", status)
        self.assertIn("stats", status)
        
        # Check values
        self.assertEqual(status["total_proxies"], 3)
        self.assertEqual(status["failed_proxies"], 0)
    
    def test_block_error_detection(self):
        """Test block error detection"""
        extractor = IntegratedDMExtractor(
            session_file=self.test_session_file,
            proxy_config=self.test_proxy_config,
            output_dir=self.test_output_dir
        )
        
        # Test various error messages
        self.assertTrue(extractor._is_block_error("HTTP 403 Forbidden"))
        self.assertTrue(extractor._is_block_error("Rate limit exceeded"))
        self.assertTrue(extractor._is_block_error("challenge_required"))
        self.assertTrue(extractor._is_block_error("Account blocked"))
        
        # Test non-block errors
        self.assertFalse(extractor._is_block_error("Connection timeout"))
        self.assertFalse(extractor._is_block_error("Invalid JSON"))
        self.assertFalse(extractor._is_block_error("Network error"))
    
    @patch('integrated_dm_extractor.ALXTradingDMExtractor')
    def test_successful_extraction(self, mock_extractor_class):
        """Test successful DM extraction"""
        # Mock the extractor to return successful results
        mock_extractor = MagicMock()
        mock_extractor.extract_all_dms.return_value = {
            "extraction_info": {
                "timestamp": datetime.now().isoformat(),
                "target": "alx.trading",
                "total_threads": 5,
                "total_messages": 100
            },
            "threads": [
                {"thread_id": "1", "messages": ["msg1", "msg2"]},
                {"thread_id": "2", "messages": ["msg3", "msg4"]}
            ]
        }
        mock_extractor_class.return_value = mock_extractor
        
        extractor = IntegratedDMExtractor(
            session_file=self.test_session_file,
            proxy_config=self.test_proxy_config,
            output_dir=self.test_output_dir
        )
        
        # Run extraction
        results = extractor.run_extraction(max_retries=1)
        
        # Check results
        self.assertTrue(results["success"])
        self.assertIn("results", results)
        self.assertIn("output_file", results)
        self.assertIn("stats", results)
        
        # Check that output file was created
        self.assertTrue(os.path.exists(results["output_file"]))
    
    @patch('integrated_dm_extractor.ALXTradingDMExtractor')
    def test_extraction_with_retry(self, mock_extractor_class):
        """Test extraction with retry logic"""
        # Mock the extractor to fail first, then succeed
        mock_extractor = MagicMock()
        mock_extractor.extract_all_dms.side_effect = [
            Exception("403 Forbidden"),  # First attempt fails
            {  # Second attempt succeeds
                "extraction_info": {
                    "timestamp": datetime.now().isoformat(),
                    "target": "alx.trading",
                    "total_threads": 3,
                    "total_messages": 50
                },
                "threads": [{"thread_id": "1", "messages": ["msg1"]}]
            }
        ]
        mock_extractor_class.return_value = mock_extractor
        
        extractor = IntegratedDMExtractor(
            session_file=self.test_session_file,
            proxy_config=self.test_proxy_config,
            output_dir=self.test_output_dir
        )
        
        # Mock the block recovery to return success
        with patch.object(extractor, '_attempt_block_recovery', return_value=True):
            results = extractor.run_extraction(max_retries=2)
        
        # Check that it eventually succeeded
        self.assertTrue(results["success"])
        self.assertEqual(results["stats"]["total_attempts"], 2)
    
    def test_save_results(self):
        """Test result saving functionality"""
        extractor = IntegratedDMExtractor(
            session_file=self.test_session_file,
            proxy_config=self.test_proxy_config,
            output_dir=self.test_output_dir
        )
        
        test_results = {
            "extraction_info": {
                "timestamp": datetime.now().isoformat(),
                "target": "alx.trading",
                "total_threads": 2,
                "total_messages": 20
            },
            "threads": [
                {"thread_id": "1", "messages": ["test message"]}
            ]
        }
        
        # Save results
        output_file = extractor._save_results(test_results)
        
        # Check that file was created
        self.assertTrue(os.path.exists(output_file))
        self.assertTrue(output_file.startswith(self.test_output_dir))
        self.assertTrue(output_file.endswith('.json'))
        
        # Check file contents
        with open(output_file, 'r') as f:
            saved_data = json.load(f)
        
        self.assertIn("extraction_info", saved_data)
        self.assertIn("threads", saved_data)
        self.assertIn("extraction_stats", saved_data)


class TestProxyRotator(unittest.TestCase):
    """Test cases for the proxy rotator"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_proxy_file = "test_proxy_rotator.json"
        self.test_proxies = [
            "http://proxy1.example.com:8080",
            "http://proxy2.example.com:8080",
            "http://proxy3.example.com:8080"
        ]
        
        with open(self.test_proxy_file, 'w') as f:
            json.dump(self.test_proxies, f)
    
    def tearDown(self):
        """Clean up test fixtures"""
        if os.path.exists(self.test_proxy_file):
            os.remove(self.test_proxy_file)
    
    def test_proxy_loading(self):
        """Test proxy loading from JSON file"""
        rotator = ProxyRotator(self.test_proxy_file)
        
        self.assertEqual(len(rotator.proxies), 3)
        self.assertEqual(rotator.proxies, self.test_proxies)
    
    def test_proxy_rotation(self):
        """Test proxy rotation logic"""
        rotator = ProxyRotator(self.test_proxy_file)
        
        # Test round-robin rotation
        proxy1 = rotator.get_next_proxy()
        proxy2 = rotator.get_next_proxy()
        proxy3 = rotator.get_next_proxy()
        proxy4 = rotator.get_next_proxy()  # Should wrap around
        
        self.assertEqual(proxy1, self.test_proxies[0])
        self.assertEqual(proxy2, self.test_proxies[1])
        self.assertEqual(proxy3, self.test_proxies[2])
        self.assertEqual(proxy4, self.test_proxies[0])  # Wrapped around
    
    def test_proxy_removal(self):
        """Test removing failed proxies"""
        rotator = ProxyRotator(self.test_proxy_file)
        
        # Remove a proxy
        proxy_to_remove = self.test_proxies[1]
        rotator.remove_proxy(proxy_to_remove)
        
        self.assertEqual(len(rotator.proxies), 2)
        self.assertNotIn(proxy_to_remove, rotator.proxies)
        self.assertIn(proxy_to_remove, rotator.failed_proxies)


def run_integration_test():
    """Run a complete integration test"""
    print("🧪 Running Integration Test Suite")
    print("=" * 50)
    
    # Test 1: Proxy Configuration
    print("\n1. Testing Proxy Configuration...")
    try:
        proxy_config = "/workspaces/sugarglitch-realops/config/proxies.json"
        if os.path.exists(proxy_config):
            rotator = ProxyRotator(proxy_config)
            print(f"   ✅ Loaded {len(rotator.proxies)} proxies")
            
            # Test rotation
            proxy = rotator.get_next_proxy()
            print(f"   ✅ Proxy rotation working: {proxy}")
        else:
            print(f"   ❌ Proxy config not found: {proxy_config}")
    except Exception as e:
        print(f"   ❌ Proxy test failed: {e}")
    
    # Test 2: Session File
    print("\n2. Testing Session Configuration...")
    try:
        session_file = "/workspaces/sugarglitch-realops/tools/session_alx_trading.json"
        if os.path.exists(session_file):
            with open(session_file, 'r') as f:
                session_data = json.load(f)
            print(f"   ✅ Session file loaded successfully")
            print(f"   ✅ Session contains {len(session_data)} keys")
        else:
            print(f"   ❌ Session file not found: {session_file}")
    except Exception as e:
        print(f"   ❌ Session test failed: {e}")
    
    # Test 3: Component Integration
    print("\n3. Testing Component Integration...")
    try:
        extractor = IntegratedDMExtractor()
        health = extractor.run_health_check()
        print(f"   ✅ Integration test completed")
        print(f"   ✅ Overall status: {health['overall_status']}")
        
        # Show component status
        for component, status in health['components'].items():
            status_icon = "✅" if status['status'] == 'healthy' else "❌"
            print(f"   {status_icon} {component}: {status['status']}")
    except Exception as e:
        print(f"   ❌ Integration test failed: {e}")
    
    # Test 4: Proxy Pool Status
    print("\n4. Testing Proxy Pool...")
    try:
        extractor = IntegratedDMExtractor()
        proxy_status = extractor.get_proxy_status()
        print(f"   ✅ Total proxies: {proxy_status['total_proxies']}")
        print(f"   ✅ Failed proxies: {proxy_status['failed_proxies']}")
        print(f"   ✅ Current proxy: {proxy_status['current_proxy']}")
    except Exception as e:
        print(f"   ❌ Proxy pool test failed: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 Integration test completed!")


def main():
    """Main test runner"""
    print("🧪 Comprehensive Test Suite for Integrated DM Extraction")
    print("=" * 60)
    
    # Ask user what to run
    print("\nAvailable tests:")
    print("1. Unit Tests")
    print("2. Integration Test")
    print("3. Both")
    
    choice = input("\nEnter your choice (1/2/3): ").strip()
    
    if choice in ['1', '3']:
        print("\n🧪 Running Unit Tests...")
        unittest.main(argv=[''], exit=False, verbosity=2)
    
    if choice in ['2', '3']:
        print("\n🔧 Running Integration Test...")
        run_integration_test()
    
    print("\n✅ All tests completed!")


if __name__ == "__main__":
    main()

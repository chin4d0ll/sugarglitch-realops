#!/usr/bin/env python3
"""
Optimized ALX.Trading Extractor - Performance focused with session validation
"""

import requests
import json
import time
import random
from pathlib import Path
from datetime import datetime
import logging

class OptimizedAlxExtractor:
    def __init__(self):
        self.target_username = "alx.trading"
        self.session = requests.Session()
        self.setup_logging()
        self.setup_session()
        
    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def setup_session(self):
        """Setup optimized session with validation"""
        # Load existing session if available
        session_file = Path("sessions/session-alx.trading")
        
        if session_file.exists():
            try:
                with open(session_file, 'r') as f:
                    session_data = json.load(f)
                    
                # Apply cookies
                if 'cookies' in session_data:
                    for name, value in session_data['cookies'].items():
                        self.session.cookies.set(name, value, domain='.instagram.com')
                    
                    self.logger.info("Session loaded from file")
                    
                    # Validate session
                    if self.validate_session():
                        self.logger.info("Session validation successful")
                        return True
                    else:
                        self.logger.warning("Session validation failed, creating new session")
            except Exception as e:
                self.logger.error(f"Error loading session: {e}")
        
        # Setup fresh session
        self.setup_fresh_session()
        return True
    
    def validate_session(self):
        """Validate current session by testing Instagram access"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',
                'Connection': 'keep-alive'
            }
            
            self.session.headers.update(headers)
            response = self.session.get(
                'https://www.instagram.com/',
                timeout=10,
                allow_redirects=True
            )
            
            # Check if we get a proper Instagram page
            if response.status_code == 200 and 'instagram' in response.text.lower():
                return True
                
        except Exception as e:
            self.logger.error(f"Session validation error: {e}")
        
        return False
    
    def setup_fresh_session(self):
        """Setup fresh session with optimal headers"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache'
        }
        
        self.session.headers.update(headers)
        self.logger.info("Fresh session configured")
    
    def extract_profile_data(self):
        """Extract ALX.Trading profile data with optimization"""
        self.logger.info(f"Starting optimized extraction for {self.target_username}")
        
        # Try multiple endpoints for best performance
        endpoints = [
            f"https://www.instagram.com/{self.target_username}/",
            f"https://i.instagram.com/api/v1/users/web_profile_info/?username={self.target_username}",
        ]
        
        for endpoint in endpoints:
            try:
                self.logger.info(f"Trying endpoint: {endpoint}")
                
                # Add small delay to avoid rate limiting
                time.sleep(random.uniform(1, 2))
                
                response = self.session.get(endpoint, timeout=15)
                
                if response.status_code == 200:
                    self.logger.info(f"✅ Success with {endpoint}")
                    
                    # Save response
                    timestamp = int(time.time())
                    output_file = f"data/optimized_alx_extraction_{timestamp}.json"
                    
                    # Ensure data directory exists
                    Path("data").mkdir(exist_ok=True)
                    
                    # Process and save data
                    result = self.process_response(response, endpoint)
                    
                    with open(output_file, 'w', encoding='utf-8') as f:
                        json.dump(result, f, indent=2, ensure_ascii=False)
                    
                    self.logger.info(f"Data saved to: {output_file}")
                    return result
                    
                else:
                    self.logger.warning(f"Failed with status {response.status_code}: {endpoint}")
                    
            except Exception as e:
                self.logger.error(f"Error with {endpoint}: {e}")
                continue
        
        self.logger.error("All endpoints failed")
        return None
    
    def process_response(self, response, endpoint):
        """Process response data for optimal extraction"""
        result = {
            "timestamp": datetime.now().isoformat(),
            "endpoint": endpoint,
            "status_code": response.status_code,
            "content_length": len(response.text),
            "extraction_method": "optimized"
        }
        
        content = response.text
        
        # Try to extract JSON data
        import re
        
        # Look for shared data
        json_match = re.search(r'window\._sharedData = ({.+?});', content)
        if json_match:
            try:
                shared_data = json.loads(json_match.group(1))
                result["shared_data"] = shared_data
                self.logger.info("Extracted shared data successfully")
            except:
                pass
        
        # Look for GraphQL data
        graphql_match = re.search(r'"graphql":\s*({.+?})', content)
        if graphql_match:
            try:
                graphql_data = json.loads(graphql_match.group(1))
                result["graphql_data"] = graphql_data
                self.logger.info("Extracted GraphQL data successfully")
            except:
                pass
        
        # Extract basic profile info
        if self.target_username.lower() in content.lower():
            result["contains_target"] = True
            self.logger.info("Target username found in content")
        
        # Store raw content for analysis
        result["raw_content"] = content[:5000]  # First 5KB for analysis
        
        return result
    
    def run_extraction(self):
        """Run the complete optimized extraction process"""
        self.logger.info("🚀 Starting Optimized ALX.Trading Extraction")
        
        start_time = time.time()
        
        try:
            # Extract data
            data = self.extract_profile_data()
            
            if data:
                execution_time = time.time() - start_time
                self.logger.info(f"✅ Extraction completed in {execution_time:.2f}s")
                
                print("\n📊 Extraction Summary:")
                print(f"   Target: {self.target_username}")
                print(f"   Status: Success")
                print(f"   Execution Time: {execution_time:.2f}s")
                print(f"   Data Size: {data.get('content_length', 0):,} chars")
                
                return data
            else:
                self.logger.error("❌ Extraction failed")
                return None
                
        except Exception as e:
            self.logger.error(f"Critical extraction error: {e}")
            return None

def main():
    """Main execution function"""
    extractor = OptimizedAlxExtractor()
    result = extractor.run_extraction()
    
    if result:
        print("\n🎉 Optimized extraction completed successfully!")
    else:
        print("\n❌ Extraction failed")

if __name__ == "__main__":
    main()

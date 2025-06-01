"""
Session Data Validator and Sanitizer
Validates and cleans existing session data without deleting anything
"""

import json
import re
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from pathlib import Path

class SessionValidator:
    def __init__(self):
        self.required_fields = ['sessionid']
        self.recommended_fields = ['username', 'csrftoken', 'user_id']
        self.optional_fields = ['expires', 'created_at', 'is_active', 'cookies']
        
        # Instagram sessionid pattern (usually 32+ characters alphanumeric)
        self.sessionid_pattern = re.compile(r'^[a-zA-Z0-9]{10,}$')
        
    def validate_session_data(self, session_data: Dict) -> Tuple[bool, List[str], Dict[str, str]]:
        """
        Validate session data structure
        Returns: (is_valid, errors, suggestions)
        """
        errors = []
        suggestions = {}
        
        if not isinstance(session_data, dict):
            errors.append("Session data must be a dictionary")
            return False, errors, suggestions
        
        # Check required fields
        for field in self.required_fields:
            if field not in session_data:
                errors.append(f"Missing required field: {field}")
            elif not session_data[field]:
                errors.append(f"Required field '{field}' is empty")
        
        # Validate sessionid format if present
        if 'sessionid' in session_data:
            sessionid = str(session_data['sessionid']).strip()
            if not self.sessionid_pattern.match(sessionid):
                errors.append("Invalid sessionid format (should be alphanumeric, 10+ characters)")
            elif len(sessionid) < 20:
                suggestions['sessionid'] = "Short sessionid - might be invalid or truncated"
        
        # Check recommended fields
        for field in self.recommended_fields:
            if field not in session_data:
                suggestions[field] = f"Recommended field '{field}' is missing"
        
        # Validate username format if present
        if 'username' in session_data:
            username = str(session_data['username']).strip()
            if not username:
                errors.append("Username is empty")
            elif not re.match(r'^[a-zA-Z0-9._]{1,30}$', username):
                suggestions['username'] = "Username format might be invalid for Instagram"
        
        # Check expiration if present
        if 'expires' in session_data:
            try:
                if isinstance(session_data['expires'], str):
                    expires = datetime.fromisoformat(session_data['expires'].replace('Z', '+00:00'))
                else:
                    expires = datetime.fromtimestamp(session_data['expires'])
                
                if expires < datetime.now():
                    suggestions['expires'] = "Session appears to be expired"
                elif expires < datetime.now() + timedelta(days=1):
                    suggestions['expires'] = "Session expires soon (within 24 hours)"
                    
            except (ValueError, TypeError):
                errors.append("Invalid expiration date format")
        
        # Validate CSRF token if present
        if 'csrftoken' in session_data:
            csrf = str(session_data['csrftoken']).strip()
            if len(csrf) < 10:
                suggestions['csrftoken'] = "CSRF token seems too short"
        
        return len(errors) == 0, errors, suggestions
    
    def sanitize_session_data(self, session_data: Dict) -> Dict:
        """Clean and sanitize session data"""
        if not isinstance(session_data, dict):
            return {}
        
        sanitized = {}
        
        for key, value in session_data.items():
            if isinstance(value, str):
                # Remove whitespace, quotes, and common prefixes
                cleaned_value = value.strip().strip('"').strip("'")
                
                # Remove common cookie prefixes
                if key == 'sessionid' and cleaned_value.startswith('sessionid='):
                    cleaned_value = cleaned_value[10:]
                elif key == 'csrftoken' and cleaned_value.startswith('csrftoken='):
                    cleaned_value = cleaned_value[10:]
                
                sanitized[key] = cleaned_value
            else:
                sanitized[key] = value
        
        # Add metadata
        sanitized['_validation_timestamp'] = datetime.now().isoformat()
        sanitized['_sanitized'] = True
        
        return sanitized
    
    def extract_session_from_cookies(self, cookie_string: str) -> Dict:
        """Extract session data from cookie string"""
        session_data = {}
        
        if not cookie_string:
            return session_data
        
        # Split cookies by semicolon
        cookies = cookie_string.split(';')
        
        for cookie in cookies:
            if '=' in cookie:
                key, value = cookie.split('=', 1)
                key = key.strip()
                value = value.strip()
                
                # Look for Instagram session fields
                if key in ['sessionid', 'csrftoken', 'mid', 'ig_did', 'ig_nrcb']:
                    session_data[key] = value
                elif key == 'ds_user_id':
                    session_data['user_id'] = value
                elif key == 'ds_user':
                    session_data['username'] = value
        
        return session_data
    
    def merge_session_data(self, *session_dicts) -> Dict:
        """Merge multiple session data dictionaries safely"""
        merged = {}
        source_info = []
        
        for i, session_dict in enumerate(session_dicts):
            if not isinstance(session_dict, dict):
                continue
                
            for key, value in session_dict.items():
                if key.startswith('_'):  # Skip metadata
                    continue
                    
                if key not in merged and value:
                    merged[key] = value
                    source_info.append(f"{key}: source_{i}")
        
        # Add merge metadata
        merged['_merged_from'] = len(session_dicts)
        merged['_merge_timestamp'] = datetime.now().isoformat()
        merged['_source_info'] = source_info
        
        return merged
    
    def validate_session_file(self, file_path: Path) -> Dict:
        """Validate a session file and return detailed report"""
        report = {
            'file': str(file_path),
            'exists': file_path.exists(),
            'readable': False,
            'valid_json': False,
            'session_valid': False,
            'errors': [],
            'suggestions': {},
            'data': None,
            'sanitized_data': None
        }
        
        if not report['exists']:
            report['errors'].append("File does not exist")
            return report
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                report['readable'] = True
                
                # Try to parse JSON
                data = json.loads(content)
                report['valid_json'] = True
                report['data'] = data
                
                # Validate session structure
                is_valid, errors, suggestions = self.validate_session_data(data)
                report['session_valid'] = is_valid
                report['errors'].extend(errors)
                report['suggestions'].update(suggestions)
                
                # Generate sanitized version
                report['sanitized_data'] = self.sanitize_session_data(data)
                
        except json.JSONDecodeError as e:
            report['errors'].append(f"Invalid JSON: {str(e)}")
        except Exception as e:
            report['errors'].append(f"Error reading file: {str(e)}")
        
        return report

# Batch session validation utility
class SessionBatchValidator:
    def __init__(self, base_dir: str = "."):
        self.base_dir = Path(base_dir)
        self.validator = SessionValidator()
        self.results_dir = self.base_dir / "validation_results"
        self.results_dir.mkdir(exist_ok=True)
    
    def find_all_session_files(self) -> List[Path]:
        """Find all potential session files"""
        session_files = []
        
        patterns = [
            "**/*session*.json",
            "**/*SESSION*.json",
            "**/session.json",
            "**/*sessionid*.json",
            "**/*cookies*.json"
        ]
        
        for pattern in patterns:
            session_files.extend(self.base_dir.glob(pattern))
        
        return [f for f in session_files if f.is_file()]
    
    def validate_all_sessions(self) -> Dict:
        """Validate all found session files"""
        session_files = self.find_all_session_files()
        
        results = {
            'total_files': len(session_files),
            'valid_sessions': [],
            'invalid_sessions': [],
            'unreadable_files': [],
            'validation_timestamp': datetime.now().isoformat(),
            'summary': {}
        }
        
        print(f"🔍 Found {len(session_files)} potential session files")
        
        for file_path in session_files:
            print(f"   Validating {file_path}...")
            
            validation_result = self.validator.validate_session_file(file_path)
            
            if not validation_result['readable']:
                results['unreadable_files'].append(validation_result)
            elif validation_result['session_valid']:
                results['valid_sessions'].append(validation_result)
                print(f"   ✅ Valid")
            else:
                results['invalid_sessions'].append(validation_result)
                print(f"   ⚠️ Issues found: {len(validation_result['errors'])} errors")
        
        # Generate summary
        results['summary'] = {
            'valid_count': len(results['valid_sessions']),
            'invalid_count': len(results['invalid_sessions']),
            'unreadable_count': len(results['unreadable_files']),
            'success_rate': len(results['valid_sessions']) / max(len(session_files), 1) * 100
        }
        
        # Save detailed results
        results_file = self.results_dir / "session_validation_report.json"
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\n📊 Validation Summary:")
        print(f"   ✅ Valid sessions: {results['summary']['valid_count']}")
        print(f"   ⚠️ Invalid sessions: {results['summary']['invalid_count']}")
        print(f"   ❌ Unreadable files: {results['summary']['unreadable_count']}")
        print(f"   📈 Success rate: {results['summary']['success_rate']:.1f}%")
        print(f"   📄 Detailed report: {results_file}")
        
        return results

# Example usage
if __name__ == "__main__":
    # Test individual validation
    validator = SessionValidator()
    
    # Test with sample data
    sample_session = {
        'sessionid': 'abcd123456789',
        'username': 'testuser',
        'csrftoken': 'xyz789'
    }
    
    is_valid, errors, suggestions = validator.validate_session_data(sample_session)
    print(f"Sample validation - Valid: {is_valid}")
    if errors:
        print(f"Errors: {errors}")
    if suggestions:
        print(f"Suggestions: {suggestions}")
    
    # Test batch validation
    print("\n🔍 Running batch validation...")
    batch_validator = SessionBatchValidator()
    results = batch_validator.validate_all_sessions()

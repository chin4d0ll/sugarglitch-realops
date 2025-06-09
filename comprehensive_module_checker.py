#!/usr/bin/env python3
"""
Comprehensive Module Checker and Fixer
Scans all Python files for import errors, missing dependencies, and broken modules.
Updates requirements.txt and fixes common issues.
"""

import os
import ast
import sys
import subprocess
import importlib
import traceback
import json
from pathlib import Path
from collections import defaultdict, Counter
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('module_check.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ModuleChecker:
    def __init__(self, root_dir="/workspaces/sugarglitch-realops"):
        self.root_dir = Path(root_dir)
        self.issues = []
        self.imports_found = defaultdict(set)
        self.missing_packages = set()
        self.broken_imports = []
        self.syntax_errors = []
        self.standard_lib_modules = self._get_standard_lib_modules()
        self.builtin_modules = set(sys.builtin_module_names)
        
    def _get_standard_lib_modules(self):
        """Get list of Python standard library modules"""
        # Common standard library modules
        return {
            'os', 'sys', 'json', 'time', 'datetime', 'pathlib', 'collections',
            'itertools', 'functools', 'operator', 'typing', 'dataclasses',
            'logging', 'traceback', 'subprocess', 'shutil', 'glob', 'csv',
            'sqlite3', 'urllib', 'http', 'html', 'xml', 'email', 'base64',
            'hashlib', 'hmac', 'secrets', 'uuid', 'random', 'math', 'statistics',
            're', 'string', 'textwrap', 'difflib', 'unicodedata', 'stringprep',
            'readline', 'rlcompleter', 'threading', 'multiprocessing', 'concurrent',
            'asyncio', 'socket', 'ssl', 'select', 'selectors', 'signal',
            'mmap', 'ctypes', 'array', 'weakref', 'copy', 'pickle', 'copyreg',
            'shelve', 'marshal', 'dbm', 'zlib', 'gzip', 'bz2', 'lzma',
            'zipfile', 'tarfile', 'configparser', 'netrc', 'xdrlib', 'plistlib',
            'calendar', 'mailcap', 'mailbox', 'mimetypes', 'quopri', 'uu',
            'binascii', 'encodings', 'codecs', 'locale', 'gettext', 'argparse',
            'optparse', 'getopt', 'tempfile', 'shlex', 'platform', 'errno',
            'io', 'warnings', 'contextlib', 'abc', 'atexit', 'gc', 'inspect',
            'site', 'user', 'builtins', '__future__', 'imp', 'importlib',
            'pkgutil', 'modulefinder', 'runpy', 'parser', 'ast', 'symtable',
            'symbol', 'token', 'keyword', 'tokenize', 'tabnanny', 'pyclbr',
            'py_compile', 'compileall', 'dis', 'pickletools', 'distutils',
            'ensurepip', 'venv', 'zipapp', 'faulthandler', 'pdb', 'profile',
            'pstats', 'hotshot', 'timeit', 'trace', 'unittest', 'doctest',
            'test', 'bdb', 'cmd', 'pprint', 'reprlib', 'queue', 'dummy_threading',
            '_thread', '_dummy_thread', 'sched', 'mutex', 'getpass', 'curses',
            'wsgiref', 'urllib2', 'urlparse', 'BaseHTTPServer', 'SimpleHTTPServer',
            'CGIHTTPServer', 'cookielib', 'Cookie', 'xmlrpclib', 'SimpleXMLRPCServer',
            'DocXMLRPCServer', 'SocketServer', 'forking', 'popen2', 'commands'
        }
    
    def scan_python_files(self):
        """Scan all Python files in the workspace"""
        logger.info(f"Scanning Python files in {self.root_dir}")
        
        python_files = []
        for py_file in self.root_dir.rglob("*.py"):
            # Skip backup and removed directories
            if any(part in str(py_file) for part in ['removed_fake_data', 'backup', '__pycache__', '.git']):
                continue
            python_files.append(py_file)
        
        logger.info(f"Found {len(python_files)} Python files to analyze")
        
        for py_file in python_files:
            self.analyze_file(py_file)
        
        return python_files
    
    def analyze_file(self, file_path):
        """Analyze a single Python file for imports and issues"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Check for syntax errors
            try:
                tree = ast.parse(content, filename=str(file_path))
            except SyntaxError as e:
                self.syntax_errors.append({
                    'file': str(file_path),
                    'error': str(e),
                    'line': e.lineno,
                    'text': e.text
                })
                logger.warning(f"Syntax error in {file_path}: {e}")
                return
            
            # Extract imports
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        self.imports_found[str(file_path)].add(alias.name)
                        self.check_import(alias.name, file_path)
                
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        self.imports_found[str(file_path)].add(node.module)
                        self.check_import(node.module, file_path)
        
        except Exception as e:
            logger.error(f"Error analyzing {file_path}: {e}")
            self.issues.append({
                'file': str(file_path),
                'type': 'analysis_error',
                'error': str(e)
            })
    
    def check_import(self, module_name, file_path):
        """Check if an import is available"""
        # Skip standard library and builtin modules
        if (module_name in self.standard_lib_modules or 
            module_name in self.builtin_modules or
            module_name.split('.')[0] in self.standard_lib_modules or
            module_name.split('.')[0] in self.builtin_modules):
            return
        
        # Skip relative imports
        if module_name.startswith('.'):
            return
        
        try:
            importlib.import_module(module_name)
        except ImportError:
            self.missing_packages.add(module_name)
            self.broken_imports.append({
                'file': str(file_path),
                'module': module_name
            })
    
    def generate_requirements(self):
        """Generate comprehensive requirements.txt"""
        # Common package mappings
        package_mappings = {
            'cv2': 'opencv-python',
            'PIL': 'Pillow',
            'serial': 'pyserial',
            'crypto': 'pycryptodome',
            'Crypto': 'pycryptodome',
            'yaml': 'PyYAML',
            'bs4': 'beautifulsoup4',
            'sklearn': 'scikit-learn',
            'skimage': 'scikit-image',
            'dateutil': 'python-dateutil',
            'psutil': 'psutil',
            'paramiko': 'paramiko',
            'pexpect': 'pexpect',
            'tabulate': 'tabulate',
            'colorama': 'colorama',
            'termcolor': 'termcolor',
            'tqdm': 'tqdm',
            'click': 'click',
            'flask': 'Flask',
            'django': 'Django',
            'fastapi': 'fastapi',
            'uvicorn': 'uvicorn',
            'gunicorn': 'gunicorn',
            'celery': 'celery',
            'redis': 'redis',
            'pymongo': 'pymongo',
            'sqlalchemy': 'SQLAlchemy',
            'pandas': 'pandas',
            'numpy': 'numpy',
            'matplotlib': 'matplotlib',
            'seaborn': 'seaborn',
            'plotly': 'plotly',
            'bokeh': 'bokeh',
            'scipy': 'scipy',
            'tensorflow': 'tensorflow',
            'torch': 'torch',
            'keras': 'keras',
            'xgboost': 'xgboost',
            'lightgbm': 'lightgbm',
            'catboost': 'catboost',
            'jupyter': 'jupyter',
            'jupyterlab': 'jupyterlab',
            'notebook': 'notebook',
            'ipython': 'ipython',
            'selenium': 'selenium',
            'playwright': 'playwright',
            'scrapy': 'scrapy',
            'beautifulsoup4': 'beautifulsoup4',
            'lxml': 'lxml',
            'html5lib': 'html5lib',
            'aiohttp': 'aiohttp',
            'httpx': 'httpx',
            'requests': 'requests',
            'urllib3': 'urllib3',
            'certifi': 'certifi',
            'websockets': 'websockets',
            'socketio': 'python-socketio',
            'eventlet': 'eventlet',
            'gevent': 'gevent',
            'twisted': 'Twisted',
            'tornado': 'tornado',
            'bottle': 'bottle',
            'cherrypy': 'CherryPy',
            'pyramid': 'pyramid',
            'falcon': 'falcon',
            'starlette': 'starlette',
            'sanic': 'sanic',
            'quart': 'Quart',
            'fastapi': 'fastapi',
            'pydantic': 'pydantic',
            'marshmallow': 'marshmallow',
            'jsonschema': 'jsonschema',
            'cerberus': 'Cerberus',
            'voluptuous': 'voluptuous',
            'schema': 'schema',
            'attrs': 'attrs',
            'dataclasses': 'dataclasses',
            'typing_extensions': 'typing-extensions',
            'mypy': 'mypy',
            'pyright': 'pyright',
            'black': 'black',
            'flake8': 'flake8',
            'pylint': 'pylint',
            'autopep8': 'autopep8',
            'isort': 'isort',
            'pre_commit': 'pre-commit',
            'pytest': 'pytest',
            'unittest2': 'unittest2',
            'nose': 'nose',
            'coverage': 'coverage',
            'mock': 'mock',
            'faker': 'Faker',
            'factory_boy': 'factory-boy',
            'hypothesis': 'hypothesis',
            'freezegun': 'freezegun',
            'responses': 'responses',
            'betamax': 'betamax',
            'vcr': 'vcrpy',
            'docker': 'docker',
            'kubernetes': 'kubernetes',
            'boto3': 'boto3',
            'botocore': 'botocore',
            'azure': 'azure',
            'google': 'google-cloud',
            'gcp': 'google-cloud',
            'aws': 'boto3',
            'stripe': 'stripe',
            'paypal': 'paypalrestsdk',
            'twilio': 'twilio',
            'sendgrid': 'sendgrid',
            'mailgun': 'mailgun2',
            'slack': 'slack-sdk',
            'discord': 'discord.py',
            'telegram': 'python-telegram-bot',
            'whatsapp': 'twilio',
            'instagram': 'instapy',
            'twitter': 'tweepy',
            'facebook': 'facebook-sdk',
            'youtube': 'google-api-python-client',
            'spotify': 'spotipy',
            'github': 'PyGithub',
            'gitlab': 'python-gitlab',
            'bitbucket': 'atlassian-python-api',
            'jira': 'jira',
            'confluence': 'atlassian-python-api',
            'slack': 'slack-sdk',
            'microsoft': 'microsoft-graph',
            'office365': 'Office365-REST-Python-Client',
            'sharepoint': 'Office365-REST-Python-Client',
            'outlook': 'O365',
            'exchange': 'exchangelib',
            'ldap': 'python-ldap',
            'ad': 'python-ldap',
            'kerberos': 'kerberos',
            'oauth': 'oauthlib',
            'jwt': 'PyJWT',
            'cryptography': 'cryptography',
            'passlib': 'passlib',
            'bcrypt': 'bcrypt',
            'argon2': 'argon2-cffi',
            'scrypt': 'scrypt',
            'pbkdf2': 'pbkdf2',
            'rsa': 'rsa',
            'ecdsa': 'ecdsa',
            'ed25519': 'ed25519',
            'nacl': 'PyNaCl',
            'gpg': 'python-gnupg',
            'keyring': 'keyring',
            'decouple': 'python-decouple',
            'dotenv': 'python-dotenv',
            'configparser': 'configparser',
            'toml': 'toml',
            'pytoml': 'pytoml',
            'ruamel': 'ruamel.yaml',
            'oyaml': 'oyaml',
            'strictyaml': 'strictyaml'
        }
        
        requirements = set()
        
        # Add packages from missing imports
        for module in self.missing_packages:
            base_module = module.split('.')[0]
            if base_module in package_mappings:
                requirements.add(package_mappings[base_module])
            else:
                requirements.add(base_module)
        
        # Add common packages found in workspace
        common_packages = [
            'requests', 'aiohttp', 'httpx', 'urllib3',
            'selenium', 'playwright', 'beautifulsoup4', 'lxml',
            'pandas', 'numpy', 'matplotlib', 'seaborn',
            'flask', 'fastapi', 'django', 'uvicorn',
            'sqlalchemy', 'psycopg2-binary', 'pymongo',
            'celery', 'redis', 'boto3',
            'pytest', 'black', 'flake8', 'isort',
            'python-dotenv', 'pydantic', 'click',
            'colorama', 'tqdm', 'tabulate',
            'cryptography', 'PyJWT', 'passlib',
            'pillow', 'opencv-python',
            'websockets', 'socketio',
            'docker', 'kubernetes'
        ]
        
        for pkg in common_packages:
            requirements.add(pkg)
        
        return sorted(requirements)
    
    def fix_common_issues(self):
        """Fix common import and module issues"""
        fixes_applied = []
        
        # Create __init__.py files for packages
        for py_file in self.root_dir.rglob("*.py"):
            parent_dir = py_file.parent
            if not (parent_dir / "__init__.py").exists() and parent_dir != self.root_dir:
                # Check if it's a package directory (has multiple .py files)
                py_files_in_dir = list(parent_dir.glob("*.py"))
                if len(py_files_in_dir) > 1:
                    init_file = parent_dir / "__init__.py"
                    init_file.touch()
                    fixes_applied.append(f"Created {init_file}")
        
        return fixes_applied
    
    def generate_report(self):
        """Generate comprehensive analysis report"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        report = {
            'timestamp': timestamp,
            'summary': {
                'total_files_analyzed': len(self.imports_found),
                'syntax_errors': len(self.syntax_errors),
                'broken_imports': len(self.broken_imports),
                'missing_packages': len(self.missing_packages),
                'total_issues': len(self.issues)
            },
            'syntax_errors': self.syntax_errors,
            'broken_imports': self.broken_imports,
            'missing_packages': list(self.missing_packages),
            'issues': self.issues,
            'imports_by_file': dict(self.imports_found),
            'recommendations': self.get_recommendations()
        }
        
        # Save report
        report_file = self.root_dir / f"MODULE_CHECK_REPORT_{timestamp}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        logger.info(f"Report saved to {report_file}")
        return report
    
    def get_recommendations(self):
        """Get actionable recommendations"""
        recommendations = []
        
        if self.syntax_errors:
            recommendations.append({
                'category': 'Syntax Errors',
                'priority': 'HIGH',
                'action': 'Fix syntax errors in files',
                'files': [error['file'] for error in self.syntax_errors]
            })
        
        if self.missing_packages:
            recommendations.append({
                'category': 'Missing Dependencies',
                'priority': 'HIGH',
                'action': 'Install missing packages',
                'packages': list(self.missing_packages)
            })
        
        if self.broken_imports:
            recommendations.append({
                'category': 'Import Errors',
                'priority': 'MEDIUM',
                'action': 'Fix broken import statements',
                'details': self.broken_imports
            })
        
        return recommendations
    
    def update_requirements_txt(self):
        """Update requirements.txt file"""
        requirements = self.generate_requirements()
        
        req_file = self.root_dir / "requirements.txt"
        
        # Read existing requirements
        existing_reqs = set()
        if req_file.exists():
            with open(req_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        existing_reqs.add(line.split('==')[0].split('>=')[0].split('<=')[0])
        
        # Combine with new requirements
        all_requirements = existing_reqs.union(requirements)
        
        # Write updated requirements
        with open(req_file, 'w') as f:
            f.write("# Auto-generated requirements.txt\n")
            f.write(f"# Generated on {datetime.now().isoformat()}\n\n")
            
            for req in sorted(all_requirements):
                f.write(f"{req}\n")
        
        logger.info(f"Updated {req_file} with {len(all_requirements)} packages")
        return req_file
    
    def run_comprehensive_check(self):
        """Run comprehensive module check and fix"""
        logger.info("Starting comprehensive module check...")
        
        # Scan all files
        files_scanned = self.scan_python_files()
        
        # Fix common issues
        fixes = self.fix_common_issues()
        
        # Update requirements.txt
        req_file = self.update_requirements_txt()
        
        # Generate report
        report = self.generate_report()
        
        # Print summary
        self.print_summary(report, fixes)
        
        return report
    
    def print_summary(self, report, fixes):
        """Print summary of findings and fixes"""
        print("\n" + "="*80)
        print("COMPREHENSIVE MODULE CHECK SUMMARY")
        print("="*80)
        
        summary = report['summary']
        print(f"Files Analyzed: {summary['total_files_analyzed']}")
        print(f"Syntax Errors: {summary['syntax_errors']}")
        print(f"Broken Imports: {summary['broken_imports']}")
        print(f"Missing Packages: {summary['missing_packages']}")
        print(f"Total Issues: {summary['total_issues']}")
        
        if fixes:
            print(f"\nFixes Applied: {len(fixes)}")
            for fix in fixes[:10]:  # Show first 10 fixes
                print(f"  - {fix}")
            if len(fixes) > 10:
                print(f"  ... and {len(fixes) - 10} more")
        
        if report['missing_packages']:
            print(f"\nMissing Packages ({len(report['missing_packages'])}):")
            for pkg in sorted(report['missing_packages'])[:20]:
                print(f"  - {pkg}")
            if len(report['missing_packages']) > 20:
                print(f"  ... and {len(report['missing_packages']) - 20} more")
        
        if report['syntax_errors']:
            print(f"\nSyntax Errors ({len(report['syntax_errors'])}):")
            for error in report['syntax_errors'][:10]:
                print(f"  - {error['file']}: {error['error']}")
            if len(report['syntax_errors']) > 10:
                print(f"  ... and {len(report['syntax_errors']) - 10} more")
        
        print("\nNext Steps:")
        print("1. Install missing packages: pip install -r requirements.txt")
        print("2. Fix syntax errors in reported files")
        print("3. Update import statements for broken imports")
        print("4. Test critical scripts after fixes")
        
        print("\n" + "="*80)

def main():
    """Main function"""
    checker = ModuleChecker()
    
    try:
        report = checker.run_comprehensive_check()
        
        # Return success code
        if report['summary']['syntax_errors'] == 0 and report['summary']['missing_packages'] == 0:
            print("\n✅ All modules check passed!")
            return 0
        else:
            print(f"\n⚠️  Found {report['summary']['total_issues']} issues to fix")
            return 1
            
    except Exception as e:
        logger.error(f"Module check failed: {e}")
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())

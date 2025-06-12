#!/usr/bin/env python3
"""
🚀 SugarGlitch RealOps - Production Runner
Production deployment entry point with enhanced features
"""

import sys
import os
import time
import signal
import logging
from pathlib import Path

# Add project to path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

# Import main application
try:
    from main import main as app_main, banner, check_environment
except ImportError as e:
    print(f"❌ Failed to import main application: {e}")
    print("💡 Please ensure all dependencies are installed:")
    print("   pip install -r requirements.txt")
    sys.exit(1)


def setup_logging():
    """Setup production logging"""
    log_dir = PROJECT_ROOT / "logs"
    log_dir.mkdir(exist_ok=True)
    
    log_file = log_dir / "realops.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    return logging.getLogger(__name__)


def signal_handler(signum, frame):
    """Handle system signals gracefully"""
    print(f"\n⚠️ Received signal {signum}. Shutting down gracefully...")
    sys.exit(0)


def production_checks():
    """Perform production readiness checks"""
    print("🔍 Performing production readiness checks...")
    
    # Check environment
    if not check_environment():
        print("❌ Environment check failed")
        return False
    
    # Check critical files
    critical_files = [
        'main.py',
        'requirements.txt',
        '.env'
    ]
    
    for file in critical_files:
        if not os.path.exists(file):
            print(f"❌ Critical file missing: {file}")
            return False
    
    print("✅ Production checks passed")
    return True


def docker_deployment():
    """Docker deployment mode"""
    print("🐳 Running in Docker deployment mode")
    
    # Check if running in container
    if os.path.exists('/.dockerenv'):
        print("✅ Detected Docker environment")
    else:
        print("⚠️ Not running in Docker container")
    
    # Setup container-specific configurations
    os.environ.setdefault('PYTHONUNBUFFERED', '1')
    os.environ.setdefault('LOG_LEVEL', 'INFO')
    
    return True


def main():
    """Production runner main function"""
    # Setup signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Setup logging
    logger = setup_logging()
    logger.info("🚀 SugarGlitch RealOps starting...")
    
    try:
        # Show banner
        banner()
        
        # Production mode checks
        if not production_checks():
            logger.error("❌ Production checks failed")
            return 1
        
        # Check for Docker environment
        if os.environ.get('DOCKER_DEPLOYMENT'):
            docker_deployment()
        
        # Log startup information
        logger.info(f"Python version: {sys.version}")
        logger.info(f"Working directory: {os.getcwd()}")
        logger.info(f"Environment: {'Docker' if os.path.exists('/.dockerenv') else 'Local'}")
        
        # Start main application
        logger.info("🎯 Starting main application...")
        return app_main()
        
    except KeyboardInterrupt:
        logger.info("⚠️ Application interrupted by user")
        return 130
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}")
        return 1
    finally:
        logger.info("👋 SugarGlitch RealOps shutting down")


if __name__ == "__main__":
    # Check for help flags before importing heavy modules
    if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help', 'help']:
        print("""
🚀 SugarGlitch RealOps - Production Runner

Usage:
  python runner.py [OPTIONS]

This is the production entry point for SugarGlitch RealOps.
All command-line options are passed through to main.py

Examples:
  python runner.py --list
  python runner.py ssh-brute
  python runner.py --interactive

Environment Variables:
  DOCKER_DEPLOYMENT=1     Enable Docker deployment mode
  LOG_LEVEL=INFO          Set logging level
  PYTHONUNBUFFERED=1      Disable Python output buffering

For detailed help:
  python main.py --help
        """)
        sys.exit(0)
    
    # Run main application
    exit_code = main()
    sys.exit(exit_code)

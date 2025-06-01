# Fleming Integration - Instagram Intelligence Platform

## Overview

This module integrates the Fleming Production Extractor with the Master Configuration Management system, providing a powerful and configurable solution for Instagram data extraction.

## Features

- **Unified Configuration** - Uses the master configuration system to control Fleming operations
- **Automated Session Handling** - Integrates with session management for seamless authentication
- **Enhanced Proxy Support** - Uses the configured proxy system for improved stealth
- **Comprehensive Monitoring** - Real-time monitoring of extraction operations
- **Integrated Reporting** - PDF, JSON, and CSV export options
- **Streamlined Operation** - Simple launch script for one-click execution

## Quick Start

### Setup

```bash
# Setup the Fleming integration
python setup_fleming_integration.py

# Make the launch script executable
chmod +x launch_fleming.sh
```

### Running

```bash
# Launch with the convenience script
./launch_fleming.sh

# Or run directly
python fleming_integrated_launcher.py
```

## Configuration

The Fleming integration uses the master configuration system, with specific settings in:

- `config/fleming_integration_config.json` - Fleming-specific settings
- `config/master_config.json` - General platform settings
- `config/proxy_master_config.json` - Proxy configuration
- `config/session_master_config.json` - Session management

## Components

- `fleming_integrated_launcher.py` - Main launcher for Fleming operations
- `setup_fleming_integration.py` - Setup script for integration
- `launch_fleming.sh` - Convenience script for running operations
- `config/fleming_integration_config.json` - Fleming integration configuration

## Advanced Usage

### 1. Customizing Extraction Parameters

Edit `config/fleming_integration_config.json` to modify:

```json
"extraction": {
  "dm_extraction": {
    "max_threads_per_target": 50,
    "max_messages_per_thread": 200
  }
}
```

### 2. Enabling Proxy Support

Edit `config/proxy_master_config.json` to configure proxies:

```json
"primary_proxy": {
  "host": "proxy.brightdata.com",
  "port": "22225",
  "username": "username",
  "password": "password"
}
```

### 3. Session Management

Fleming sessions are stored in `sessions/` and managed through the configuration system.

## Troubleshooting

- **Session Issues**: Run `python fleming_session_regenerator.py` to create new sessions
- **Extraction Failures**: Check the logs in `logs/` for detailed error information
- **Configuration Problems**: Verify all configuration files in `config/` directory

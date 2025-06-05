# SugarGlitch RealOps

## Project Overview

SugarGlitch RealOps is a comprehensive Instagram DM extraction and analysis platform designed for legitimate security research, data recovery, and intelligence gathering purposes.

## Features

- **Advanced DM Extraction**: Extract direct messages from Instagram accounts with session-based authentication.
- **Data Analysis**: Analyze extracted data for insights and trends.
- **Report Generation**: Generate professional reports in JSON, HTML, and PDF formats.
- **Targeted Extraction**: Focus on specific accounts or conversations.
- **Automation**: Use scripts for streamlined operations.
- **Security Compliance**: Follow OWASP guidelines for secure data handling.

## Project Structure

```text
.
├── automation_scripts/       # Scripts for automation
├── backups/                  # Backup files
├── config/                   # Configuration files
├── configuration/            # Python configuration scripts
├── core_extraction_tools/    # Core tools for DM extraction
│   ├── advanced_tools/       # Advanced extraction tools
│   ├── instagram_tools/      # Instagram-specific tools
│   ├── targeted/             # Targeted extraction tools
├── data/                     # Data files (JSON, DB, CSV)
├── documentation/            # Documentation files
├── logs/                     # Log files
├── media/                    # Media files (screenshots, HTML)
├── modules/                  # Python modules
├── output/                   # Output files
├── reports/                  # Reports generated
├── sessions/                 # Session files
├── templates/                # HTML templates
├── utils/                    # Utility scripts
├── visualizations/           # Data visualizations
├── webhook/                  # Webhook scripts
└── temp_files/               # Temporary files
```

## Installation

### Prerequisites

- Python 3.8+ (Python 3.12+ recommended)
- Linux/macOS environment (Windows WSL supported)
- Valid Instagram session credentials

### Steps

1. Clone the repository:

   ```bash
   git clone https://github.com/your-repo/sugarglitch-realops.git
   cd sugarglitch-realops
   ```

2. Set up the environment:

   ```bash
   ./setup_environment.sh
   ```

## Usage

### Quick Start

Run the main extraction script:

```bash
./run_dm_extractor.sh
```

### Targeted Extraction

Run extraction for a specific account:

```bash
./run_alx_trading_extractor.sh
```

### Manual Process

1. Extract DM data:

   ```bash
   python3 core_extraction_tools/instagram_tools/dm_extractor.py
   ```

2. Convert to HTML:

   ```bash
   python3 core_extraction_tools/instagram_tools/json_to_html_converter.py
   ```

3. Generate PDF:

   ```bash
   python3 core_extraction_tools/instagram_tools/html_to_pdf_converter.py
   ```

## Contributing

We welcome contributions! Feel free to submit issues or pull requests to improve the project.

## License

This project is licensed under the MIT License.

## Support

For questions or support, please contact [chin4d0ll](mailto:chin4d0ll).

---

**SugarGlitch RealOps** - Professional Instagram Intelligence Platform
*Built for researchers, by researchers* 🚀

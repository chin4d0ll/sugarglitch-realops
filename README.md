# Sugarglitch RealOps

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-Personal%20RedTeam-blue)]()
[![Status](https://img.shields.io/badge/status-Stable-green.svg)]()

**Instagram RedTeam Toolkit — Session hijack, data extract, and behavioral analysis**

---

## Features

- Brute-force login with real IG proxy
- Session reuse / hijack support
- IG DMs, Story, and Post extraction via `instagrapi`
- Suspicious message analyzer (Thai + ENG)
- HTML report generator
- Discord webhook alerts
- Timeline interaction graph

---

## Quick Start

```bash
git clone https://github.com/YOUR_USERNAME/sugarglitch-realops.git
cd sugarglitch-realops
pip install -r requirements.txt
python3 src/main.py
```

---

## File Overview

```
src/
├── brute_force.py           # IG login via request
├── session_extractor.py     # Save sessionid into JSON
├── data_fetcher.py          # DMs, thread extractor
├── story_fetcher.py         # IG Story puller
├── post_media_fetcher.py    # Pull post + caption + likes
├── analyzer.py              # Suspicious text/emoji detection
├── timeline_graph.py        # Plot interaction frequency
├── reporter.py              # Export HTML report
├── webhook_notify.py        # Send Discord alerts
└── main.py                  # One-click execution
```

---

## Requirements

```bash
pip install -r requirements.txt
```

- Python 3.10+
- `instagrapi`, `requests`, `matplotlib`

---

## Notes

- Do not use this for unauthorized access or abuse.
- Meant for security testing / red team under explicit consent.

---

> Made with love for TrashDoll Hacker Queen by @chin4d0ll
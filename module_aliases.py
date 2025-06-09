"""
Module Aliases and Compatibility Layer
Provides compatibility for missing or renamed modules
"""

# Python 2/3 compatibility
try:
    import urllib2
except ImportError:
    import urllib.request as urllib2

try:
    from urlparse import urlparse, parse_qs
except ImportError:
    from urllib.parse import urlparse, parse_qs

try:
    from Queue import Queue
except ImportError:
    from queue import Queue

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

try:
    import ConfigParser as configparser
except ImportError:
    import configparser

try:
    from HTMLParser import HTMLParser
except ImportError:
    from html.parser import HTMLParser

# Optional imports with fallbacks
try:
    import requests
except ImportError:
    requests = None

try:
    import aiohttp
except ImportError:
    aiohttp = None

try:
    from playwright.async_api import async_playwright
except ImportError:
    async_playwright = None

try:
    from selenium import webdriver
except ImportError:
    webdriver = None

try:
    import pandas as pd
except ImportError:
    pd = None

try:
    import numpy as np
except ImportError:
    np = None

try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None

try:
    import websockets
except ImportError:
    websockets = None

try:
    from fake_useragent import UserAgent
except ImportError:
    UserAgent = None

# Utility functions for missing modules
def check_module_availability():
    """Check which modules are available"""
    modules = {
        'requests': requests is not None,
        'aiohttp': aiohttp is not None,
        'playwright': async_playwright is not None,
        'selenium': webdriver is not None,
        'pandas': pd is not None,
        'numpy': np is not None,
        'beautifulsoup4': BeautifulSoup is not None,
        'websockets': websockets is not None,
        'fake_useragent': UserAgent is not None,
    }
    return modules

def get_missing_modules():
    """Get list of missing critical modules"""
    available = check_module_availability()
    return [module for module, available in available.items() if not available]

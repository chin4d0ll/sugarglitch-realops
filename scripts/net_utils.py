# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
import random
import requests

USER_AGENTS = [
    # Chrome, Firefox, Safari, Mobile, etc.
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 13; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0"
]

def get_random_user_agent():
    """Return a random user-agent string."""
    return random.choice(USER_AGENTS)

def get_proxies_from_file(proxy_file):
    """Load proxies from a file (one per line, http[s]://user:pass@host:port)."""
    proxies = []
    try:
        with open(proxy_file) as f:
            for line in f:
                proxy = line.strip()
                if proxy:
                    proxies.append(proxy)
    except Exception as e:
        print(f"[net_utils] Could not load proxies: {e}")
    return proxies

def get_random_proxy(proxies):
    """Return a random proxy from the list (or None if empty)."""
    if proxies:
        return random.choice(proxies)
    return None

def requests_with_retry(url, method="GET", headers=None, proxies=None, max_retries=3, backoff=2, timeout=10, **kwargs):
    """
    Make a request with retry and exponential backoff.
    """
    for attempt in range(1, max_retries+1):
        try:
            if method.upper() == "GET":
                resp = requests.get(url, headers=headers, proxies=proxies, timeout=timeout, **kwargs)
            else:
                resp = requests.request(method, url, headers=headers, proxies=proxies, timeout=timeout, **kwargs)
            return resp
        except Exception as e:
            print(f"[net_utils] Attempt {attempt} failed: {e}")
            if attempt < max_retries:
                import time
                time.sleep(backoff ** attempt)
    return None

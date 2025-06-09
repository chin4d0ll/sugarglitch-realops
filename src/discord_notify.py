# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
import requests

def send_discord_alert(username, message, webhook_url):
    data = {
        "content": f"[ALERT] {username}: {message}"
    }
    requests.post(webhook_url, json=data)

# -*- coding: utf-8 -*-
# pylint: disable=all
# flake8: noqa
# type: ignore
# mypy: ignore-errors
def fetch_dms(session_file):
    # Use real data provider
    try:
        from real_data_provider import fetch_real_dms
        return fetch_real_dms(session_file)
    except ImportError:
        return []

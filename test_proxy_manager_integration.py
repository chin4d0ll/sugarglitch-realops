#!/usr/bin/env python3
"""
Test Bright Data Proxy Manager integration using urllib and Proxy Manager endpoint.
Works for Python 3. Handles proxy authentication and SSL context.
"""
import sys
import ssl

if sys.version_info[0] == 2:
    import six
    from six.moves.urllib import request
    ctx = ssl.create_default_context()
    ctx.verify_flags = ssl.VERIFY_DEFAULT
    opener = request.build_opener(
        request.ProxyHandler({'http': 'http://fuzzy-fishstick-r4w55pwpvp59hvrg-22999.app.github.dev:24000'}),
        request.HTTPSHandler(context=ctx))
    print(opener.open('https://geo.brdtest.com/mygeo.json').read())
else:
    import urllib.request
    ctx = ssl.create_default_context()
    ctx.verify_flags = ssl.VERIFY_DEFAULT
    opener = urllib.request.build_opener(
        urllib.request.ProxyHandler({'http': 'http://brd-auth-token:eackrzayqSbccMSji2QsEcrwEkMgPGPQ@fuzzy-fishstick-r4w55pwpvp59hvrg-22999.app.github.dev:24000'}),
        urllib.request.HTTPSHandler(context=ctx))
    print(opener.open('https://geo.brdtest.com/mygeo.json').read())

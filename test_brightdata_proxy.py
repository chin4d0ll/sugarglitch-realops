import sys
import urllib.request
import ssl

# Bright Data Access
brd_user = 'hl_63f0835e'
brd_zone = 'mobile_proxy'
brd_passwd = 'q9yihckpz3qk'
brd_superpoxy = 'brd.superproxy.io:33335'
brd_connectStr = 'brd-customer-' + brd_user + '-zone-' + brd_zone + ':' + brd_passwd + '@' + brd_superpoxy

brd_test_url = 'https://geo.brdtest.com/welcome.txt'

# Skip SSL verification for test
context = ssl._create_unverified_context()

opener = urllib.request.build_opener(
    urllib.request.ProxyHandler(
        {'http': 'http://' + brd_connectStr,
         'https': 'https://' + brd_connectStr }),
    urllib.request.HTTPSHandler(context=context)
)
print(opener.open(brd_test_url).read().decode())

import sys
import urllib.request
import ssl

# Bright Data Access
brd_user = 'hl_63f0835e'
brd_zone = 'mobile_proxy'
brd_passwd = 'q9yihckpz3qk'
brd_superpoxy = 'brd.superproxy.io:33335'
brd_connectStr = 'brd-customer-' + brd_user + '-zone-' + brd_zone + ':' + brd_passwd + '@' + brd_superpoxy

brd_test_url = 'https://geo.brdtest.com/mygeo.json'


# Use the downloaded CA certificate for SSL verification
ca_cert_path = 'brightdata_ca/New SSL certifcate - MUST BE USED WITH PORT 33335/BrightData SSL certificate (port 33335).crt'
context = ssl.create_default_context(cafile=ca_cert_path)

opener = urllib.request.build_opener(
    urllib.request.ProxyHandler(
        {'http': 'http://' + brd_connectStr,
         'https': 'https://' + brd_connectStr }),
    urllib.request.HTTPSHandler(context=context)
)
print(opener.open(brd_test_url).read().decode())

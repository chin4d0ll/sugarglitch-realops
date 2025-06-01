import urllib.request
import ssl

proxy = 'http://brd-customer-hl_63f0835e-zone-residential_proxy:2h1han033ed3@brd.superproxy.io:33335'
url = 'https://www.instagram.com/alx.trading/'

opener = urllib.request.build_opener(
    urllib.request.ProxyHandler({'https': proxy, 'http': proxy}),
    urllib.request.HTTPSHandler(context=ssl._create_unverified_context())
)

try:
    print(opener.open(url).read().decode())
except Exception as e:
    print(f"Error: {e}")

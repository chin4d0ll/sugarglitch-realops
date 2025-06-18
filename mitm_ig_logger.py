from mitmproxy import http


def response(flow: http.HTTPFlow):
    if "instagram.com" in flow.request.pretty_url:
        print(f"[mitmproxy] {flow.request.method} {flow.request.pretty_url}")
        if flow.response:
            print(f"[mitmproxy] Response: {flow.response.status_code}")

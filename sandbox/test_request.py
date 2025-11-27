from request import Request


# Giả lập một raw HTTP request giống thật
raw_request = (
    "POST /message HTTP/1.1\r\n"
    "Host: peerB.local:8080\r\n"
    "User-Agent: P2PClient/1.0\r\n"
    "Content-Type: application/json\r\n"
    "Cookie: session=abc123; theme=dark\r\n"
    "Content-Length: 49\r\n"
    "\r\n"
    '{"from": "peerA", "to": "peerB", "msg": "hi bro"}'
)

# Định nghĩa route giả (routing test)
def handle_message(req):
    print("[Handler] Received message:", req.data["msg"])
    print("[Handler] From:", req.data["from"], "-> To:", req.data["to"])

routes = {
    ('POST', '/message'): handle_message
}

# Tạo và parse request
req = Request(raw_request).prepare(raw_request, routes)

# In ra các phần để kiểm tra
print("\n--- Parsed Request ---")
print("Method :", req.method)
print("Path   :", req.path)
print("Version:", req.version)
print("Headers:", req.headers)
print("Body   :", req.body)
print("Cookies:", getattr(req, 'cookies', {}))
print("Data   :", getattr(req, 'data', {}))

# Thử gọi handler (routing test)
if req.hook:
    print("\n--- Calling Handler ---")
    req.hook(req)
else:
    print("\n[Warning] No route found for this request.")

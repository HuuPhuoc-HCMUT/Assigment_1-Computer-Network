# import requests
# import time

# BASE = "http://127.0.0.1:9001"

# def post(path, data=None):
#     return requests.post(BASE + path, json=data, timeout=3)

# def get(path):
#     return requests.get(BASE + path, timeout=3)

# print("=== LOGIN user1 ===")
# post("/login", {
#     "username": "user1",
#     "password": "123456"
# })

# print("=== START peer user1 ===")
# post("/start", {"port": 9005})

# print("=== LOGIN user2 ===")
# post("/login", {
#     "username": "user2",
#     "password": "123456"
# })

# print("=== START peer user2 ===")
# post("/start", {"port": 9006})

# time.sleep(1)

# print("=== user1 DM user2 ===")
# post("/dm", {
#     "to": "user2",
#     "message": "hello user2"
# })

# time.sleep(1)

# print("=== user2 read messages ===")
# r = get("/messages?channel=global")
# print(r.json())





# import requests
# import time

# BASE = "http://127.0.0.1:9001"

# def post(path, data=None):
#     return requests.post(BASE + path, json=data, timeout=3)

# def get(path):
#     return requests.get(BASE + path, timeout=3)

# print("=== LOGIN user1 ===")
# post("/login", {"username": "user1", "password": "123456"})
# post("/start", {"port": 9005})

# print("=== LOGIN user2 ===")
# post("/login", {"username": "user2", "password": "123456"})
# post("/start", {"port": 9006})

# time.sleep(1)

# print("=== user1 DM user2 ===")
# post("/dm", {
#     "to": "user2",
#     "message": "hello user2"
# })

# time.sleep(1)

# print("=== user2 read DM inbox ===")
# r = get("/messages?channel=dm:user2")
# print(r.json())





# import requests
# import time

# # Peer HTTP API endpoints
# PEER1 = "http://127.0.0.1:9005"
# PEER2 = "http://127.0.0.1:9006"


# def post(base, path, data=None):
#     r = requests.post(base + path, json=data, timeout=3)
#     try:
#         return r.json()
#     except:
#         return r.text


# def get(base, path):
#     r = requests.get(base + path, timeout=3)
#     try:
#         return r.json()
#     except:
#         return r.text


# print("=== LOGIN user1 ===")
# print(post(PEER1, "/login", {
#     "username": "user1",
#     "password": "123456"
# }))

# print("=== START peer user1 ===")
# print(post(PEER1, "/start", {"port": 9005}))


# print("=== LOGIN user2 ===")
# print(post(PEER2, "/login", {
#     "username": "user2",
#     "password": "123456"
# }))

# print("=== START peer user2 ===")
# print(post(PEER2, "/start", {"port": 9006}))

# # cho tracker + heartbeat cập nhật
# time.sleep(1)


# print("=== user1 DM user2 ===")
# print(post(PEER1, "/dm", {
#     "to": "user2",
#     "message": "hello user2"
# }))

# time.sleep(1)


# print("=== user2 read DM inbox ===")
# r = get(PEER2, "/messages?channel=dm:user1")
# print(r)











BASE = "http://127.0.0.1:9007"
import requests, time

def post(path, data=None):
    return requests.post(BASE + path, json=data, timeout=3)

def get(path):
    return requests.get(BASE + path, timeout=3)

print("=== LOGIN user1 ===")
post("/login", {"username": "user1", "password": "123456"})
post("/start", {"port": 9005})

print("=== LOGIN user2 ===")
post("/login", {"username": "user2", "password": "123456"})
post("/start", {"port": 9006})

time.sleep(1)

print("=== user1 DM user2 (thực ra là user2 tự gửi cho chính nó) ===")
post("/dm", {"to": "user2", "message": "hello user2"})

time.sleep(1)

print("=== user2 read DM inbox ===")
r = get("/messages?channel=dm:user2")  # <<< QUAN TRỌNG
print(r.json())

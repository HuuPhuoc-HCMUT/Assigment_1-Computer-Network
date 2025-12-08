# from daemon.weaprous import WeApRous
# import json, time, os

# TOKENS_FILE = "tokens.json"

# print("=== DEBUG START ===")
# print("WORKING DIR:", os.getcwd())
# print("SERVER FILE DIR:", os.path.dirname(os.path.abspath(__file__)))
# print("TOKENS_FILE:", TOKENS_FILE)
# print("===================")

# app = WeApRous()

# # ======================================================
# #  TOKEN STORAGE
# # ======================================================

# def load_tokens():
#     if os.path.exists(TOKENS_FILE):
#         try:
#             with open(TOKENS_FILE, "r") as f:
#                 return json.load(f)
#         except:
#             return {}
#     return {}

# def save_tokens(tokens):
#     with open(TOKENS_FILE, "w") as f:
#         json.dump(tokens, f)


# # ======================================================
# # IN-MEMORY PEERS & MESSAGES
# # ======================================================
# MESSAGES = {}   # { peer_id : [ {"from":"...", "text":"..."} ] }

# # Peer mặc định (demo)
# PEERS = [
#     {"id": "A17F", "name": "Laptop-01", "online": True},
#     {"id": "B29C", "name": "Workstation", "online": True},
#     {"id": "C3D0", "name": "VM-Linux", "online": False},
#     {"id": "E58B", "name": "MacbookPro", "online": True},
# ]

# VALID_USERS = {
#     "admin": "123",
#     "peer1": "123",
#     "peer2": "123",
#     "peer3": "123",
# }

# # ======================================================
# # JSON PARSER (Fix full WeApRous body types)
# # ======================================================

# def parse_json(body):
#     try:
#         if isinstance(body, (bytes, bytearray)):
#             raw = body.decode()
#         elif isinstance(body, memoryview):
#             raw = body.tobytes().decode()
#         else:
#             raw = body
#         return json.loads(raw)
#     except Exception as e:
#         print("JSON ERROR:", e, "BODY:", body)
#         return None


# # ======================================================
# # AUTH CHECK
# # ======================================================

# def check_auth(headers):
#     # Header key bị chuyển thành lowercase bởi WeApRous
#     auth = headers.get("authorization", "")

#     if not auth.startswith("Bearer "):
#         return False

#     token = auth.replace("Bearer ", "")
#     tokens = load_tokens()
#     return token in tokens



# # ======================================================
# # LOGIN
# # ======================================================

# @app.route('/api/login', methods=['POST'])
# def login(headers, body):
#     data = parse_json(body)
#     if not data:
#         return {"ok": False, "error": "invalid json"}

#     user = data.get("username")
#     pw   = data.get("password")

#     if user in VALID_USERS and VALID_USERS[user] == pw:

#         token = f"tok_{user}_{int(time.time())}"

#         tokens = load_tokens()
#         tokens[token] = user
#         save_tokens(tokens)

#         # Gán peer ID theo username (tạo nếu chưa có)
#         found = False
#         for peer in PEERS:
#             if peer["id"] == user:
#                 peer["online"] = True
#                 found = True
#                 break

#         if not found:
#             PEERS.append({
#                 "id": user,
#                 "name": user,
#                 "online": True
#             })

#         return {"ok": True, "token": token}

#     return {"ok": False, "error": "wrong username/password"}


# # ======================================================
# # LOGOUT
# # ======================================================

# @app.route('/api/logout', methods=['POST'])
# def logout(headers, body):
#     auth = headers.get("Authorization", "")
#     token = auth.replace("Bearer ", "")

#     tokens = load_tokens()
#     if token in tokens:
#         tokens.pop(token)
#         save_tokens(tokens)

#     return {"ok": True}


# # ======================================================
# # GET PEERS
# # ======================================================

# @app.route('/api/peers', methods=['GET'])
# def get_peers(headers, body):
#     print("=== DEBUG AUTH HEADERS ===")
#     print(headers)
#     print("==========================")

#     if not check_auth(headers):
#         return {"ok": False, "error": "unauthorized"}

#     return {"ok": True, "peers": PEERS}



# # ======================================================
# # LOAD MESSAGES
# # ======================================================

# @app.route('/api/messages', methods=['POST'])
# def load_messages(headers, body):
#     if not check_auth(headers):
#         return {"ok": False, "error": "unauthorized"}

#     data = parse_json(body)
#     if not data:
#         return {"ok": False, "error": "invalid json"}

#     peer = data.get("peer_id")
#     return {"ok": True, "messages": MESSAGES.get(peer, [])}


# # ======================================================
# # SEND MESSAGE
# # ======================================================

# @app.route('/api/send', methods=['POST'])
# def send(headers, body):
#     if not check_auth(headers):
#         return {"ok": False, "error": "unauthorized"}

#     data = parse_json(body)
#     if not data:
#         return {"ok": False, "error": "invalid json"}

#     peer = data.get("peer_id")
#     msg  = data.get("msg")

#     if peer not in MESSAGES:
#         MESSAGES[peer] = []

#     MESSAGES[peer].append({
#         "from": "me",
#         "text": msg
#     })

#     return {"ok": True}


# # ======================================================
# # STATIC FILE SERVER
# # ======================================================

# STATIC_DIR = "www"

# @app.route('/<path>', methods=['GET'])
# def serve_static(headers, body, path):
#     filepath = os.path.join(STATIC_DIR, path)

#     if not os.path.exists(filepath):
#         return ("File not found", 404)

#     if path.endswith(".html"):
#         headers["Content-Type"] = "text/html"
#     elif path.endswith(".css"):
#         headers["Content-Type"] = "text/css"
#     elif path.endswith(".js"):
#         headers["Content-Type"] = "application/javascript"

#     with open(filepath, "r", encoding="utf-8") as f:
#         return f.read()


# @app.route('/', methods=['GET'])
# def root(headers, body):
#     return '<script>window.location="/login.html"</script>'


# # ======================================================
# # RUN SERVER
# # ======================================================

# if __name__ == "__main__":
#     app.prepare_address("127.0.0.1", 8000)
#     app.run()








from daemon.weaprous import WeApRous
import json, time, os

TOKENS_FILE = "tokens.json"

print("=== DEBUG START ===")
print("WORKING DIR:", os.getcwd())
print("SERVER FILE DIR:", os.path.dirname(os.path.abspath(__file__)))
print("TOKENS_FILE:", TOKENS_FILE)
print("===================")

app = WeApRous()

# ======================================================
# TOKEN STORAGE
# ======================================================

def load_tokens():
    if os.path.exists(TOKENS_FILE):
        try:
            with open(TOKENS_FILE, "r") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_tokens(tokens):
    with open(TOKENS_FILE, "w") as f:
        json.dump(tokens, f)


# ======================================================
# IN-MEMORY PEERS & MESSAGES
# ======================================================

# Lưu tin nhắn theo CẶP, không phải theo peer_id một phía
# key = tuple(sorted([userA, userB]))
MESSAGES = {}

# Peer mặc định (demo)
PEERS = [
    {"id": "A17F", "name": "Laptop-01", "online": True},
    {"id": "B29C", "name": "Workstation", "online": True},
    {"id": "C3D0", "name": "VM-Linux", "online": False},
    {"id": "E58B", "name": "MacbookPro", "online": True},
]

VALID_USERS = {
    "admin": "123",
    "peer1": "123",
    "peer2": "123",
    "peer3": "123",
}


# ======================================================
# JSON PARSER
# ======================================================

def parse_json(body):
    try:
        if isinstance(body, (bytes, bytearray)):
            raw = body.decode()
        elif isinstance(body, memoryview):
            raw = body.tobytes().decode()
        else:
            raw = body
        return json.loads(raw)
    except Exception as e:
        print("JSON ERROR:", e, "BODY:", body)
        return None


# ======================================================
# AUTH
# ======================================================

def check_auth(headers):
    auth = headers.get("authorization", "")
    if not auth.startswith("Bearer "):
        return None

    token = auth.replace("Bearer ", "")
    tokens = load_tokens()

    if token not in tokens:
        return None

    return tokens[token]   # return username


# ======================================================
# LOGIN
# ======================================================

@app.route('/api/login', methods=['POST'])
def login(headers, body):
    data = parse_json(body)
    if not data:
        return {"ok": False, "error": "invalid json"}

    user = data.get("username")
    pw   = data.get("password")

    if user in VALID_USERS and VALID_USERS[user] == pw:

        token = f"tok_{user}_{int(time.time())}"

        tokens = load_tokens()
        tokens[token] = user
        save_tokens(tokens)

        # Đánh dấu online
        found = False
        for peer in PEERS:
            if peer["id"] == user:
                peer["online"] = True
                found = True
                break

        if not found:
            PEERS.append({
                "id": user,
                "name": user,
                "online": True
            })

        return {"ok": True, "token": token}

    return {"ok": False, "error": "wrong username/password"}


# ======================================================
# LOGOUT
# ======================================================

@app.route('/api/logout', methods=['POST'])
def logout(headers, body):
    auth = headers.get("authorization", "")
    token = auth.replace("Bearer ", "")

    tokens = load_tokens()
    if token in tokens:
        tokens.pop(token)
        save_tokens(tokens)

    return {"ok": True}


# ======================================================
# GET PEERS
# ======================================================

@app.route('/api/peers', methods=['GET'])
def get_peers(headers, body):

    username = check_auth(headers)
    if not username:
        return {"ok": False, "error": "unauthorized"}

    return {"ok": True, "peers": PEERS}


# ======================================================
# LOAD MESSAGES — theo cặp (sender <-> peer)
# ======================================================

@app.route('/api/messages', methods=['POST'])
def load_messages(headers, body):

    sender = check_auth(headers)
    if not sender:
        return {"ok": False, "error": "unauthorized"}

    data = parse_json(body)
    if not data:
        return {"ok": False, "error": "invalid json"}

    peer = data.get("peer_id")
    if not peer:
        return {"ok": False, "error": "missing peer_id"}

    # Key cho cặp chat
    key = tuple(sorted([sender, peer]))

    return {"ok": True, "messages": MESSAGES.get(key, [])}


# ======================================================
# SEND MESSAGE — theo cặp chat
# ======================================================

@app.route('/api/send', methods=['POST'])
def send(headers, body):

    sender = check_auth(headers)
    if not sender:
        return {"ok": False, "error": "unauthorized"}

    data = parse_json(body)
    if not data:
        return {"ok": False, "error": "invalid json"}

    peer = data.get("peer_id")
    msg  = data.get("msg")

    if not peer or not msg:
        return {"ok": False, "error": "missing fields"}

    key = tuple(sorted([sender, peer]))

    if key not in MESSAGES:
        MESSAGES[key] = []

    MESSAGES[key].append({
        "from": sender,   # không dùng "me" nữa
        "text": msg,
        "timestamp": int(time.time())
    })

    return {"ok": True}


# ======================================================
# STATIC FILE SERVER
# ======================================================

STATIC_DIR = "www"

@app.route('/<path>', methods=['GET'])
def serve_static(headers, body, path):
    filepath = os.path.join(STATIC_DIR, path)

    if not os.path.exists(filepath):
        return ("File not found", 404)

    if path.endswith(".html"):
        headers["Content-Type"] = "text/html"
    elif path.endswith(".css"):
        headers["Content-Type"] = "text/css"
    elif path.endswith(".js"):
        headers["Content-Type"] = "application/javascript"

    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


@app.route('/', methods=['GET'])
def root(headers, body):
    return '<script>window.location="/login.html"</script>'


# ======================================================
# RUN
# ======================================================

if __name__ == "__main__":
    app.prepare_address("127.0.0.1", 8000)
    app.run()

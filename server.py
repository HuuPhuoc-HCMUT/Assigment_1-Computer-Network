# tracker.py
from daemon import create_backend
import json, time, secrets

USERS = {
    "admin": "password",
    "user1": "123456",
    "user2": "123456",
    "user3": "123456",
    "user4": "123456"
}
SESSIONS = {}                  # token -> username
PEERS = {}                     # peer_id -> info


def json_response(obj, status=200):
    return {
        "status": status,
        "json": obj
    }


def route_login(headers, body, cookies):
    data = json.loads(body or "{}")
    user = data.get("username", "")
    pwd = data.get("password", "")

    if USERS.get(user) != pwd:
        return json_response({"status": "error", "error": "invalid_credentials"}, 401)

    token = secrets.token_hex(32)
    SESSIONS[token] = {"username": user, "exp": time.time() + 3600}

    return json_response({"status": "ok", "token": token})


def get_username_from_token(token):
    s = SESSIONS.get(token)
    if not s:
        return None
    if s["exp"] < time.time():
        del SESSIONS[token]
        return None
    return s["username"]


def route_submit_info(headers, body, cookies):
    data = json.loads(body or "{}")
    token = data.get("token")
    username = get_username_from_token(token)
    if not username:
        return json_response({"status": "error", "error": "unauthorized"}, 401)

    listen_port = int(data.get("listen_port", 0))
    if not listen_port:
        return json_response({"status": "error", "error": "missing_listen_port"}, 400)

    channels = set(data.get("channels", []))

    # lấy IP từ headers do daemon cung cấp, ví dụ:
    ip = headers.get("remote_addr", "0.0.0.0")

    peer_id = data.get("peer_id") or secrets.token_hex(8)
    PEERS[peer_id] = {
        "username": username,
        "ip": ip,
        "port": listen_port,
        "channels": channels,
        "last_seen": time.time()
    }

    return json_response({"status": "ok", "peer_id": peer_id})


def route_get_list(headers, body, cookies):
    # giả sử daemon parse query string ra headers["query"] = dict
    query = headers.get("query", {})
    token = query.get("token")
    username = get_username_from_token(token)
    if not username:
        return json_response({"status": "error", "error": "unauthorized"}, 401)

    channel = query.get("channel")  # có thể None = lấy tất cả
    now = time.time()
    res = []

    for pid, info in PEERS.items():
        # timeout 30s
        if now - info["last_seen"] > 30:
            continue
        if channel and channel not in info["channels"]:
            continue
        if info["username"] == username:
            continue

        res.append({
            "peer_id": pid,
            "username": info["username"],
            "ip": info["ip"],
            "port": info["port"]
        })

    return json_response({"status": "ok", "peers": res})


def route_add_list(headers, body, cookies):
    data = json.loads(body or "{}")
    token = data.get("token")
    username = get_username_from_token(token)
    if not username:
        return json_response({"status": "error", "error": "unauthorized"}, 401)

    channel = data.get("channel")
    if not channel:
        return json_response({"status": "error", "error": "missing_channel"}, 400)

    # thêm channel cho tất cả peer của user này (đơn giản)
    for info in PEERS.values():
        if info["username"] == username:
            info["channels"].add(channel)

    return json_response({"status": "ok"})


def route_connect_peer(headers, body, cookies):
    data = json.loads(body or "{}")
    token = data.get("token")
    target = data.get("target")  # username muốn connect

    username = get_username_from_token(token)
    if not username:
        return json_response({"status": "error", "error": "unauthorized"}, 401)

    if not target:
        return json_response({"status": "error", "error": "missing_target"}, 400)

    for peer_id, info in PEERS.items():
        if info["username"] == target:
            return json_response({
                "status": "ok",
                "peer": {
                    "username": target,
                    "ip": info["ip"],
                    "port": info["port"]
                }
            })

    return json_response({"status": "error", "error": "peer_not_found"}, 404)


def route_send_peer(headers, body, cookies):
    data = json.loads(body or "{}")
    token = data.get("token")
    to = data.get("to")
    message = data.get("message")

    if not get_username_from_token(token):
        return json_response(
            {"status": "error", "error": "unauthorized"}, 401
        )

    if not to or not message:
        return json_response(
            {"status": "error", "error": "missing_fields"}, 400
        )

    # KHÔNG relay message
    return json_response({
        "status": "ok",
        "note": "message delivered via P2P"
    })


def route_send_peer(headers, body, cookies):
    data = json.loads(body or "{}")
    token = data.get("token")
    to = data.get("to")
    message = data.get("message")

    if not get_username_from_token(token):
        return json_response(
            {"status": "error", "error": "unauthorized"}, 401
        )

    if not to or not message:
        return json_response(
            {"status": "error", "error": "missing_fields"}, 400
        )

    # KHÔNG relay message
    return json_response({
        "status": "ok",
        "note": "message delivered via P2P"
    })



def route_broadcast_peer(headers, body, cookies):
    data = json.loads(body or "{}")
    token = data.get("token")
    channel = data.get("channel")
    message = data.get("message")

    if not get_username_from_token(token):
        return json_response(
            {"status": "error", "error": "unauthorized"}, 401
        )

    if not channel or not message:
        return json_response(
            {"status": "error", "error": "missing_fields"}, 400
        )

    return json_response({
        "status": "ok",
        "note": "broadcast delivered via P2P"
    })



routes = {
    ('PUT', '/login'): route_login,
    ('POST', '/submit-info'): route_submit_info,
    ('GET', '/get-list'): route_get_list,
    ('POST', '/add-list'): route_add_list,
    ('POST', '/connect-peer'): route_connect_peer,
    ('POST', '/send-peer'): route_send_peer,
    ('POST', '/broadcast-peer'): route_broadcast_peer
}

create_backend('0.0.0.0', 8000, routes)

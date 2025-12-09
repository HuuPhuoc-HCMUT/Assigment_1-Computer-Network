# peer_server.py
from daemon.weaprous import WeApRous
import json, time, threading, os

from peer import (
    TrackerClient,
    P2PClient,
    P2PServer,
    ChannelManager,
    heartbeat_loop
)

# -------------------------
# GLOBAL STATE (peer runtime)
# -------------------------
TRACKER_URL = "http://127.0.0.1:8000"

app = WeApRous()

tracker = TrackerClient(TRACKER_URL)
channel_manager = ChannelManager()

listen_port = None
channels = ["global"]
username = None

# -------------------------
# Helpers
# -------------------------
def cors_headers():
    return {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type"
    }


# -------------------------
# API ROUTES
# -------------------------
@app.route("/login", methods=["POST"])
def login(headers, body, cookies):
    global username
    data = json.loads(body or "{}")
    username = data.get("username")

    if tracker.login(data["username"], data["password"]):
        return {"ok": True}
    return {"error": "login_failed"}



@app.route("/start", methods=["POST"])
def start_peer(headers, body, cookies):
    global listen_port

    data = json.loads(body or "{}")
    listen_port = int(data["port"])

    tracker.submit_info(listen_port, channels)

    # start P2P server
    P2PServer("0.0.0.0", listen_port, channel_manager).start()

    # start heartbeat thread
    threading.Thread(
        target=heartbeat_loop,
        args=(tracker, listen_port, channels),
        daemon=True
    ).start()

    return {"port": listen_port}



@app.route("/peers", methods=["GET"])
def peers(headers, body, cookies):
    query = headers.get("query", {})
    channel = query.get("channel", "global")
    return tracker.get_peer_list(channel)



@app.route("/dm", methods=["POST"])
def dm(headers, body, cookies):
    data = json.loads(body or "{}")

    peer = tracker.connect_peer(data["to"])
    if not peer:
        return {"error": "peer_not_found"}

    P2PClient.send(peer, {
        "type": "direct",
        "from": username,
        "to": data["to"],
        "message": data["message"],
        "timestamp": time.time()
    })

    return {"ok": True}


@app.route("/broadcast", methods=["POST"])
def broadcast(headers, body, cookies):
    data = json.loads(body or "{}")
    channel = data.get("channel", "global")
    message = data["message"]

    peers = tracker.get_peer_list(channel)
    for p in peers:
        P2PClient.send(p, {
            "type": "broadcast",
            "from": username,
            "channel": channel,
            "message": message,
            "timestamp": time.time()
        })

    return {"ok": True}



@app.route("/", methods=["GET"])
def index(headers, body, cookies):
    with open("index.html") as f:
        return {
            "status": 200,
            "headers": {"Content-Type": "text/html"},
            "body": f.read()
        }


@app.route("/messages", methods=["GET"])
def messages(headers, body, cookies):
    query = headers.get("query", {})
    channel = query.get("channel", "global")
    return channel_manager.get_messages(channel)




@app.route("/login", methods=["OPTIONS"])
@app.route("/start", methods=["OPTIONS"])
@app.route("/peers", methods=["OPTIONS"])
@app.route("/dm", methods=["OPTIONS"])
@app.route("/broadcast", methods=["OPTIONS"])
def cors_preflight(headers, body, cookies):
    return {
        "status": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type"
        }
    }



# -------------------------
# MAIN
# -------------------------

if __name__ == "__main__":
    port = int(os.environ.get("PEER_PORT", "9001"))
    print(f"[Peer] HTTP API listening on {port}")

    app.prepare_address("127.0.0.1", port)
    app.run()

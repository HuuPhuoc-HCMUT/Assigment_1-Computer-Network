# peer.py
import socket
import threading
import json
import time
import requests
import sys

TRACKER_URL = "http://127.0.0.1:8000"
HEARTBEAT_INTERVAL = 10
P2P_BUFFER = 4096


class ChannelManager:
    def __init__(self):
        self.channels = {}   # channel -> list of messages
        self.lock = threading.Lock()

    def add_message(self, channel, msg):
        with self.lock:
            self.channels.setdefault(channel, []).append(msg)

    def get_messages(self, channel):
        with self.lock:
            return list(self.channels.get(channel, []))


class TrackerClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.token = None
        self.peer_id = None
        self.peer_cache = {}   # username -> peer info

        self.username = None
        self.password = None

    def login(self, username, password):
        self.username = username
        self.password = password

        r = requests.put(
            f"{self.base_url}/login",
            json={"username": username, "password": password}
        )
        if r.status_code != 200:
            print("Login failed")
            return False

        data = r.json()
        print(data)
        self.token = data["json"]["token"]
        return True
    


    def relogin(self):
        if not self.username or not self.password:
            print("[ERROR] no credential to relogin")
            return False

        print("[INFO] re-login to tracker")
        return self.login(self.username, self.password)
    
    

    def submit_info(self, listen_port, channels):
        payload = {
            "token": self.token,
            "listen_port": listen_port,
            "channels": channels
        }

        if self.peer_id:
            payload["peer_id"] = self.peer_id

        r = requests.post(
            f"{self.base_url}/submit-info",
            json=payload
        )

        if r.status_code == 401:
            print("[INFO] session expired, re-login required")
            return "RELOGIN"

        if r.status_code != 200:
            return False

        self.peer_id = r.json()["json"]["peer_id"]
        return True

        

    def get_peer_list(self, channel):
        try:
            r = requests.get(
                f"{self.base_url}/get-list",
                params={"token": self.token, "channel": channel}
            )

            if r.status_code == 200:
                peers = r.json()["json"]["peers"]
                for p in peers:
                    self.peer_cache[p["username"]] = p
                return peers

        except Exception as e:
            print("[WARN] Tracker offline, using cached peers")
            return []

        if r.status_code != 200:
            print("get-list failed")
            return []
        
        return list(self.peer_cache.values())
    


    def connect_peer(self, target):
        r = requests.post(
            f"{self.base_url}/connect-peer",
            json={
                "token": self.token,
                "target": target
            }
        )
        if r.status_code != 200:
            return None
        return r.json()["json"]["peer"]

    def send_peer_api(self, to, message):
        try:
            requests.post(
                f"{self.base_url}/send-peer",
                json={
                    "token": self.token,
                    "to": to,
                    "message": message
                }
            )
        except Exception as e:
            print("[WARN] Tracker offline, skip send-peer API")

    def broadcast_peer_api(self, channel, message):
        try:
            requests.post(
                f"{self.base_url}/broadcast-peer",
                json={
                    "token": self.token,
                    "channel": channel,
                    "message": message
                }
            )
        except Exception as e:
            print("[WARN] Tracker offline, skip broadcast-peer API")



class P2PServer(threading.Thread):
    def __init__(self, host, port, channel_manager):
        super().__init__(daemon=True)
        self.host = host
        self.port = port
        self.channel_manager = channel_manager

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((self.host, self.port))
        sock.listen()

        print(f"[P2P] Listening on {self.port}")

        while True:
            conn, addr = sock.accept()
            threading.Thread(
                target=self.handle_peer,
                args=(conn, addr),
                daemon=True
            ).start()

    def handle_peer(self, conn, addr):
        try:
            data = conn.recv(P2P_BUFFER)
            msg = json.loads(data.decode())

            if msg["type"] == "broadcast":
                channel = msg["channel"]
                self.channel_manager.add_message(channel, msg)
                print(f"\n[{channel}] {msg['from']}: {msg['message']}")

            elif msg["type"] == "direct":
                channel = f"dm:{msg['from']}"
                self.channel_manager.add_message(channel, msg)

        except Exception as e:
            print("P2P error:", e)
        finally:
            conn.close()



class P2PClient:
    @staticmethod
    def send(peer, payload):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((peer["ip"], peer["port"]))
            sock.sendall(json.dumps(payload).encode())
            sock.close()
        except Exception as e:
            print("Send failed:", e)


def heartbeat_loop(tracker, listen_port, channels):
    while True:
        try:
            res = tracker.submit_info(listen_port, channels)

            if res == "RELOGIN":
                print("[INFO] re-login to tracker")
                if tracker.relogin():
                    tracker.submit_info(listen_port, channels)

        except Exception:
            pass
        time.sleep(HEARTBEAT_INTERVAL)



def main():
    username = input("Username: ")
    password = input("Password: ")

    tracker = TrackerClient(TRACKER_URL)
    if not tracker.login(username, password):
        return

    listen_port = int(input("P2P listen port: "))
    channels = ["global"]

    if not tracker.submit_info(listen_port, channels):
        return

    channel_manager = ChannelManager()

    # Start P2P server
    p2p_server = P2PServer("0.0.0.0", listen_port, channel_manager)
    p2p_server.start()

    # Start heartbeat
    threading.Thread(
        target=heartbeat_loop,
        args=(tracker, listen_port, channels),
        daemon=True
    ).start()

    current_channel = "global"

    print("\nCommands:")
    print("/peers           list peers")
    print("/join <channel>  join channel")
    print("/dm <user> <msg> direct message")
    print("/quit")

    while True:
        msg = input("> ").strip()

        if msg == "/quit":
            sys.exit(0)

        if msg.startswith("/peers"):
            peers = tracker.get_peer_list(current_channel)
            for p in peers:
                print(p["username"], p["ip"], p["port"])
            continue

        if msg.startswith("/join"):
            _, ch = msg.split(maxsplit=1)
            if ch not in channels:
                channels.append(ch)
            current_channel = ch
            print(f"Joined channel {ch}")
            continue

        if msg.startswith("/dm"):
            _, user, text = msg.split(maxsplit=2)

            tracker.send_peer_api(user, text)

            peers = tracker.peer_cache.get(user)

            if not peers:
                print("User not found")
                continue
            
            P2PClient.send(peers, {
                "type": "direct",
                "from": username,
                "message": text,
                "timestamp": time.time()
            })
            continue

        # broadcast
        peers = tracker.get_peer_list(current_channel)
        for p in peers:
            P2PClient.send(p, {
                "type": "broadcast",
                "from": username,
                "channel": current_channel,
                "message": msg,
                "timestamp": time.time()
            })



if __name__ == "__main__":
    main()

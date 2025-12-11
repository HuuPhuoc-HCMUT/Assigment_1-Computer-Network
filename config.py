# config.py - Cấu hình mạng cho P2P Chat

# IP của máy chạy Tracker Server
# - Nếu chạy local: dùng "127.0.0.1"  
# - Nếu chạy qua mạng LAN: dùng IP thực (ví dụ: "10.130.17.55")
TRACKER_HOST = "127.0.0.1"
TRACKER_PORT = 8000

TRACKER_URL = f"http://{TRACKER_HOST}:{TRACKER_PORT}"

# IP để bind peer server
# - "127.0.0.1" = chỉ localhost truy cập được
# - "0.0.0.0" = cho phép máy khác trong mạng LAN truy cập
PEER_BIND_IP = "0.0.0.0"

# IP thực của peer để gửi cho tracker
# - Nếu chạy local: dùng "127.0.0.1"
# - Nếu chạy qua mạng LAN: dùng IP thực (ví dụ: "10.130.17.55")
MY_IP = "127.0.0.1"




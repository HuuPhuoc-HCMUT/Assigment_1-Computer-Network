#!/usr/bin/env python3
"""
Mở 4 VS Code Terminal + 3 HTML files
Chạy: python run_all.py
"""

import subprocess
import os
import webbrowser
import time

DIR = os.path.dirname(os.path.abspath(__file__))

commands = [
    "python server.py",
    "PEER_PORT=10005 python peer_server.py",
    "PEER_PORT=10006 python peer_server.py",
    "PEER_PORT=10007 python peer_server.py"
]

print("✅ Opening 4 VS Code terminals...")
print("⚠️  Hãy tắt bộ gõ tiếng Việt (chuyển sang English)")
time.sleep(1)

for cmd in commands:
    # Copy lệnh vào clipboard
    subprocess.run(['pbcopy'], input=cmd.encode(), check=True)
    
    # Mở terminal mới và paste
    applescript = '''
    tell application "Visual Studio Code"
        activate
    end tell
    delay 0.3
    tell application "System Events"
        tell process "Code"
            key code 50 using {control down, shift down}
            delay 0.5
            key code 9 using {command down}
            delay 0.2
            key code 36
        end tell
    end tell
    '''
    subprocess.run(['osascript', '-e', applescript])
    time.sleep(1)

print("✅ Opened 4 VS Code terminals")

# Đợi server khởi động
time.sleep(2)

# Mở 3 HTML files
for port in [10005, 10006, 10007]:
    webbrowser.open(f"file://{DIR}/index_{port}.html")

print("✅ Opened 3 HTML files")

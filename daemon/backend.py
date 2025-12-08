#
# Copyright (C) 2025 pdnguyen…
#

"""
daemon.backend
~~~~~~~~~~~~~~~~~
Backend server hỗ trợ HTTP basic để chạy kèm HttpAdapter.
"""

import socket
import threading
import argparse

from .httpadapter import HttpAdapter
from .dictionary import CaseInsensitiveDict


def handle_client(ip, port, conn, addr, routes):
    """
    Tạo HttpAdapter cho mỗi client và xử lý request.
    """
    daemon = HttpAdapter(ip, port, conn, addr, routes)
    daemon.handle_client(conn, addr, routes)


def run_backend(ip, port, routes):
    """
    Chạy server backend:
        - tạo socket
        - bind ip/port
        - accept clients
        - mỗi client chạy trong 1 thread
    """

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind((ip, port))
        server.listen(50)
        print("[Backend] Listening on {}:{}".format(ip, port))

        print("Đã vào File Backend")
        
        if routes:
            print("[Backend] Loaded routes:")
            for k, v in routes.items():
                print("   →  METHOD={} PATH={}  => {}".format(k[0], k[1], v))

        while True:
            conn, addr = server.accept()
            print(f"[Backend] Incoming connection from {addr}")

            # Tạo thread để xử lý client
            client_thread = threading.Thread(
                target=handle_client,
                args=(ip, port, conn, addr, routes),
                daemon=True                  # thread tự tắt khi main tắt
            )
            client_thread.start()

    except socket.error as e:
        print("Socket error:", e)

    finally:
        server.close()


def create_backend(ip, port, routes={}):
    """
    Entry point để chạy server.
    """
    run_backend(ip, port, routes)

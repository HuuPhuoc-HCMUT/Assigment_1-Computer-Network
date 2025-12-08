import json
from .request import Request
from .response import Response

class HttpAdapter:

    def __init__(self, ip, port, conn, connaddr, routes):
        self.ip = ip
        self.port = port
        self.conn = conn
        self.connaddr = connaddr
        self.routes = routes
        self.response = Response()

    def handle_client(self, conn, addr, routes):

        raw = self.recv_all(conn)
        if not raw.strip():
            conn.close()
            return

        # Parse request
        try:
            req = Request(raw)
            req.prepare(raw, routes)
            req.headers["remote_addr"] = addr[0]
            # Sau bước prepare thì req là 1 object request đã được parser full thông tin
        except Exception as e:
            print("[HttpAdapter] Error parsing request:", e)
            err = (
                "HTTP/1.1 400 Bad Request\r\n"
                "Content-Type: text/plain\r\n"
                "Content-Length: 11\r\n"
                "Connection: close\r\n\r\n"
                "Bad Request"
            ).encode()
            conn.sendall(err)
            conn.close()
            return

        # -----------------------
        # 1. Nếu là API (HOOK)
        # -----------------------
        print("đã đến được Hook của httpadapter")
        if req.hook:
            try:
                # result = req.hook(headers=req.headers, body=req.body)
                result = req.hook(headers=req.headers, body=req.body, cookies=req.cookies)
                print(f"in thử result: {result}")
                # Auto JSON
                # if isinstance(result, dict):
                #     body = json.dumps(result).encode("utf-8")
                #     header = (
                #         "HTTP/1.1 200 OK\r\n"
                #         "Content-Type: application/json\r\n"
                #         f"Content-Length: {len(body)}\r\n"
                #         "Connection: close\r\n\r\n"
                #     ).encode()
                #     conn.sendall(header + body)
                #     return

                if isinstance(result, dict):

                    # ---- 1. Status code ----
                    status = result.get("status", 200)
                    if status == 200:
                        reason = "OK"
                    elif status == 401:
                        reason = "Unauthorized"
                    elif status == 302:
                        reason = "Found"
                    else:
                        reason = "OK"

                    # ---- 2. Cookie ----
                    if "cookie" in result:
                        cookie = result["cookie"]
                        header_extra = f"Set-Cookie: {cookie}\r\n"
                    else:
                        header_extra = ""

                    # ---- 3. Body (html or json) ----
                    if "html" in result:
                        body = result["html"].encode()
                        content_type = "text/html"
                    else:
                        body = json.dumps(result).encode()
                        content_type = "application/json"

                    # ---- 4. Build header ----
                    header = (
                        f"HTTP/1.1 {status} {reason}\r\n"
                        f"Content-Type: {content_type}\r\n"
                        f"Content-Length: {len(body)}\r\n"
                        f"{header_extra}"
                        "Connection: close\r\n\r\n"
                    ).encode()

                    conn.sendall(header + body)
                    return


                # Plain text
                elif isinstance(result, str):
                    body = result.encode("utf-8")
                    header = (
                        "HTTP/1.1 200 OK\r\n"
                        "Content-Type: text/plain\r\n"
                        f"Content-Length: {len(body)}\r\n"
                        "Connection: close\r\n\r\n"
                    ).encode()
                    conn.sendall(header + body)
                    print("Check thử body này")
                    return

                else:  # unsupported
                    resp = self.response
                    resp.status_code = 500
                    resp.body = "Unsupported return type"
                    conn.sendall(resp.build_response(req))
                    return

            except Exception as e:
                print("[Hook error]", e)
                resp = self.response
                resp.status_code = 500
                resp.body = "Hook error"
                conn.sendall(resp.build_response(req))

                print("Vuive")
                print("[Hook error]", type(e), e)
                return

        # -----------------------
        # 2. Không phải API → STATIC FILE
        # -----------------------
        response = self.response.build_response(req)
        print("Trước hello")
        conn.sendall(response)
        conn.close()


    # receive enough bytes
    def recv_all(self, conn):
        chunks = []
        conn.settimeout(0.2)
        try:
            while True:
                data = conn.recv(4096)
                if not data:
                    break
                chunks.append(data)
                if len(data) < 4096:
                    break
        except Exception:
            pass
        return b"".join(chunks).decode(errors="ignore")

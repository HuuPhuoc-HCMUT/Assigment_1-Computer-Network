# My Httpadapter.py
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
        self.request = Request()
        self.response = Response()


    def handle_client(self, conn, addr, routes):
        """
        Handle single HTTP client connection

        Steps:
            1. Receive full data from socket
            2. Parse HTTP request by using request.py
            3. Routing
            4. Serve static page
            5. Send back response and close connection

        """
        
        self.conn = conn
        self.connaddr = addr
        req = self.request
        resp = self.response

        # Nhận HTTP Request
        raw = self.recv_all(conn)  # Sửa lại do có thể dài hơn 1024 bytes
        if not raw.strip():
            conn.close()
            return
    
        # Parse request
        try: 
            req.prepare(raw, routes)
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
        
        # Handle Hook
        try:
            if req.hook:
                result = req.hook(headers=req.headers, body=req.body)

                if isinstance(result, dict):
                    resp.status_code = 200
                    resp.headers["Content-Type"] = "application/json"
                    resp.body = json.dumps(result)

                elif isinstance(result, str):
                    resp.status_code = 200
                    resp.headers["Content-Type"] = "text/plain"
                    resp.body = result

                else:
                    resp.status_code = 500
                    resp.body = "Unsupported return type from route"

        except Exception as e:
            resp.status_code = 500
            resp.body = f"Hook error: {str(e)}"
            

        # Build response
        send_response = resp.build_response(req)
        conn.sendall(send_response)
        conn.close()



    def build_proxy_headers(self, proxy):
        """Returns a dictionary of the headers to add to any request sent
        through a proxy. 

        :class:`HttpAdapter <HttpAdapter>`.

        :param proxy: The url of the proxy being used for this request.
        :rtype: dict
        """
        headers = {}
        #
        # TODO: build your authentication here
        #       username, password =...
        # we provide dummy auth here
        #
        username, password = ("user1", "password")

        if username:
            headers["Proxy-Authorization"] = (username, password)

        return headers



































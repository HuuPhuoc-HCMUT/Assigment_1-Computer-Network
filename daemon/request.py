# #
# # Copyright (C) 2025 pdnguyen of HCMC University of Technology VNU-HCM.
# # All rights reserved.
# # This file is part of the CO3093/CO3094 course.
# #
# # WeApRous release
# #
# # The authors hereby grant to Licensee personal permission to use
# # and modify the Licensed Source Code for the sole purpose of studying
# # while attending the course
# #

# """
# daemon.request
# ~~~~~~~~~~~~~~~~~

# This module provides a Request object to manage and persist 
# request settings (cookies, auth, proxies).
# """
# from .dictionary import CaseInsensitiveDict

# class Request():
#     """The fully mutable "class" `Request <Request>` object,
#     containing the exact bytes that will be sent to the server.

#     Instances are generated from a "class" `Request <Request>` object, and
#     should not be instantiated manually; doing so may produce undesirable
#     effects.

#     Usage::

#       >>> import daemon.request
#       >>> req = request.Request()
#       ## Incoming message obtain aka. incoming_msg
#       >>> r = req.prepare(incoming_msg)
#       >>> r
#       <Request>
#     """
#     __attrs__ = [
#         "method",
#         "url",
#         "headers",
#         "body",
#         "reason",
#         "cookies",
#         "body",
#         "routes",
#         "hook",
#     ]

#     def __init__(self):
#         #: HTTP verb to send to the server.
#         self.method = None
#         #: HTTP URL to send the request to.
#         self.url = None
#         #: dictionary of HTTP headers.
#         self.headers = None
#         #: HTTP path
#         self.path = None        
#         # The cookies set used to create Cookie header
#         self.cookies = None
#         #: request body to send to the server.
#         self.body = None
#         #: Routes
#         self.routes = {}
#         #: Hook point for routed mapped-path
#         self.hook = None

#         self.version = None

#     def extract_request_line(self, request):
#         try:
#             lines = request.splitlines()
#             first_line = lines[0]
#             method, path, version = first_line.split()

#             if path == '/':
#                 path = '/index.html'
#         except Exception:
#             return None, None

#         return method, path, version
             
#     def prepare_headers(self, request):
#         """Prepares the given HTTP headers."""
#         lines = request.split('\r\n')
#         headers = {}
#         for line in lines[1:]:
#             if ': ' in line:
#                 key, val = line.split(': ', 1)
#                 headers[key.lower()] = val
#         return headers

#     def prepare(self, request, routes=None):
#         """Prepares the entire request with the given parameters."""

#         # Prepare the request line from the request header
#         self.method, self.path, self.version = self.extract_request_line(request)
#         print("[Request] {} path {} version {}".format(self.method, self.path, self.version))

#         #
#         # @bksysnet Preapring the webapp hook with WeApRous instance
#         # The default behaviour with HTTP server is empty routed
#         #
#         # TODO manage the webapp hook in this mounting point
#         #
        
#         if not routes == {}:
#             self.routes = routes
#             self.hook = routes.get((self.method, self.path))
#             #
#             # self.hook manipulation goes here
#             # ...
#             #

#         self.headers = self.prepare_headers(request)
#         cookies = self.headers.get('cookie', '')
#             #
#             #  TODO: implement the cookie function here
#             #        by parsing the header            #

#         return

#     def prepare_body(self, data, files, json=None):
#         self.prepare_content_length(self.body)
#         self.body = body
#         #
#         # TODO prepare the request authentication
#         #
# 	# self.auth = ...
#         return


#     def prepare_content_length(self, body):
#         self.headers["Content-Length"] = "0"
#         #
#         # TODO prepare the request authentication
#         #
# 	# self.auth = ...
#         return


#     def prepare_auth(self, auth, url=""):
#         #
#         # TODO prepare the request authentication
#         #
# 	# self.auth = ...
#         return

#     def prepare_cookies(self, cookies):
#             self.headers["Cookie"] = cookies




#* My Request.py
from urllib.parse import parse_qs

class Request():
    def __init__(self, raw_request:str):
        self.raw = raw_request

        # meta data
        self.method = None
        self.path = None
        self.version = None
        self.url = None

        # header và cookies
        self.headers = {}
        self.cookies = {}

        # body
        self.body = ''
        self.data = {}

        # routing
        self.routes = {}
        self.hook = None

    # def parse_request_line(self, request_lines):
    #     try:
    #         method, path, version = request_lines.split()    # tách theo dấu cách: GET /index.html HTTP/1.1
    #         return method, path, version
    #     except ValueError:
    #         return None, None, None

    def parse_request_line(self, request_lines):
        try:
            method, full_path, version = request_lines.split()

            # Tách path và query
            path, _, query_string = full_path.partition('?')

            return method, path, version, query_string
        except ValueError:
            return None, None, None, ""


    def parse_request_headers(self, header_lines):
        headers = {}
        for line in header_lines:
            if line.strip() == '':
                continue
            if ':' not in line: # để đảm bảo an toàn
                continue
            
            key, value = line.split(': ', 1)

            key = key.lower() # Do HTTP không phân biệt chữ hoa, chữ thường
            headers[key] = value

        return headers


    def parse_cookies(self):
        cookies = {}
        cookie_header = self.headers.get('cookie')
        if not cookie_header:
            return {}
        
        pairs = cookie_header.split(';')

        for pair in pairs:
            if '=' in pair:
                pair = pair.strip()
                key, value = pair.split('=', 1)
                cookies[key] = value

        return cookies
        
    def parse_body(self):
        content_type = self.headers.get('content-type', '')
        body = self.body.strip()

        if 'application/json' in content_type and body:
            import json
            try:
                return json.loads(body)
            except json.JSONDecodeError:
                return {}
        return {}



    # def prepare(self, raw_request, routes = None):
    #     parts = raw_request.split('\r\n\r\n', 1)
    #     header_part = parts[0]
    #     body_part   = parts[1] if len(parts) > 1 else ''
        
    #     lines = header_part.split('\r\n')
    #     request_line = lines[0]
    #     header_line  = lines[1:]

    #     print("=== DEBUG ====")

    #     # Request
    #     self.method, self.path, self.version = self.parse_request_line(request_line)

    #     # Header
    #     self.headers = self.parse_request_headers(header_line)

    #     # Body
    #     self.body = body_part

    #     # Cookies
    #     self.cookies = self.parse_cookies()

    #     # Chuyển body thành dictionary
    #     self.data = self.parse_body()

    #     if routes:
    #         self.routes = routes
    #         self.hook = routes.get((self.method, self.path))
    #         print("XYZ")
    #         print(self.hook)
    #     return self


    def prepare(self, raw_request, routes = None):
        parts = raw_request.split('\r\n\r\n', 1)
        header_part = parts[0]
        body_part   = parts[1] if len(parts) > 1 else ''
        
        lines = header_part.split('\r\n')
        request_line = lines[0]
        header_line  = lines[1:]

        print("=== DEBUG ====")

        # Request
        self.method, self.path, self.version, query_string = self.parse_request_line(request_line)
        query_params = parse_qs(query_string)
        # chuyển {k: [v]} → {k: v}
        self.query = {k: v[0] for k, v in query_params.items()}



        # Header
        self.headers = self.parse_request_headers(header_line)
        self.headers["query"] = self.query

        # Body
        self.body = body_part

        # Cookies
        self.cookies = self.parse_cookies()

        # Chuyển body thành dictionary
        self.data = self.parse_body()

        if routes:
            self.routes = routes
            self.hook = routes.get((self.method, self.path))
            print("XYZ")
            print(self.hook)
        return self



    def prepare_cookies(self, cookies:str):
        self.headers["Cookie"] = cookies

    def prepare_body(self, data, files, json=None):
        pass


    def prepare_content_length(self, body):
        pass

    def prepare_auth(self, auth, url=""):
        pass


#* My Request.py

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

    def parse_request_line(self, request_lines):
        try:
            method, path, version = request_lines.split()    # tách theo dấu cách: GET /index.html HTTP/1.1
            return method, path, version
        except ValueError:
            return None, None, None

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



    def prepare(self, raw_request, routes = None):
        parts = raw_request.split('\r\n\r\n', 1)
        header_part = parts[0]
        body_part   = parts[1] if len(parts) > 1 else ''
        
        lines = header_part.split('\r\n')
        request_line = lines[0]
        header_line  = lines[1:]

        # Request
        self.method, self.path, self.version = self.parse_request_line(request_line)

        # Header
        self.headers = self.parse_request_headers(header_line)

        # Body
        self.body = body_part

        # Cookies
        self.cookies = self.parse_cookies()

        # Chuyển body thành dictionary
        self.data = self.parse_body()

        if routes:
            import pdb; pdb.set_trace() # BREAKPOINT Ở ĐÂY
            self.routes = routes
            self.hook = routes.get((self.method, self.path))

        return self




    def prepare_cookies(self, cookies:str):
        self.headers["Cookie"] = cookies

    def prepare_body(self, data, files, json=None):
        pass


    def prepare_content_length(self, body):
        pass

    def prepare_auth(self, auth, url=""):
        pass


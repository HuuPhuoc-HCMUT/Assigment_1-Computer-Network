import datetime
import os
import mimetypes
from daemon.dictionary import CaseInsensitiveDict

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) + "/../"


class Response:
    """
    Support both:
      - Static HTML/CSS/JS/image
      - API response (JSON or text)
    """

    def __init__(self, request=None):
        self.status_code = 200
        self.reason = "OK"
        self.headers = {}
        self.cookies = CaseInsensitiveDict()
        self.request = request

        # Body for API mode
        self.body = None       # str or bytes

        # Static mode
        self._content = b""
        self._header = b""

    # ----------------------------------------------------------
    def is_api(self):
        """API mode if handler assigned a body"""
        return self.body is not None

    # ----------------------------------------------------------
    def build_api_response(self):
        """Return JSON/text API response."""
        if isinstance(self.body, str):
            body_bytes = self.body.encode("utf-8")
        elif isinstance(self.body, bytes):
            body_bytes = self.body
        else:
            body_bytes = b""

        if "Content-Type" not in self.headers:
            self.headers["Content-Type"] = "text/plain"

        # Build header
        header = (
            f"HTTP/1.1 {self.status_code} {self.reason}\r\n"
            f"Date: {datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')}\r\n"
            f"Server: WeApRous/1.0\r\n"
            f"Content-Length: {len(body_bytes)}\r\n"
            f"Connection: close\r\n"
        )

        # Custom headers
        for k, v in self.headers.items():
            header += f"{k}: {v}\r\n"

        header += "\r\n"
        return header.encode() + body_bytes

    # ----------------------------------------------------------
    # STATIC MODE
    # ----------------------------------------------------------
    def get_mime_type(self, path):
        mime, _ = mimetypes.guess_type(path)
        return mime or "text/html"

    def prepare_content_type(self, mime):
        main, sub = mime.split("/", 1)

        if main == "text":
            self.headers["Content-Type"] = mime
            if sub == "html":
                return BASE_DIR + "www/"
            return BASE_DIR + "static/"

        if main == "image":
            self.headers["Content-Type"] = mime
            return BASE_DIR + "static/"

        raise ValueError("Unsupported MIME:", mime)

    def build_static_file(self, request):
        path = request.path
        mime = self.get_mime_type(path)

        try:
            base_dir = self.prepare_content_type(mime)
        except Exception:
            return self.build_notfound()

        try:
            full = os.path.join(base_dir, path.lstrip("/"))
            with open(full, "rb") as f:
                self._content = f.read()
        except FileNotFoundError:
            return self.build_notfound()

        header = (
            f"HTTP/1.1 {self.status_code} {self.reason}\r\n"
            f"Content-Type: {self.headers['Content-Type']}\r\n"
            f"Content-Length: {len(self._content)}\r\n"
            f"Date: {datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')}\r\n"
            f"Cache-Control: no-cache\r\n"
            f"Server: WeApRous/1.0\r\n"
            f"Connection: close\r\n\r\n"
        ).encode()

        return header + self._content

    def build_notfound(self):
        body = b"404 Not Found"
        header = (
            "HTTP/1.1 404 Not Found\r\n"
            "Content-Type: text/plain\r\n"
            f"Content-Length: {len(body)}\r\n"
            "Connection: close\r\n\r\n"
        ).encode()
        return header + body

    # ----------------------------------------------------------
    # MAIN ENTRY
    # ----------------------------------------------------------
    def build_response(self, request):
        """Choose API or static automatically."""
        if self.is_api():
            return self.build_api_response()
        return self.build_static_file(request)

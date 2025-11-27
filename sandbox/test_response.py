"""
test_response.py
----------------
Simple test script for the Response class implementation.

This test simulates a request object and calls build_response()
to verify if the Response class can generate valid HTTP responses
for different types of requested files.
"""

import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")

import os
from response import Response
from daemon.dictionary import CaseInsensitiveDict

# ───────────────────────────────────────────────
# Dummy request object to simulate parsed HTTP request
class DummyRequest:
    def __init__(self, path, method="GET"):
        self.path = path
        self.method = method
        self.headers = {
            "User-Agent": "FakeBrowser/1.0",
            "Accept": "text/html",
            "Accept-Language": "en-US,en;q=0.9"
        }

# ───────────────────────────────────────────────
def test_case(description, request_path):
    """Run one test case and print the result summary."""
    print("\n" + "=" * 60)
    print(f"TEST: {description}")
    print("-" * 60)

    req = DummyRequest(request_path)
    resp = Response()
    response_bytes = resp.build_response(req)

    # Decode and preview the HTTP response
    try:
        preview = response_bytes.decode("utf-8", errors="ignore")
    except Exception:
        preview = "<binary data>"

    # Print result summary
    header_end = preview.find("\r\n\r\n")
    header = preview[:header_end]
    body_preview = preview[header_end + 4: header_end + 120]  # show first ~100 chars of body

    print("Header:")
    print(header)
    print("\nBody Preview:")
    print(body_preview)
    print(f"\nResponse size: {len(response_bytes)} bytes")

# ───────────────────────────────────────────────
def main():
    print("Running Response class tests...\n")

    # Ensure test folders exist (www/ and static/)
    base_dir = os.path.dirname(os.path.abspath(__file__)) + "/"
    www_dir = os.path.join(base_dir, "../www")
    static_dir = os.path.join(base_dir, "../static")

    # Create sample files for testing
    os.makedirs(www_dir, exist_ok=True)
    os.makedirs(static_dir, exist_ok=True)

    with open(os.path.join(www_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write("<html><body><h1>Hello World!</h1></body></html>")

    with open(os.path.join(static_dir, "style.css"), "w", encoding="utf-8") as f:
        f.write("body { background-color: lightblue; }")

    # Run tests
    test_case("Serve existing HTML file", "/index.html")
    test_case("Serve existing CSS file", "/style.css")
    test_case("Serve missing file", "/no_such_file.html")
    test_case("Unsupported MIME", "/video.mp4")

    print("\nAll tests completed.\n")

# ───────────────────────────────────────────────
if __name__ == "__main__":
    main()

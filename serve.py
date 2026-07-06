"""Local preview server that mimics GitHub Pages' clean-URL handling.

Run:  python serve.py
Then open http://localhost:8000
"""
import http.server
import os

PORT = 8000
ROOT = os.path.dirname(os.path.abspath(__file__))


class CleanURLHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)

    def end_headers(self):
        # Never cache during local preview, so CSS/JS edits show on plain reload
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        super().end_headers()

    def send_head(self):
        path = self.path.split("?")[0].split("#")[0]
        # /team -> /team.html, like GitHub Pages
        if path != "/" and "." not in os.path.basename(path):
            candidate = os.path.join(ROOT, path.strip("/") + ".html")
            if os.path.isfile(candidate):
                self.path = path.rstrip("/") + ".html"
        return super().send_head()


if __name__ == "__main__":
    with http.server.ThreadingHTTPServer(("", PORT), CleanURLHandler) as httpd:
        print(f"Serving at http://localhost:{PORT}")
        httpd.serve_forever()

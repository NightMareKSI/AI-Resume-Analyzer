from http.server import BaseHTTPRequestHandler
import subprocess
import os
import sys

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        port = os.environ.get("PORT", "8501")

        subprocess.Popen([
            sys.executable,
            "-m",
            "streamlit",
            "run",
            "app.py",
            "--server.port",
            port,
            "--server.address",
            "0.0.0.0",
            "--server.headless",
            "true"
        ])

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Streamlit app starting...")
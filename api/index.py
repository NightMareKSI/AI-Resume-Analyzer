import subprocess
import os

def handler(request):
    port = os.environ.get("PORT", "8000")

    subprocess.Popen([
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

    return {
        "statusCode": 200,
        "body": "Streamlit app starting..."
    }
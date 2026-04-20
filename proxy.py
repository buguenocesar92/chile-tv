from flask import Flask, Response
import subprocess
import requests

app = Flask(__name__)

CANALES = {
    "tvn":  "https://www.youtube.com/channel/UCTXNz3gjAypWp3EhlIATEJQ/live",
    "t13":  "https://www.youtube.com/channel/UCsRnhjcUCR78Q3Ud6OXCTNg/live",
    "chv":  "https://www.youtube.com/@Chilevision/live",
    "mega": "https://www.youtube.com/channel/UCkccyEbqhhM3uKOI6Shm-4Q/live",
}

@app.route("/stream/<canal>")
def stream(canal):
    yt_url = CANALES.get(canal)
    if not yt_url:
        return "Canal no encontrado", 404
    result = subprocess.run(
        ["/home/cesar/.local/bin/yt-dlp", "-g", "--no-warnings", yt_url],
        capture_output=True, text=True, timeout=60
    )
    lines = [l for l in result.stdout.strip().splitlines() if l.startswith("http")]
    if not lines:
        return "Stream no disponible", 503
    hls_url = lines[0]
    req = requests.get(hls_url, stream=True)
    return Response(req.iter_content(chunk_size=1024),
                    content_type=req.headers.get("Content-Type", "application/x-mpegURL"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
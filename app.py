from flask import Flask, request, jsonify, render_template
import subprocess
import json

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    url = request.json.get("url")

    cmd = [
        "yt-dlp",
        "-j",
        url
    ]

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        return jsonify({"error": "Không phân tích được link"}), 400

    info = json.loads(result.stdout)

    formats = []
    for f in info.get("formats", []):
        if f.get("url"):
            formats.append({
                "quality": f.get("format_note"),
                "ext": f.get("ext"),
                "url": f.get("url")
            })

    return jsonify({
        "title": info.get("title"),
        "formats": formats
    })

if __name__ == "__main__":
    app.run()

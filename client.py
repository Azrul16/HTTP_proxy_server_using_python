from flask import Flask, render_template, request, jsonify
import requests
import threading

app = Flask(__name__)

PROXY_URL = "http://localhost:8080"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/send_request", methods=["POST"])
def send_request():
    try:
        endpoint = request.json.get("endpoint", "/")
        response = requests.get(f"{PROXY_URL}{endpoint}")
        return jsonify({"status": "success", "response": response.text})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

def run_web_server():
    app.run(port=5000, debug=True, use_reloader=False)

if __name__ == "__main__":
    # Run Flask app in a separate thread
    threading.Thread(target=run_web_server).start()

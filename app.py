
import requests
from flask import Flask, jsonify, make_response

app = Flask(__name__)

API = "https://api.coingecko.com/api/v3/coins/markets"

@app.after_request
def add_cors(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response

@app.route("/")
def home():
    return jsonify({"status": "online"})

@app.route("/api/coingecko/page/<int:page>")
def get_page(page):
    if page < 3 or page > 999:
        return jsonify({"error": "页码超出范围"}), 400

    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 250,
        "page": page,
        "sparkline": "false"
    }

    try:
        r = requests.get(API, params=params, timeout=25)
        r.raise_for_status()
        return jsonify(r.json())
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 502

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

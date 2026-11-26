
import time
import requests
from flask import Flask, jsonify

app = Flask(__name__)

COINGECKO_URL = "https://api.coingecko.com/api/v3/coins/markets"


@app.route("/")
def home():
    return jsonify({
        "status": "online",
        "message": "CoinGecko API is running",
        "endpoint": "/api/coingecko/after700"
    })


@app.route("/api/coingecko/after700", methods=["GET"])
def get_coins():
    all_coins = []
    session = requests.Session()

    try:
        for page in range(3, 1000):
            params = {
                "vs_currency": "usd",
                "order": "market_cap_desc",
                "per_page": 250,
                "page": page,
                "sparkline": "false"
            }

            response = None

            # 失败最多重试3次
            for retry in range(3):
                try:
                    response = session.get(
                        COINGECKO_URL,
                        params=params,
                        timeout=30
                    )
                    response.raise_for_status()
                    break
                except requests.RequestException:
                    if retry == 2:
                        raise
                    time.sleep(2 * (retry + 1))

            data = response.json()

            if not data:
                break

            for coin in data:
                rank = coin.get("market_cap_rank")
                if rank is not None and rank > 700:
                    all_coins.append(coin)

            print(f"第{page}页，累计获取 {len(all_coins)} 个")

            time.sleep(1)

        return jsonify(all_coins)

    except Exception as e:
        return jsonify({
            "error": str(e),
            "message": "CoinGecko 数据获取失败，请稍后重试"
        }), 502

    finally:
        session.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)


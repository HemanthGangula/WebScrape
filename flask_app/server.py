from flask import Flask, jsonify
import json
import os

app = Flask(__name__)

DATA_FILE = os.path.join(os.path.dirname(__file__), '..', 'scraper', 'scraped_data.json')


@app.route('/')
def get_scraped_data():
    if not os.path.exists(DATA_FILE):
        return jsonify({"error": "scraped_data.json not found"}), 404

    with open(DATA_FILE, 'r') as f:
        data = json.load(f)
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

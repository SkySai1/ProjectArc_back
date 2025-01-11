from flask import jsonify
from app import app
import os
import json

BASE_DIR = "project_data"
HISTORY_FILE = os.path.join(BASE_DIR, "history_log.json")

@app.route('/history', methods=['GET'])
def get_history():
    """Получить историю изменений."""
    if not os.path.exists(HISTORY_FILE):
        return jsonify({"error": "No history found."}), 404

    with open(HISTORY_FILE, "r") as f:
        history_data = json.load(f)

    return jsonify(history_data), 200
from flask import jsonify, current_app
from app.utils import require_api_key
import os
import json

@require_api_key
def get_history():
    """
    Получение истории изменений.
    """
    BASE_DIR = current_app.config["BASE_DIR"]
    HISTORY_FILE = os.path.join(BASE_DIR, "history_log.json")

    if not os.path.exists(HISTORY_FILE):
        return jsonify({"error": "History log file does not exist."}), 404

    with open(HISTORY_FILE, "r") as f:
        try:
            history = json.load(f)
        except json.JSONDecodeError:
            history = []

    return jsonify(history), 200

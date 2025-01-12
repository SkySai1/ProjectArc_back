from flask import jsonify, current_app
import os
import json

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

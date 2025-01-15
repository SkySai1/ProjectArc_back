from flask import request, jsonify, current_app
from app.utils import require_api_key
import os
import json
import time

@require_api_key
def log_change():
    """
    Записать изменение в лог истории.
    """
    BASE_DIR = current_app.config["BASE_DIR"]
    HISTORY_FILE = os.path.join(BASE_DIR, "history_log.json")

    data = request.json
    description = data.get("description")
    affected_files = data.get("affected_files", [])

    if not description:
        return jsonify({"error": "Description is required."}), 400

    log_entry = {
        "timestamp": int(time.time()),
        "description": description,
        "affected_files": affected_files
    }

    if not os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "w") as f:
            json.dump([log_entry], f, indent=4)
    else:
        with open(HISTORY_FILE, "r+") as f:
            logs = json.load(f)
            logs.append(log_entry)
            f.seek(0)
            json.dump(logs, f, indent=4)

    return jsonify({"message": "Change logged successfully."}), 201
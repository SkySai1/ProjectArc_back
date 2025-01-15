from flask import request, jsonify, current_app
from app.utils import require_api_key
import os
import json
import time

@require_api_key
def create_about():
    """
    Создание описания проекта.
    """
    BASE_DIR = current_app.config["BASE_DIR"]
    ABOUT_FILE = os.path.join(BASE_DIR, "project_description.json")

    data = request.json
    description = data.get("description")

    if not description:
        return jsonify({"error": "'description' is required."}), 400

    os.makedirs(BASE_DIR, exist_ok=True)

    if os.path.exists(ABOUT_FILE):
        return jsonify({"error": "Project description already exists."}), 400

    project_description = {
        "description": description,
        "created_at": int(time.time()),
        "updated_at": int(time.time())
    }

    with open(ABOUT_FILE, "w") as f:
        json.dump(project_description, f, indent=4)

    return jsonify({"message": "Project description created successfully."}), 201
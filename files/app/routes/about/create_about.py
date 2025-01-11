from flask import request, jsonify
from app import app
import os
import json
import time
from app.utils import log_change

BASE_DIR = "project_data"
ABOUT_FILE = os.path.join(BASE_DIR, "project_description.json")

@app.route('/about', methods=['POST'])
def create_about():
    """
    Создание описания проекта.
    """
    data = request.json
    description = data.get("description")

    if not description:
        return jsonify({"error": "'description' is required."}), 400

    os.makedirs(BASE_DIR, exist_ok=True)  # Создание директории, если её нет

    if os.path.exists(ABOUT_FILE):
        return jsonify({"error": "Project description already exists."}), 400

    project_description = {
        "description": description,
        "created_at": int(time.time()),
        "updated_at": int(time.time())
    }

    with open(ABOUT_FILE, "w") as f:
        json.dump(project_description, f, indent=4)

    # Логируем изменение
    log_change("Project description created", affected_files=["project_description.json"])

    return jsonify({"message": "Project description created successfully."}), 201
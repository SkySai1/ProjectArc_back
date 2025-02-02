from flask import request, jsonify, current_app
from app.utils import require_api_key
import os
import json
import time

@require_api_key
def update_about():
    """
    Обновление описания проекта.
    """
    BASE_DIR = current_app.config["BASE_DIR"]
    ABOUT_FILE = os.path.join(BASE_DIR, "project_description.json")

    data = request.json
    new_description = data.get("description")

    if not new_description:
        return jsonify({"error": "'description' is required."}), 400

    if not os.path.exists(ABOUT_FILE):
        return jsonify({"error": "Project description does not exist."}), 404

    with open(ABOUT_FILE, "r") as f:
        project_description = json.load(f)

    project_description["description"] = new_description
    project_description["updated_at"] = int(time.time())

    with open(ABOUT_FILE, "w") as f:
        json.dump(project_description, f, indent=4)

    return jsonify({"message": "Project description updated successfully."}), 200
from flask import request, jsonify
from app import app
import os
import json
import time

BASE_DIR = "project_data"
ABOUT_FILE = os.path.join(BASE_DIR, "project_description.json")

@app.route('/about', methods=['PUT'])
def update_about():
    """Обновление описания проекта."""
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
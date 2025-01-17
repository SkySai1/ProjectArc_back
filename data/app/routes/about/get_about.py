from flask import jsonify, current_app
from app.utils import require_api_key
import os
import json

@require_api_key
def get_about():
    """
    Получение описания проекта.
    """
    BASE_DIR = current_app.config["BASE_DIR"]
    ABOUT_FILE = os.path.join(BASE_DIR, "project_description.json")

    if not os.path.exists(ABOUT_FILE):
        return jsonify({"error": "Project description does not exist."}), 404

    with open(ABOUT_FILE, "r") as f:
        project_description = json.load(f)

    return jsonify(project_description), 200
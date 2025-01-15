from flask import request, jsonify, current_app
import os
from app.utils import update_project_file, require_api_key

@require_api_key
def update_map():
    """
    Обновление описания файла в проекте.
    """
    BASE_DIR = current_app.config["BASE_DIR"]

    data = request.json
    path = data.get("path")
    description = data.get("description")

    if not path or not description:
        return jsonify({"error": "'path' and 'description' are required."}), 400

    file_path = os.path.join(BASE_DIR, path)

    if not os.path.exists(file_path):
        return jsonify({"error": f"File '{path}' does not exist."}), 404

    # Обновляем запись в базе данных
    file_size = os.path.getsize(file_path)
    last_modified = os.path.getmtime(file_path)
    if update_project_file(path, description, file_size, last_modified):
        return jsonify({"message": f"File '{path}' information updated successfully."}), 200

    return jsonify({"error": f"Failed to update file '{path}' in project database."}), 500
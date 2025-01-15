from flask import request, jsonify, current_app
from app.utils import delete_project_file, require_api_key
import os

@require_api_key
def delete_file():
    """
    Удаление файла из проекта.
    """
    BASE_DIR = current_app.config["BASE_DIR"]

    data = request.json
    path = data.get("path")

    if not path:
        return jsonify({"error": "'path' is required."}), 400

    file_path = os.path.join(BASE_DIR, path)

    if not os.path.exists(file_path):
        return jsonify({"error": f"File '{path}' does not exist."}), 404

    os.remove(file_path)

    # Удаляем запись из карты проекта
    if delete_project_file(path):
        return jsonify({"message": f"File '{path}' deleted from project database."}), 200

    return jsonify({"error": f"File '{path}' not found in project database."}), 404
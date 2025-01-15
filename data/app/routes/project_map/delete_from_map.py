from flask import request, jsonify, current_app
from app.utils import delete_project_file, require_api_key
import os

@require_api_key
def delete_from_map():
    """
    Удаление файла из проекта.
    """
    data = request.json
    path = data.get("path")

    if not path:
        return jsonify({"error": "'path' is required."}), 400

    # Удаляем запись из базы данных
    if delete_project_file(path):
        return jsonify({"message": f"File '{path}' deleted from project database."}), 200

    return jsonify({"error": f"File '{path}' not found in project database."}), 404
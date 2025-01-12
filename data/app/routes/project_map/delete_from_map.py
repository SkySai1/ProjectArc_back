from flask import request, jsonify, current_app
import os
from app.utils import delete_project_file

def delete_from_map():
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

    # Удаляем файл
    os.remove(file_path)

    # Удаляем запись из базы данных
    if delete_project_file(path):
        return jsonify({"message": f"File '{path}' deleted from project database."}), 200

    return jsonify({"error": f"File '{path}' not found in project database."}), 404
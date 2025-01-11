from flask import request, jsonify
from app import app
import os
from app.utils import log_change

BASE_DIR = "project_data"

@app.route('/project_map', methods=['POST'])
def delete_file():
    """
    Удаление файла из проекта.
    """
    data = request.json
    path = data.get("path")

    if not path:
        return jsonify({"error": "'path' is required."}), 400

    file_path = os.path.join(BASE_DIR, path)

    if not os.path.exists(file_path):
        return jsonify({"error": f"File '{path}' does not exist."}), 404

    os.remove(file_path)

    # Логируем удаление файла
    log_change(f"File {path} deleted", affected_files=[path])

    return jsonify({"message": f"File '{path}' deleted from project database."}), 200
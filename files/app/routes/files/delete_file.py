from flask import request, jsonify
from app import app
import os
from app.utils import log_change

@app.route('/project_map', methods=['POST'])
def delete_file():
    """
    Удаление файла из проекта.
    """
    BASE_DIR = app.config["BASE_DIR"]

    data = request.json
    path = data.get("path")

    if not path:
        return jsonify({"error": "'path' is required."}), 400

    file_path = os.path.join(BASE_DIR, path)

    if not os.path.exists(file_path):
        return jsonify({"error": f"File '{path}' does not exist."}), 404

    os.remove(file_path)

    return jsonify({"message": f"File '{path}' deleted from project database."}), 200
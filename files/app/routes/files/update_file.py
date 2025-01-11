from flask import request, jsonify
from app import app
import os

@app.route('/project_map', methods=['PUT'])
def update_file():
    """
    Обновление описания файла в проекте.
    """
    BASE_DIR = app.config["BASE_DIR"]

    data = request.json
    path = data.get("path")
    description = data.get("description")

    if not path or not description:
        return jsonify({"error": "'path' and 'description' are required."}), 400

    file_path = os.path.join(BASE_DIR, path)

    if not os.path.exists(file_path):
        return jsonify({"error": f"File '{path}' does not exist."}), 404

    return jsonify({"message": f"File {path} information updated successfully."}), 200
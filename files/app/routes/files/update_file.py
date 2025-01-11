from flask import request, jsonify
from app import app
import os
from app.utils import log_change

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

    # Логируем обновление файла
    log_change(f"File {path} updated", affected_files=[path])

    return jsonify({"message": f"File {path} information updated successfully."}), 200
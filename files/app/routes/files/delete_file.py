from flask import request, jsonify
from app import app
import os
from app.utils import delete_project_file

@app.route('/delete', methods=['GET'])
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

    # Удаляем файл из файловой системы
    os.remove(file_path)

    # Удаляем запись из карты проекта
    if delete_project_file(path):
        return jsonify({"message": f"File '{path}' deleted from project database."}), 200

    return jsonify({"error": f"File '{path}' not found in project database."}), 404

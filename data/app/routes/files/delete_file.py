from flask import request, jsonify, current_app
from app.utils import delete_project_file, require_api_key, delete_files_from_project
import os
import shutil

@require_api_key
def delete_file():
    """
    Удаление файла или директории из проекта.
    """
    BASE_DIR = current_app.config["BASE_DIR"]

    data = request.json
    path = data.get("path")

    if not path:
        return jsonify({"error": "'path' is required."}), 400

    full_path = os.path.join(BASE_DIR, path)

    if not os.path.exists(full_path):
        return jsonify({"error": f"Path '{path}' does not exist."}), 404

    try:
        if os.path.isfile(full_path):
            os.remove(full_path)  # Удаляем файл
            if delete_project_file(path):
                return jsonify({"message": f"File '{path}' deleted successfully."}), 200
            else:
                return jsonify({
                    "message": f"File '{path}' deleted, but not found in database.",
                    "status": "not_in_db"
                }), 207

        elif os.path.isdir(full_path):
            if not os.listdir(full_path):  # Если директория пустая
                os.rmdir(full_path)  # Удаляем пустую директорию
            else:
                shutil.rmtree(full_path)  # Удаляем рекурсивно
            deleted_count = delete_files_from_project(path)
            if deleted_count > 0:
                return jsonify({
                    "message": f"Directory '{path}' and {deleted_count} associated records deleted successfully."
                }), 200
            else:
                return jsonify({
                    "message": f"Directory '{path}' deleted, but no records found in database.",
                    "status": "not_in_db"
                }), 207

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
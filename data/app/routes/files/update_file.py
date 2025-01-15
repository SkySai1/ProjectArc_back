from flask import request, jsonify, current_app
from app.utils import update_project_file, require_api_key
import os

@require_api_key
def update_file():
    """
    Обновление информации и/или содержимого файла в проекте.
    """
    BASE_DIR = current_app.config["BASE_DIR"]

    data = request.json
    path = data.get("path")
    description = data.get("description")
    content = data.get("content")  # Новое содержимое файла

    if not path:
        return jsonify({"error": "'path' required."}), 400

    file_path = os.path.join(BASE_DIR, path)

    if not os.path.exists(file_path):
        return jsonify({"error": f"File '{path}' does not exist."}), 404

    try:
        # Если передано новое содержимое, обновляем файл
        if content is not None:
            with open(file_path, "w") as f:
                f.write(content)

        # Получаем обновлённые метаданные
        file_size = os.path.getsize(file_path)
        last_modified = os.path.getmtime(file_path)

        # Обновляем карту проекта
        if update_project_file(path, description, file_size, last_modified):
            return jsonify({"message": f"File '{path}' updated successfully."}), 200

        return jsonify({"error": f"Failed to update file '{path}' in project database."}), 500

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
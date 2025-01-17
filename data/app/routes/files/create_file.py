from flask import request, jsonify, current_app
from app.utils import require_api_key, add_project_file
import os

@require_api_key
def create_file():
    """
    Создание нового файла в проекте.
    """
    BASE_DIR = current_app.config["BASE_DIR"]

    data = request.json
    path = data.get("path")
    content = data.get("content", "")
    description = data.get("description", "")

    if not path:
        return jsonify({"error": "path is required."}), 400

    file_path = os.path.join(BASE_DIR, path)

    if os.path.exists(file_path):
        return jsonify({"error": f"File '{path}' already exists."}), 400

    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, "w") as f:
        f.write(content)

    file_size = os.path.getsize(file_path)
    last_modified = os.path.getmtime(file_path)

    # Добавляем запись в карту проекта
    add_project_file(
        path=path,
        type="file",
        description=description or "No description provided",
        size=file_size,
        last_modified=last_modified
    )

    return jsonify({"message": f"File '{path}' created successfully."}), 201
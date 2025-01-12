from flask import request, jsonify, current_app
import os
from app.utils import add_project_file

def create_file():
    """
    Создание нового файла в проекте.
    """
    BASE_DIR = current_app.config["BASE_DIR"]

    data = request.json
    filename = data.get("filename")
    content = data.get("content", "")
    description = data.get("description", "")

    if not filename:
        return jsonify({"error": "Filename is required."}), 400

    file_path = os.path.join(BASE_DIR, filename)

    if os.path.exists(file_path):
        return jsonify({"error": f"File '{filename}' already exists."}), 400

    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, "w") as f:
        f.write(content)

    file_size = os.path.getsize(file_path)
    last_modified = os.path.getmtime(file_path)

    # Добавляем запись в карту проекта
    add_project_file(
        path=filename,
        type="file",
        description=description or "No description provided",
        size=file_size,
        last_modified=last_modified
    )

    return jsonify({"message": f"File '{filename}' created successfully."}), 201
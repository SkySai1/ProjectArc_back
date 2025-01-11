from flask import request, jsonify
from app import app
import os
from app.utils import log_change

@app.route('/create', methods=['POST'])
def create_file():
    """
    Создание нового файла в проекте.
    """
    BASE_DIR = app.config["BASE_DIR"]

    data = request.json
    filename = data.get("filename")
    content = data.get("content")
    description = data.get("description")

    if not filename or not content:
        return jsonify({"error": "'filename' and 'content' are required."}), 400

    file_path = os.path.join(BASE_DIR, filename)

    if os.path.exists(file_path):
        return jsonify({"error": f"File '{filename}' already exists."}), 400

    os.makedirs(BASE_DIR, exist_ok=True)

    with open(file_path, "w") as f:
        f.write(content)

    return jsonify({"message": f"File {filename} created successfully."}), 201
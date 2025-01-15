from flask import request, jsonify, current_app
from app.utils import require_api_key
import os

@require_api_key
def read_file():
    """
    Чтение содержимого файла в проекте.
    """
    BASE_DIR = current_app.config["BASE_DIR"]

    filename = request.args.get("filename")

    if not filename:
        return jsonify({"error": "Filename is required."}), 400

    file_path = os.path.join(BASE_DIR, filename)

    if not os.path.exists(file_path):
        return jsonify({"error": f"File '{filename}' does not exist."}), 404

    try:
        with open(file_path, "r") as f:
            content = f.read()
    except Exception as e:
        return jsonify({"error": f"Failed to read file: {str(e)}"}), 500

    return jsonify({
        "filename": filename,
        "content": content,
        "size": os.path.getsize(file_path),
        "last_modified": os.path.getmtime(file_path)
    }), 200
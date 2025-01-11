from flask import request, jsonify
from app import app
from app.utils import delete_project_file

@app.route('/project_map', methods=['POST'])
def delete_from_map():
    """Удалить информацию о файле или папке из карты проекта."""
    data = request.json
    target_path = data.get("path")

    if not target_path or not isinstance(target_path, str):
        return jsonify({"error": "Path must be a valid string."}), 400

    try:
        if delete_project_file(target_path):
            return jsonify({"message": f"File '{target_path}' deleted from project database."}), 200
        else:
            return jsonify({"error": f"File '{target_path}' not found in project database."}), 404
    except Exception as e:
        return jsonify({"error": f"Failed to delete path from project map: {str(e)}"}), 500
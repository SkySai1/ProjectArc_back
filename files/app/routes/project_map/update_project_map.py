from flask import request, jsonify
from app import app
from app.utils import update_project_file
import os

@app.route('/project_map', methods=['PUT'])
def update_project_map():
    """
    Обновление информации о файле в базе данных.
    """
    try:
        BASE_DIR = app.config["BASE_DIR"]
        PROJECT_FOLDER = os.path.join(BASE_DIR, "files")

        data = request.json
        filename = data.get("path")
        new_description = data.get("description", None)

        if not filename:
            return jsonify({"error": "Filename is required."}), 400

        filepath = os.path.join(PROJECT_FOLDER, filename)

        if not os.path.isfile(filepath):
            return jsonify({"error": f"File {filename} does not exist."}), 404

        file_size = os.path.getsize(filepath)
        last_modified = os.path.getmtime(filepath)

        update_project_file(
            path=filename,
            description=new_description,
            size=file_size,
            last_modified=last_modified
        )

        return jsonify({"message": f"File {filename} information updated successfully."}), 200

    except Exception as e:
        return jsonify({"error": f"Failed to update project map: {str(e)}"}), 500
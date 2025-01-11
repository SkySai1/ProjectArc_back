from flask import jsonify
from app import app
from app.models import ProjectFile
from datetime import datetime

@app.route('/project_map', methods=['GET'])
def get_project_map():
    """
    Получить карту проекта из базы данных.
    """
    try:
        project_files = ProjectFile.query.all()

        project_map = [
            {
                "path": file.path,
                "description": file.description,
                "size": file.size,
                "last_modified": datetime.fromtimestamp(file.last_modified).isoformat() if file.last_modified else None
            }
            for file in project_files
        ]

        return jsonify(project_map), 200
    except Exception as e:
        return jsonify({"error": f"Failed to retrieve project map: {str(e)}"}), 500
from flask import jsonify
from app.utils import get_list_project_files, require_api_key
from datetime import datetime

@require_api_key
def get_project_map():
    """
    Получить карту проекта из базы данных.
    """
    try:
        project_map = get_list_project_files()
        return jsonify(project_map), 200
    except Exception as e:
        return jsonify({"error": f"Failed to retrieve project map: {str(e)}"}), 500
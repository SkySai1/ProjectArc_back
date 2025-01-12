from flask import Blueprint, request, jsonify, current_app
from werkzeug.exceptions import BadRequest
import os
from app.utils import add_project_file
from datetime import datetime

# Blueprint
project_map_bp = Blueprint('project_map', __name__)

@project_map_bp.route('/sync', methods=['POST'])
def sync_project_files():
    """
    Синхронизация файлов из массива JSON с картой проекта.
    Проверяет существование файлов и добавляет их в СУБД.
    """
    try:
        # Получение данных из запроса
        files_data = request.json
        if not isinstance(files_data, list):
            raise BadRequest("Expected a JSON array of file data.")

        results = {
            "synchronized": [],
            "not_found": []
        }

        for file_info in files_data:
            if not isinstance(file_info, dict) or 'path' not in file_info or 'description' not in file_info:
                raise BadRequest("Each file must have 'path' and 'description'.")

            file_path = os.path.join(current_app.config['BASE_DIR'], file_info['path'])
            if os.path.exists(file_path):
                # Получение информации о файле
                file_size = os.path.getsize(file_path)
                last_modified = datetime.utcfromtimestamp(os.path.getmtime(file_path))

                # Использование утилиты для добавления в СУБД
                add_project_file(
                    path=file_info['path'],
                    type="file",
                    description=file_info['description'],
                    size=file_size,
                    last_modified=last_modified
                )

                results["synchronized"].append(file_info['path'])
            else:
                results["not_found"].append(file_info['path'])

        # Определение кода ответа
        if len(results["synchronized"]) == 0:
            return jsonify({"error": "No files were synchronized.", "details": results}), 404
        elif len(results["not_found"]) > 0:
            return jsonify({"message": "Some files were not found.", "details": results}), 207
        else:
            return jsonify({"message": "All files synchronized successfully.", "details": results}), 200

    except BadRequest as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        current_app.logger.error(f"Error during synchronization: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
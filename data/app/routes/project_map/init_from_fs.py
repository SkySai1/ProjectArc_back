from flask import request, jsonify, current_app
from werkzeug.exceptions import BadRequest
import os
from app.utils import add_project_file, require_api_key, get_project_file
from datetime import datetime

@require_api_key
def sync_project_files():
    """
    Синхронизация файлов из массива JSON с картой проекта.
    Проверяет существование файлов и добавляет их в СУБД.
    """
    try:
        # Получение данных из запроса
        request_data = request.json
        if not isinstance(request_data, dict) or 'files' not in request_data:
            raise BadRequest("Expected a JSON object with a 'files' key containing an array of file data.")
        
        files_data = request_data['files']  # Извлекаем массив файлов из ключа 'files'
        
        if not isinstance(files_data, list):
            raise BadRequest("The 'files' key must contain a JSON array of file data.")

        results = {
            "synchronized": [],
            "not_found": [],
            "already_in_db": []
        }

        for file_info in files_data:
            if not isinstance(file_info, dict) or 'path' not in file_info or 'description' not in file_info:
                raise BadRequest("Each file must have 'path' and 'description'.")

            file_path = os.path.join(current_app.config['BASE_DIR'], file_info['path'])
            if os.path.exists(file_path):
                # Проверяем, есть ли файл в базе данных
                existing_file = get_project_file(file_info['path'])
                if existing_file:
                    results["already_in_db"].append(file_info['path'])
                    continue

                # Получение информации о файле
                file_size = os.path.getsize(file_path)
                last_modified = datetime.utcfromtimestamp(os.path.getmtime(file_path))

                # Добавление записи в СУБД
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
        if len(results["synchronized"]) == 0 and len(results["already_in_db"]) == 0:
            return jsonify({"error": "No files were synchronized.", "details": results}), 404
        elif len(results["not_found"]) > 0:
            return jsonify({"message": "Some files were not found.", "details": results}), 207
        else:
            return jsonify({"message": "Synchronization completed.", "details": results}), 200

    except BadRequest as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        current_app.logger.error(f"Error during synchronization: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
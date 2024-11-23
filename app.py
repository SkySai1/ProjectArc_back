from flask import Flask, request, jsonify
import time
import os
import json
import shutil
from functools import wraps

app = Flask(__name__)

# Параметры приложения
BASE_DIR = os.getenv("PROJECT_DIR", "project_data")  # Директория проекта, можно задать через переменную окружения
PROJECT_FOLDER = os.path.join(BASE_DIR, "files")    # Папка для файлов
PROJECT_MAP = os.path.join(BASE_DIR, "project_map.json")  # Карта проекта
API_KEY = os.getenv("API_KEY", "default_secret_api_key")  # API-ключ из переменной окружения

# Создать директории для хранения данных
os.makedirs(PROJECT_FOLDER, exist_ok=True)

# Проверить наличие карты проекта и создать, если её нет
if not os.path.exists(PROJECT_MAP):
    with open(PROJECT_MAP, "w") as f:
        json.dump({}, f)

def require_api_key(f):
    """Декоратор для проверки API-ключа."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get("Authorization")
        if api_key != API_KEY:
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return decorated_function

def update_project_map():
    """Обновление карты проекта с описаниями файлов."""
    project_map = {}
    for root, _, files in os.walk(PROJECT_FOLDER):
        rel_path = os.path.relpath(root, PROJECT_FOLDER)
        project_map[rel_path] = {}
        for file in files:
            file_path = os.path.join(root, file)
            project_map[rel_path][file] = {
                "description": f"Description for {file}",  # Здесь вы можете динамически добавлять описание
                "size": os.path.getsize(file_path),
                "last_modified": os.path.getmtime(file_path)
            }
    with open(PROJECT_MAP, "w") as f:
        json.dump(project_map, f, indent=4)

@app.route('/create', methods=['POST'])
@require_api_key
def create_file():
    """Создание нового файла (включая создание папок)."""
    data = request.json
    filename = data.get("filename")
    content = data.get("content", "")
    description = data.get("description", f"Description for {filename}")

    if not filename:
        return jsonify({"error": "Filename is required."}), 400

    # Полный путь к файлу
    filepath = os.path.join(PROJECT_FOLDER, filename)
    
    # Проверка существования файла
    if os.path.exists(filepath):
        return jsonify({"error": "File already exists."}), 400

    # Создание всех недостающих папок
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    # Создание нового файла
    with open(filepath, 'w') as f:
        f.write(content)

    # Обновление только для нового файла в карте проекта
    if os.path.exists(PROJECT_MAP):
        with open(PROJECT_MAP, "r") as f:
            project_map = json.load(f)
    else:
        project_map = {}

    # Добавление новой информации в карту проекта
    dir_path = os.path.dirname(filename)
    base_filename = os.path.basename(filename)
    relative_dir_path = os.path.relpath(os.path.dirname(filepath), PROJECT_FOLDER)

    if relative_dir_path not in project_map:
        project_map[relative_dir_path] = {}

    project_map[relative_dir_path][base_filename] = {
        "description": description,
        "size": os.path.getsize(filepath),
        "last_modified": os.path.getmtime(filepath)
    }

    # Сохранение обновленной карты проекта
    with open(PROJECT_MAP, "w") as f:
        json.dump(project_map, f, indent=4)

    return jsonify({"message": f"File {filename} created successfully."}), 201

@app.route('/delete', methods=['GET'])
@require_api_key
def delete():
    """Удаление файла или папки."""
    path = request.args.get("path")

    if not path:
        return jsonify({"error": "Path is required."}), 400

    # Полный путь к файлу или папке
    target_path = os.path.join(PROJECT_FOLDER, path)
    file_exists = os.path.exists(target_path)

    # Удаление файла или папки, если существует
    if file_exists:
        if os.path.isfile(target_path):
            os.remove(target_path)
            message = f"File {path} deleted successfully."
        elif os.path.isdir(target_path):
            shutil.rmtree(target_path)
            message = f"Folder {path} deleted successfully."
        else:
            return jsonify({"error": "Unknown target type."}), 400
    else:
        return jsonify({"error": "File or folder does not exist."}), 404

    # Удаление из карты проекта
    if os.path.exists(PROJECT_MAP):
        with open(PROJECT_MAP, "r") as f:
            project_map = json.load(f)
    else:
        project_map = {}

    # Удаление элемента из карты проекта
    def delete_from_map(map_data, folder_path, file_name):
        """Удаляет файл из карты проекта, учитывая вложенные папки."""
        if folder_path in map_data and isinstance(map_data[folder_path], dict):
            if file_name in map_data[folder_path]:
                del map_data[folder_path][file_name]
                # Удаляем папку, если она становится пустой
                if not map_data[folder_path]:
                    del map_data[folder_path]
                return True
        return False

    # Разделение пути на папку и файл
    folder_path, file_name = os.path.split(path)
    found_in_map = delete_from_map(project_map, folder_path, file_name)

    # Сохраняем обновленную карту проекта, если были изменения
    if found_in_map:
        with open(PROJECT_MAP, "w") as f:
            json.dump(project_map, f, indent=4)

    # Возвращаем соответствующий статус
    if file_exists and not found_in_map:
        return jsonify({
            "message": f"File {path} was found and deleted, but was not listed in the project map."
        }), 207
    elif file_exists and found_in_map:
        return jsonify({
            "message": f"File {path} was deleted successfully from both the file system and the project map."
        }), 200



@app.route('/update', methods=['PUT'])
@require_api_key
def update_file():
    """Обновление содержимого и описания существующего файла."""
    data = request.json
    filename = data.get("filename")
    new_content = data.get("content", None)
    new_description = data.get("description", None)

    if not filename:
        return jsonify({"error": "Filename is required."}), 400

    # Полный путь к файлу
    filepath = os.path.join(PROJECT_FOLDER, filename)

    # Проверка существования файла
    if not os.path.isfile(filepath):
        return jsonify({"error": f"File {filename} does not exist."}), 404

    # Обновление содержимого файла (если передано)
    if new_content is not None:
        with open(filepath, 'w') as f:
            f.write(new_content)

    # Загрузка текущей карты проекта
    if os.path.exists(PROJECT_MAP):
        with open(PROJECT_MAP, "r") as f:
            project_map = json.load(f)
    else:
        project_map = {}

    # Найти путь файла в карте
    dir_path = os.path.dirname(filename)
    base_filename = os.path.basename(filename)

    # Проверяем, существует ли директория в карте
    if dir_path not in project_map:
        return jsonify({"error": f"Directory {dir_path} not found in project map."}), 404

    # Проверяем, существует ли файл в карте проекта
    if base_filename not in project_map[dir_path]:
        return jsonify({"error": f"File {base_filename} not found in project map."}), 404

    # Обновляем описание файла, если передано
    if new_description is not None:
        project_map[dir_path][base_filename]["description"] = new_description

    # Обновляем данные о файле
    project_map[dir_path][base_filename]["size"] = os.path.getsize(filepath)
    project_map[dir_path][base_filename]["last_modified"] = os.path.getmtime(filepath)

    # Сохраняем изменения в карте проекта
    with open(PROJECT_MAP, "w") as f:
        json.dump(project_map, f, indent=4)

    return jsonify({"message": f"File {filename} updated successfully."}), 200

@app.route('/get_file', methods=['GET'])
@require_api_key
def get_file():
    """Получение содержимого файла."""
    filename = request.args.get("filename")

    if not filename:
        return jsonify({"error": "Filename is required."}), 400

    # Полный путь к файлу
    filepath = os.path.join(PROJECT_FOLDER, filename)

    # Проверка существования файла
    if not os.path.isfile(filepath):
        return jsonify({"error": f"File {filename} does not exist."}), 404

    # Чтение содержимого файла
    try:
        with open(filepath, 'r') as f:
            content = f.read()
    except Exception as e:
        return jsonify({"error": f"Error reading file: {str(e)}"}), 500

    return jsonify({"filename": filename, "content": content}), 200


@app.route('/project_map', methods=['GET', 'POST', 'PUT'])
@require_api_key
def project_map():
    if request.method == 'GET':
        """Получить карту проекта."""
        if not os.path.exists(PROJECT_MAP):
            return jsonify({"error": "Project map does not exist."}), 404

        with open(PROJECT_MAP, "r") as f:
            project_map = json.load(f)

        return jsonify(project_map), 200

    elif request.method == 'POST':
        """Удалить информацию о файле или папке из карты проекта."""
        data = request.json
        target_path = data.get("path")

        if not target_path or not isinstance(target_path, str):
            return jsonify({"error": "Path must be a valid string."}), 400

        try:
            # Загружаем текущую карту проекта
            if os.path.exists(PROJECT_MAP):
                with open(PROJECT_MAP, "r") as f:
                    project_map = json.load(f)
            else:
                return jsonify({"error": "Project map does not exist."}), 404

            # Рекурсивное удаление элемента или поддерева из карты проекта
            def delete_path(map_data, full_path):
                """
                Удаляет путь из карты проекта, включая файлы и промежуточные узлы.
                """
                keys = list(map_data.keys())
                for key in keys:
                    # Если ключ совпадает с искомым путём
                    if key == full_path:
                        del map_data[key]
                        return True
                    # Если текущий ключ является поддиректорией
                    if key in full_path:
                        # Рекурсивный поиск в поддиректориях
                        sub_path = full_path[len(key) + 1:]  # Убираем текущий ключ из пути
                        if isinstance(map_data[key], dict) and delete_path(map_data[key], sub_path):
                            # Если поддиректория пустая, удаляем её
                            if not map_data[key]:
                                del map_data[key]
                            return True
                return False

            # Пытаемся удалить путь
            if delete_path(project_map, target_path):
                # Сохраняем обновлённую карту
                with open(PROJECT_MAP, "w") as f:
                    json.dump(project_map, f, indent=4)
                return jsonify({"message": f"Path '{target_path}' deleted from project map."}), 200
            else:
                return jsonify({"error": f"Path '{target_path}' not found in project map."}), 404

        except Exception as e:
            return jsonify({"error": f"Failed to delete path from project map: {str(e)}"}), 500

    elif request.method == 'PUT':
        """Дополнить карту проекта данными о конкретном файле."""
        data = request.json

        # Проверка наличия обязательных ключей
        required_keys = {"path", "description", "size", "last_modified"}
        if not data or not isinstance(data, dict):
            return jsonify({"error": "Invalid data format. A JSON object is required."}), 400
        if not required_keys.issubset(data.keys()):
            return jsonify({"error": f"Missing required keys. Required keys are: {list(required_keys)}"}), 400

        path = data["path"]
        description = data["description"]
        size = data["size"]
        last_modified = data["last_modified"]

        # Проверка типов данных
        if not isinstance(path, str) or not path:
            return jsonify({"error": "Path must be a non-empty string."}), 400
        if not isinstance(description, str) or not description:
            return jsonify({"error": "Description must be a non-empty string."}), 400
        if not isinstance(size, int) or size < 0:
            return jsonify({"error": "Size must be a non-negative integer."}), 400
        if not isinstance(last_modified, (int, float)) or last_modified <= 0:
            return jsonify({"error": "Last_modified must be a positive number."}), 400

        try:
            # Загружаем текущую карту проекта
            if os.path.exists(PROJECT_MAP):
                with open(PROJECT_MAP, "r") as f:
                    project_map = json.load(f)
            else:
                project_map = {}

            # Разбиваем путь на директорию и имя файла
            dir_path, file_name = os.path.split(path)

            # Проверка и создание вложенной структуры
            if dir_path not in project_map:
                project_map[dir_path] = {}

            # Добавление или обновление информации о файле
            project_map[dir_path][file_name] = {
                "description": description,
                "size": size,
                "last_modified": last_modified
            }

            # Сохраняем обновлённую карту
            with open(PROJECT_MAP, "w") as f:
                json.dump(project_map, f, indent=4)

            return jsonify({"message": f"File '{path}' successfully added or updated in the project map."}), 200
        except Exception as e:
            return jsonify({"error": f"Failed to update project map: {str(e)}"}), 500
        
        
@app.route('/history', methods=['GET', 'POST'])
@require_api_key
def history():
    history_file = os.path.join(BASE_DIR, "history_log.json")  # Лог истории в директории проекта
    
    # Функция для записи изменений в файл
    def log_change(description, affected_files):
        log_entry = {
            "timestamp": int(time.time()),  # Время изменения в секундах
            "description": description,
            "affected_files": affected_files
        }

        if not os.path.exists(history_file):
            with open(history_file, "w") as f:
                json.dump([log_entry], f, indent=4)
        else:
            with open(history_file, "r+") as f:
                logs = json.load(f)
                logs.append(log_entry)
                f.seek(0)
                json.dump(logs, f, indent=4)

    if request.method == 'POST':
        """Записать изменение в лог истории."""
        data = request.json
        description = data.get("description")
        affected_files = data.get("affected_files", [])

        if not description:
            return jsonify({"error": "Description is required."}), 400

        # Логируем изменения
        log_change(description, affected_files)

        return jsonify({"message": "Change logged successfully."}), 201

    elif request.method == 'GET':
        """Получить историю изменений."""
        if not os.path.exists(history_file):
            return jsonify({"error": "No history found."}), 404

        with open(history_file, "r") as f:
            history_data = json.load(f)

        return jsonify(history_data), 200



@app.route('/privacy', methods=['GET'])
def privacy_policy():
    """
    Политика конфиденциальности.
    """
    privacy_text = """
    <h1>Политика конфиденциальности</h1>
    <p>Ваши данные защищены. Мы не передаем личные данные третьим лицам.</p>
    <p>Эта политика описывает, как мы обрабатываем и храним ваши данные.</p>
    <ul>
        <li>Мы собираем данные только для улучшения качества сервиса.</li>
        <li>Ваши данные хранятся на защищенных серверах.</li>
        <li>Вы можете запросить удаление ваших данных в любое время.</li>
    </ul>
    """
    return privacy_text, 200, {'Content-Type': 'text/html'}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

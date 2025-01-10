from datetime import datetime
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import time
import os
import json
import shutil
from functools import wraps

def require_api_key(f):
    """Декоратор для проверки API-ключа."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get("Authorization")
        if api_key != API_KEY:
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return decorated_function


app = Flask(__name__)

# Параметры приложения
BASE_DIR = os.getenv("PROJECT_DIR", "project_data")  # Директория проекта, можно задать через переменную окружения
ABS_DIR = os.path.abspath(BASE_DIR)  # Преобразуем в абсолютный путь
PROJECT_FOLDER = os.path.join(BASE_DIR, "files")    # Папка для файлов
PROJECT_MAP_DB = os.path.join(ABS_DIR, "project_map.db")  # Карта проекта
API_KEY = os.getenv("API_KEY", "default_secret_api_key")  # API-ключ из переменной окружения

# Относительный путь для работы с файлами через API
RELATIVE_FILE_PATH = os.path.join("files")  # Относительный путь от корня папки с файлами проекта


if not os.path.exists(BASE_DIR):
    os.makedirs(BASE_DIR)

# Конфигурация Flask для работы с SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{PROJECT_MAP_DB}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Создать директории для хранения данных
os.makedirs(PROJECT_FOLDER, exist_ok=True)

# Модель для записи в карту проекта
class ProjectFile(db.Model):
    __tablename__ = 'project_files'

    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(512), unique=True, nullable=False)
    type = db.Column(db.String(10), nullable=False)
    description = db.Column(db.String(256), nullable=True)
    size = db.Column(db.Integer, nullable=False)
    last_modified = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<ProjectFile {self.path}>"

# Функция для создания базы данных и таблиц, если они не существуют
def create_db():
    db_folder = os.path.dirname(PROJECT_MAP_DB)
    
    # Создаём директорию, если она не существует
    if not os.path.exists(db_folder):
        os.makedirs(db_folder)

    if not os.path.exists(PROJECT_MAP_DB):
        with app.app_context():
            db.create_all()  # Создаст все таблицы, если они не существуют

# Создание базы данных
create_db()

# Функция для добавления записи в карту проекта
def add_project_file(path, type, description, size, last_modified):
    project_file = ProjectFile(
        path=path,
        type=type,
        description=description,
        size=size,
        last_modified=last_modified
    )
    db.session.add(project_file)
    db.session.commit()

# Функция для удаления записи из карты проекта
def delete_project_file(path):
    project_file = ProjectFile.query.filter_by(path=path).first()
    if project_file:
        db.session.delete(project_file)
        db.session.commit()
        return True
    return False

# Функция для обновления записи в карте проекта
def update_project_file(path, description=None, size=None, last_modified=None):
    project_file = ProjectFile.query.filter_by(path=path).first()
    if project_file:
        if description:
            project_file.description = description
        if size is not None:
            project_file.size = size
        if last_modified is not None:
            project_file.last_modified = last_modified
        db.session.commit()
        return True
    return False

# Функция для получения записи из карты проекта
def get_project_file(path):
    project_file = ProjectFile.query.filter_by(path=path).first()
    if project_file:
        return {
            'path': project_file.path,
            'type': project_file.type,
            'description': project_file.description,
            'size': project_file.size,
            'last_modified': project_file.last_modified
        }
    return None

# Функция для получения всех записей из карты проекта
def get_all_project_files():
    project_files = ProjectFile.query.all()
    return [{
        'path': file.path,
        'type': file.type,
        'description': file.description,
        'size': file.size,
        'last_modified': file.last_modified
    } for file in project_files]

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

    filepath = os.path.join(PROJECT_FOLDER, filename)

    if os.path.exists(filepath):
        return jsonify({"error": "File already exists."}), 400

    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    with open(filepath, 'w') as f:
        f.write(content)

    add_project_file(
        path=filename,
        type="file",
        description=description,
        size=os.path.getsize(filepath),
        last_modified=os.path.getmtime(filepath)
    )

    return jsonify({"message": f"File {filename} created successfully."}), 201

@app.route('/delete', methods=['GET'])
@require_api_key
def delete():
    """Удаление файла или папки."""
    path = request.args.get("path")

    if not path:
        return jsonify({"error": "Path is required."}), 400

    target_path = os.path.join(PROJECT_FOLDER, path)

    if os.path.exists(target_path):
        if os.path.isfile(target_path):
            os.remove(target_path)
            message = f"File {path} deleted successfully."
        else:
            os.rmdir(target_path)
            message = f"Folder {path} deleted successfully."

        delete_project_file(path)

        return jsonify({"message": message}), 200

    return jsonify({"error": "File or folder does not exist."}), 404

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

    filepath = os.path.join(PROJECT_FOLDER, filename)

    if not os.path.isfile(filepath):
        return jsonify({"error": f"File {filename} does not exist."}), 404

    if new_content is not None:
        with open(filepath, 'w') as f:
            f.write(new_content)

    update_project_file(
        path=filename,
        description=new_description,
        size=os.path.getsize(filepath),
        last_modified=os.path.getmtime(filepath)
    )

    return jsonify({"message": f"File {filename} updated successfully."}), 200

@app.route('/get_file', methods=['GET'])
@require_api_key
def get_file():
    """Получение содержимого файла и информации о нем из базы данных."""
    filename = request.args.get("filename")

    if not filename:
        return jsonify({"error": "Filename is required."}), 400

    filepath = os.path.join(PROJECT_FOLDER, filename)

    if not os.path.isfile(filepath):
        return jsonify({"error": f"File {filename} does not exist on disk."}), 404

    try:
        with open(filepath, 'r') as f:
            content = f.read()
    except Exception as e:
        return jsonify({"error": f"Error reading file: {str(e)}"}), 500

    # Попытка получить информацию о файле из базы данных
    project_file = ProjectFile.query.filter_by(path=filename).first()

    if project_file:
        # Если файл найден в БД, возвращаем дополнительную информацию
        return jsonify({
            "filename": filename,
            "content": content,
            "description": project_file.description,
            "size": project_file.size,
            "last_modified": project_file.last_modified
        }), 200
    else:
        # Если файл не найден в БД
        return jsonify({
            "filename": filename,
            "content": content,
            "message": "File not found in the project database."
        }), 207


@app.route('/project_map', methods=['GET', 'POST', 'PUT'])
@require_api_key
def project_map():
    if request.method == 'GET':
        """Получить карту проекта из базы данных."""
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

    elif request.method == 'POST':
        """Удалить информацию о файле или папке из карты проекта."""
        data = request.json
        target_path = data.get("path")

        if not target_path or not isinstance(target_path, str):
            return jsonify({"error": "Path must be a valid string."}), 400

        try:
            # Пытаемся удалить запись о файле из базы данных
            if delete_project_file(target_path):
                return jsonify({"message": f"File '{target_path}' deleted from project database."}), 200
            else:
                return jsonify({"error": f"File '{target_path}' not found in project database."}), 404
        except Exception as e:
            return jsonify({"error": f"Failed to delete path from project map: {str(e)}"}), 500

    elif request.method == 'PUT':
        try:
            """Обновление информации о файле в базе данных."""
            data = request.json
            filename = data.get("path")
            new_description = data.get("description", None)

            if not filename:
                return jsonify({"error": "Filename is required."}), 400

            filepath = os.path.join(PROJECT_FOLDER, filename)

            if not os.path.isfile(filepath):
                return jsonify({"error": f"File {filename} does not exist."}), 404

            # Получаем актуальные данные о файле на диске
            file_size = os.path.getsize(filepath)
            last_modified = os.path.getmtime(filepath)

            # Обновляем информацию о файле в базе данных
            update_project_file(
                path=filename,
                description=new_description,
                size=file_size,
                last_modified=last_modified
            )

            return jsonify({"message": f"File {filename} information updated successfully."}), 200

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

@app.route('/about', methods=['GET', 'POST', 'PUT'])
@require_api_key
def about_project():
    """
    Управление описанием проекта (один общий файл project_description.json):
    - GET: Получить описание проекта.
    - POST: Создать описание проекта.
    - PUT: Обновить описание проекта.
    """
    # Путь к файлу с описанием проекта
    project_description_file = os.path.join(BASE_DIR, "project_description.json")

    if request.method == 'POST':
        """Создание описания проекта."""
        data = request.json
        description = data.get("description")

        if not description:
            return jsonify({"error": "'description' is required."}), 400

        # Проверка существования файла
        if os.path.exists(project_description_file):
            return jsonify({"error": "Project description already exists."}), 400

        # Создание описания
        project_description = {
            "description": description,
            "created_at": int(time.time())
        }

        with open(project_description_file, "w") as f:
            json.dump(project_description, f, indent=4)

        return jsonify({"message": "Project description created successfully."}), 201

    elif request.method == 'PUT':
        """Обновление описания проекта."""
        data = request.json
        new_description = data.get("description")

        if not new_description:
            return jsonify({"error": "'description' is required."}), 400

        # Проверка существования файла
        if not os.path.exists(project_description_file):
            return jsonify({"error": "Project description does not exist."}), 404

        # Обновление описания
        with open(project_description_file, "r") as f:
            project_description = json.load(f)

        project_description["description"] = new_description
        project_description["updated_at"] = int(time.time())

        with open(project_description_file, "w") as f:
            json.dump(project_description, f, indent=4)

        return jsonify({"message": "Project description updated successfully."}), 200

    elif request.method == 'GET':
        """Получение описания проекта."""
        if not os.path.exists(project_description_file):
            return jsonify({"error": "Project description does not exist."}), 404

        # Чтение описания
        with open(project_description_file, "r") as f:
            project_description = json.load(f)

        return jsonify(project_description), 200


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
    # Создание базы данных, если она не существует
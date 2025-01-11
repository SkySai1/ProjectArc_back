import os
import json
import time
from app import db
from app.models import ProjectFile

# Путь для истории изменений
HISTORY_FILE = os.path.join(os.getenv("PROJECT_DIR", "project_data"), "history_log.json")

def log_change(description, affected_files):
    """Логирование изменений в проекте."""
    log_entry = {
        "timestamp": int(time.time()),  # Время изменения
        "description": description,
        "affected_files": affected_files
    }

    if not os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "w") as f:
            json.dump([log_entry], f, indent=4)
    else:
        with open(HISTORY_FILE, "r+") as f:
            logs = json.load(f)
            logs.append(log_entry)
            f.seek(0)
            json.dump(logs, f, indent=4)

def add_project_file(path, type, description, size, last_modified):
    """Добавление записи о файле в карту проекта."""
    project_file = ProjectFile(
        path=path,
        type=type,
        description=description,
        size=size,
        last_modified=last_modified
    )
    db.session.add(project_file)
    db.session.commit()

def delete_project_file(path):
    """Удаление записи о файле из карты проекта."""
    project_file = ProjectFile.query.filter_by(path=path).first()
    if project_file:
        db.session.delete(project_file)
        db.session.commit()
        return True
    return False

def update_project_file(path, description=None, size=None, last_modified=None):
    """Обновление записи о файле в карте проекта."""
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

def get_project_file(path):
    """Получение записи о файле из карты проекта."""
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

def get_all_project_files():
    """Получение всех записей из карты проекта."""
    project_files = ProjectFile.query.all()
    return [ {
        'path': file.path,
        'type': file.type,
        'description': file.description,
        'size': file.size,
        'last_modified': file.last_modified
    } for file in project_files ]
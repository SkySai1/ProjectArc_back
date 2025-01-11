import os
import json
import time

HISTORY_FILE = "project_data/history.json"

# --- Работа с картой проекта ---

def add_project_file(path, type, description, size, last_modified):
    from app import db, ProjectFile
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
    from app import db, ProjectFile
    project_file = ProjectFile.query.filter_by(path=path).first()
    if project_file:
        db.session.delete(project_file)
        db.session.commit()
        return True
    return False

def update_project_file(path, description=None, size=None, last_modified=None):
    from app import db, ProjectFile
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
    from app import ProjectFile
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
    from app import ProjectFile
    project_files = ProjectFile.query.all()
    return [{
        'path': file.path,
        'type': file.type,
        'description': file.description,
        'size': file.size,
        'last_modified': file.last_modified
    } for file in project_files]

# --- Создание базы данных ---

def create_db(project_map_db):
    from app import db
    db_folder = os.path.dirname(project_map_db)

    # Создаём директорию, если она не существует
    if not os.path.exists(db_folder):
        os.makedirs(db_folder)

    if not os.path.exists(project_map_db):
        with db.app.app_context():
            db.create_all()
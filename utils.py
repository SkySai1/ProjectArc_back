import os
import json

def update_project_map(project_folder, map_file):
    """Обновление карты проекта."""
    project_map = {}
    for root, _, files in os.walk(project_folder):
        rel_root = os.path.relpath(root, project_folder)
        project_map[rel_root] = files

    with open(map_file, 'w') as f:
        json.dump(project_map, f, indent=4)

def load_project_map(map_file):
    """Загрузка карты проекта."""
    with open(map_file, 'r') as f:
        return json.load(f)

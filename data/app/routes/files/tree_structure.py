from flask import request, jsonify, current_app
from app.utils import require_api_key
import os

def generate_tree(directory, depth=None, base_dir=None):
    """
    Генерация структуры дерева для указанной директории.
    Параметры:
    - directory: Абсолютный путь к директории.
    - depth: Максимальная глубина обхода.
    - base_dir: Базовая директория для преобразования путей в относительные.
    """
    tree = {
        "directory": os.path.relpath(directory, base_dir) if base_dir else directory,
        "subdirectories": [],
        "files": []
    }
    try:
        for root, dirs, files in os.walk(directory):
            level = root[len(directory):].count(os.sep)
            if depth is not None and level >= depth:
                dirs[:] = []  # Ограничиваем обход
                continue

            # Добавляем только директории
            tree["subdirectories"].extend(
                [os.path.relpath(os.path.join(root, d), base_dir) for d in dirs]
            )

            # Добавляем только файлы
            tree["files"].extend(
                [os.path.relpath(os.path.join(root, f), base_dir) for f in files]
            )
    except Exception as e:
        return {"error": str(e)}
    return tree


@require_api_key
def tree_structure():
    """
    Маршрут для получения структуры файлов и папок.
    Возвращает пути относительно BASE_DIR.
    """
    BASE_DIR = current_app.config["BASE_DIR"]
    relative_path = request.args.get("path", "")
    full_path = os.path.abspath(os.path.join(BASE_DIR, relative_path))
    
    # Проверка на выход за пределы BASE_DIR
    if not full_path.startswith(os.path.abspath(BASE_DIR)):       
        return jsonify({"error": "Invalid path."}), 400

    if not os.path.exists(full_path):
        return jsonify({"error": f"Path '{relative_path}' does not exist."}), 404

    depth = request.args.get("depth")
    depth = int(depth) if depth is not None else None

    tree = generate_tree(full_path, depth=depth, base_dir=BASE_DIR)

    if "error" in tree:
        return jsonify(tree), 500

    return jsonify(tree), 200
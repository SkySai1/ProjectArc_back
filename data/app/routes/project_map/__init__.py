from flask import Blueprint

project_map_bp = Blueprint('project_map', __name__)

# Импорт маршрутов
from .get_project_map import get_project_map
from .delete_from_map import delete_from_map
from .update_project_map import update_map
from .init_from_fs import sync_project_files

# Регистрация маршрутов
project_map_bp.add_url_rule('/', view_func=get_project_map, methods=['GET'], strict_slashes=False)
project_map_bp.add_url_rule('/', view_func=delete_from_map, methods=['POST'], strict_slashes=False)
project_map_bp.add_url_rule('/', view_func=update_map, methods=['PUT'], strict_slashes=False)
project_map_bp.add_url_rule('/sync', view_func=sync_project_files, methods=['POST'])

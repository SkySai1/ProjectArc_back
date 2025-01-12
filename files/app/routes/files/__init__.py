from flask import Blueprint

files_bp = Blueprint('files', __name__)

# Импорт маршрутов
from .create_file import create_file
from .delete_file import delete_file
from .update_file import update_file

# Регистрация маршрутов
files_bp.add_url_rule('/create', view_func=create_file, methods=['POST'], strict_slashes=False)
files_bp.add_url_rule('/delete', view_func=delete_file, methods=['DELETE'], strict_slashes=False)
files_bp.add_url_rule('/update', view_func=update_file, methods=['PUT'], strict_slashes=False)
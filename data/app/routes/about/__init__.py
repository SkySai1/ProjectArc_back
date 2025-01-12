from flask import Blueprint

about_bp = Blueprint('about', __name__)

# Импорт маршрутов
from .get_about import get_about
from .create_about import create_about
from .update_about import update_about

# Регистрация маршрутов
about_bp.add_url_rule('/', view_func=get_about, methods=['GET'], strict_slashes=False)
about_bp.add_url_rule('/', view_func=create_about, methods=['POST'], strict_slashes=False)
about_bp.add_url_rule('/', view_func=update_about, methods=['PUT'], strict_slashes=False)

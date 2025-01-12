from flask import Blueprint

history_bp = Blueprint('history', __name__)

# Импорт маршрутов
from .get_history import get_history
from .log_change import log_change

# Регистрация маршрутов
history_bp.add_url_rule('/', view_func=get_history, methods=['GET'], strict_slashes=False)
history_bp.add_url_rule('/', view_func=log_change, methods=['POST'], strict_slashes=False)
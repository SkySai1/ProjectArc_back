from flask import Blueprint

privacy_bp = Blueprint('privacy', __name__)

# Импорт маршрута
from .privacy_policy import privacy_policy

# Регистрация маршрута
privacy_bp.add_url_rule('/', view_func=privacy_policy, methods=['GET'], strict_slashes=False)
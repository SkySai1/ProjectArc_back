from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Создание экземпляра SQLAlchemy
db = SQLAlchemy()

def create_app(config_class=None):
    """
    Фабрика для создания приложения Flask.
    """
    app = Flask(__name__)
    if config_class:
        app.config.from_object(config_class)

    # Инициализация SQLAlchemy
    db.init_app(app)

    # Регистрация маршрутов
    with app.app_context():
        from app.routes.files import create_file, delete_file, update_file
        from app.routes.project_map import get_project_map, delete_from_map, update_project_map
        from app.routes.history import get_history, log_change
        from app.routes.about import get_about, create_about, update_about
        from app.routes.privacy import privacy_policy

    return app

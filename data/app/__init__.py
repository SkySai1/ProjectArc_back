from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(config_class=None):
    """
    Фабрика для создания экземпляра приложения Flask с настройкой конфигурации и регистрацией маршрутов.
    """
    app = Flask(__name__)
    if config_class:
        app.config.from_object(config_class)

    db.init_app(app)

    # Регистрация маршрутов через Blueprints
    from app.routes.about import about_bp
    from app.routes.files import files_bp
    from app.routes.project_map import project_map_bp
    from app.routes.history import history_bp
    from app.routes.privacy import privacy_bp
    app.register_blueprint(about_bp, url_prefix='/about')
    app.register_blueprint(files_bp, url_prefix='/files')
    app.register_blueprint(project_map_bp, url_prefix='/project_map')
    app.register_blueprint(history_bp, url_prefix='/history')
    app.register_blueprint(privacy_bp, url_prefix='/privacy')

    return app
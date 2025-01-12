import os
from app import create_app
from config import Config, DevelopmentConfig, ProductionConfig

# Определяем конфигурацию на основе окружения
config_class = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
}.get(os.getenv("FLASK_ENV", "development"), Config)

# Создаём приложение
app = create_app(config_class)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))

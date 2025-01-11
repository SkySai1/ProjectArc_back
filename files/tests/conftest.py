import pytest
import os
import tempfile
import shutil
from app import app as flask_app

@pytest.fixture(scope="session")
def temp_test_dir():
    """Создание временной директории для тестов."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        os.environ["PROJECT_DIR"] = tmp_dir  # Устанавливаем переменную окружения
        yield tmp_dir  # Возвращаем путь к временной директории
        # Директория автоматически удалится после завершения

@pytest.fixture(scope="session", autouse=True)
def app(temp_test_dir):
    """
    Фикстура для тестового клиента Flask.
    """
    # Создаём временную базу данных в temp_test_dir
    db_path = os.path.join(temp_test_dir, "test.db")
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    flask_app.config["TESTING"] = True
    flask_app.config["BASE_DIR"] = temp_test_dir

    # Переподключаем SQLAlchemy для работы с новой конфигурацией
    from app import db
    db.init_app(flask_app)

    with flask_app.app_context():
        db.create_all()

    yield flask_app

    # Удаляем базу данных после завершения тестов
    if os.path.exists(db_path):
        os.remove(db_path)


@pytest.fixture(scope="module")
def client(app):
    """Фикстура для тестового клиента Flask."""
    return app.test_client()


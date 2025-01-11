import pytest
import os
import tempfile
import shutil
from app import app as flask_app, db

@pytest.fixture(scope="session")
def temp_test_dir():
    """Создание временной директории для тестов."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        os.environ["PROJECT_DIR"] = tmp_dir  # Устанавливаем переменную окружения
        yield tmp_dir  # Возвращаем путь к временной директории
        # Директория автоматически удалится после завершения

@pytest.fixture(scope="session", autouse=True)
def app(temp_test_dir):
    """Фикстура для тестового клиента Flask."""
    # Создаём временную базу данных
    tmp_dir = os.environ.get("PROJECT_DIR")
    db_fd, db_path = tempfile.mkstemp()
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{tmp_dir}/{db_path}"
    flask_app.config["TESTING"] = True
    flask_app.config["BASE_DIR"] = temp_test_dir

    with flask_app.app_context():
        db.create_all()

    yield flask_app

    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture(scope="module")
def client(app):
    """Фикстура для тестового клиента Flask."""
    return app.test_client()

@pytest.fixture(autouse=True)
def reset_database(app):
    """Сбрасывает базу данных перед каждым тестом."""
    with app.app_context():
        db.drop_all()
        db.create_all()
import pytest
import os
import tempfile
from app import create_app
from app import db
from config import Config

class TestConfig(Config):
    """
    Конфигурация для тестов.
    """
    TESTING = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    def __init__(self, temp_test_dir):
        super().__init__()
        self.SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(temp_test_dir, 'test.db')}"
        self.BASE_DIR = temp_test_dir

@pytest.fixture(scope="session")
def temp_test_dir():
    """
    Создание временной директории для тестов.
    """
    with tempfile.TemporaryDirectory() as tmp_dir:
        os.environ["PROJECT_DIR"] = tmp_dir
        yield tmp_dir

@pytest.fixture(scope="session", autouse=True)
def app(temp_test_dir):
    """
    Фикстура для тестового клиента Flask.
    """
    app = create_app(TestConfig(temp_test_dir))  # Передаём TestConfig с временной директорией

    with app.app_context():
        db.create_all()

    yield app

    # Удаляем временные данные
    temp_test_db = os.path.join(temp_test_dir, "test.db")
    if os.path.exists(temp_test_db):
        os.remove(temp_test_db)

@pytest.fixture(scope="module")
def client(app):
    """
    Фикстура для тестового клиента Flask.
    """
    return app.test_client()

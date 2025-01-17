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
    API_KEY = os.getenv("API_KEY", "key")  # API-ключ из переменной окружения
    API_HEADER = os.getenv("API_KEY", "Authorization") 

    def __init__(self, temp_test_dir):
        super().__init__()
        self.SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(temp_test_dir, 'test.db')}"
        self.BASE_DIR = temp_test_dir

@pytest.fixture(scope="module")
def temp_test_dir():
    """
    Создание временной директории для тестов.
    """
    with tempfile.TemporaryDirectory() as tmp_dir:
        os.environ["PROJECT_DIR"] = tmp_dir
        yield tmp_dir

@pytest.fixture(scope="module", autouse=True)
def app(temp_test_dir):
    """
    Фикстура для тестового клиента Flask.
    """
    app = create_app(TestConfig(temp_test_dir))

    with app.app_context():
        db.create_all()

        # Отладка: Проверка регистрации SQLAlchemy
        if 'sqlalchemy' not in app.extensions:
            print("ERROR: SQLAlchemy not registered in app.extensions")

    yield app

    # Удаляем временные данные
    temp_test_db = os.path.join(temp_test_dir, "test.db")
    if os.path.exists(temp_test_db):
        os.remove(temp_test_db)

@pytest.fixture(scope="module")
def client(app):
    """
    Фикстура для тестового клиента Flask с автоматическим добавлением API-заголовка.
    """
    client = app.test_client()

    class AuthenticatedClient:
        def __init__(self, client, app):
            self.client = client
            self.application = app
            self.api_key = app.config["API_KEY"]

        def get(self, *args, **kwargs):
            headers = kwargs.pop('headers', {})
            headers['Authorization'] = self.api_key
            return self.client.get(*args, headers=headers, **kwargs)

        def post(self, *args, **kwargs):
            headers = kwargs.pop('headers', {})
            headers['Authorization'] = self.api_key
            return self.client.post(*args, headers=headers, **kwargs)

        def put(self, *args, **kwargs):
            headers = kwargs.pop('headers', {})
            headers['Authorization'] = self.api_key
            return self.client.put(*args, headers=headers, **kwargs)

        def delete(self, *args, **kwargs):
            headers = kwargs.pop('headers', {})
            headers['Authorization'] = self.api_key
            return self.client.delete(*args, headers=headers, **kwargs)

    return AuthenticatedClient(client, app)

@pytest.fixture(scope="module")
def non_headers_client(app):
    """
    Фикстура для тестового клиента Flask.
    """
    return app.test_client()

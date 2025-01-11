import pytest
import os
import tempfile
from app import create_app
from app import db

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
    db_path = os.path.join(temp_test_dir, "test.db")
    app = create_app()
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    app.config["TESTING"] = True
    app.config["BASE_DIR"] = temp_test_dir

    with app.app_context():
        db.create_all()

    yield app

    if os.path.exists(db_path):
        os.remove(db_path)


@pytest.fixture(scope="module")
def client(app):
    """
    Фикстура для тестового клиента Flask.
    """
    return app.test_client()
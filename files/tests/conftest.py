import pytest
import os
import shutil
from app import app as flask_app, db
import tempfile

BASE_DIR = "project_data"

@pytest.fixture(scope='module')
def app():
    """
    Фикстура для тестового клиента Flask.
    """
    # Создаем временную базу данных
    db_fd, db_path = tempfile.mkstemp()
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    flask_app.config['TESTING'] = True

    with flask_app.app_context():
        db.create_all()

    yield flask_app

    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture(scope='module')
def client(app):
    """
    Фикстура для тестового клиента Flask.
    """
    return app.test_client()

@pytest.fixture(scope='session', autouse=True)
def cleanup_project_dir():
    """
    Удаляет директорию проекта после выполнения всех тестов.
    """
    yield
    if os.path.exists(BASE_DIR):
        shutil.rmtree(BASE_DIR)

@pytest.fixture(autouse=True)
def reset_database(app):
    """
    Сбрасывает базу данных перед каждым тестом.
    """
    with app.app_context():
        db.drop_all()
        db.create_all()
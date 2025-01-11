import os
import pytest
import json
from app.utils import log_change

@pytest.fixture
def setup_test_env():
    """Инициализация тестовой среды."""
    test_dir = "test_project_data"
    history_file = os.path.join(test_dir, "history_log.json")

    # Создаём директорию
    os.makedirs(test_dir, exist_ok=True)

    # Удаляем файл истории, если он существует
    if os.path.exists(history_file):
        os.remove(history_file)

    yield test_dir

    # Удаляем тестовую директорию после тестов
    if os.path.exists(test_dir):
        import shutil
        shutil.rmtree(test_dir)

def test_log_and_get_history(setup_test_env, monkeypatch):
    """Тест: логирование изменений и получение истории."""
    test_dir = setup_test_env
    history_file = os.path.join(test_dir, "history_log.json")

    # Подмена пути в log_change
    monkeypatch.setattr("app.utils.HISTORY_FILE", history_file)

    # Логируем изменения
    log_change("Added test file", ["test_file.txt"])
    log_change("Removed test file", ["test_file.txt"])

    # Проверяем, что файл истории создан
    assert os.path.exists(history_file)

    # Читаем историю
    with open(history_file, "r") as f:
        history = json.load(f)

    assert len(history) == 2
    assert history[0]["description"] == "Added test file"
    assert history[1]["description"] == "Removed test file"
def test_missing_history_file(client, temp_test_dir):
    """
    Тест: файл истории отсутствует.
    """
    import os
    # Убеждаемся, что файл отсутствует
    history_file = os.path.join(temp_test_dir, "history_log.json")
    if os.path.exists(history_file):
        os.remove(history_file)

    response = client.get('/history/')
    assert response.status_code == 404
    assert response.json == {"error": "History log file does not exist."}



def test_log_and_get_history(client):
    """
    Интеграционный тест для логирования и получения истории.
    """
    # Логируем изменение
    log_data = {
        "description": "Test log entry",
        "affected_files": ["test_file.txt"]
    }
    response = client.post('/history/', json=log_data)
    assert response.status_code == 201
    assert response.json == {"message": "Change logged successfully."}

    # Логируем второе изменение
    log_data_2 = {
        "description": "Another log entry",
        "affected_files": ["another_file.txt"]
    }
    response = client.post('/history/', json=log_data_2)
    assert response.status_code == 201
    assert response.json == {"message": "Change logged successfully."}

    # Проверяем историю
    response = client.get('/history/')
    assert response.status_code == 200
    history = response.json
    assert len(history) == 2

    # Проверяем первую запись
    assert history[0]["description"] == "Test log entry"
    assert history[0]["affected_files"] == ["test_file.txt"]
    assert "timestamp" in history[0]

    # Проверяем вторую запись
    assert history[1]["description"] == "Another log entry"
    assert history[1]["affected_files"] == ["another_file.txt"]
    assert "timestamp" in history[1]

def test_invalid_log_entry(client):
    """
    Тест для проверки ошибок при логировании.
    """
    # Пустое описание
    log_data = {"affected_files": ["test_file.txt"]}
    response = client.post('/history/', json=log_data)
    assert response.status_code == 400
    assert response.json == {"error": "Description is required."}

def test_empty_history_file_with_content(client, temp_test_dir):
    """
    Тест: файл истории существует, но он пустой.
    """
    import os
    history_file = os.path.join(temp_test_dir, "history_log.json")
    with open(history_file, "w") as f:
        pass  # Создаём пустой файл

    response = client.get('/history/')
    assert response.status_code == 200
    assert response.json == []


def test_history_api_require(non_headers_client):
    """
    Тест на срабатывание проверки API ключа
    """
    client = non_headers_client

    # Проверка файла истории
    response = client.get('/history/')
    assert response.status_code == 401

    # Логируем изменение
    log_data = {
        "description": "Test log entry",
        "affected_files": ["test_file.txt"]
    }
    response = client.post('/history/', json=log_data)

    assert response.status_code == 401

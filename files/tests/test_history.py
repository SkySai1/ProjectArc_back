def test_log_and_get_history(client):
    """
    Интеграционный тест для логирования и получения истории.
    """
    # Проверяем начальное состояние истории
    response = client.get('/history')
    assert response.status_code == 404
    assert response.json == {"error": "No history found."}

    # Логируем изменение
    log_data = {
        "description": "Test log entry",
        "affected_files": ["test_file.txt"]
    }
    response = client.post('/history', json=log_data)
    assert response.status_code == 201
    assert response.json == {"message": "Change logged successfully."}

    # Логируем второе изменение
    log_data_2 = {
        "description": "Another log entry",
        "affected_files": ["another_file.txt"]
    }
    response = client.post('/history', json=log_data_2)
    assert response.status_code == 201
    assert response.json == {"message": "Change logged successfully."}

    # Проверяем историю
    response = client.get('/history')
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
    response = client.post('/history', json=log_data)
    assert response.status_code == 400
    assert response.json == {"error": "Description is required."}
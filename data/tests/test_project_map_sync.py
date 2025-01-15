def test_sync_project_files(client, temp_test_dir):
    """
    Тест: проверка синхронизации файлов с картой проекта.
    """
    import os
    # Создаём тестовые файлы в временной директории
    file1_path = os.path.join(temp_test_dir, "file1.txt")
    file2_path = os.path.join(temp_test_dir, "file2.txt")

    with open(file1_path, "w") as f:
        f.write("Test content for file1")

    # Формируем запрос
    payload = [
        {"path": "file1.txt", "description": "Test file 1"},
        {"path": "file2.txt", "description": "Test file 2"},  # Этот файл не будет создан
    ]

    # Выполняем запрос к эндпоинту синхронизации
    response = client.post('/project_map/sync', json=payload)
    response_data = response.get_json()

    # Проверяем код ответа и содержимое
    assert response.status_code == 207  # Ожидается мультистатус
    assert "synchronized" in response_data["details"]
    assert "not_found" in response_data["details"]
    assert "file1.txt" in response_data["details"]["synchronized"]
    assert "file2.txt" in response_data["details"]["not_found"]

    # Запрашиваем карту проекта через стандартный endpoint
    response = client.get('/project_map/')
    assert response.status_code == 200
    project_map = response.get_json()

    # Проверяем, что файл был добавлен в карту проекта
    file1_entry = next((item for item in project_map if item["path"] == "file1.txt"), None)
    assert file1_entry is not None
    assert file1_entry["description"] == "Test file 1"
    assert file1_entry["size"] == os.path.getsize(file1_path)

def test_sync_file_already_in_db(client, app):
    """
    Тест: синхронизация файла, который уже существует в базе данных.
    """
    # Создаём файл на диске
    client.post("/files/create", json={
        "path": "existing_file.txt",
        "content": "Existing file content"
    })

    # Синхронизируем файл в базу данных
    client.post("/project_map/sync", json=[{
        "path": "existing_file.txt",
        "description": "This is a test file"
    }])

    # Пытаемся повторно синхронизировать тот же файл
    response = client.post("/project_map/sync", json=[{
        "path": "existing_file.txt",
        "description": "This is a test file"
    }])

    assert response.status_code == 200
    response_data = response.json

    # Проверяем, что файл указан в "already_in_db"
    assert "existing_file.txt" in response_data["details"]["already_in_db"]
    assert len(response_data["details"]["synchronized"]) == 0
    assert len(response_data["details"]["not_found"]) == 0

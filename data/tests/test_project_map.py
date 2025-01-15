def test_add_and_get_project_map(client):
    """
    Тест: Добавление файла и получение карты проекта.
    """
    # Создаём файл через маршрут /files/create
    response = client.post('/files/create', json={
        'path': 'map_test.txt',
        'content': 'Content for map test',
        'description': 'Test file for map'
    })
    assert response.status_code == 201
    assert response.json['message'] == "File 'map_test.txt' created successfully."

    # Проверяем карту проекта
    response = client.get('/project_map/')
    assert response.status_code == 200
    project_map = response.json

    # Проверяем, что файл добавлен в карту
    file_entry = next((file for file in project_map if file['path'] == 'map_test.txt'), None)
    assert file_entry is not None
    assert file_entry['description'] == 'Test file for map'
    assert file_entry['size'] > 0
    assert 'last_modified' in file_entry

def test_delete_from_project_map(client):
    """
    Тест: Удаление записи из карты проекта.
    """
    # Создаём файл через маршрут /files/create
    response = client.post('/files/create', json={
        'path': 'delete_map_test.txt',
        'content': 'Content for delete test',
        'description': 'File to delete'
    })
    assert response.status_code == 201
    assert response.json['message'] == "File 'delete_map_test.txt' created successfully."

    # Удаляем файл через маршрут /project_map
    response = client.post('/project_map/', json={
        'path': 'delete_map_test.txt'
    })
    assert response.status_code == 200
    assert response.json['message'] == "File 'delete_map_test.txt' deleted from project database."

    # Проверяем, что файл удалён из карты
    response = client.get('/project_map/')
    assert response.status_code == 200
    project_map = response.json
    deleted_file = next((file for file in project_map if file['path'] == 'delete_map_test.txt'), None)
    assert deleted_file is None

def test_update_project_map(client):
    """
    Тест: Обновление записи в карте проекта.
    """
    # Создаём файл через маршрут /files/create
    response = client.post('/files/create', json={
        'path': 'update_map_test.txt',
        'content': 'Content for update test',
        'description': 'Initial description'
    })
    assert response.status_code == 201
    assert response.json['message'] == "File 'update_map_test.txt' created successfully."

    # Обновляем описание файла через маршрут /project_map
    response = client.put('/project_map/', json={
        'path': 'update_map_test.txt',
        'description': 'Updated description'
    })
    assert response.status_code == 200
    assert response.json['message'] == "File 'update_map_test.txt' information updated successfully."

    # Проверяем изменения в карте проекта
    response = client.get('/project_map/')
    assert response.status_code == 200
    project_map = response.json

    updated_file = next((file for file in project_map if file['path'] == 'update_map_test.txt'), None)
    assert updated_file is not None
    assert updated_file['description'] == 'Updated description'

def test_invalid_delete_request(client):
    """
    Тест: Ошибка при удалении записи с отсутствующим 'path'.
    """
    response = client.post('/project_map/', json={})
    assert response.status_code == 400
    assert response.json['error'] == "'path' is required."

def test_invalid_update_request(client):
    """
    Тест: Ошибка при обновлении записи с некорректными данными.
    """
    response = client.put('/project_map/', json={})
    assert response.status_code == 400
    assert response.json['error'] == "'path' and 'description' are required."

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


def test_projectmap_api_require(non_headers_client):
    """
    Тест на срабатывание проверки API ключа
    """
    client = non_headers_client

    # Проверяем карту проекта
    response = client.get('/project_map/')
    assert response.status_code == 401

    # Обновляем описание файла через маршрут /project_map
    response = client.put('/project_map/', json={
        'path': 'update_map_test.txt',
        'description': 'Updated description'
    })
    assert response.status_code == 401

    # Удаляем файл через маршрут /project_map
    response = client.post('/project_map/', json={
        'path': 'delete_map_test.txt'
    })
    assert response.status_code == 401

    # Формируем запрос
    payload = [
        {"path": "file1.txt", "description": "Test file 1"},
    ]

    # Выполняем запрос к эндпоинту синхронизации
    response = client.post('/project_map/sync', json=payload)
    assert response.status_code == 401
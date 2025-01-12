def test_add_and_get_project_map(client):
    """
    Тест: Добавление файла и получение карты проекта.
    """
    # Создаём файл через маршрут /files/create
    response = client.post('/files/create', json={
        'filename': 'map_test.txt',
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
        'filename': 'delete_map_test.txt',
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
        'filename': 'update_map_test.txt',
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
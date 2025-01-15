def test_add_and_get_project_map(client):
    """
    Тест: добавление файла и получение карты проекта.
    """
    # Создаём файл через маршрут /files/create
    client.post('/files/create', json={
        'path': 'map_test.txt',
        'content': 'Content for map test',
        'description': 'Test file for map'
    })

    response = client.get('/project_map')
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]['path'] == 'map_test.txt'

def test_delete_from_project_map(client):
    """
    Тест: удаление файла из карты проекта.
    """
    # Создаём файл через маршрут /files/create
    client.post('/files/create', json={
        'path': 'map_test.txt',
        'content': 'Content for map test',
        'description': 'Test file for map'
    })

    response = client.post('/project_map', json={'path': 'map_test.txt'})
    assert response.status_code == 200
    assert response.json['message'] == 'File \'map_test.txt\' deleted from project database.'

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

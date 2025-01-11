def test_get_project_map_empty(client):
    """Тест на получение пустой карты проекта."""
    response = client.get('/project_map')
    assert response.status_code == 200
    assert response.json == []

def test_add_and_get_project_map(client):
    """Тест на добавление файла и получение карты проекта."""
    # Создаем файл
    client.post('/create', json={
        'filename': 'map_test.txt',
        'content': 'Content for map test',
        'description': 'Test file for map'
    })

    # Получаем карту проекта
    response = client.get('/project_map')
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]['path'] == 'map_test.txt'

def test_delete_from_project_map(client):
    """Тест на удаление записи из карты проекта."""
    # Создаем файл
    client.post('/create', json={
        'filename': 'delete_map_test.txt',
        'content': 'Content for delete test'
    })

    # Удаляем из карты проекта
    response = client.post('/project_map', json={
        'path': 'delete_map_test.txt'
    })
    assert response.status_code == 200
    assert response.json['message'] == "File 'delete_map_test.txt' deleted from project database."

    # Проверяем, что файл удален
    response = client.get('/project_map')
    assert len(response.json) == 0

def test_update_project_map(client):
    """Тест на обновление записи в карте проекта."""
    # Создаем файл
    client.post('/create', json={
        'filename': 'update_map_test.txt',
        'content': 'Content for update test'
    })

    # Обновляем описание
    response = client.put('/project_map', json={
        'path': 'update_map_test.txt',
        'description': 'Updated description'
    })
    assert response.status_code == 200
    assert response.json['message'] == 'File update_map_test.txt information updated successfully.'

    # Проверяем обновление
    response = client.get('/project_map')
    assert response.json[0]['description'] == 'Updated description'
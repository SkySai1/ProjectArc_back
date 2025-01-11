def test_create_file(client):
    """Тест на создание файла через маршрут /create."""
    response = client.post('/create', json={
        'filename': 'test_file.txt',
        'content': 'Test content',
        'description': 'Test file'
    })
    assert response.status_code == 201
    assert response.json['message'] == 'File test_file.txt created successfully.'

def test_create_file_missing_filename(client):
    """Тест на создание файла без имени файла."""
    response = client.post('/create', json={})
    assert response.status_code == 400
    assert response.json['error'] == 'Filename is required.'

def test_delete_file(client):
    """Тест на удаление файла через маршрут /delete."""
    # Сначала создаем файл
    client.post('/create', json={
        'filename': 'delete_test.txt',
        'content': 'Content to delete'
    })

    # Затем удаляем
    response = client.get('/delete', query_string={'path': 'delete_test.txt'})
    assert response.status_code == 200
    assert response.json['message'] == 'File delete_test.txt deleted successfully.'

def test_update_file(client):
    """Тест на обновление содержимого файла через маршрут /update."""
    # Создаем файл
    client.post('/create', json={
        'filename': 'update_test.txt',
        'content': 'Initial content'
    })

    # Обновляем файл
    response = client.put('/update', json={
        'filename': 'update_test.txt',
        'content': 'Updated content',
        'description': 'Updated file'
    })
    assert response.status_code == 200
    assert response.json['message'] == 'File update_test.txt updated successfully.'
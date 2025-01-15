def test_projectmap_api_require(non_headers_client):
    """
    Тест: проверка авторизации для маршрутов карты проекта.
    """
    client = non_headers_client

    # Проверяем добавление файла без авторизации
    response = client.post('/project_map', json={
        'path': 'unauthorized_file.txt',
        'description': 'Unauthorized file',
        'size': 123,
        'last_modified': 1672531200
    })
    assert response.status_code == 401

    # Проверяем удаление файла без авторизации
    response = client.post('/project_map', json={
        'path': 'unauthorized_file.txt'
    })
    assert response.status_code == 401

    # Проверяем синхронизацию файлов без авторизации
    response = client.post('/project_map/sync', json=[{
        'path': 'unauthorized_file.txt',
        'description': 'Unauthorized file',
        'size': 123,
        'last_modified': 1672531200
    }])
    assert response.status_code == 401
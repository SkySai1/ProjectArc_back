def test_history_api_require(non_headers_client):
    """
    Тест: проверка авторизации для маршрутов /history.
    """
    client = non_headers_client

    # Проверяем получение истории без авторизации
    response = client.get('/history')
    assert response.status_code == 401

    # Проверяем логирование изменений без авторизации
    response = client.post('/history', json={
        'description': 'Unauthorized attempt',
        'affected_files': ['unauthorized_file.txt']
    })
    assert response.status_code == 401
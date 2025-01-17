def test_about_api_require(non_headers_client):
    """
    Тест на срабатывание проверки API ключа
    """
    client = non_headers_client

    response = client.get('/about', headers={})
    assert response.status_code == 401

    response = client.post('/about', json={
        'description': 'Another test project.'
    })
    assert response.status_code == 401

    response = client.put('/about', json={
        'description': 'Updated test project description.'
    })

    assert response.status_code == 401
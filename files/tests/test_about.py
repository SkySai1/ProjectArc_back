def test_get_about_empty(client):
    """Тест на получение пустого описания проекта."""
    response = client.get('/about')
    assert response.status_code == 404
    assert response.json['error'] == 'Project description does not exist.'

def test_create_and_get_about(client):
    """Тест на создание описания проекта и его получение."""
    # Создаем описание проекта
    response = client.post('/about', json={
        'description': 'This is a test project.'
    })
    assert response.status_code == 201
    assert response.json['message'] == 'Project description created successfully.'

    # Получаем описание проекта
    response = client.get('/about')
    assert response.status_code == 200
    assert response.json['description'] == 'This is a test project.'

def test_update_about(client):
    """Тест на обновление описания проекта."""
    # Обновляем описание проекта
    response = client.put('/about', json={
        'description': 'Updated test project description.'
    })
    assert response.status_code == 200
    assert response.json['message'] == 'Project description updated successfully.'

    # Проверяем обновление
    response = client.get('/about')
    assert response.json['description'] == 'Updated test project description.'
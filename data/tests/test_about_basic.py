def test_get_about_empty(client):
    """
    Тест на получение пустого описания проекта.
    """
    response = client.get('/about')
    assert response.status_code == 404
    assert response.json['error'] == 'Project description does not exist.'

def test_create_and_get_about(client, temp_test_dir):
    """
    Тест на создание описания проекта и его получение.
    """
    # Создаём описание проекта
    response = client.post('/about', json={
        'description': 'This is a test project.'
    })
    assert response.status_code == 201
    assert response.json['message'] == 'Project description created successfully.'

    # Проверяем, что описание создано в временной директории
    import os
    about_file = os.path.join(temp_test_dir, 'project_description.json')
    assert os.path.exists(about_file)

    # Получаем описание проекта
    response = client.get('/about')
    assert response.status_code == 200
    assert response.json['description'] == 'This is a test project.'
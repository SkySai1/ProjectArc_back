def test_update_about(client, temp_test_dir):
    """
    Тест на обновление описания проекта.
    """

    # Создаём описание проекта
    response = client.post('/about', json={
        'description': 'This is a test project.'
    })

    # Обновляем описание проекта
    response = client.put('/about', json={
        'description': 'Updated test project description.'
    })
    assert response.status_code == 200
    assert response.json['message'] == 'Project description updated successfully.'

    # Проверяем, что описание обновлено
    response = client.get('/about')
    assert response.status_code == 200
    assert response.json['description'] == 'Updated test project description.'

    # Проверяем файл в директории
    import os
    about_file = os.path.join(temp_test_dir, 'project_description.json')
    assert os.path.exists(about_file)

def test_create_about_already_exists(client):
    """
    Тест на повторное создание описания проекта.
    """
    response = client.post('/about', json={
        'description': 'Another test project.'
    })
    assert response.status_code == 400
    assert response.json['error'] == 'Project description already exists.'
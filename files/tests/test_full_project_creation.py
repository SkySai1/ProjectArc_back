import pytest

def test_full_project_creation(client):
    """
    Тест полного создания проекта, включая варианты добавления, изменения и удаления файлов.
    """
    # Создание описания проекта
    response = client.post('/about', json={
        'description': 'This is a test project for full workflow.'
    })
    assert response.status_code == 201
    assert response.json['message'] == 'Project description created successfully.'

    # Проверка получения описания проекта
    response = client.get('/about')
    assert response.status_code == 200
    assert response.json['description'] == 'This is a test project for full workflow.'

    # Добавление файла в проект
    response = client.post('/create', json={
        'filename': 'file1.txt',
        'content': 'Content of file 1',
        'description': 'First test file'
    })
    assert response.status_code == 201
    assert response.json['message'] == 'File file1.txt created successfully.'

    # Добавление второго файла в проект
    response = client.post('/create', json={
        'filename': 'file2.txt',
        'content': 'Content of file 2',
        'description': 'Second test file'
    })
    assert response.status_code == 201
    assert response.json['message'] == 'File file2.txt created successfully.'

    # Получение карты проекта
    response = client.get('/project_map')
    assert response.status_code == 200
    assert len(response.json) == 2

    # Обновление описания первого файла
    response = client.put('/project_map', json={
        'path': 'file1.txt',
        'description': 'Updated description for first file'
    })
    assert response.status_code == 200
    assert response.json['message'] == 'File file1.txt information updated successfully.'

    # Удаление второго файла
    response = client.post('/project_map', json={
        'path': 'file2.txt'
    })
    assert response.status_code == 200
    assert response.json['message'] == "File 'file2.txt' deleted from project database."

    # Проверка карты проекта после удаления
    response = client.get('/project_map')
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]['path'] == 'file1.txt'

    # Проверка истории изменений
    response = client.get('/history')
    assert response.status_code == 200
    assert len(response.json) >= 4  # Описание проекта, два файла, удаление файла
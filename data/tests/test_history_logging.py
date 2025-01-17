import os
import json
import time

def test_log_and_get_history(client):
    """
    Тест: логирование изменений и их получение.
    """
    # Логируем изменение
    response = client.post('/history', json={
        'description': 'Initial commit',
        'affected_files': ['file1.txt', 'file2.txt']
    })
    assert response.status_code == 201
    assert response.json['message'] == 'Change logged successfully.'

    # Получаем историю
    response = client.get('/history')
    assert response.status_code == 200
    assert len(response.json) == 1
    entry = response.json[0]
    assert entry['description'] == 'Initial commit'
    assert entry['affected_files'] == ['file1.txt', 'file2.txt']

def test_invalid_log_entry(client):
    """
    Тест: попытка логирования с некорректными данными.
    """
    response = client.post('/history', json={})
    assert response.status_code == 400
    assert response.json['error'] == 'Description is required.'

def test_log_updates_project_description(client):
    """
    Тест: Проверяет обновление поля updated_at в project_description.json при логировании.
    """
    base_dir = client.application.config["BASE_DIR"]
    about_file = os.path.join(base_dir, "project_description.json")

    # Создать файл project_description.json
    initial_time = int(time.time())
    project_description = {
        "description": "Test project",
        "created_at": initial_time,
        "updated_at": initial_time
    }
    with open(about_file, "w") as f:
        json.dump(project_description, f, indent=4)

    # Логировать изменение
    time.sleep(1)  # Ждать, чтобы было различие во времени
    response = client.post('/history', json={
        'description': 'Updated description',
        'affected_files': ['test_file.py']
    })
    assert response.status_code == 201
    assert response.json['message'] == 'Change logged successfully.'

    # Проверить обновление updated_at
    with open(about_file, "r") as f:
        updated_project_description = json.load(f)
    
    assert updated_project_description["updated_at"] > initial_time
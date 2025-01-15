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
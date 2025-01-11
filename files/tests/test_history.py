def test_get_empty_history(client):
    """Тест на получение пустой истории изменений."""
    response = client.get('/history')
    assert response.status_code == 404
    assert response.json['error'] == 'No history found.'

def test_log_and_get_history(client):
    """Тест на добавление записи в историю и получение истории."""
    # Логируем изменение
    response = client.post('/history', json={
        'description': 'Initial change',
        'affected_files': ['test_file.txt']
    })
    assert response.status_code == 201
    assert response.json['message'] == 'Change logged successfully.'

    # Получаем историю
    response = client.get('/history')
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]['description'] == 'Initial change'
    assert 'test_file.txt' in response.json[0]['affected_files']
def test_invalid_delete_request(client):
    """
    Тест: попытка удалить файл из карты проекта без указания пути.
    """
    response = client.post('/project_map', json={})
    assert response.status_code == 400
    assert response.json['error'] == "'path' is required."

def test_invalid_update_request(client):
    """
    Тест: попытка обновить файл в карте проекта с некорректными данными.
    """
    response = client.put('/project_map', json={
        'description': 'Updated description'
    })
    assert response.status_code == 400
    assert response.json['error'] == "'path' and 'description' are required."

CREATE_URL = "/files/create"
UPDATE_URL = "/files/update"
DELETE_URL = "/files/delete"
READ_URL = "/files/read"

def test_files_api_require(non_headers_client):
    """
    Тест на срабатывание проверки API ключа
    """
    client = non_headers_client

    # Создание файла
    response = client.post(CREATE_URL, json={
        "filename": "test.txt",
        "content": "Hello, World!",
        "description": "Test file"
    })
    assert response.status_code == 401

    # Обновление файла
    response = client.put(UPDATE_URL, json={
        "path": "nonexistent.txt",
        "description": "Updated description"
    })

    assert response.status_code == 401

    # Удаление файла
    response = client.delete(DELETE_URL, json={"path": "test.txt"})
    assert response.status_code == 401
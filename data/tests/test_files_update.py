CREATE_URL = "/files/create"
UPDATE_URL = "/files/update"
READ_URL = "/files/read"

def test_update_file_content_success(client):
    """
    Тест: успешное обновление содержимого файла.
    """
    # Создание файла для теста
    client.post(CREATE_URL, json={
        "path": "test_update_content.txt",
        "content": "Original content",
        "description": "Test file"
    })

    # Обновление содержимого файла
    response = client.put(UPDATE_URL, json={
        "path": "test_update_content.txt",
        "description": "Updated description",
        "content": "Updated content"
    })

    assert response.status_code == 200
    assert response.json["message"] == "File 'test_update_content.txt' updated successfully."

    # Проверка содержимого
    response = client.get(READ_URL, query_string={"path": "test_update_content.txt"})
    assert response.status_code == 200
    assert response.json["content"] == "Updated content"
    assert response.json["path"] == "test_update_content.txt"

def test_update_file_content_nonexistent(client):
    """
    Тест: обновление содержимого несуществующего файла.
    """
    response = client.put(UPDATE_URL, json={
        "path": "nonexistent_file.txt",
        "description": "Description",
        "content": "New content"
    })

    assert response.status_code == 404
    assert response.json["error"] == "File 'nonexistent_file.txt' does not exist."

def test_update_file_without_content(client):
    """
    Тест: обновление только описания без изменения содержимого.
    """
    # Создание файла для теста
    client.post(CREATE_URL, json={
        "path": "test_update_no_content.txt",
        "content": "Initial content",
        "description": "Test file"
    })

    # Обновление описания без изменения содержимого
    response = client.put(UPDATE_URL, json={
        "path": "test_update_no_content.txt",
        "description": "Updated description"
    })

    assert response.status_code == 200
    assert response.json["message"] == "File 'test_update_no_content.txt' updated successfully."

    # Проверка, что содержимое осталось неизменным
    response = client.get(READ_URL, query_string={"path": "test_update_no_content.txt"})
    assert response.status_code == 200
    assert response.json["content"] == "Initial content"
    assert response.json["path"] == "test_update_no_content.txt"

def test_update_file_info_only(client):
    """
    Тест: обновление только описания файла без изменения его содержимого.
    """
    # Создание файла для теста
    client.post(CREATE_URL, json={
        "path": "test_update_info_only.txt",
        "content": "Content remains unchanged.",
        "description": "Initial description"
    })

    # Обновление только описания файла
    response = client.put(UPDATE_URL, json={
        "path": "test_update_info_only.txt",
        "description": "Updated description"
    })

    assert response.status_code == 200
    assert response.json["message"] == "File 'test_update_info_only.txt' updated successfully."

    # Проверка, что содержимое файла осталось неизменным
    response = client.get(READ_URL, query_string={"path": "test_update_info_only.txt"})
    assert response.status_code == 200
    assert response.json["content"] == "Content remains unchanged."
    assert response.json["path"] == "test_update_info_only.txt"
import pytest

CREATE_URL = "/files/create"
UPDATE_URL = "/files/update"
DELETE_URL = "/files/delete"
READ_URL = "/files/read"

def test_read_file_success(client):
    """
    Тест: успешное чтение существующего файла.
    """
    # Создание файла для теста
    client.post(CREATE_URL, json={
        "filename": "test_read.txt",
        "content": "This is a test file."
    })

    # Чтение содержимого файла
    response = client.get(READ_URL, query_string={"filename": "test_read.txt"})
    assert response.status_code == 200
    assert response.json["filename"] == "test_read.txt"
    assert response.json["content"] == "This is a test file."
    assert "size" in response.json
    assert "last_modified" in response.json

def test_read_file_missing_filename(client):
    """
    Тест: попытка чтения файла без указания имени.
    """
    response = client.get(READ_URL)
    assert response.status_code == 400
    assert response.json["error"] == "Filename is required."

def test_read_file_nonexistent(client):
    """
    Тест: попытка чтения несуществующего файла.
    """
    response = client.get(READ_URL, query_string={"filename": "nonexistent.txt"})
    assert response.status_code == 404
    assert response.json["error"] == "File 'nonexistent.txt' does not exist."

def test_create_file_missing_filename(client):
    """
    Тест: создание файла без 'filename'.
    """
    response = client.post(CREATE_URL, json={"content": "Test content"})
    assert response.status_code == 400
    assert response.json["error"] == "Filename is required."

def test_create_file_success(client):
    """
    Тест: успешное создание файла.
    """
    response = client.post(CREATE_URL, json={
        "filename": "test.txt",
        "content": "Hello, World!",
        "description": "Test file"
    })
    assert response.status_code == 201
    assert response.json["message"] == "File 'test.txt' created successfully."

def test_delete_file(client):
    """
    Тест: удаление существующего файла.
    """
    # Создание файла для теста
    client.post(CREATE_URL, json={
        "filename": "test.txt",
        "content": "Hello, World!"
    })

    # Удаление файла
    response = client.delete(DELETE_URL, json={"path": "test.txt"})
    assert response.status_code == 200
    assert response.json["message"] == "File 'test.txt' deleted from project database."

def test_delete_file_nonexistent(client):
    """
    Тест: удаление несуществующего файла.
    """
    response = client.delete(DELETE_URL, json={"path": "nonexistent.txt"})
    assert response.status_code == 404
    assert response.json["error"] == "File 'nonexistent.txt' does not exist."

def test_update_file(client):
    """
    Тест: обновление описания файла.
    """
    # Создание файла для теста
    client.post(CREATE_URL, json={
        "filename": "test.txt",
        "content": "Hello, World!",
    })

    # Обновление файла
    response = client.put(UPDATE_URL, json={
        "path": "test.txt",
        "description": "Updated description"
    })
    assert response.status_code == 200
    assert response.json["message"] == "File 'test.txt' information updated successfully."

def test_update_file_nonexistent(client):
    """
    Тест: обновление описания для несуществующего файла.
    """
    response = client.put(UPDATE_URL, json={
        "path": "nonexistent.txt",
        "description": "Updated description"
    })
    assert response.status_code == 404
    assert response.json["error"] == "File 'nonexistent.txt' does not exist."


def test_files_api_require(non_headers_client):
    """
    Тест на срабатывание проверки API ключа
    """
    client = non_headers_client

    # Чтение содержимого файла
    response = client.get(READ_URL, query_string={"filename": "test_read.txt"})
    assert response.status_code == 401

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


    
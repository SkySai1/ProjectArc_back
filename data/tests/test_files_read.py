CREATE_URL = "/files/create"
READ_URL = "/files/read"

def test_read_file_success(client):
    """
    Тест: успешное чтение существующего файла.
    """
    # Создание файла для теста
    client.post(CREATE_URL, json={
        "path": "test_read.txt",
        "content": "This is a test file."
    })

    # Чтение содержимого файла
    response = client.get(READ_URL, query_string={"path": "test_read.txt"})
    assert response.status_code == 200
    assert response.json["path"] == "test_read.txt"
    assert response.json["content"] == "This is a test file."
    assert "size" in response.json
    assert "last_modified" in response.json

def test_read_file_missing_filename(client):
    """
    Тест: попытка чтения файла без указания имени.
    """
    response = client.get(READ_URL)
    assert response.status_code == 400
    assert response.json["error"] == "path is required."

def test_read_file_nonexistent(client):
    """
    Тест: попытка чтения несуществующего файла.
    """
    response = client.get(READ_URL, query_string={"path": "nonexistent.txt"})
    assert response.status_code == 404
    assert response.json["error"] == "File 'nonexistent.txt' does not exist."
CREATE_URL = "/files/create"

def test_create_file_missing_filename(client):
    """
    Тест: создание файла без 'filename'.
    """
    response = client.post(CREATE_URL, json={"content": "Test content"})
    assert response.status_code == 400
    assert response.json["error"] == "path is required."

def test_create_file_success(client):
    """
    Тест: успешное создание файла.
    """
    response = client.post(CREATE_URL, json={
        "path": "test.txt",
        "content": "Hello, World!",
        "description": "Test file"
    })
    assert response.status_code == 201
    assert response.json["message"] == "File 'test.txt' created successfully."
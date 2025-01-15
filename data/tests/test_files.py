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
    assert response.json["error"] == "Path 'nonexistent.txt' does not exist."

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
    Тест: обновление только описания файла без изменения содержимого.
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

    # Проверка, что описание обновлено (если оно где-то доступно)
    # Здесь подразумевается, что информация об описании записывается в карту проекта.

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

def test_delete_directory_success(client, app):
    """
    Тест: успешное рекурсивное удаление директории и всех её файлов.
    """
    # Создание файловой структуры
    client.post(CREATE_URL, json={"path": "test_dir/file1.txt", "content": "File 1 content"})
    client.post(CREATE_URL, json={"path": "test_dir/file2.txt", "content": "File 2 content"})
    client.post(CREATE_URL, json={"path": "test_dir/sub_dir/file3.txt", "content": "File 3 content"})

    # Удаление директории
    response = client.delete(DELETE_URL, json={"path": "test_dir"})
    assert response.status_code == 200
    assert "test_dir" in response.json["message"]
    assert "associated records deleted successfully" in response.json["message"]

    # Проверка отсутствия файлов
    response = client.get(READ_URL, query_string={"path": "test_dir/file1.txt"})
    assert response.status_code == 404

    response = client.get(READ_URL, query_string={"path": "test_dir/file2.txt"})
    assert response.status_code == 404

    response = client.get(READ_URL, query_string={"path": "test_dir/sub_dir/file3.txt"})
    assert response.status_code == 404

    # Проверка отсутствия записей в базе данных\
    from app.models import ProjectFile
    with app.app_context():
        files = ProjectFile.query.filter(ProjectFile.path.like("test_dir/%")).all()
        assert len(files) == 0, f"Unexpected records in database: {files}"

def test_delete_directory_nonexistent(client):
    """
    Тест: попытка удалить несуществующую директорию.
    """
    response = client.delete(DELETE_URL, json={"path": "nonexistent_dir"})
    assert response.status_code == 404
    assert response.json["error"] == "Path 'nonexistent_dir' does not exist."


def test_delete_empty_directory(client):
    """
    Тест: успешное удаление пустой директории.
    """
    # Создание файла с тестовой директорией
    client.post(CREATE_URL, json={"path": "empty_dir/.keep", "content": ""})
    #Удаление файла и перевод директории в статус пустой
    client.delete(DELETE_URL, json={"path": "empty_dir/.keep"})

    # Удаление директории
    response = client.delete(DELETE_URL, json={"path": "empty_dir"})
    assert response.status_code == 200
    assert "empty_dir" in response.json["message"]
    assert "associated records deleted successfully" in response.json["message"]

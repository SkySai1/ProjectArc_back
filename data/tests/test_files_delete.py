CREATE_URL = "/files/create"
DELETE_URL = "/files/delete"
READ_URL = "/files/read"

def test_delete_file(client):
    """
    Тест: удаление существующего файла.
    """
    # Создание файла для теста
    client.post(CREATE_URL, json={
        "path": "test.txt",
        "content": "Hello, World!"
    })

    # Удаление файла
    response = client.post(DELETE_URL, json={"path": "test.txt"})
    assert response.status_code == 200
    assert response.json["message"] == "File 'test.txt' deleted successfully."

def test_delete_file_nonexistent(client):
    """
    Тест: удаление несуществующего файла.
    """
    response = client.post(DELETE_URL, json={"path": "nonexistent.txt"})
    assert response.status_code == 404
    assert response.json["error"] == "Path 'nonexistent.txt' does not exist."

def test_delete_file_not_in_db(client, app):
    """
    Тест: удаление файла, который отсутствует в базе данных, но существует физически.
    """
    from app import db
    from app.models import ProjectFile

    # Создаём физический файл без добавления в БД
    file_path = "test_not_in_db_file.txt"
    client.post(CREATE_URL, json={
        "path": file_path,
        "content": "This file exists only physically."
    })

    # Удаляем запись о файле из базы данных
    with app.app_context():
        file_record = ProjectFile.query.filter_by(path=file_path).first()
        if file_record:
            db.session.delete(file_record)
            db.session.commit()

    # Попытка удалить файл через API
    response = client.post(DELETE_URL, json={"path": file_path})

    assert response.status_code == 207
    response_data = response.json

    # Проверяем, что файл удалён физически, но был отмечен как отсутствующий в БД
    assert response_data["message"] == f"File '{file_path}' deleted, but not found in database."
    assert response_data["status"] == "not_in_db"

def test_delete_directory_success(client):
    """
    Тест: успешное рекурсивное удаление директории и всех её файлов.
    """
    # Создание файловой структуры
    client.post(CREATE_URL, json={"path": "test_dir/file1.txt", "content": "File 1 content"})
    client.post(CREATE_URL, json={"path": "test_dir/file2.txt", "content": "File 2 content"})
    client.post(CREATE_URL, json={"path": "test_dir/sub_dir/file3.txt", "content": "File 3 content"})

    # Удаление директории
    response = client.post(DELETE_URL, json={"path": "test_dir"})
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

def test_delete_directory_nonexistent(client):
    """
    Тест: попытка удалить несуществующую директорию.
    """
    response = client.post(DELETE_URL, json={"path": "nonexistent_dir"})
    assert response.status_code == 404
    assert response.json["error"] == "Path 'nonexistent_dir' does not exist."
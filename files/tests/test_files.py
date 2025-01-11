import pytest
from flask import Flask

BASE_URL = "/project_map"
CREATE_URL = "/create"


def test_create_file_missing_filename(client):
    """Тест: создание файла без 'filename'."""
    response = client.post(CREATE_URL, json={"content": "Test content"})
    assert response.status_code == 400
    assert response.json["error"] == "'filename' and 'content' are required."

def test_create_file_success(client):
    """Тест: успешное создание файла."""
    response = client.post(CREATE_URL, json={
        "filename": "test.txt",
        "content": "Hello, World!",
        "description": "Test file"
    })
    assert response.status_code == 201
    assert response.json["message"] == "File test.txt created successfully."

def test_delete_file(client):
    """Тест: удаление существующего файла."""
    # Создание файла для теста
    client.post(CREATE_URL, json={
        "filename": "test.txt",
        "content": "Hello, World!"
    })

    # Удаление файла
    response = client.post(BASE_URL, json={"path": "test.txt"})
    assert response.status_code == 200
    assert response.json["message"] == "File 'test.txt' deleted from project database."

def test_delete_file_nonexistent(client):
    """Тест: удаление несуществующего файла."""
    response = client.post(BASE_URL, json={"path": "nonexistent.txt"})
    assert response.status_code == 404
    assert response.json["error"] == "File 'nonexistent.txt' does not exist."

def test_update_file(client):
    """Тест: обновление описания файла."""
    # Создание файла для теста
    client.post(CREATE_URL, json={
        "filename": "test.txt",
        "content": "Hello, World!"
    })

    # Обновление описания файла
    response = client.put(BASE_URL, json={
        "path": "test.txt",
        "description": "Updated description"
    })
    assert response.status_code == 200
    assert response.json["message"] == "File test.txt information updated successfully."

def test_update_file_nonexistent(client):
    """Тест: обновление описания для несуществующего файла."""
    response = client.put(BASE_URL, json={
        "path": "nonexistent.txt",
        "description": "Updated description"
    })
    assert response.status_code == 404
    assert response.json["error"] == "File 'nonexistent.txt' does not exist."
TREE_URL = "/files/tree"


def test_tree_no_path(client):
    """
    Тест: получение структуры дерева без указания пути.
    """
    response = client.get(TREE_URL)
    assert response.status_code == 200
    assert "directory" in response.json
    assert "subdirectories" in response.json
    assert "files" in response.json


def test_tree_with_valid_path(client):
    """
    Тест: получение структуры дерева для указанной директории.
    """
    # Создание тестовой директории и файлов
    client.post("/files/create", json={"path": "test_dir/test_file1.txt", "content": "Content 1"})
    client.post("/files/create", json={"path": "test_dir/test_file2.txt", "content": "Content 2"})

    response = client.get(TREE_URL, query_string={"path": "test_dir"})
    assert response.status_code == 200
    assert response.json["directory"].endswith("test_dir")
    assert len(response.json["files"]) == 2


def test_tree_invalid_path(client):
    """
    Тест: ошибка при запросе для несуществующей директории.
    """
    response = client.get(TREE_URL, query_string={"path": "non_existent_dir"})
    assert response.status_code == 404
    assert "error" in response.json


def test_tree_with_depth(client):
    """
    Тест: проверка ограничения глубины анализа.
    """
    # Создание тестовой структуры
    client.post("/files/create", json={"path": "depth_test/level1/file1.txt", "content": "File 1"})
    client.post("/files/create", json={"path": "depth_test/level1/level2/file2.txt", "content": "File 2"})

    # Запрос с глубиной 1
    response = client.get(TREE_URL, query_string={"path": "depth_test", "depth": 1})
    assert response.status_code == 200
    assert response.json["directory"].endswith("depth_test")
    assert len(response.json["subdirectories"]) == 1  # Только level1
    assert len(response.json["files"]) == 0  # Нет файлов на первом уровне

    # Запрос с глубиной 2
    response = client.get(TREE_URL, query_string={"path": "depth_test", "depth": 2})
    assert response.status_code == 200
    assert len(response.json["subdirectories"]) == 2  # level2 внутри level1
    assert len(response.json["files"]) == 1  # file1.txt на уровне level1


def test_tree_with_excluded_dirs(client):
    """
    Тест: проверка исключения указанных директорий из результата.
    """
    # Создание тестовой структуры
    client.post("/files/create", json={"path": "exclude_test/dir1/file1.txt", "content": "File 1"})
    client.post("/files/create", json={"path": "exclude_test/dir2/file2.txt", "content": "File 2"})
    client.post("/files/create", json={"path": "exclude_test/dir3/file3.txt", "content": "File 3"})

    # Запрос с исключением dir2
    response = client.get(TREE_URL, query_string={
        "path": "exclude_test",
        "excluded_dirs": ["exclude_test/dir2"]
    })

    assert response.status_code == 200
    assert response.json["directory"].endswith("exclude_test")
    assert "exclude_test/dir2" not in response.json["subdirectories"]
    assert len(response.json["subdirectories"]) == 2  # Только dir1 и dir3


def test_tree_with_excluded_patterns(client):
    """
    Тест: проверка исключения директорий по паттернам.
    """
    # Создание тестовой структуры
    client.post("/files/create", json={"path": "pattern_test/dir1/__pycache__/file1.pyc", "content": "File 1"})
    client.post("/files/create", json={"path": "pattern_test/dir2/file2.txt", "content": "File 2"})
    client.post("/files/create", json={"path": "pattern_test/dir3/__pycache__/file3.pyc", "content": "File 3"})

    # Запрос с исключением __pycache__
    response = client.get(TREE_URL, query_string={
        "path": "pattern_test",
        "excluded_patterns": ["__pycache__"]
    })

    assert response.status_code == 200
    assert "pattern_test/dir1/__pycache__" not in response.json["subdirectories"]
    assert "pattern_test/dir3/__pycache__" not in response.json["subdirectories"]
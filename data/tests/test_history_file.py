def test_missing_history_file(client):
    """
    Тест: попытка получить историю при отсутствии файла истории.
    """
    response = client.get('/history')
    assert response.status_code == 404
    assert response.json['error'] == 'History log file does not exist.'

def test_empty_history_file_with_content(client, temp_test_dir):
    """
    Тест: попытка получить историю из пустого файла истории.
    """
    # Создаём пустой файл истории
    import os
    history_file = os.path.join(temp_test_dir, 'history_log.json')
    with open(history_file, 'w') as f:
        f.write('[]')

    # Проверяем, что история пуста
    response = client.get('/history')
    assert response.status_code == 200
    assert response.json == []
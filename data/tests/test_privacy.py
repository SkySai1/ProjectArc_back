def test_privacy_policy_default(client):
    """
    Тест: Политика конфиденциальности по умолчанию (английский).
    """
    response = client.get('/privacy/')
    assert response.status_code == 200
    assert "Privacy Policy" in response.data.decode('utf-8')

def test_privacy_policy_russian(client):
    """
    Тест: Политика конфиденциальности на русском языке.
    """
    response = client.get('/privacy/?lang=ru')
    assert response.status_code == 200
    assert "Политика конфиденциальности" in response.data.decode('utf-8')

def test_privacy_policy_german(client):
    """
    Тест: Политика конфиденциальности на немецком языке.
    """
    response = client.get('/privacy/?lang=de')
    assert response.status_code == 200
    assert "Datenschutz-Bestimmungen" in response.data.decode('utf-8')

def test_privacy_policy_french(client):
    """
    Тест: Политика конфиденциальности на французском языке.
    """
    response = client.get('/privacy/?lang=fr')
    assert response.status_code == 200
    assert "Politique de confidentialité" in response.data.decode('utf-8')

def test_privacy_policy_chinese(client):
    """
    Тест: Политика конфиденциальности на китайском языке.
    """
    response = client.get('/privacy/?lang=zh')
    assert response.status_code == 200
    assert "隐私政策" in response.data.decode('utf-8')

def test_privacy_policy_invalid_language(client):
    """
    Тест: Политика конфиденциальности с недопустимым параметром языка (по умолчанию — английский).
    """
    response = client.get('/privacy/?lang=invalid')
    assert response.status_code == 200
    assert "Privacy Policy" in response.data.decode('utf-8')


def test_privacy_api_require(non_headers_client):
    """
    Тест на срабатывание проверки API ключа
    """
    client = non_headers_client

    response = client.get('/privacy/')
    assert response.status_code == 401
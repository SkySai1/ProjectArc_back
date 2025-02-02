import os
import logging

BASE_DIR = os.getenv("PROJECT_DIR", "project_data")

class Config:
    BASE_DIR = BASE_DIR
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.abspath(os.path.join(BASE_DIR, 'project_map.db'))}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    API_KEY = os.getenv("API_KEY", "default_secret_api_key")  # API-ключ из переменной окружения
    API_HEADER = os.getenv("API_HEADER", "Authorization") 

class DevelopmentConfig(Config):
    """
    Конфигурация для среды разработки.
    """
    DEBUG = True

class ProductionConfig(Config):
    """
    Конфигурация для продакшена.
    """
    DEBUG = False

class TestingConfig(Config):
    """
    Конфигурация для тестирования.
    """
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"  # Используем базу данных в памяти для тестов

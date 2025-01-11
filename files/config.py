import os

BASE_DIR = os.getenv("PROJECT_DIR", "project_data")

class Config:
    BASE_DIR = BASE_DIR
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.abspath(os.path.join(BASE_DIR, 'project_map.db'))}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
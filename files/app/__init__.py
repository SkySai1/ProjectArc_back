from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project_map.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Импорт маршрутов
from app.routes.files import create_file, delete_file, update_file
from app.routes.project_map import get_project_map, delete_from_map, update_project_map
from app.routes.history import get_history, log_change
from app.routes.about import get_about, create_about, update_about
from app.routes.privacy import privacy_policy
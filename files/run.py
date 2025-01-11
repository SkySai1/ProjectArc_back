from app import app, db
from models import ProjectDescription, ChangeLog, ProjectMap

if __name__ == "__main__":
    app.run(debug=True)
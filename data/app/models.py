from app import db

class ProjectFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(255), nullable=False, unique=True)
    type = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255))
    size = db.Column(db.Integer, nullable=False)
    last_modified = db.Column(db.Integer, nullable=False)
from app import db

class ProjectDescription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

class ChangeLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text, nullable=False)
    affected_files = db.Column(db.Text, nullable=True)

class ProjectMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=True)
    size = db.Column(db.Integer, nullable=False)
    last_modified = db.Column(db.DateTime, nullable=False)

class ProjectFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(255), nullable=False, unique=True)
    type = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255))
    size = db.Column(db.Integer, nullable=False)
    last_modified = db.Column(db.Integer, nullable=False)
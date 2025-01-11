from flask import jsonify
from app import app

@app.route('/')
def index():
    return jsonify({"message": "Welcome to the GPT External Storage API!"})
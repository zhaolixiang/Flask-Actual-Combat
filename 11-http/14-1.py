from app import app
from flask import current_app

with app.app_context():
    print(current_app.name)


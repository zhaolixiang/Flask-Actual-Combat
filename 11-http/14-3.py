from app import app
from flask import request

with app.test_request_context('/hello'):
    print(request.method)


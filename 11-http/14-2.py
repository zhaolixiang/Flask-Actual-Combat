from app import app
from flask import current_app

app_ctx=app.app_context()
app_ctx.push()
print(current_app.name)
app_ctx.pop()


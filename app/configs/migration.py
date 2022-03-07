from flask import Flask
from flask_migrate import Migrate

def init_app(app: Flask):
    Migrate(app, app.db)
    from app.models.user_model import UserModel
from flask import Flask
from app.routes.user_route import bp_users

def init_app(app: Flask):

    app.register_blueprint(bp_users)
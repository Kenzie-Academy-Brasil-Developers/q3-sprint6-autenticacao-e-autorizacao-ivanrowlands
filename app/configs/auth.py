from flask_httpauth import HTTPTokenAuth
from app.models.user_model import UserModel

auth = HTTPTokenAuth()

@auth.verify_token
def verify(api_key: str):
    user = UserModel.query.filter(UserModel.api_key == api_key).first()

    return user 
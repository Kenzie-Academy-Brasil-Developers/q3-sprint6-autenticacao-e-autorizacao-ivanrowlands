from flask import request, current_app, jsonify
from app.models.user_model import UserModel
from secrets import token_urlsafe
from sqlalchemy.exc import IntegrityError
from app.configs.auth import auth
from werkzeug.exceptions import Unauthorized

def create_user():
    try: 
        user_data = request.get_json()
        user_data["api_key"] = token_urlsafe(16)

        new_user = UserModel(**user_data)

        current_app.db.session.add(new_user)
        current_app.db.session.commit()

        return jsonify({
            "name": new_user.name,
            "last_name": new_user.last_name,
            "email": new_user.email
        }), 201
    except IntegrityError:
        return jsonify({"msg": "Email already exists"}), 409

def signin():
    user_data = request.get_json()

    found_user= UserModel.query.filter(UserModel.email==user_data["email"]).first()

    if not found_user:
        return jsonify({"msg": "email not registered"}), 404

    if found_user.check_password(user_data["password"]):
        return jsonify({"api_key": found_user.api_key}), 200

    return jsonify({"msg": "user not found"}), 404

@auth.login_required()
def get_user():
    api_key = request.headers["Authorization"].split()[1]
    user = UserModel.query.filter_by(api_key = api_key).first()

    return jsonify({
        "name": user.name,
        "last_name": user.last_name,
        "email": user.email
    }), 200

@auth.login_required()
def update_user():
    data = request.get_json()
    api_key = request.headers["Authorization"].split()[1]

    user = UserModel.query.filter_by(api_key = api_key).first()

    for key, value in data.items():
        setattr(user, key, value)

    current_app.db.session.add(user)
    current_app.db.session.commit()

    return jsonify({
        "name": user.name,
        "last_name": user.last_name,
        "email": user.email
    }), 200

@auth.login_required()
def delete_user():
    api_key = request.headers["Authorization"].split()[1]

    user = UserModel.query.filter_by(api_key = api_key).first()

    current_app.db.session.delete(user)
    current_app.db.session.commit()

    return jsonify({"msg": f"User {user.name} has been deleted"}), 200 
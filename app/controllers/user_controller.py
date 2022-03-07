from flask import request, current_app, jsonify
from app.models.user_model import UserModel
from secrets import token_urlsafe
from sqlalchemy.exc import IntegrityError
from app.configs.auth import auth
import email
from flask_jwt_extended import create_access_token, jwt_required, decode_token

def create_user():
    try: 
        user_data = request.get_json()

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
        token = create_access_token(found_user)
        return jsonify({"access_token": token}), 200
    
    return jsonify({"msg": "user not found"}), 404

@jwt_required()
def get_user():
    token = request.headers["Authorization"].split()[1]
    user = decode_token(token)["sub"]

    return jsonify({
        "name": user["name"],
        "last_name": user["last_name"],
        "email": user["email"]
    }), 200

@jwt_required()
def update_user():
    data = request.get_json()
    token = request.headers["Authorization"].split()[1]
    email = decode_token(token)["sub"]["email"]

    user = UserModel.query.filter_by(email = email).first()

    for key, value in data.items():
        setattr(user, key, value)

    current_app.db.session.add(user)
    current_app.db.session.commit()

    return jsonify({
        "name": user.name,
        "last_name": user.last_name,
        "email": user.email
    }), 200

@jwt_required()
def delete_user():
    token = request.headers["Authorization"].split()[1]
    email = decode_token(token)["sub"]["email"]
    user = UserModel.query.filter_by(email = email).first()

    current_app.db.session.delete(user)
    current_app.db.session.commit()

    return jsonify({"msg": f"User {user.name} has been deleted"}), 200
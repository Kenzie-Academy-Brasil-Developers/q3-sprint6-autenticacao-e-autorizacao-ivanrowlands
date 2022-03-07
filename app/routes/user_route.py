from flask import Blueprint

from app.controllers.user_controller import create_user, signin, get_user, update_user, delete_user

bp_users = Blueprint("bp_users", __name__, url_prefix="/api")

bp_users.post("/signup")(create_user)
bp_users.post("/signin")(signin)
bp_users.get("")(get_user)
bp_users.put("")(update_user)
bp_users.delete("")(delete_user)
from flask import Blueprint
from app.controllers import user_controller

bp = Blueprint("api", __name__, url_prefix="/api")

bp.get("/")(user_controller.get_user)
bp.put("/")(user_controller.put_user)
bp.delete("/")(user_controller.delete_user)
bp.post("/signin")(user_controller.sigin)
bp.post("/signup")(user_controller.signup)

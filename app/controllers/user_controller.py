import copy
import secrets
from http import HTTPStatus

from app.configs.auth import auth
from app.configs.database import db
from app.decorators import validate_keys
from app.models.user_model import UserModel
from flask import jsonify, request
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.session import Session

keys = ["name", "last_name", "email", "password"]
signin_keys = ["email", "password"]


@validate_keys(signin_keys)
def sigin():
    data = request.get_json()
    session: Session = db.session

    user: UserModel = session.query(UserModel).filter_by(email=data["email"]).first()

    if not user or not user.verify_password(data["password"]):
        return {"detail": "email and password missmatch"}, HTTPStatus.UNAUTHORIZED

    return {"api_key": "{}".format(user.api_key)}, HTTPStatus.OK


@validate_keys(keys)
def signup():
    data = request.get_json()
    session: Session = db.session

    data["api_key"] = secrets.token_urlsafe(32)

    try:
        user: UserModel = UserModel(**data)

        session.add(user)
        session.commit()

        [data.pop(k) for k in ("password", "api_key")]

        return jsonify(data), HTTPStatus.CREATED
    except IntegrityError:
        session.rollback()

        return {"error": "user already exists!"}, HTTPStatus.CONFLICT
    finally:
        session.close()


@auth.login_required
def get_user():
    user: UserModel = auth.current_user()

    response = {"name": user.name, "last_name": user.last_name, "email": user.email}

    return response, HTTPStatus.OK


@auth.login_required
@validate_keys(keys, keys)
def put_user():
    data = request.get_json()
    session: Session = db.session

    user: UserModel = auth.current_user()

    for key, value in data.items():
        setattr(user, key, value)

    session.add(user)
    session.commit()

    response: UserModel = (
        session.query(UserModel.name, UserModel.last_name, UserModel.email)
        .filter_by(email=user.email)
        .first()
    )

    return dict(response), HTTPStatus.OK


@auth.login_required
def delete_user():
    session: Session = db.session

    current_user: UserModel = auth.current_user()

    user: UserModel = (
        session.query(UserModel).filter_by(email=current_user.email).first()
    )

    session.delete(user)
    session.commit()

    return {"msg": f"User {user.name} has been deleted."}, HTTPStatus.OK

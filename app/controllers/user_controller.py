from datetime import timedelta
from http import HTTPStatus

from flask import jsonify, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError
from sqlalchemy.orm.session import Session

from app.configs.database import db
from app.decorators import login_validates, register_validates, validates
from app.models.user_model import UserModel


@login_validates()
def sigin():
    data = request.get_json()
    session: Session = db.session

    user: UserModel = session.query(UserModel).filter_by(email=data["email"]).first()

    if not user or not user.verify_password(data["password"]):
        return {"detail": "email and password missmatch"}, HTTPStatus.UNAUTHORIZED

    token = create_access_token(user, expires_delta=timedelta(minutes=5))

    return {"access_token": "{}".format(token)}, HTTPStatus.OK


@register_validates()
def signup():
    data = request.get_json()
    session: Session = db.session

    try:
        user: UserModel = UserModel(**data)

        session.add(user)
        session.commit()

        return (
            {
                "id": user.id,
                "name": user.name,
                "last_name": user.last_name,
                "email": user.email,
                "password": user.password_hash,
            },
            HTTPStatus.CREATED,
        )
    except IntegrityError:
        session.rollback()
        return {"error": "user already exists!"}, HTTPStatus.CONFLICT
    finally:
        session.close()


@jwt_required()
def get_user():
    user: UserModel = get_jwt_identity()
    return jsonify(user), HTTPStatus.OK


@jwt_required()
@validates()
def put_user():
    data = request.get_json()
    session: Session = db.session

    current_user = get_jwt_identity()

    try:
        user: UserModel = (
            session.query(UserModel).filter_by(email=current_user["email"]).first()
        )

        for key, value in data.items():
            setattr(user, key, value)

        session.add(user)
        session.commit()

        return jsonify(user), HTTPStatus.OK
    except IntegrityError:
        session.rollback()
        return {"error": "user already exists!"}, HTTPStatus.CONFLICT
    finally:
        session.close()


@jwt_required()
def delete_user():
    session: Session = db.session

    current_user: UserModel = get_jwt_identity()

    try:
        user: UserModel = (
            session.query(UserModel).filter_by(email=current_user["email"]).first()
        )

        session.delete(user)
        session.commit()

        return {"msg": f"User {user.name} has been deleted."}, HTTPStatus.OK
    except UnmappedInstanceError:
        session.rollback()
        return {"error": "user not found"}, HTTPStatus.NOT_FOUND
    finally:
        session.close()

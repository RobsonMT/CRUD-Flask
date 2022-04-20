from app.configs.database import db
from app.models.user_model import UserModel
from flask_httpauth import HTTPTokenAuth
from sqlalchemy.orm.session import Session

auth = HTTPTokenAuth()


@auth.verify_token
def verify_token(api_key: str):
    session: Session = db.session

    user = session.query(UserModel).filter_by(api_key=api_key).first()

    return user

from functools import wraps
from http import HTTPStatus
from typing import Callable

from flask import request

from app.exceptions import MissingKeyError, WrongKeyError


def register_validates():
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            data = request.get_json()

            required_keys = ["name", "last_name", "email", "password"]

            wrong_key = set(data.keys()).difference(required_keys)
            missing_key = set(required_keys).difference(data.keys())

            try:
                if wrong_key:
                    raise WrongKeyError(
                        {
                            "accepted_keys": list(required_keys),
                            "wrong_key(s)": list(wrong_key),
                        }
                    )
                if missing_key:
                    raise MissingKeyError(
                        {
                            "required_keys": list(required_keys),
                            "missing_key(s)": list(missing_key),
                        }
                    )
                return func(*args, **kwargs)
            except (MissingKeyError, WrongKeyError) as e:
                return e.args[0], HTTPStatus.BAD_REQUEST

        return wrapper

    return decorator

from functools import wraps
from http import HTTPStatus
from typing import Callable

from flask import request

from app.exceptions import WrongKeyError


def validates():
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            data = request.get_json()

            keys = ["name", "last_name", "email", "password"]

            wrong_key = set(data.keys()).difference(keys)

            try:
                if wrong_key:
                    raise WrongKeyError(
                        {
                            "accepted_keys": list(keys),
                            "wrong_key(s)": list(wrong_key),
                        }
                    )

                return func(*args, **kwargs)
            except WrongKeyError as e:
                return e.args[0], HTTPStatus.BAD_REQUEST

        return wrapper

    return decorator

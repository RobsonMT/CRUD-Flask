from functools import wraps
from http import HTTPStatus
from typing import Callable

from flask import request


def validate_keys(required_keys: list[str], optional_keys: list[str] or str = False):

    """Validate if the key is wrong or missing.
    Parameters:
        argument1: type(`list[str]`):
        (keys required) -> A list of keys that will be checked in the request.
        argument2: type(`str` or `list[str]`), default(False):
        (keys not required) -> A string or list of keys that will be ignored if not passed.
        - If argument2 is not passed, all fields of argument1 will be considered mandatory.
    Returns:
        dict: Return value.
        - In case any key has a syntax error:
            {
                "available_keys": [
                    "name",
                    "description"
                ],
                "wrong_keys_sended": [
                    "naaame"
                ]
            }
        - If any mandatory key is missing:
            {
                "available_keys": [
                    "name",
                    "description"
                ],
                "missing_key(s)": [
                    "name"
                ]
            }
    """

    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            data = request.get_json()

            missing_keys = set(required_keys).difference(data.keys())

            if optional_keys:
                missing_keys = [
                    key
                    for key in set(required_keys).difference(optional_keys)
                    if key not in data.keys()
                ]

            if type(optional_keys) == str:
                missing_keys = [
                    key
                    for key in set(required_keys).difference([optional_keys])
                    if key not in data.keys()
                ]

            wrong_keys = set(data.keys()).difference(required_keys)

            try:
                if wrong_keys:
                    raise KeyError(
                        {
                            "required_keys": list(required_keys),
                            "wrong_key(s)_sended": list(wrong_keys),
                        }
                    )
                if missing_keys:
                    raise KeyError(
                        {
                            "required_keys": list(required_keys),
                            "missing_key(s)": list(missing_keys),
                        }
                    )
                return func(*args, **kwargs)
            except (KeyError, TypeError) as e:
                return e.args[0], HTTPStatus.BAD_REQUEST

        return wrapper

    return decorator

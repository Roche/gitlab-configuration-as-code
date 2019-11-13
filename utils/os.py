import os

from . import strings


def get_env_or_else(env, default=None):
    if isinstance(env, list):
        for val in env:
            value = os.getenv(val)
            if strings.is_not_blank(value):
                return value

    if isinstance(env, str):
        return os.getenv(env, default)

    return default

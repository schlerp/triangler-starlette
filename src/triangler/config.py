import os
from typing import TypeVar

_T = TypeVar("_T", bound=str | int)


def ensure_value_set(env_var: str, value: _T | None) -> _T:
    """
    Ensure that an environment variable is set. If the environment variable is not set, raise a
    ValueError.

    :param env_var: The environment variable to check.
    """
    if value is None:
        raise ValueError(f"{env_var} is not set")

    return value


def get_bool_from_env(env_var: str, default: bool | None = None) -> bool | None:
    """
    Get a boolean value from an environment variable. If the environment variable is not set,
    return the default.

    :param env_var: The environment variable to get the boolean value from.
    :param default: The default value to return if the environment variable is not set.
    :return: The boolean value of the environment variable or the default.
    """

    value = os.environ.get(env_var, "false").lower() in ("true", "t", "1", "yes", "y")

    if env_var not in os.environ:
        return default

    return value


def get_str_from_env(env_var: str, default: str | None = None) -> str | None:
    """
    Get a string value from an environment variable. If the environment variable is not set,
    return the default.

    :param env_var: The environment variable to get the string value from.
    :param default: The default value to return if the environment variable is not set.
    :return: The string value of the environment variable or the default.
    """

    value = os.environ.get(env_var)

    if env_var not in os.environ:
        return default

    return value


def get_mandatory_bool_from_env(env_var: str, default: bool | None = None) -> bool:
    """
    Get a mandatory boolean value from an environment variable.

    If the environment variable is not set, raise a ValueError.

    :param env_var: The environment variable to get the string value from.
    :return: The string value of the environment variable.
    """

    value = get_bool_from_env(env_var, default)

    return ensure_value_set(env_var, value)


def get_mandatory_str_from_env(env_var: str, default: str | None = None) -> str:
    """
    Get a mandatory string value from an environment variable.

    If the environment variable is not set, raise a ValueError.

    :param env_var: The environment variable to get the integer value from.
    :return: The integer value of the environment variable.
    """

    value = get_str_from_env(env_var, default=default)

    return ensure_value_set(env_var, value)


DEBUG = get_bool_from_env("DEBUG", False)

SQLALCHEMY_DATABASE_URL = get_mandatory_str_from_env(
    "SQLALCHEMY_DATABASE_URL", default="sqlite:///./triangler.db"
)

SECRET_KEY = get_mandatory_str_from_env("SECRET_KEY", "secret")

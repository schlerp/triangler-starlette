import os


def get_bool_from_env(env_var: str, default: bool | None = None) -> bool | None:
    """
    Get a boolean value from an environment variable. If the environment variable is not set,
    return the default.


    :param env_var: The environment variable to get the boolean value from.
    :param default: The default value to return if the environment variable is not set.
    :return: The boolean value of the environment variable or the default.
    """
    if env_var not in os.environ:
        return default
    return os.environ.get(env_var, "false").lower() in ("true", "t", "1", "yes", "y")


def get_str_from_env(env_var: str, default: str | None = None) -> str | None:
    if env_var not in os.environ:
        return default
    return os.environ.get(env_var)


DEBUG = get_bool_from_env("DEBUG", False)

SECRET_KEY = get_str_from_env("SECRET_KEY", "secret")

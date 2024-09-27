from typing import Callable, TypeVar
from unittest import mock

import pytest

from triangler import config

AnyTestMethod = Callable[..., None]

_CONFIG_NAMES_WITH_TESTS: set[str] = set()

C = TypeVar("C", bound=AnyTestMethod)

_ALL_CONFIG_VAR_NAMES: set[str] = set(
    name for name in dir(config) if name.isupper() and not name.startswith("_")
)


def register_config_name(config_name: str) -> Callable[[C], C]:
    def decorator(func: C) -> C:
        _CONFIG_NAMES_WITH_TESTS.add(config_name)
        return func

    return decorator


class TestConfig:
    @pytest.mark.parametrize(
        ["config_name", "env_value", "expected_boolean"],
        (
            ("TEST_VARIABLE", "true", True),
            ("TEST_VARIABLE", "t", True),
            ("TEST_VARIABLE", "yes", True),
            ("TEST_VARIABLE", "y", True),
            ("TEST_VARIABLE", "1", True),
            ("TEST_VARIABLE", "some other value", False),
            ("TEST_VARIABLE", "false", False),
            ("TEST_VARIABLE", "", False),
        ),
    )
    def test_get_bool_from_env(
        self, config_name: str, env_value: str, expected_boolean: bool
    ) -> None:
        with mock.patch.dict("os.environ", {config_name: env_value}):
            assert config.get_bool_from_env(config_name) is expected_boolean

    @pytest.mark.parametrize("config_name", _ALL_CONFIG_VAR_NAMES)
    def test_config_value_has_test(self, config_name: str) -> None:
        assert config_name in _CONFIG_NAMES_WITH_TESTS

    @register_config_name(config_name="DEBUG")
    def test_debug_default(self) -> None:
        assert config.DEBUG is False

    @register_config_name(config_name="SECRET_KEY")
    def test_secret_key_default(self) -> None:
        assert config.SECRET_KEY == "secret"

    @register_config_name(config_name="SQLALCHEMY_DATABASE_URL")
    def test_sqlalchemy_database_url_default(self) -> None:
        assert config.SQLALCHEMY_DATABASE_URL == "sqlite:///./triangler.db"

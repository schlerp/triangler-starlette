from unittest import mock

from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from triangler.data import persistence


class TestPersistence:
    @mock.patch("os.environ", {"SQLALCHEMY_DATABASE_URL": "sqlite:///:memory:"})
    def test_get_engine(self) -> None:
        engine = persistence.get_engine()

        assert engine is not None
        assert isinstance(engine, Engine)

    @mock.patch("os.environ", {"SQLALCHEMY_DATABASE_URL": "sqlite:///:memory:"})
    def test_get_db_session(self) -> None:
        with persistence.get_db_session() as session:
            assert session is not None
            assert isinstance(session, Session)

from collections.abc import Generator
from contextlib import contextmanager

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import Engine
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import declarative_base

from triangler import config

Base: DeclarativeBase = declarative_base()


def get_engine() -> Engine:
    """Get a SQLAlchemy engine for the configured database."""
    connection_args = {}
    if config.SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
        connection_args["check_same_thread"] = False

    return create_engine(config.SQLALCHEMY_DATABASE_URL, connect_args=connection_args)


@contextmanager
def get_db_session() -> Generator[Session, None, None]:
    engine = get_engine()
    factory = sessionmaker(engine, expire_on_commit=False)
    with factory() as session:
        try:
            yield session
            session.commit()
        except SQLAlchemyError as error:
            session.rollback()
            raise error
        finally:
            session.close()

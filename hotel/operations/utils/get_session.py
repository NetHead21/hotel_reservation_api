from sqlmodel import Session
from hotel.database.database_engine import engine


def get_session() -> Session:
    session = Session(engine)
    try:
        return session
    finally:
        session.close()


def with_session(func) -> any:
    def wrapper(*args, **kwargs):
        with get_session() as session:
            return func(session, *args, **kwargs)

    return wrapper

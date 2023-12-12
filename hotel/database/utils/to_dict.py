from sqlmodel import SQLModel


def to_dict(obj: SQLModel) -> dict:
    return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}

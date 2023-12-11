from fastapi import HTTPException
from sqlmodel import Session


def get_or_404(session: Session, model: object, identifier: int) -> object | str:
    instance = session.get(model, identifier)
    if instance is None:
        raise HTTPException(status_code=404, detail=f"{model.__name__} not found")
    return instance

from typing import Any
from sqlmodel import SQLModel, Session, select

from hotel.database.models import Customer
from hotel.database.utils.delete_message import get_delete_message
from hotel.database.utils.get_or_404 import get_or_404
from hotel.database.utils.get_session import get_session
from hotel.database.utils.to_dict import to_dict

DataObject = dict[str, Any]


class DatabaseInterface:
    def __init__(self, db_class: type[SQLModel]):
        self.db_class = db_class

    def read_by_id(self, id: int) -> DataObject | str:
        session: Session = get_session()
        return get_or_404(session, self.db_class, id)

    def read_all(self) -> list[DataObject]:
        session: Session = get_session()
        result = select(self.db_class)
        return [to_dict(r) for r in session.exec(result).all()]

    def create(self, data: DataObject) -> DataObject:
        session: Session = get_session()
        result = self.db_class(**data)
        session.add(result)
        session.commit()
        session.refresh(result)
        return to_dict(result)

    def update(self, id: int, data: DataObject) -> DataObject | str:
        session: Session = get_session()
        result = get_or_404(session, self.db_class, id)

        for key, value in data.items():
            setattr(result, key, value)

        session.commit()
        session.refresh(result)
        return to_dict(result)

    def delete(self, id: int) -> DataObject:
        session: Session = get_session()
        result = get_or_404(session, self.db_class, id)
        session.delete(result)
        session.commit()
        return get_delete_message(Customer)

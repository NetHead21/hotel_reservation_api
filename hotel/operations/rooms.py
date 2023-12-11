from sqlmodel import Session, select
from hotel.database.models import Room
from hotel.operations.utils.get_session import with_session
from hotel.operations.utils.get_or_404 import get_or_404


@with_session
def get_rooms(session: Session):
    statement = select(Room)
    return session.exec(statement).all()


@with_session
def get_room(session: Session, room_id: int):
    return get_or_404(session, Room, room_id)

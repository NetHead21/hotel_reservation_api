from typing import Type, List, Any

from fastapi import HTTPException
from sqlmodel import Session, select
from hotel.database.models import Booking, Room
from hotel.operations.utils.delete_message import get_delete_message
from hotel.operations.utils.get_or_404 import get_or_404
from hotel.operations.utils.get_session import with_session
from hotel.operations.models import BookingCreateData, BookingResult
from hotel.operations.utils.to_dict import to_dict


def get_room_price(booking_data, session) -> int | str:
    room = get_or_404(session, Room, booking_data.room_id)
    return room.price


def compute_days(booking_data) -> int:
    return (booking_data.to_date - booking_data.from_date).days


@with_session
def get_bookings(session: Session) -> List[BookingResult]:
    statement = select(Booking)
    return [BookingResult(**to_dict(b)) for b in session.exec(statement).all()]


@with_session
def get_booking(session: Session, booking_id: int) -> BookingResult | str:
    return get_or_404(session, Booking, booking_id)


@with_session
def create_booking(
    session: Session, booking_data: BookingCreateData
) -> BookingResult | str:
    room_price = get_room_price(booking_data, session)
    days = compute_days(booking_data)
    if days <= 0:
        raise HTTPException(status_code=404, detail="Invalid Dates")

    new_booking = Booking(**booking_data.dict(), price=room_price * days)
    session.add(new_booking)
    session.commit()
    session.refresh(new_booking)
    return BookingResult(**to_dict(new_booking))


# @with_session
# def update_booking(
#     session: Session, booking_id: int, updated_booking: BookingCreateData
# ):
#     booking = get_or_404(session, Booking, booking_id)
#     room_price = get_room_price(updated_booking, session)
#     days = compute_days(updated_booking)
#     if days <= 0:
#         raise HTTPException(status_code=404, detail="Invalid Dates")
#
#     updated_booking["price"] = room_price * days
#
#     for key, value in updated_booking.dict(exclude_unset=True).items():
#         setattr(booking, key, value)
#
#     session.commit()
#     session.refresh(booking)
#     return updated_booking


@with_session
def delete_booking(session: Session, booking_id: int) -> dict:
    booking = get_or_404(session, Booking, booking_id)
    session.delete(booking)
    session.commit()
    return get_delete_message(Booking)

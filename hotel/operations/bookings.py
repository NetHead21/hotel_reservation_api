from typing import List
from fastapi import HTTPException
from hotel.database.models import Booking
from hotel.operations.interface import DataInterface, DataObject
from hotel.operations.models import BookingCreateData
from hotel.database.utils.to_dict import to_dict


def get_room_price(room: dict) -> int:
    return room.price


def compute_days(booking_data) -> int:
    return (booking_data.to_date - booking_data.from_date).days


def get_bookings(booking_interface: DataInterface) -> List[DataObject]:
    return booking_interface.read_all()


def get_booking(booking_id: int, booking_interface: DataInterface) -> DataObject | str:
    return booking_interface.read_by_id(booking_id)


def create_booking(
    booking_data: BookingCreateData,
    booking_interface: DataInterface,
    room_interface: DataInterface,
) -> DataObject | str:
    room_price = get_room_price(room_interface.read_by_id(booking_data.room_id))
    days = compute_days(booking_data)
    if days <= 0:
        raise HTTPException(status_code=404, detail="Invalid Dates")

    new_booking = Booking(**booking_data.dict(), price=room_price * days)
    return booking_interface.create(to_dict(new_booking))


def delete_booking(booking_id: int, booking_interface: DataInterface) -> DataObject:
    return booking_interface.delete(booking_id)

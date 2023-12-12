from typing import List
from fastapi import APIRouter

from hotel.database.database_interface import DatabaseInterface, DataObject
from hotel.database.models import Booking, Room
from hotel.operations.bookings import (
    get_booking,
    get_bookings,
    create_booking,
    delete_booking,
)
from hotel.operations.models import BookingCreateData, BookingResult

router = APIRouter()


@router.get("/bookings", response_model=List[BookingResult])
def api_get_bookings():
    booking_interface = DatabaseInterface(Booking)
    return get_bookings(booking_interface)


@router.get("/bookings/{booking_id}", response_model=BookingResult | str)
def api_get_booking(booking_id: int) -> DataObject | str:
    booking_interface = DatabaseInterface(Booking)
    return get_booking(booking_id, booking_interface)


@router.post("/bookings", response_model=BookingResult, status_code=201)
def api_create_booking(booking: BookingCreateData) -> DataObject:
    booking_interface = DatabaseInterface(Booking)
    room_interface = DatabaseInterface(Room)
    return create_booking(booking, booking_interface, room_interface)


@router.delete("/bookings/{booking_id}", response_model=dict)
def api_delete_booking(booking_id: int) -> DataObject | str:
    booking_interface = DatabaseInterface(Booking)
    return delete_booking(booking_id, booking_interface)

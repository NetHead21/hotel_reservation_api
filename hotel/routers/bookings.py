from typing import List
from fastapi import APIRouter
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
    return get_bookings()


@router.get("/bookings/{booking_id}", response_model=BookingResult | str)
def api_get_booking(booking_id: int):
    return get_booking(booking_id)


@router.post("/bookings", response_model=BookingResult, status_code=201)
def api_create_booking(booking: BookingCreateData) -> BookingResult:
    return create_booking(booking)


# @router.put("/bookings/{booking_id}", response_model=BookingResult | str)
# def api_update_booking(
#     booking_id: int, booking: BookingCreateData
# ) -> BookingResult | str:
#     return update_booking(booking_id, booking)


@router.delete("/bookings/{booking_id}", response_model=dict)
def api_delete_booking(booking_id: int) -> dict:
    return delete_booking(booking_id)

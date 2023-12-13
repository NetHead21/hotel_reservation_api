import pytest
from datetime import date
from fastapi import HTTPException
from hotel.operations.bookings import create_booking
from hotel.operations.interface import DataInterface
from hotel.operations.models import BookingCreateData
from hotel.database.models import Booking


# Mocks for DataInterface and DataObject
class MockDataInterface(DataInterface):
    def create(self, data):
        return data  # Mocking the creation process

    def read_by_id(self, id):
        return {"id": id, "price": 100}  # Mocking room data retrieval


class MockDataObject:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


# Helper functions
def get_room_price(room_data):
    return room_data["price"]


def compute_days(booking_data):
    return (booking_data.end_date - booking_data.start_date).days


# Parametrized test cases
@pytest.mark.parametrize(
    "booking_data, expected_price, test_id",
    [
        (
            BookingCreateData(
                room_id=1, start_date=date(2023, 4, 10), end_date=date(2023, 4, 15)
            ),
            500,
            "happy_path_5_days",
        ),
        (
            BookingCreateData(
                room_id=2, start_date=date(2023, 5, 1), end_date=date(2023, 5, 3)
            ),
            200,
            "happy_path_2_days",
        ),
        (
            BookingCreateData(
                room_id=3, start_date=date(2023, 6, 20), end_date=date(2023, 6, 25)
            ),
            500,
            "happy_path_5_days_different_room",
        ),
    ],
)
def test_create_booking_happy_path(booking_data, expected_price, test_id):
    # Arrange
    booking_interface = MockDataInterface()
    room_interface = MockDataInterface()

    # Act
    result = create_booking(booking_data, booking_interface, room_interface)

    # Assert
    assert isinstance(result, dict)
    assert result["price"] == expected_price


@pytest.mark.parametrize(
    "booking_data, test_id",
    [
        (
            BookingCreateData(
                room_id=1, start_date=date(2023, 4, 15), end_date=date(2023, 4, 10)
            ),
            "error_case_invalid_dates",
        ),
        (
            BookingCreateData(
                room_id=1, start_date=date(2023, 4, 10), end_date=date(2023, 4, 10)
            ),
            "error_case_same_day",
        ),
    ],
)
def test_create_booking_error_cases(booking_data, test_id):
    # Arrange
    booking_interface = MockDataInterface()
    room_interface = MockDataInterface()

    # Act & Assert
    with pytest.raises(HTTPException) as exc_info:
        create_booking(booking_data, booking_interface, room_interface)
    assert exc_info.value.status_code == 404
    assert "Invalid Dates" in str(exc_info.value.detail)

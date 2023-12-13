import pytest
from hotel.operations.interface import DataInterface, DataObject
from hotel.operations.bookings import get_booking


# Mock classes for DataInterface and DataObject
class MockDataInterface(DataInterface):
    def read_by_id(self, booking_id: int) -> DataObject | str:
        if booking_id == 0:
            return "No booking found"
        elif booking_id < 0:
            raise ValueError("Invalid booking ID")
        else:
            return MockDataObject(booking_id)


class MockDataObject(DataObject):
    def __init__(self, booking_id: int):
        self.booking_id = booking_id


# Parametrized test cases
@pytest.mark.parametrize(
    "booking_id, expected",
    [
        (1, MockDataObject(1)),  # TC1: Happy path with valid booking ID
        (2, MockDataObject(2)),  # TC2: Happy path with another valid booking ID
        (
            0,
            "No booking found",
        ),  # TC3: Edge case with booking ID that leads to no booking found
        # TC4: Error case with negative booking ID
        pytest.param(
            -1,
            ValueError("Invalid booking ID"),
            marks=pytest.mark.xfail(raises=ValueError),
        ),
    ],
    ids=[
        "happy-path-valid-1",
        "happy-path-valid-2",
        "edge-case-no-booking",
        "error-case-negative-id",
    ],
)
def test_get_booking(booking_id, expected):
    # Arrange
    booking_interface = MockDataInterface()

    # Act
    result = get_booking(booking_id, booking_interface)

    # Assert
    assert result == expected

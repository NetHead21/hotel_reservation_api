import pytest
from unittest.mock import MagicMock
from hotel.operations.interface import DataInterface, DataObject
from hotel.operations.bookings import delete_booking


# Mock DataObject for successful deletion
class MockSuccessDataObject(DataObject):
    def __init__(self, deleted: bool):
        self.deleted = deleted

    def is_deleted(self):
        return self.deleted


# Mock DataObject for failure in deletion
class MockFailureDataObject(DataObject):
    def __init__(self, error: str):
        self.error = error

    def get_error(self):
        return self.error


@pytest.mark.parametrize(
    "booking_id, expected_result, test_id",
    [
        (1, MockSuccessDataObject(True), "happy_path_1"),
        (999, MockSuccessDataObject(True), "happy_path_999"),
        (0, MockFailureDataObject("Invalid ID"), "edge_case_zero_id"),
        (-1, MockFailureDataObject("Invalid ID"), "edge_case_negative_id"),
        (None, TypeError("booking_id must be an integer"), "error_case_none_id"),
    ],
)
def test_delete_booking(booking_id, expected_result, test_id):
    # Arrange
    mock_interface = MagicMock(spec=DataInterface)
    if isinstance(expected_result, DataObject):
        mock_interface.delete.return_value = expected_result
    else:
        mock_interface.delete.side_effect = expected_result

    # Act
    if isinstance(expected_result, Exception):
        with pytest.raises(type(expected_result)) as exc_info:
            result = delete_booking(booking_id, mock_interface)
        # Assert
        assert str(exc_info.value) == str(expected_result)
    else:
        result = delete_booking(booking_id, mock_interface)
        # Assert
        assert result == expected_result

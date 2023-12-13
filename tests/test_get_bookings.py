import pytest
from unittest.mock import Mock
from hotel.operations.interface import DataInterface, DataObject
from hotel.operations.bookings import get_bookings


# Mock DataObject for testing purposes
class MockDataObject(DataObject):
    def __init__(self, data):
        self.data = data


# Parametrized test for happy path scenarios
@pytest.mark.parametrize(
    "test_id, mock_return_value, expected_result",
    [
        (
            "happy_path_single",
            [MockDataObject(data={"id": 1, "guest": "John Doe"})],
            [{"id": 1, "guest": "John Doe"}],
        ),
        (
            "happy_path_multiple",
            [
                MockDataObject(data={"id": 1, "guest": "John Doe"}),
                MockDataObject(data={"id": 2, "guest": "Jane Smith"}),
            ],
            [{"id": 1, "guest": "John Doe"}, {"id": 2, "guest": "Jane Smith"}],
        ),
        ("happy_path_empty", [], []),
    ],
    ids=str,
)
def test_get_bookings_happy_path(test_id, mock_return_value, expected_result):
    # Arrange
    mock_interface = Mock(spec=DataInterface)
    mock_interface.read_all.return_value = mock_return_value

    # Act
    result = get_bookings(mock_interface)

    # Assert
    assert result == expected_result
    mock_interface.read_all.assert_called_once()


# Parametrized test for edge cases
@pytest.mark.parametrize(
    "test_id, mock_return_value, expected_result",
    [
        (
            "edge_case_large_dataset",
            [MockDataObject(data={"id": i, "guest": f"Guest{i}"}) for i in range(1000)],
            [{"id": i, "guest": f"Guest{i}"} for i in range(1000)],
        ),
    ],
    ids=str,
)
def test_get_bookings_edge_cases(test_id, mock_return_value, expected_result):
    # Arrange
    mock_interface = Mock(spec=DataInterface)
    mock_interface.read_all.return_value = mock_return_value

    # Act
    result = get_bookings(mock_interface)

    # Assert
    assert result == expected_result
    mock_interface.read_all.assert_called_once()


# Parametrized test for error cases
@pytest.mark.parametrize(
    "test_id, exception",
    [
        ("error_interface_method_not_implemented", NotImplementedError),
        ("error_interface_returns_none", TypeError),
    ],
    ids=str,
)
def test_get_bookings_error_cases(test_id, exception):
    # Arrange
    mock_interface = Mock(spec=DataInterface)
    mock_interface.read_all.side_effect = exception

    # Act & Assert
    with pytest.raises(exception):
        get_bookings(mock_interface)
    mock_interface.read_all.assert_called_once()

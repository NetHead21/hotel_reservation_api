import pytest
from unittest.mock import MagicMock
from hotel.operations.interface import DataInterface, DataObject
from hotel.operations.customers import get_customers


# Mock DataObject for testing purposes
class MockDataObject(DataObject):
    def __init__(self, data):
        self.data = data


# Parametrized test for happy path scenarios
@pytest.mark.parametrize(
    "test_id, customer_data, expected_result",
    [
        (
            "happy-1",
            [MockDataObject({"id": 1, "name": "Alice"})],
            [{"id": 1, "name": "Alice"}],
        ),
        ("happy-2", [], []),
        (
            "happy-3",
            [
                MockDataObject({"id": 2, "name": "Bob"}),
                MockDataObject({"id": 3, "name": "Charlie"}),
            ],
            [{"id": 2, "name": "Bob"}, {"id": 3, "name": "Charlie"}],
        ),
    ],
)
def test_get_customers_happy_path(test_id, customer_data, expected_result):
    # Arrange
    mock_interface = MagicMock(spec=DataInterface)
    mock_interface.read_all.return_value = customer_data

    # Act
    result = get_customers(mock_interface)

    # Assert
    assert result == expected_result, f"Failed test ID: {test_id}"


# Parametrized test for edge cases
@pytest.mark.parametrize(
    "test_id, customer_data, expected_exception",
    [
        ("edge-1", Exception("Database error"), Exception),
        ("edge-2", TypeError("Invalid data type"), TypeError),
    ],
)
def test_get_customers_edge_cases(test_id, customer_data, expected_exception):
    # Arrange
    mock_interface = MagicMock(spec=DataInterface)
    mock_interface.read_all.side_effect = customer_data

    # Act / Assert
    with pytest.raises(expected_exception):
        get_customers(mock_interface)


# Parametrized test for error cases
@pytest.mark.parametrize(
    "test_id, customer_interface, expected_exception",
    [
        ("error-1", None, AttributeError),
        ("error-2", "not an interface", AttributeError),
    ],
)
def test_get_customers_error_cases(test_id, customer_interface, expected_exception):
    # Act / Assert
    with pytest.raises(expected_exception):
        get_customers(customer_interface)

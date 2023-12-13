import pytest
from hotel.operations.interface import DataInterface, DataObject
from hotel.operations.customers import get_customer
from unittest.mock import MagicMock


# Mock classes for DataInterface and DataObject
class MockDataInterface(DataInterface):
    def read_by_id(self, customer_id: int) -> DataObject | str:
        pass


class MockDataObject(DataObject):
    pass


# Parametrized test for happy path scenarios
@pytest.mark.parametrize(
    "customer_id, expected_result, test_id",
    [
        (1, MockDataObject(), "happy_path_1"),
        (2, MockDataObject(), "happy_path_2"),
        (100, MockDataObject(), "happy_path_100"),
    ],
)
def test_get_customer_happy_path(customer_id, expected_result, test_id):
    # Arrange
    customer_interface = MockDataInterface()
    customer_interface.read_by_id = MagicMock(return_value=expected_result)

    # Act
    result = get_customer(customer_id, customer_interface)

    # Assert
    assert result == expected_result
    customer_interface.read_by_id.assert_called_once_with(customer_id)


# Parametrized test for edge cases
@pytest.mark.parametrize(
    "customer_id, expected_result, test_id",
    [
        (0, "Invalid ID", "edge_case_zero_id"),
        (-1, "Invalid ID", "edge_case_negative_id"),
    ],
)
def test_get_customer_edge_cases(customer_id, expected_result, test_id):
    # Arrange
    customer_interface = MockDataInterface()
    customer_interface.read_by_id = MagicMock(return_value=expected_result)

    # Act
    result = get_customer(customer_id, customer_interface)

    # Assert
    assert result == expected_result
    customer_interface.read_by_id.assert_called_once_with(customer_id)


# Parametrized test for error cases
@pytest.mark.parametrize(
    "customer_id, exception, test_id",
    [
        (None, TypeError, "error_case_none_id"),
        ("abc", TypeError, "error_case_string_id"),
    ],
)
def test_get_customer_error_cases(customer_id, exception, test_id):
    # Arrange
    customer_interface = MockDataInterface()
    customer_interface.read_by_id = MagicMock(side_effect=exception)

    # Act & Assert
    with pytest.raises(exception):
        get_customer(customer_id, customer_interface)
    customer_interface.read_by_id.assert_not_called()

import pytest
from unittest.mock import MagicMock
from hotel.operations.interface import DataInterface
from hotel.operations.customers import delete_customer


# Parametrized test for happy path scenarios
@pytest.mark.parametrize(
    "customer_id, expected_result",
    [
        pytest.param(1, {"status": "success"}, id="delete_existing_customer"),
        pytest.param(123, {"status": "success"}, id="delete_customer_high_id"),
        # Add more realistic customer IDs and expected results as needed
    ],
    ids=str,
)
def test_delete_customer_happy_path(customer_id, expected_result):
    # Arrange
    mock_interface = MagicMock(spec=DataInterface)
    mock_interface.delete.return_value = expected_result

    # Act
    result = delete_customer(customer_id, mock_interface)

    # Assert
    mock_interface.delete.assert_called_once_with(customer_id)
    assert result == expected_result


# Parametrized test for edge cases
@pytest.mark.parametrize(
    "customer_id, expected_result",
    [
        pytest.param(
            0,
            {"status": "error", "message": "Invalid ID"},
            id="delete_customer_zero_id",
        ),
        pytest.param(
            -1,
            {"status": "error", "message": "Invalid ID"},
            id="delete_customer_negative_id",
        ),
        # Add more edge case IDs and expected results as needed
    ],
    ids=str,
)
def test_delete_customer_edge_cases(customer_id, expected_result):
    # Arrange
    mock_interface = MagicMock(spec=DataInterface)
    mock_interface.delete.return_value = expected_result

    # Act
    result = delete_customer(customer_id, mock_interface)

    # Assert
    mock_interface.delete.assert_called_once_with(customer_id)
    assert result == expected_result


# Parametrized test for error scenarios
@pytest.mark.parametrize(
    "customer_id, expected_exception, mock_side_effect",
    [
        pytest.param(
            1,
            KeyError,
            KeyError("Customer not found"),
            id="delete_nonexistent_customer",
        ),
        pytest.param(
            2,
            ValueError,
            ValueError("Invalid customer ID"),
            id="delete_invalid_customer_id",
        ),
        # Add more error scenarios as needed
    ],
    ids=str,
)
def test_delete_customer_error_cases(customer_id, expected_exception, mock_side_effect):
    # Arrange
    mock_interface = MagicMock(spec=DataInterface)
    mock_interface.delete.side_effect = mock_side_effect

    # Act & Assert
    with pytest.raises(expected_exception):
        delete_customer(customer_id, mock_interface)
    mock_interface.delete.assert_called_once_with(customer_id)

import pytest
from unittest.mock import Mock
from hotel.operations.customers import update_customer
from hotel.operations.models import CustomerUpdateData, CustomerResult


# Mock the DataInterface to simulate database operations
class MockDataInterface(Mock):
    def update(self, customer_id, updated_customer):
        # Simulate a successful update
        if customer_id == 1:
            return CustomerResult(id=1, **updated_customer)
        # Simulate a customer not found scenario
        elif customer_id == 999:
            return "Customer not found"
        # Simulate a database error
        else:
            raise Exception("Database error")


@pytest.mark.parametrize(
    "customer_id, updated_customer, expected_result, test_id",
    [
        # Happy path tests
        (
            1,
            CustomerUpdateData(name="John Doe", email="john@example.com"),
            CustomerResult(id=1, name="John Doe", email="john@example.com"),
            "happy-path-1",
        ),
        (
            1,
            CustomerUpdateData(name="Jane Smith", email="jane@example.com"),
            CustomerResult(id=1, name="Jane Smith", email="jane@example.com"),
            "happy-path-2",
        ),
        # Edge case tests
        (
            1,
            CustomerUpdateData(name="", email=""),
            CustomerResult(id=1, name="", email=""),
            "edge-case-empty-fields",
        ),
        # Error case tests
        (
            999,
            CustomerUpdateData(name="Ghost", email="ghost@example.com"),
            "Customer not found",
            "error-case-not-found",
        ),
        (
            0,
            CustomerUpdateData(name="Error", email="error@example.com"),
            Exception("Database error"),
            "error-case-db-error",
        ),
    ],
)
def test_update_customer(customer_id, updated_customer, expected_result, test_id):
    # Arrange
    customer_interface = MockDataInterface()

    # Act
    result = update_customer(customer_id, updated_customer, customer_interface)

    # Assert
    if isinstance(expected_result, Exception):
        with pytest.raises(Exception) as exc_info:
            update_customer(customer_id, updated_customer, customer_interface)
        assert str(exc_info.value) == str(expected_result)
    else:
        assert result == expected_result

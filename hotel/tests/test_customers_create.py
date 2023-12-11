import pytest
from sqlmodel import Session
from hotel.operations.customers import create_customer
from hotel.operations.models import CustomerCreateData
from hotel.database.models import Customer
from unittest.mock import Mock


# Parametrized test for happy path with various realistic test values
@pytest.mark.parametrize(
    "test_id, customer_data",
    [
        ("happy_path_1", {"name": "John Doe", "email": "john.doe@example.com"}),
        ("happy_path_2", {"name": "Jane Smith", "email": "jane.smith@example.com"}),
        # Add more test cases as needed
    ],
    ids=lambda x: x[0],
)
def test_create_customer_happy_path(test_id, customer_data):
    # Arrange
    session_mock = Mock(spec=Session)
    customer_create_data = CustomerCreateData(**customer_data)

    # Act
    result = create_customer(session=session_mock, customer=customer_create_data)

    # Assert
    session_mock.add.assert_called_once()
    session_mock.commit.assert_called_once()
    session_mock.refresh.assert_called_once_with(result)
    assert isinstance(result, Customer)
    assert result.name == customer_data["name"]
    assert result.email == customer_data["email"]


# Parametrized test for edge cases
@pytest.mark.parametrize(
    "test_id, customer_data",
    [
        ("edge_case_empty_name", {"name": "", "email": "no.name@example.com"}),
        ("edge_case_long_name", {"name": "a" * 256, "email": "long.name@example.com"}),
        # Add more edge cases as needed
    ],
    ids=lambda x: x[0],
)
def test_create_customer_edge_cases(test_id, customer_data):
    # Arrange
    session_mock = Mock(spec=Session)
    customer_create_data = CustomerCreateData(**customer_data)

    # Act
    result = create_customer(session=session_mock, customer=customer_create_data)

    # Assert
    session_mock.add.assert_called_once()
    session_mock.commit.assert_called_once()
    session_mock.refresh.assert_called_once_with(result)
    assert isinstance(result, Customer)
    assert result.name == customer_data["name"]
    assert result.email == customer_data["email"]


# Parametrized test for error cases
@pytest.mark.parametrize(
    "test_id, customer_data, expected_exception",
    [
        (
            "error_case_invalid_email",
            {"name": "Invalid Email", "email": "not-an-email"},
            ValueError,
        ),
        # Add more error cases as needed
    ],
    ids=lambda x: x[0],
)
def test_create_customer_error_cases(test_id, customer_data, expected_exception):
    # Arrange
    session_mock = Mock(spec=Session)
    customer_create_data = CustomerCreateData(**customer_data)

    # Act / Assert
    with pytest.raises(expected_exception):
        create_customer(session=session_mock, customer=customer_create_data)

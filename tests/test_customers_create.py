import pytest
from hotel.operations.customers import create_customer
from hotel.operations.interface import DataInterface
from hotel.operations.models import CustomerCreateData
from pytest_mock import MockerFixture


# Define a fixture for the customer data
@pytest.fixture
def customer_data():
    return CustomerCreateData(name="John Doe", email="john.doe@example.com")


# Define a fixture for the mock interface
@pytest.fixture
def mock_interface(mocker: MockerFixture):
    return mocker.Mock(spec=DataInterface)


# Happy path tests with various realistic test values
@pytest.mark.parametrize(
    "customer_data, expected_id",
    [
        (CustomerCreateData(name="Jane Doe", email="jane.doe@example.com"), "HP-1"),
        (CustomerCreateData(name="Bob Smith", email="bob.smith@example.com"), "HP-2"),
        (CustomerCreateData(name="Alice Johnson", email="alice.j@example.com"), "HP-3"),
    ],
    ids=["happy-path-jane", "happy-path-bob", "happy-path-alice"],
)
def test_create_customer_happy_path(customer_data, expected_id, mock_interface):
    # Arrange
    mock_interface.create.return_value = {
        "id": expected_id,
        "name": customer_data.name,
        "email": customer_data.email,
    }

    # Act
    result = create_customer(customer_data, mock_interface)

    # Assert
    assert result == {
        "id": expected_id,
        "name": customer_data.name,
        "email": customer_data.email,
    }
    mock_interface.create.assert_called_once_with(customer_data.dict())


# Edge cases
@pytest.mark.parametrize(
    "customer_data, expected_exception",
    [
        (CustomerCreateData(name="", email="jane.doe@example.com"), ValueError, "EC-1"),
        (CustomerCreateData(name="Jane Doe", email=""), ValueError, "EC-2"),
    ],
    ids=["edge-case-empty-name", "edge-case-empty-email"],
)
def test_create_customer_edge_cases(customer_data, expected_exception, mock_interface):
    # Arrange
    mock_interface.create.side_effect = expected_exception

    # Act & Assert
    with pytest.raises(expected_exception):
        create_customer(customer_data, mock_interface)


# Error cases
@pytest.mark.parametrize(
    "customer_data, expected_exception",
    [
        (
            CustomerCreateData(name="John Doe", email="not-an-email"),
            ValueError,
            "ERR-1",
        ),
        (
            CustomerCreateData(name="John Doe", email="john.doe@example.com"),
            Exception,
            "ERR-2",
        ),
    ],
    ids=["error-case-invalid-email", "error-case-exception"],
)
def test_create_customer_error_cases(customer_data, expected_exception, mock_interface):
    # Arrange
    mock_interface.create.side_effect = expected_exception

    # Act & Assert
    with pytest.raises(expected_exception):
        create_customer(customer_data, mock_interface)

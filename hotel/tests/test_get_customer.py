import pytest
from sqlmodel import Session, create_engine
from sqlmodel.pool import StaticPool
from hotel.database.models import Customer
from hotel.operations.customers import get_customer
from hotel.operations.utils.get_or_404 import ItemNotFound


# Setup a test database and session fixture
@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    with Session(engine) as session:
        yield session


# Parametrized test for the happy path
@pytest.mark.parametrize(
    "customer_id, expected_name",
    [
        (1, "John Doe"),  # ID: happy-path-1
        (2, "Jane Smith"),  # ID: happy-path-2
        (3, "Alice Johnson"),  # ID: happy-path-3
    ],
    ids=["happy-path-1", "happy-path-2", "happy-path-3"],
)
def test_get_customer_happy_path(session, customer_id, expected_name):
    # Arrange
    customer = Customer(id=customer_id, name=expected_name)
    session.add(customer)
    session.commit()

    # Act
    result = get_customer(session, customer_id)

    # Assert
    assert result.id == customer_id
    assert result.name == expected_name


# Parametrized test for edge cases
@pytest.mark.parametrize(
    "customer_id",
    [
        (0),  # ID: edge-case-zero-id
        (-1),  # ID: edge-case-negative-id
        (99999),  # ID: edge-case-nonexistent-id
    ],
    ids=["edge-case-zero-id", "edge-case-negative-id", "edge-case-nonexistent-id"],
)
def test_get_customer_edge_cases(session, customer_id):
    # Arrange
    # No arrangement needed as we are testing non-existent customers

    # Act & Assert
    with pytest.raises(ItemNotFound):
        get_customer(session, customer_id)


# Parametrized test for error cases
@pytest.mark.parametrize(
    "customer_id, exception",
    [
        ("abc", ValueError),  # ID: error-case-invalid-type
        (None, TypeError),  # ID: error-case-none-id
    ],
    ids=["error-case-invalid-type", "error-case-none-id"],
)
def test_get_customer_error_cases(session, customer_id, exception):
    # Arrange
    # No arrangement needed as we are testing input errors

    # Act & Assert
    with pytest.raises(exception):
        get_customer(session, customer_id)

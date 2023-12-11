import pytest
from sqlmodel import Session, create_engine
from sqlmodel.pool import StaticPool
from hotel.database.models import Customer
from hotel.operations.customers import delete_customer


# Setup a test database and session fixture
@pytest.fixture(name="test_session")
def session_fixture():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    Session.configure(bind=engine)
    with Session() as session:
        yield session


# Parametrized test for the happy path
@pytest.mark.parametrize(
    "customer_id, expected_message",
    [
        (1, {"detail": "Customer deleted successfully."}, "happy_path_1"),
        (2, {"detail": "Customer deleted successfully."}, "happy_path_2"),
        # Add more test cases with different realistic customer IDs
    ],
    ids=["happy_path_1", "happy_path_2"],
)
def test_delete_customer_happy_path(test_session, customer_id, expected_message):
    # Arrange
    customer = Customer(id=customer_id, name="Test Customer", email="test@example.com")
    test_session.add(customer)
    test_session.commit()

    # Act
    result = delete_customer(test_session, customer_id)

    # Assert
    assert result == expected_message
    assert (
        test_session.exec(select(Customer).where(Customer.id == customer_id)).first()
        is None
    )


# Parametrized test for edge cases
@pytest.mark.parametrize(
    "customer_id, expected_exception",
    [
        (0, {"detail": "Customer not found."}, "edge_case_0"),
        # Add more edge cases if applicable
    ],
    ids=["edge_case_0"],
)
def test_delete_customer_edge_cases(test_session, customer_id, expected_exception):
    # Arrange
    # No arrangement needed as we are testing non-existent customer deletion

    # Act & Assert
    with pytest.raises(expected_exception):
        delete_customer(test_session, customer_id)


# Parametrized test for error cases
@pytest.mark.parametrize(
    "customer_id, setup_customer, expected_exception",
    [
        (-1, False, {"detail": "Customer not found."}, "error_negative_id"),
        (999, False, {"detail": "Customer not found."}, "error_nonexistent_id"),
        # Add more error cases with invalid or non-existent customer IDs
    ],
    ids=["error_negative_id", "error_nonexistent_id"],
)
def test_delete_customer_error_cases(
    test_session, customer_id, setup_customer, expected_exception
):
    # Arrange
    if setup_customer:
        customer = Customer(
            id=customer_id, name="Test Customer", email="test@example.com"
        )
        test_session.add(customer)
        test_session.commit()

    # Act & Assert
    with pytest.raises(expected_exception):
        delete_customer(test_session, customer_id)

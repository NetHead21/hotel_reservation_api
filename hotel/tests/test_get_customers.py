import pytest
from sqlmodel import Session, create_engine
from sqlmodel.pool import StaticPool
from hotel.database.models import Customer
from hotel.operations.customers import get_customers


# Setup a test database and session fixture
@pytest.fixture(name="test_session")
def session_fixture():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    with Session(engine) as session:
        yield session


# Happy path tests with various realistic test values
@pytest.mark.parametrize(
    "test_id, input_customers, expected_count",
    [
        ("happy_path_single_customer", [Customer(name="John Doe")], 1),
        (
            "happy_path_multiple_customers",
            [Customer(name="John Doe"), Customer(name="Jane Doe")],
            2,
        ),
        ("happy_path_no_customers", [], 0),
    ],
    ids=lambda x: x[0],
)
def test_get_customers_happy_path(
    test_id, input_customers, expected_count, test_session
):
    # Arrange
    for customer in input_customers:
        test_session.add(customer)
    test_session.commit()

    # Act
    result = get_customers(test_session)

    # Assert
    assert len(result) == expected_count
    for customer in result:
        assert isinstance(customer, Customer)


# Edge cases
# Assuming there are no specific edge cases for this function as it's a simple select all

# Error cases
# Assuming the function does not handle any specific errors as it's a simple select all
# Any database connection errors would be outside the scope of this function and not handled here

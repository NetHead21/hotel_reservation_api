import pytest
from sqlmodel import Session, create_engine, SQLModel
from sqlalchemy.orm import sessionmaker
from hotel.database.models import Customer
from hotel.operations.customers import update_customer

# Setup a test database and session
TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(name="session", scope="function")
def session_fixture():
    SQLModel.metadata.create_all(engine)
    with TestingSessionLocal() as session:
        yield session
    SQLModel.metadata.drop_all(engine)


@pytest.fixture(name="existing_customer", scope="function")
def existing_customer_fixture(session: Session):
    customer = Customer(name="John Doe", email="john.doe@example.com")
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer


@pytest.mark.parametrize(
    "customer_id, updated_data, test_id",
    [
        (1, {"name": "Jane Doe"}, "happy_path_name_change"),
        (1, {"email": "jane.doe@example.com"}, "happy_path_email_change"),
        # Add more test cases for different fields and combinations
    ],
)
def test_update_customer_happy_path(
    session: Session,
    existing_customer: Customer,
    customer_id: int,
    updated_data: dict,
    test_id: str,
):
    # Arrange
    updated_customer = Customer(**updated_data)

    # Act
    result = update_customer(session, customer_id, updated_customer)

    # Assert
    assert result.id == customer_id
    for key, value in updated_data.items():
        assert getattr(result, key) == value


@pytest.mark.parametrize(
    "customer_id, updated_data, test_id",
    [
        (999, {"name": "Ghost"}, "error_nonexistent_customer"),
        # Add more error cases as needed
    ],
)
def test_update_customer_error_cases(
    session: Session, customer_id: int, updated_data: dict, test_id: str
):
    # Arrange
    updated_customer = Customer(**updated_data)

    # Act & Assert
    with pytest.raises(ValueError) as excinfo:
        update_customer(session, customer_id, updated_customer)
    assert "404" in str(excinfo.value)


@pytest.mark.parametrize(
    "customer_id, updated_data, test_id",
    [
        (1, {}, "edge_case_no_updates"),
        # Add more edge cases as needed
    ],
)
def test_update_customer_edge_cases(
    session: Session,
    existing_customer: Customer,
    customer_id: int,
    updated_data: dict,
    test_id: str,
):
    # Arrange
    updated_customer = Customer(**updated_data)

    # Act
    result = update_customer(session, customer_id, updated_customer)

    # Assert
    assert result.id == customer_id
    assert result.name == existing_customer.name
    assert result.email == existing_customer.email

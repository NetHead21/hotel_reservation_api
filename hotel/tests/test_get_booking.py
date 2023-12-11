import pytest
from sqlmodel import Session, create_engine
from sqlalchemy.orm import sessionmaker
from hotel.database.models import Booking
from hotel.operations.bookings import get_booking
from sqlmodel.pool import StaticPool

# Setup a test database and session
TEST_DATABASE_URL = "sqlite://"
engine = create_engine(
    TEST_DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(name="session")
def session_fixture():
    with SessionLocal() as session:
        yield session


@pytest.fixture
def setup_database():
    from sqlmodel import SQLModel

    SQLModel.metadata.create_all(engine)


# Parametrized test cases for happy path, edge cases, and error cases
@pytest.mark.parametrize(
    "setup_booking, booking_id, expected_id",
    [
        # Happy path tests with various realistic test values
        (
            {"id": 1, "room_id": 101, "user_id": 1001},
            1,
            1,
            pytest.mark.id("happy-path-1"),
        ),
        (
            {"id": 2, "room_id": 102, "user_id": 1002},
            2,
            2,
            pytest.mark.id("happy-path-2"),
        ),
        # Edge cases
        (
            {"id": 2147483647, "room_id": 103, "user_id": 1003},
            2147483647,
            2147483647,
            pytest.mark.id("edge-case-max-int"),
        ),
        # Error cases
        (
            {"id": 3, "room_id": 104, "user_id": 1004},
            999,
            None,
            pytest.mark.id("error-case-nonexistent-id"),
        ),
    ],
    indirect=["setup_booking"],
)
def test_get_booking(setup_database, session, setup_booking, booking_id, expected_id):
    # Arrange
    new_booking = Booking(**setup_booking)
    session.add(new_booking)
    session.commit()

    # Act
    if expected_id is not None:
        booking = get_booking(booking_id, session)
    else:
        with pytest.raises(ValueError):
            get_booking(booking_id, session)

    # Assert
    if expected_id is not None:
        assert booking.id == expected_id

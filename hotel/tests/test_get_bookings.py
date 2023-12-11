import pytest
from sqlmodel import Session, create_engine
from sqlmodel.pool import StaticPool
from hotel.database.models import Booking
from hotel.operations.bookings import get_bookings


# Setup a test database and session fixture
@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    Session.configure(bind=engine)
    with Session() as session:
        yield session


# Parametrized test for happy path scenarios
@pytest.mark.parametrize(
    "booking_data, expected",
    [
        pytest.param(
            [{"id": 1, "room_id": 101, "guest_name": "Alice"}],
            [Booking(id=1, room_id=101, guest_name="Alice")],
            id="single_booking",
        ),
        pytest.param([], [], id="no_bookings"),
        pytest.param(
            [
                {"id": 2, "room_id": 102, "guest_name": "Bob"},
                {"id": 3, "room_id": 103, "guest_name": "Charlie"},
            ],
            [
                Booking(id=2, room_id=102, guest_name="Bob"),
                Booking(id=3, room_id=103, guest_name="Charlie"),
            ],
            id="multiple_bookings",
        ),
    ],
)
def test_get_bookings_happy_path(session, booking_data, expected):
    # Arrange
    for data in booking_data:
        session.add(Booking(**data))
    session.commit()

    # Act
    result = get_bookings(session)

    # Assert
    assert result == expected


# Parametrized test for edge cases
@pytest.mark.parametrize(
    "booking_data, expected",
    [
        pytest.param(
            [{"id": 1, "room_id": 101, "guest_name": ""}],
            [Booking(id=1, room_id=101, guest_name="")],
            id="empty_guest_name",
        ),
        pytest.param(
            [{"id": 1, "room_id": None, "guest_name": "Alice"}],
            [Booking(id=1, room_id=None, guest_name="Alice")],
            id="null_room_id",
        ),
    ],
)
def test_get_bookings_edge_cases(session, booking_data, expected):
    # Arrange
    for data in booking_data:
        session.add(Booking(**data))
    session.commit()

    # Act
    result = get_bookings(session)

    # Assert
    assert result == expected


# Parametrized test for error cases
@pytest.mark.parametrize(
    "session_state, expected_exception",
    [
        pytest.param(
            "closed_session", pytest.raises(RuntimeError), id="closed_session"
        ),
    ],
)
def test_get_bookings_error_cases(session, session_state, expected_exception):
    # Arrange
    if session_state == "closed_session":
        session.close()

    # Act / Assert
    with expected_exception:
        get_bookings(session)

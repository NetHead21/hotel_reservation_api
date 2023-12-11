import pytest
from sqlmodel import Session, create_engine
from sqlmodel.pool import StaticPool
from hotel.database.models import Booking, Room
from hotel.operations.bookings import delete_booking
from sqlalchemy.exc import NoResultFound


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
    "booking_id, expected_message",
    [
        (1, {"detail": "Booking successfully deleted"}),
        (2, {"detail": "Booking successfully deleted"}),
        # Add more test cases with different realistic booking IDs
    ],
    ids=["happy-path-booking-1", "happy-path-booking-2"],
)
def test_delete_booking_happy_path(test_session, booking_id, expected_message):
    # Arrange
    room = Room(id=1, number="101", level="1", status="available")
    booking = Booking(id=booking_id, room_id=room.id)
    test_session.add(room)
    test_session.add(booking)
    test_session.commit()

    # Act
    result = delete_booking(test_session, booking_id)

    # Assert
    assert result == expected_message
    with pytest.raises(NoResultFound):
        test_session.execute(select(Booking).where(Booking.id == booking_id)).one()


# Parametrized test for edge cases
@pytest.mark.parametrize(
    "booking_id, expected_exception",
    [
        (0, NoResultFound),  # Assuming 0 is not a valid ID
        (-1, NoResultFound),  # Negative ID
        # Add more edge cases if necessary
    ],
    ids=["edge-case-invalid-id-0", "edge-case-negative-id"],
)
def test_delete_booking_edge_cases(test_session, booking_id, expected_exception):
    # Act & Assert
    with pytest.raises(expected_exception):
        delete_booking(test_session, booking_id)


# Parametrized test for error cases
@pytest.mark.parametrize(
    "booking_id, setup_booking, expected_exception",
    [
        (999, False, NoResultFound),  # Non-existent booking ID without setup
        # Add more error cases if there are other possible errors
    ],
    ids=["error-non-existent-booking"],
)
def test_delete_booking_error_cases(
    test_session, booking_id, setup_booking, expected_exception
):
    # Arrange
    if setup_booking:
        booking = Booking(id=booking_id, room_id=1)
        test_session.add(booking)
        test_session.commit()

    # Act & Assert
    with pytest.raises(expected_exception):
        delete_booking(test_session, booking_id)

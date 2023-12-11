import pytest
from datetime import datetime, timedelta
from sqlmodel import Session
from hotel.database.models import Booking, Room
from hotel.operations.bookings import create_booking
from hotel.operations.models import BookingCreateData

# Constants for tests
ROOM_ID = 1
PRICE_PER_DAY = 100


# Fixtures
@pytest.fixture
def mock_room(db_session: Session):
    room = Room(id=ROOM_ID, price=PRICE_PER_DAY)
    db_session.add(room)
    db_session.commit()
    return room


@pytest.fixture
def booking_data():
    return BookingCreateData(
        room_id=ROOM_ID,
        from_date=datetime.now(),
        to_date=datetime.now() + timedelta(days=3),
        customer_id=1,
    )


# Parametrized tests
@pytest.mark.parametrize(
    "from_date, to_date, expected_days, expected_price, test_id",
    [
        (
            datetime.now(),
            datetime.now() + timedelta(days=1),
            1,
            PRICE_PER_DAY,
            "happy_path_one_day",
        ),
        (
            datetime.now(),
            datetime.now() + timedelta(days=2),
            2,
            PRICE_PER_DAY * 2,
            "happy_path_two_days",
        ),
        (
            datetime.now(),
            datetime.now() + timedelta(days=7),
            7,
            PRICE_PER_DAY * 7,
            "happy_path_one_week",
        ),
    ],
)
def test_create_booking_happy_path(
    mock_room,
    db_session: Session,
    from_date,
    to_date,
    expected_days,
    expected_price,
    test_id,
    booking_data,
):
    # Arrange
    booking_data.from_date = from_date
    booking_data.to_date = to_date

    # Act
    result = create_booking(db_session, booking_data)

    # Assert
    assert result.price == expected_price
    assert (result.to_date - result.from_date).days == expected_days
    assert db_session.exec(select(Booking)).first() is not None


@pytest.mark.parametrize(
    "from_date, to_date, test_id",
    [
        (datetime.now() + timedelta(days=1), datetime.now(), "error_past_date"),
        (datetime.now(), datetime.now(), "error_same_day"),
    ],
)
def test_create_booking_invalid_dates(
    mock_room, db_session: Session, from_date, to_date, test_id, booking_data
):
    # Arrange
    booking_data.from_date = from_date
    booking_data.to_date = to_date

    # Act / Assert
    with pytest.raises(HTTPException) as exc_info:
        create_booking(db_session, booking_data)
    assert exc_info.value.status_code == 404
    assert "Invalid Dates" in str(exc_info.value.detail)


@pytest.mark.parametrize(
    "room_id, test_id",
    [
        (999, "error_room_not_found"),
    ],
)
def test_create_booking_room_not_found(
    db_session: Session, room_id, test_id, booking_data
):
    # Arrange
    booking_data.room_id = room_id

    # Act / Assert
    with pytest.raises(HTTPException) as exc_info:
        create_booking(db_session, booking_data)
    assert exc_info.value.status_code == 404
    assert "Not Found" in str(exc_info.value.detail)

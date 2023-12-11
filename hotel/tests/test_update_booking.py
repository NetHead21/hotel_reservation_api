import pytest
from sqlmodel import Session
from hotel.database.models import Booking
from hotel.operations.bookings import update_booking
from hotel.operations.models import BookingResult


# Fixture to mock the database session
@pytest.fixture
def mock_session(mocker):
    session = mocker.MagicMock(spec=Session)
    return session


# Fixture to create a mock booking object
@pytest.fixture
def mock_booking(mocker):
    return mocker.MagicMock(spec=Booking)


# Parametrized test for the happy path
@pytest.mark.parametrize(
    "booking_id, updated_data, expected_result, test_id",
    [
        (
            1,
            BookingResult(start_date="2023-04-10", end_date="2023-04-15"),
            BookingResult(start_date="2023-04-10", end_date="2023-04-15"),
            "happy_path_1",
        ),
        (
            2,
            BookingResult(number_of_guests=2),
            BookingResult(number_of_guests=2),
            "happy_path_2",
        ),
        # Add more test cases with different combinations of BookingResult fields
    ],
)
def test_update_booking_happy_path(
    mock_session, mock_booking, booking_id, updated_data, expected_result, test_id
):
    # Arrange
    mock_session.get.return_value = mock_booking
    mock_booking.dict.return_value = updated_data.dict()

    # Act
    result = update_booking(mock_session, booking_id, updated_data)

    # Assert
    assert result == expected_result
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once_with(mock_booking)


# Parametrized test for edge cases
@pytest.mark.parametrize(
    "booking_id, updated_data, test_id",
    [
        (
            1,
            BookingResult(start_date="2023-04-10", end_date="2023-04-09"),
            "edge_case_invalid_date_range",
        ),
        # Add more edge cases as needed
    ],
)
def test_update_booking_edge_cases(
    mock_session, mock_booking, booking_id, updated_data, test_id
):
    # Arrange
    mock_session.get.return_value = mock_booking
    mock_booking.dict.return_value = updated_data.dict()

    # Act
    with pytest.raises(
        ValueError
    ):  # Assuming the function raises ValueError for invalid date range
        update_booking(mock_session, booking_id, updated_data)

    # Assert
    mock_session.commit.assert_not_called()


# Parametrized test for error cases
@pytest.mark.parametrize(
    "booking_id, updated_data, exception, test_id",
    [
        (
            1,
            BookingResult(start_date="2023-04-10"),
            KeyError,
            "error_case_missing_end_date",
        ),
        # Add more error cases as needed
    ],
)
def test_update_booking_error_cases(
    mock_session, mock_booking, booking_id, updated_data, exception, test_id
):
    # Arrange
    mock_session.get.return_value = mock_booking
    mock_booking.dict.side_effect = exception

    # Act & Assert
    with pytest.raises(exception):
        update_booking(mock_session, booking_id, updated_data)

import pytest
from sqlmodel import Session, create_engine
from sqlmodel.pool import StaticPool
from hotel.database.models import Room
from hotel.operations.rooms import get_rooms


# Setup a test database and session for the tests
@pytest.fixture(name="test_session")
def session_fixture():
    # Create a new database for the tests
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    Session.configure(bind=engine)
    with Session() as session:
        yield session


@pytest.mark.parametrize(
    "test_id, room_data, expected",
    [
        (
            "happy_path_single_room",
            [Room(number="101", floor=1)],
            [Room(number="101", floor=1)],
        ),
        (
            "happy_path_multiple_rooms",
            [Room(number="102", floor=1), Room(number="201", floor=2)],
            [Room(number="102", floor=1), Room(number="201", floor=2)],
        ),
        ("edge_case_no_rooms", [], []),
        # Add more test cases for error scenarios if applicable
    ],
)
def test_get_rooms(test_id, room_data, expected, test_session):
    # Arrange
    for room in room_data:
        test_session.add(room)
    test_session.commit()

    # Act
    result = get_rooms(test_session)

    # Assert
    assert result == expected
    assert all(isinstance(room, Room) for room in result)

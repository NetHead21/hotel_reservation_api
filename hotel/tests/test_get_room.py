import pytest
from sqlmodel import create_engine
from sqlalchemy.orm import sessionmaker
from hotel.database.models import Room
from hotel.operations.rooms import get_room
from hotel.database.utils.get_or_404 import NotFoundError

# Setup a test database and session
TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Create a fixture for the database session
@pytest.fixture(name="session")
def session_fixture():
    with SessionLocal() as session:
        yield session


# Parametrized test for the happy path
@pytest.mark.parametrize(
    "room_id, expected_id",
    [
        (1, 1),  # Test with room ID 1
        (2, 2),  # Test with room ID 2
        (100, 100),  # Test with room ID 100
    ],
    ids=["happy-path-room-1", "happy-path-room-2", "happy-path-room-100"],
)
def test_get_room_happy_path(session, room_id, expected_id):
    # Arrange
    room = Room(id=expected_id, number="101", level="1", status="available")
    session.add(room)
    session.commit()

    # Act
    result = get_room(session, room_id)

    # Assert
    assert result.id == expected_id


# Parametrized test for edge cases
@pytest.mark.parametrize(
    "room_id",
    [
        (0),  # Test with room ID 0
        (-1),  # Test with negative room ID
        (999999),  # Test with a very large room ID
    ],
    ids=["edge-case-room-0", "edge-case-negative-room-id", "edge-case-large-room-id"],
)
def test_get_room_edge_cases(session, room_id):
    # Arrange
    # No room setup required for edge cases

    # Act & Assert
    with pytest.raises(NotFoundError):
        get_room(session, room_id)


# Parametrized test for error cases
@pytest.mark.parametrize(
    "room_id, exception",
    [
        (None, TypeError),  # Test with None as room ID
        ("one", TypeError),  # Test with string as room ID
    ],
    ids=["error-case-none-room-id", "error-case-string-room-id"],
)
def test_get_room_error_cases(session, room_id, exception):
    # Arrange
    # No room setup required for error cases

    # Act & Assert
    with pytest.raises(exception):
        get_room(session, room_id)

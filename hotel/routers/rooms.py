from typing import List
from fastapi import APIRouter

from hotel.database.database_interface import DatabaseInterface
from hotel.database.models import Room
from hotel.operations.rooms import get_rooms, get_room

router = APIRouter()


@router.get("/rooms", response_model=List[Room])
def api_get_rooms():
    room_interface = DatabaseInterface(Room)
    return get_rooms(room_interface)


@router.get("/room/{room_id}", response_model=Room | str)
def api_get_room(room_id: int):
    room_interface = DatabaseInterface(Room)
    return get_room(room_id, room_interface)

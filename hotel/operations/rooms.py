from hotel.operations.interface import DataInterface, DataObject


def get_rooms(room_interface: DataInterface) -> list[DataObject]:
    return room_interface.read_all()


def get_room(room_id: int, room_interface: DataInterface):
    return room_interface.read_by_id(room_id)

from datetime import date
from typing import Optional
from sqlmodel import SQLModel


class CustomerCreateData(SQLModel):
    first_name: str
    last_name: str
    email_address: str


class CustomerUpdateData(SQLModel):
    first_name: Optional[str]
    last_name: Optional[str]
    email_address: Optional[str]


class CustomerResult(SQLModel):
    id: int
    first_name: str
    last_name: str
    email_address: str


class BookingCreateData(SQLModel):
    room_id: int
    customer_id: int
    from_date: date
    to_date: date


class BookingResult(SQLModel):
    id: int
    room_id: int
    customer_id: int
    price: int
    from_date: date
    to_date: date


class RoomResult(SQLModel):
    id: int
    number: str
    size: int
    price: int

from sqlmodel import Field, SQLModel, Relationship
from typing import Optional
from datetime import date


class Customer(SQLModel, table=True):
    __tablename__ = "customers"
    id: Optional[int] = Field(default=None, unique=True, primary_key=True)
    first_name: str
    last_name: str
    email_address: str


class Room(SQLModel, table=True):
    __tablename__ = "rooms"
    id: Optional[int] = Field(default=None, unique=True, primary_key=True)
    number: str = Field(unique=True)
    size: int
    price: int


class Booking(SQLModel, table=True):
    __tablename__ = "bookings"
    id: Optional[int] = Field(default=None, unique=True, primary_key=True)
    from_date: date
    to_date: date
    price: int

    customer_id: Optional[int] = Field(default=None, foreign_key="customers.id")
    customer: Optional[Customer] = Relationship(
        sa_relationship_kwargs={"uselist": False}
    )
    room_id: Optional[int] = Field(default=None, foreign_key="rooms.id")
    room: Optional[Room] = Relationship(sa_relationship_kwargs={"uselist": False})

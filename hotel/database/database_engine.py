from datetime import date

from sqlalchemy import Engine
from sqlmodel import SQLModel, create_engine, Session
from hotel.database.models import Customer, Room, Booking

db_name: str = "sqlite:///hotel.db"
engine = create_engine(db_name, echo=True)


def create_db_and_tables(engine: Engine) -> None:
    SQLModel.metadata.create_all(engine)


def create_initial_data() -> None:
    room_1 = Room(number=101, size=10, price=2000)
    room_2 = Room(number=102, size=10, price=2000)
    room_3 = Room(number=103, size=20, price=4000)
    room_4 = Room(number=104, size=20, price=4000)
    room_5 = Room(number=105, size=50, price=5000)

    customer_juniven = Customer(
        first_name="Juniven",
        last_name="Saavedra",
        email_address="junivensaavedra@gmail.com",
    )
    customer_ellen = Customer(
        first_name="Ellen",
        last_name="Saavedra",
        email_address="ellensaavedra@gmail.com",
    )
    customer_elisio = Customer(
        first_name="Elisio",
        last_name="Pahit",
        email_address="totoygwapo@gmail.com",
    )

    book_1 = Booking(
        id=None,
        from_date=date(2023, 12, 7),
        to_date=date(2023, 12, 8),
        price=200,
        customer_id=1,
        room_id=1,
    )

    with Session(engine) as session:
        session.add(room_1)
        session.add(room_2)
        session.add(room_3)
        session.add(room_4)
        session.add(room_5)
        session.add(customer_juniven)
        session.add(customer_ellen)
        session.add(customer_elisio)
        session.add(book_1)
        session.commit()


def init_db() -> None:
    create_db_and_tables(engine)


def main() -> None:
    create_db_and_tables(engine)
    create_initial_data()


if __name__ == "__main__":
    main()

import json
from fastapi import FastAPI
from hotel.database.database_engine import init_db, engine
from sqlmodel import Session, select
from contextlib import asynccontextmanager
from hotel.database.models import Room
import pathlib

from hotel.routers import rooms, customers, bookings


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    data_path = pathlib.Path() / "hotel/database/initial_data/rooms.json"
    session = Session(engine)
    statement = select(Room)
    result = session.exec(statement).first()

    if result is None:
        rooms_data = json.loads(data_path.read_text())
        rooms = [Room(**room) for room in rooms_data]
        session.bulk_save_objects(rooms)
        session.commit()

    yield


USE_LIFESPAN = True

app = FastAPI(lifespan=lifespan if USE_LIFESPAN else None)


@app.get("/")
def read_root():
    return "The server is running."


app.include_router(rooms.router)
app.include_router(customers.router)
app.include_router(bookings.router)

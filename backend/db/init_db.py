from sqlmodel import SQLModel
from backend.db.session import engine

from backend.models import Trip, Car


def init_db():
    SQLModel.metadata.create_all(engine)

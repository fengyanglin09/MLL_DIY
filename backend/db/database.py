# backend/db/database.py

from sqlmodel import create_engine
from backend.envs.config import get_settings
from sqlmodel import Session, SQLModel

# Create the SQLAlchemy engine using the injected DATABASE_URL
engine = create_engine(
    get_settings().DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in get_settings().DATABASE_URL else {},
    echo=get_settings().DEBUG
)

# SessionLocal class to create sessions for DB

def get_db():
    db: Session = Session(engine)
    try:
        yield db
    finally:
        db.close()



def init_db():
    if get_settings().ENV in ("dev", "int"):
        print("Dev environment detected. Creating database tables...")
        SQLModel.metadata.create_all(engine)
    else:
        print(f"Environment is '{get_settings().ENV}', skipping table creation.")

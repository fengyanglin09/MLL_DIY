from sqlmodel import Session, create_engine

DATABASE_URL = "sqlite:///./test.db"  # or PostgreSQL URL
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}, echo=True)

def get_db():
    with Session(engine) as session:
        yield session

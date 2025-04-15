# # backend/db/init.py
#
# from backend.db.database import engine
# from sqlmodel import SQLModel
# from backend.envs.config import settings
#
#
# # Initialize the database (create tables)
# def init_db():
#     if settings.ENV in ("dev", "int"):
#         print("Dev environment detected. Creating database tables...")
#         SQLModel.metadata.create_all(engine)
#     else:
#         print(f"Environment is '{settings.ENV}', skipping table creation.")
#

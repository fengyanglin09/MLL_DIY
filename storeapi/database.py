import databases
import sqlalchemy
from storeapi.config import get_config


metadata = sqlalchemy.MetaData()


post_table = sqlalchemy.Table(
    "posts",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("body", sqlalchemy.String),
)

comment_table = sqlalchemy.Table(
    "comments",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("body", sqlalchemy.String),
    sqlalchemy.Column(
        "post_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("posts.id"), nullable=False
    ),
)


engine = sqlalchemy.create_engine(
    get_config().DATABASE_URL,
    connect_args=(
        {"check_same_thread": False} if "sqlite" in get_config().DATABASE_URL else {}
    ),
)

metadata.create_all(engine)

database = databases.Database(
    get_config().DATABASE_URL
)

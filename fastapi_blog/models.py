import datetime
from pathlib import Path
from typing import List, Mapping, Optional

import databases
import sqlalchemy
from pydantic import BaseModel

# SQLAlchemy specific code, as with any other app
DATABASE_URL = "sqlite:///" + str(Path(__file__).parent / "blog.db")
# DATABASE_URL = "postgresql://user:password@postgresserver/db"

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

posts = sqlalchemy.Table(
    "posts",
    metadata,
    sqlalchemy.Column("post_id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("title", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("subtitle", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("author", sqlalchemy.String, nullable=False, default="smetam"),
    sqlalchemy.Column(
        "date", sqlalchemy.DateTime, nullable=False, default=datetime.datetime.now
    ),
    sqlalchemy.Column("content", sqlalchemy.Text, nullable=False),
    sqlalchemy.Column("completed", sqlalchemy.Boolean, nullable=False, default=False),
)


engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)


class PostInput(BaseModel):
    title: str
    subtitle: str
    content: str
    completed: bool


class Post(BaseModel):
    post_id: int
    title: str
    subtitle: str
    author: str
    date: datetime.datetime
    content: str
    completed: bool


async def fetch_post(post_id: int) -> Optional[Mapping]:
    query = posts.select().where(posts.c.post_id == post_id)
    return await database.fetch_one(query)

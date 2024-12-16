import os
from typing import Annotated, Optional

from fastapi import Depends
from pydantic import BaseModel
from sqlmodel import Field, Session, SQLModel, create_engine

from dotenv import load_dotenv

load_dotenv()

TURSO_DATABASE_URL = os.getenv('TURSO_DATABASE_URL')
TURSO_AUTH_TOKEN = os.getenv('TURSO_AUTH_TOKEN')


sqlite_file_name = "database.db"
sqlite_url = f"sqlite+{TURSO_DATABASE_URL}/?authToken={TURSO_AUTH_TOKEN}&secure=true"

TURSO_DATABASE_URL = os.environ.get("TURSO_DATABASE_URL")
TURSO_AUTH_TOKEN = os.environ.get("TURSO_AUTH_TOKEN")

dbUrl = f"sqlite+{TURSO_DATABASE_URL}/?authToken={TURSO_AUTH_TOKEN}&secure=true"

engine = create_engine(
    dbUrl, connect_args={'check_same_thread': False},
    echo=True
)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


class BookBase(SQLModel):
    title: str
    author: Optional[str] = None
    cover: Optional[str] = None
    num_pages: Optional[int] = None
    year_published: Optional[int] = None
    isbn13: Optional[str] = None
    isbn10: Optional[str] = None
    is_awesome: bool = True
    have_read: bool = False


class Book(BookBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class BookCreate(BookBase):
    title: str
    author: Optional[str] = None
    cover: Optional[str] = None
    num_pages: Optional[int] = None
    year_published: Optional[int] = None
    isbn13: Optional[str] = None
    isbn10: Optional[str] = None
    is_awesome: bool = True


class BookUpdate(BookBase):
    title: Optional[str] = None  # type: ignore
    author: Optional[str] = None
    cover: Optional[str] = None
    num_pages: Optional[int] = None
    year_published: Optional[int] = None
    isbn13: Optional[str] = None
    isbn10: Optional[str] = None
    is_awesome: Optional[bool] = None  # type: ignore


class Books(BaseModel):
    books: list[Book]
    count: int

from typing import Annotated, Optional

from fastapi import Depends
from pydantic import BaseModel
from sqlmodel import Field, Session, SQLModel, create_engine


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


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

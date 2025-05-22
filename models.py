from datetime import datetime, timezone
import os
from typing import Annotated, Optional
from uuid import uuid4

from fastapi import Depends
from pydantic import BaseModel
from sqlmodel import Field, Session, SQLModel, create_engine
import asyncio
from sqlalchemy import text
from dotenv import load_dotenv
from urllib.parse import urlparse
from sqlalchemy.ext.asyncio import create_async_engine

from dotenv import load_dotenv

load_dotenv()

NEON_CONN_STR = os.getenv("DATABASE_URL")

if NEON_CONN_STR:
    engine = create_engine(NEON_CONN_STR, echo=True)
else:
    engine = create_engine("sqlite:///database.db", echo=True)


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
    stock: Optional[int] = None


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
    stock: Optional[int] = None


class BookUpdate(BookBase):
    title: Optional[str] = None  # type: ignore
    author: Optional[str] = None
    cover: Optional[str] = None
    num_pages: Optional[int] = None
    year_published: Optional[int] = None
    isbn13: Optional[str] = None
    isbn10: Optional[str] = None
    is_awesome: Optional[bool] = None  # type: ignore
    stock: Optional[int] = None


class Books(BaseModel):
    books: list[Book]
    count: int


# class User(SQLModel):
#     email: str
#     password: str


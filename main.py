# import dialect

from contextlib import asynccontextmanager
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Path, Request, Response, status
from sqlmodel import SQLModel, Session, select
from scalar_fastapi import get_scalar_api_reference
from fastapi.middleware.cors import CORSMiddleware

from models import (
    Book, BookCreate, Books, BookUpdate,
    engine, SessionDep, get_session
)

from v2_routes import v2_api


@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield


app = FastAPI(
    title="LibraryAPI",
    lifespan=lifespan,
    docs_url="/"
)

app.mount("/v2", v2_api)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/scalar", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=app.title,
    )


@app.get("/library", response_model=Books)
async def read_library(
    request: Request,
    session: Session = Depends(get_session)
):
    books = session.exec(select(Book).order_by(Book.id)).all()

    return {
        "books": books,
        "count": len(books)
    }


@app.get("/library/{id}", response_model=Book)
async def read_book(
    request: Request,
    id: Annotated[int, Path(title="id")],
    session: Session = Depends(get_session),
):
    book = session.exec(select(Book).where(Book.id == id)).first()
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book #{id} doesn't exist."
        )

    return book


@app.post("/library/add", response_model=Book)
async def create_book(
    request: Request,
    book: BookCreate,
    session: Session = Depends(get_session),
):
    db_book = Book.model_validate(book)
    session.add(db_book)
    session.commit()
    session.refresh(db_book)
    return db_book


@app.put("/library/{id}")
async def update_book(
    request: Request,
    id: Annotated[int, Path(title="id")],
    req_book: BookUpdate,
    session: Session = Depends(get_session),
):
    db_book = session.exec(select(Book).where(Book.id == id)).first()
    if not db_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book #{id} doesn't exist."
        )

    req_data = req_book.model_dump(exclude_unset=True)
    db_book = db_book.model_copy(update=req_data)
    session.merge(db_book)
    session.commit()
    return db_book


@app.delete("/library/{id}")
async def delete_book(
    request: Request,
    id: Annotated[int, Path(title="id")],
    session: Session = Depends(get_session),
):
    db_book = session.exec(select(Book).where(Book.id == id)).first()
    if not db_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book #{id} doesn't exist."
        )

    session.delete(db_book)
    session.commit()

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )

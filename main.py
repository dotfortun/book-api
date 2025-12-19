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
from v1_routes import v1_api


@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield


app = FastAPI(
    title="LibraryAPI",
    lifespan=lifespan,
    docs_url="/docs"
)

app.mount("/v1", v1_api)
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
        openapi_url=app.openapi_url, # type: ignore
        title=app.title,
    )

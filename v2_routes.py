from fastapi import (
    Depends, FastAPI, HTTPException, Path, Request, Response, status
)

from models import (
    Book, BookCreate, Books, BookUpdate,
    engine, SessionDep, get_session
)

v2_api = FastAPI(
    title="Library API",
)

@v2_api.get("/hello")
def hello():
    return "Hello, world"

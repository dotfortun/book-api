from fastapi import (
    Depends, FastAPI, HTTPException, Path, Request, Response, status
)
from scalar_fastapi import get_scalar_api_reference

from models import (
    Book, BookCreate, Books, BookUpdate,
    engine, SessionDep, get_session
)

v2_api = FastAPI(
    title="Library API",
    docs_url="/",
)

@v2_api.get("/docs", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(
        openapi_url=v2_api.openapi_url, # type: ignore
        title=v2_api.title,
    )

@v2_api.get("/hello")
def hello():
    return "Hello, world"

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from .config import settings
from .core import db
from .routers import api_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version="0.1.1",
    openapi_url="/{{ params['project_name'] }}/openapi.json/",
    docs_url="/{{ params['project_name'] }}/docs/",
    redoc_url="/{{ params['project_name'] }}/redoc/",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)
app.include_router(api_router, prefix=settings.API_V1_STR)
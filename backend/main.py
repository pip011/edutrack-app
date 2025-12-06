import asyncio 

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from .database.db import init_db
from .api.routes.auth import router as auth_router
from .api.routes.users import router as users_router
from .api.routes.groups import router as groups_router
from .api.routes.subjects import router as subjects_router
from .api.routes.grades import router as grades_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db(reset=False)
    yield 

app = FastAPI(lifespan=lifespan)
app.include_router(auth_router, prefix="/api")
app.include_router(users_router, prefix="/api")
app.include_router(groups_router, prefix="/api")
app.include_router(subjects_router, prefix="/api")
app.include_router(grades_router, prefix="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
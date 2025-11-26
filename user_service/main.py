from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from user_service.api.routes.user import router as user_router
from user_service.api.routes.auth import router as auth_router
from user_service.api.routes.language import router as language_router
from user_service.db.mongodb_models import setup_indexes

app = FastAPI()
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(language_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # must be exact
    allow_credentials=True,                   # allow cookies / Authorization headers
    allow_methods=["*"],
    allow_headers=["*"],
)

setup_indexes()

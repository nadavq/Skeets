import os

from dotenv import load_dotenv
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.routes.user import router as user_router
from api.routes.auth import router as auth_router
from api.routes.language import router as language_router
from api.routes.file import router as ai_router
from db.mongodb_models import setup_indexes

load_dotenv()
IS_PROD = os.getenv("ENV") == "production"

app = FastAPI()
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(language_router)
app.include_router(ai_router)
# app.include_router(flash_cards_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://skeets-front-kuuz.vercel.app",
        "https://skeets-front-kuuz.vercel.app/",
        "http://localhost:5173",
        "https://7a01da7e9430.ngrok-free.app",
        "https://zp1v56uxy8rdx5ypatb0ockcb9tr6a-oci3--5173--365214aa.local-credentialless.webcontainer-api.io"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

try:
    setup_indexes()
except Exception as e:
    print(e)

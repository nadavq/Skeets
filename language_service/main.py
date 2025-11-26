from fastapi import FastAPI
from language_service.api.routes.flash_cards import router as flash_cards_router

app = FastAPI()

app.include_router(flash_cards_router)

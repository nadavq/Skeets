from typing import List

from fastapi import APIRouter

from shared.common import user_dep
from shared.schema.flashcards import FlashCardCreate, FlashCardSetRead, FlashCardsSetFromTextCreate
from user_service.services.language_service import LanguageService

router = APIRouter(prefix="/language", tags=["Language"])


@router.get("/flashcards")
async def get_flashcards(user_id: user_dep):
    return await LanguageService().get_flashcards(user_id)


@router.post("/flashcards")
async def create_flashcards(flashcards: List[FlashCardCreate]):
    return await LanguageService().create_flashcards(flashcards)


@router.post("/new-set/{name}")
async def create_new_set(user_id: user_dep, name: str):
    return await LanguageService().create_new_set(user_id, name)


@router.get("/sets", response_model=List[FlashCardSetRead])
async def get_sets(user_id: user_dep):
    return await LanguageService().get_sets(user_id)


@router.post("/flashcard/{set_name}")
async def create_flashcard(user_id: user_dep, set_name: str, flashcard: FlashCardCreate):
    return await LanguageService().create_flashcards(user_id, set_name, [flashcard])


@router.post("/create-set-from-text")
async def create_set_from_text(user_id: user_dep, set_from_text_create: FlashCardsSetFromTextCreate):
    return await LanguageService().create_set_from_text(user_id, set_from_text_create)

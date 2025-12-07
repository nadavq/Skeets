from typing import List

from fastapi import APIRouter

from language_service.db.db import db_dep
from language_service.services.flashcards_service import FlashcardsService
from shared.schema.flashcards.flashcards import UpdateFlashCard, FlashCardRead, FlashCardSet, \
    FlashCardsSetFromTextCreate, FlashCardCreate

router = APIRouter(prefix="/flashcards", tags=["Flashcards"])


@router.get("/flashcards/{user_id}/{set_id}", response_model=List[FlashCardRead])
def get_flashcards_l(user_id: str, set_id: str, db: db_dep):
    return FlashcardsService(db).get_flashcards(user_id, set_id)


@router.post("/new-set/{user_id}/{name}")
def create_new_set(name: str, user_id: str, db: db_dep):
    return FlashcardsService(db).create_new_set(name, user_id)


@router.post("/{user_id}/{set_name}")
def create_flashcards(user_id: str, set_name: str, new_flashcards: List[FlashCardCreate], db: db_dep):
    return FlashcardsService(db).create_flashcards(user_id, set_name, new_flashcards)


@router.get("/sets/{user_id}", response_model=List[FlashCardSet], response_model_by_alias=False)
def get_sets_l(user_id: str, db: db_dep):
    return FlashcardsService(db).get_sets(user_id)


@router.post("/set/from-text/{user_id}", response_model=FlashCardSet)
def create_set_from_text_l(user_id: str, body: FlashCardsSetFromTextCreate, db: db_dep):
    return FlashcardsService(db).create_set_from_text(user_id, body)


@router.put("/{user_id}")
def update_flashcard(user_id: str, update_flashcard_write: UpdateFlashCard, db: db_dep):
    return FlashcardsService(db).update_flashcard(user_id, update_flashcard_write)

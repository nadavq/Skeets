from typing import List

from fastapi import APIRouter

from db.db import db_dep
from shared.common import user_dep
from shared.schema.flashcards.flashcards import UpdateFlashCard, FlashCardCreate, FlashCardSetRead, \
    FlashCardsSetFromTextCreate, FlashCardRead, FlashCardsSetFromWordsCreate
from services.language_service import LanguageService

router = APIRouter(prefix="/language", tags=["Language"])


@router.get("/flashcards/{set_id}", response_model=List[FlashCardRead], response_model_by_alias=False)
def get_flashcards(user_id: user_dep, set_id: str, db: db_dep):
    return LanguageService(db).get_flashcards(user_id, set_id)


@router.post("/new-set/{name}")
def create_new_set(user_id: user_dep, name: str, db: db_dep):
    return LanguageService(db).create_new_set(user_id, name)


@router.get("/sets", response_model=List[FlashCardSetRead], response_model_by_alias=False)
def get_sets(user_id: user_dep, db: db_dep):
    return LanguageService(db).get_sets(user_id)


@router.post("/flashcard/{set_name}")
def create_flashcard(user_id: user_dep, set_name: str, flashcard: FlashCardCreate, db: db_dep):
    return LanguageService(db).create_flashcards(user_id, set_name, [flashcard])


@router.post("/create-set-from-text")
def create_set_from_text(user_id: user_dep, set_from_text_create: FlashCardsSetFromTextCreate, db: db_dep):
    return LanguageService(db).create_set_from_text(user_id, set_from_text_create)


@router.post("/create-set-from-words")
def create_set_from_words(user_id: user_dep, set_from_words_create: FlashCardsSetFromWordsCreate, db: db_dep):
    return LanguageService(db).create_set_from_words(user_id, set_from_words_create)


@router.put("/flashcard/status")
def update_flashcard_status(user_id: user_dep, update_flashcard: UpdateFlashCard, db: db_dep):
    LanguageService(db).update_flashcard_status(user_id, update_flashcard)


@router.delete('/set/{set_id}')
def delete_set(user_id: user_dep, set_id: str, db: db_dep):
    LanguageService(db).delete_set(set_id, user_id)


@router.put('/set')
def edit_set(user_id: user_dep, db: db_dep, set_to_edit: FlashCardSetRead):
    return LanguageService(db).edit_set(user_id, set_to_edit)

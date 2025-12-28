from typing import List

from fastapi import APIRouter

from db.db import db_dep
from services.sets_service import SetsService
from shared.common import user_dep
from shared.schema.flashcards.flashcards import UpdateFlashCard, FlashCardCreate, FlashCardSetRead, \
    FlashCardsSetFromTextCreate, FlashCardRead, FlashCardsSetFromWordsCreate
from services.language_service import LanguageService
from shared.utils.type_utils import to_bool

router = APIRouter(prefix="/language", tags=["Language"])


@router.get("/flashcards/{set_id}/{is_sentences_game}", response_model=List[FlashCardRead], response_model_by_alias=False)
def get_flashcards(user_id: user_dep, set_id: str, db: db_dep, is_sentences_game: bool):
    return LanguageService(db).get_flashcards(user_id, set_id, to_bool(is_sentences_game))


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
    return SetsService(db).create_set_from_text(user_id, set_from_text_create)


@router.post("/create-set-from-words")
def create_set_from_words(user_id: user_dep, set_from_words_create: FlashCardsSetFromWordsCreate, db: db_dep):
    return LanguageService(db).create_set_from_words(user_id, set_from_words_create)


@router.put("/flashcard/status")
def update_flashcard_status(user_id: user_dep, update_flashcard: UpdateFlashCard, db: db_dep):
    LanguageService(db).update_flashcard_status(user_id, update_flashcard)


@router.get('/set/{set_id}')
def delete_set(user_id: user_dep, set_id: str, db: db_dep):
    SetsService(db).get_set(set_id, user_id)


@router.delete('/set/{set_id}')
def delete_set(user_id: user_dep, set_id: str, db: db_dep):
    LanguageService(db).delete_set(set_id, user_id)


@router.put('/set')
def edit_set(user_id: user_dep, db: db_dep, set_to_edit: FlashCardSetRead):
    return LanguageService(db).edit_set(user_id, set_to_edit)


@router.post('/asset-set-from-text')
def create_asset_set_from_text(user_id: user_dep, db: db_dep, set_from_text_create: FlashCardsSetFromTextCreate):
    return LanguageService(db).create_asset_set_from_text(user_id, set_from_text_create)


@router.get('/assets/{set_id}')
def get_assets(user_id: user_dep, db: db_dep, set_id: str):
    return LanguageService(db).get_assets(user_id, set_id)


@router.post('/generate-sentence/{set_id}')
def generate_sentences_from_set(user_id: user_dep, set_id, db: db_dep):
    return LanguageService(db).generate_sentences_from_set(user_id, set_id)

@router.delete('/card/{set_id}/{card_id}')
def delete_card(user_id: user_dep, set_id: str, card_id: str, db: db_dep):
    return LanguageService(db).delete_card(set_id, card_id)
from typing import List

from fastapi import APIRouter

from core.common import user_dep
from db.db import db_dep
from schema.words_explained import WordExplained, WordExplainedCreate
from services.words_explained_service import WordsExplainedService

router = APIRouter(prefix="/words-explained", tags=["Words Explained"])

@router.get("/", response_model=List[WordExplained], response_model_by_alias=False)
def get_words_explained(user_id: user_dep, db: db_dep):
    return WordsExplainedService(db).get_all_words_explained()

@router.post("/")
def add_word_explained(db: db_dep, words_explained: WordExplainedCreate):
    return WordsExplainedService(db).add_word_explained(words_explained)

@router.delete("/{word_id}")
def add_word_explained(db: db_dep, word_id: str):
    return WordsExplainedService(db).delete_word_explained(word_id)
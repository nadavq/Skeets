from typing import List
from services.flashcards_service import FlashcardsService
from shared.schema.flashcards.flashcards import UpdateFlashCard, FlashCardCreate, FlashCardSetRead, \
    FlashCardsSetFromTextCreate, FlashCardRead


class LanguageService:

    def __init__(self, db):
        self.db = db

    def get_flashcards(self, user_id: str, set_id: str) -> List[FlashCardRead]:
        return FlashcardsService(self.db).get_flashcards(user_id, set_id)

    def create_flashcards(self, user_id: str, set_name: str, flashcards: List[FlashCardCreate]):
        return FlashcardsService(self.db).create_flashcards(user_id, set_name, flashcards)

    def create_new_set(self, user_id: str, name: str):
        return FlashcardsService(self.db).create_new_set(name, user_id)

    def get_sets(self, user_id: str) -> List[FlashCardSetRead]:
        return FlashcardsService(self.db).get_sets(user_id)

    def create_set_from_text(self, user_id: str, set_from_text_create: FlashCardsSetFromTextCreate):
        return FlashcardsService(self.db).create_set_from_text(user_id, set_from_text_create)

    def update_flashcard_status(self, user_id: str, update_flashcard: UpdateFlashCard):
        FlashcardsService(self.db).update_flashcard(user_id, update_flashcard)

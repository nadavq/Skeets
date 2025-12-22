from typing import List
from services.sets_service import SetsService
from shared.schema.flashcards.flashcards import UpdateFlashCard, FlashCardCreate, FlashCardSetRead, \
    FlashCardRead, FlashCardsSetFromWordsCreate


class LanguageService:

    def __init__(self, db):
        self.db = db
        self.sets_service = SetsService(db)

    def get_flashcards(self, user_id: str, set_id: str) -> List[FlashCardRead]:
        return self.sets_service.get_flashcards(user_id, set_id)

    def create_flashcards(self, user_id: str, set_name: str, flashcards: List[FlashCardCreate]):
        return self.sets_service.create_flashcards(user_id, set_name, flashcards)

    def create_new_set(self, user_id: str, name: str):
        return self.sets_service.create_new_set(name, user_id)

    def get_sets(self, user_id: str) -> List[FlashCardSetRead]:
        return self.sets_service.get_sets(user_id)

    # def create_set_from_text(self, user_id: str, set_from_text_create: FlashCardsSetFromTextCreate):
    #     return self.flashcards_service.create_set_from_text(user_id, set_from_text_create)

    def update_flashcard_status(self, user_id: str, update_flashcard: UpdateFlashCard):
        self.sets_service.update_flashcard(user_id, update_flashcard)

    def delete_set(self, set_id: str, user_id: str):
        self.sets_service.delete_set(set_id, user_id)

    def edit_set(self, user_id: str, set_to_edit: FlashCardSetRead):
        self.sets_service.edit_set(user_id, set_to_edit)

    def create_set_from_words(self, user_id: str, set_from_words_create: FlashCardsSetFromWordsCreate):
        return self.sets_service.create_set_from_words(user_id, set_from_words_create)


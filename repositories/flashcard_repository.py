from abc import abstractmethod
from typing import List

from bson import ObjectId
from pymongo.results import InsertOneResult

from schema.enums import FlashcardStatus
from schema.flashcards import Flashcard, FlashCardSetRead


class IFlashcardsRepository:
    def __init__(self, db):
        self.db = db
        self.collection = db["flashcards_sets"]

    @abstractmethod
    def get_user_flashcards(self, user_id: str, set_id: str, is_sentences_game):
        pass

    def create_flashcards(self, user_id: str, set_name: str, new_flashcards: List[Flashcard]):
        pass

    def get_set(self, set_id: ObjectId):
        pass

    def create_new_set(self, name: str, user_id: str, flashcards=None) -> InsertOneResult:
        pass

    def get_user_sets(self, user_id: str):
        pass

    def update_flashcard(self, user_id: str, flash_card_id: str, set_id: str, status: FlashcardStatus):
        pass

    def delete_set(self, set_id: str, user_id: str):
        pass

    def edit_set(self, user_id: str, set_to_edit: FlashCardSetRead):
        pass

    def add_flashcards(self, set_id, new_flashcards: List[Flashcard]):
        pass

    def delete_card(self, set_id: str, card_id: str):
        pass

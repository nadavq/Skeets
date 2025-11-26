from abc import abstractmethod
from typing import List

from bson import ObjectId
from pymongo.results import UpdateResult, InsertOneResult

from shared.schema.flashcards import Flashcard


class IFlashcardsRepository:
    def __init__(self, db):
        self.db = db
        self.collection = db["flashcards_sets"]

    @abstractmethod
    def get_user_flashcards(self, user_id: str):
        pass

    def create_flashcards(self, user_id: str, set_name: str, new_flashcards: List[Flashcard]):
        pass

    def get_set(self, set_id: ObjectId):
        pass

    def create_new_set(self, name: str, user_id: str, flashcards=None) -> InsertOneResult:
        pass

    def get_user_sets(self, user_id: str):
        pass

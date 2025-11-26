from typing import List

from fastapi.encoders import jsonable_encoder
from pymongo.results import InsertOneResult

from language_service.core.repositories_dependencies import get_flashcards_repository
from language_service.repositories.flashcard_repository import IFlashcardsRepository
from shared.schema.flashcards import FlashCardCreate, FlashCardSet, FlashCardsSetFromTextCreate
from shared.schema.flashcards import Flashcard


class FlashcardsService:
    def __init__(self, db):
        self.db = db
        self.repo: IFlashcardsRepository = get_flashcards_repository(db)

    def get_flashcards(self, user_id: str):
        flash_cards = self.repo.get_user_flashcards(user_id)
        return flash_cards

    def create_flashcards(self, user_id: str, set_name: str, new_flashcards: List[FlashCardCreate]):
        flashcards: List[Flashcard] = []
        for f in new_flashcards:
            flashcards.append(Flashcard(front=f.front, back=f.back))
        flashcards = self.repo.create_flashcards(user_id, set_name, flashcards)
        return flashcards

    def create_new_set(self, name: str, user_id: str):
        a = self.repo.create_new_set(name, user_id)
        return a

    def get_sets(self, user_id: str) -> List[FlashCardSet]:
        return self.repo.get_user_sets(user_id)

    def create_set_from_text(self, user_id: str, set_from_text_create: FlashCardsSetFromTextCreate) -> FlashCardSet:
        split = set_from_text_create.text.split("\n")
        flashcards = []

        for pair in split:
            flashcard = Flashcard(front=pair[0], back=pair[1])
            flashcards.append(flashcard)

        flashcards_payload = jsonable_encoder(flashcards or [])
        new_set_res: InsertOneResult = self.repo.create_new_set(set_from_text_create.set_name, user_id,
                                                                flashcards_payload)
        new_set = self.repo.get_set(new_set_res.inserted_id)
        return new_set

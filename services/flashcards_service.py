from typing import List

from fastapi.encoders import jsonable_encoder
from pymongo.results import InsertOneResult

from core.repositories_dependencies import get_flashcards_repository
from repositories.flashcard_repository import IFlashcardsRepository
from shared.schema.flashcards.flashcards import UpdateFlashCard, FlashCardCreate, Flashcard, FlashCardSet, \
    FlashCardsSetFromTextCreate, FlashCardRead, FlashCardSetRead


class FlashcardsService:
    def __init__(self, db):
        self.db = db
        self.repo: IFlashcardsRepository = get_flashcards_repository(db)

    def get_flashcards(self, user_id: str, set_id) -> List[FlashCardRead]:
        flash_cards = self.repo.get_user_flashcards(user_id, set_id)
        return list(map(lambda card: FlashCardRead.model_validate(card), flash_cards))

    def create_flashcards(self, user_id: str, set_name: str, new_flashcards: List[FlashCardCreate]):
        flashcards: List[Flashcard] = []
        for f in new_flashcards:
            flashcards.append(Flashcard(front=f.front, back=f.back))
        flashcards = self.repo.create_flashcards(user_id, set_name, flashcards)
        return flashcards

    def create_new_set(self, name: str, user_id: str) -> FlashCardSet:
        new_set_res: InsertOneResult = self.repo.create_new_set(name, user_id)
        return self.repo.get_set(new_set_res.inserted_id)

    def get_sets(self, user_id: str) -> List[FlashCardSetRead]:
        sets = self.repo.get_user_sets(user_id)
        return list(map(lambda fl_set: FlashCardSetRead.model_validate(fl_set), sets))

    def create_set_from_text(self, user_id: str, set_from_text_create: FlashCardsSetFromTextCreate) -> FlashCardSetRead:
        split = set_from_text_create.text.split("\n")
        flashcards = []

        for pair in split:
            pair_split = pair.split(",")
            flashcard = Flashcard(front=pair_split[0], back=pair_split[1])
            flashcards.append(flashcard)

        flashcards_payload = jsonable_encoder(flashcards or [])
        new_set_res: InsertOneResult = self.repo.create_new_set(set_from_text_create.set_name, user_id,
                                                                flashcards_payload)
        new_set = self.repo.get_set(new_set_res.inserted_id)
        return FlashCardSetRead.model_validate(new_set)
        # return new_set

    def update_flashcard(self, user_id: str, update_flashcard_write: UpdateFlashCard):
        self.repo.update_flashcard(user_id, update_flashcard_write.id, update_flashcard_write.set_id,
                                   update_flashcard_write.status)

from typing import List

from bson import ObjectId
from fastapi.encoders import jsonable_encoder
from pymongo.results import InsertOneResult

from core.repositories_dependencies import get_flashcards_repository
from repositories.flashcard_repository import IFlashcardsRepository
from shared.schema.flashcards.flashcards import UpdateFlashCard, FlashCardCreate, Flashcard, FlashCardSet, \
    FlashCardsSetFromTextCreate, FlashCardRead, FlashCardSetRead, FlashCardsSetFromWordsCreate, SentenceInSet
from services.ai_service import AiService


class SetsService:
    def __init__(self, db):
        self.db = db
        self.repo: IFlashcardsRepository = get_flashcards_repository(db)
        self.ai_service = AiService(db)

    def get_flashcards(self, user_id: str, set_id, is_sentences_game) -> List[FlashCardRead]:
        flash_cards = self.repo.get_user_flashcards(user_id, set_id, is_sentences_game)
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
            if not pair:
                continue

            pair_split = pair.split(set_from_text_create.separator)
            flashcard = Flashcard(front=pair_split[1], back=pair_split[0])
            flashcards.append(flashcard)

        flashcards_payload = jsonable_encoder(flashcards or [])
        new_set_res: InsertOneResult = self.repo.create_new_set(set_from_text_create.set_name, user_id,
                                                                flashcards_payload)
        new_set = self.repo.get_set(new_set_res.inserted_id)
        return FlashCardSetRead.model_validate(new_set)

    def update_flashcard(self, user_id: str, update_flashcard_write: UpdateFlashCard):
        self.repo.update_flashcard(user_id, update_flashcard_write.id, update_flashcard_write.set_id,
                                   update_flashcard_write.status)

    def delete_set(self, set_id: str, user_id: str):
        self.repo.delete_set(set_id, user_id)

    def edit_set(self, user_id: str, set_to_edit: FlashCardSetRead):
        self.repo.edit_set(user_id, set_to_edit)

    def create_set_from_words(self, user_id: str, set_from_text_create: FlashCardsSetFromWordsCreate):
        words_for_set = set_from_text_create.words
        set_comma_separated = self.ai_service.translate_words(words_for_set)
        new_set: FlashCardSetRead = self.create_set_from_text(user_id,
                                                              FlashCardsSetFromTextCreate(
                                                                  text=set_comma_separated,
                                                                  set_name=set_from_text_create.set_name))
        return new_set

    def get_set(self, user_id: str, set_id: str):
        set_from_db = self.repo.get_set(ObjectId(set_id))
        if not set_from_db:
            raise Exception(f"Set with id {set_id} was not found.")

        return FlashCardSetRead(**set_from_db)

    def create_set_from_image(self, image_url) -> str:
        return self.ai_service.create_set_from_image(image_url)

    def save_sentences(self, user_id: str, set_id: str, sentences_to_persist: List[SentenceInSet]):
        flashcards_to_persist = [Flashcard(front=sentence.sentence_in_english, back=sentence.sentence_in_russian, is_sentence=True)
             for sentence in sentences_to_persist]
        self.repo.add_flashcards(set_id, flashcards_to_persist)
        pass

    def delete_card(self, set_id: str, card_id: str):
        self.repo.delete_card(set_id, card_id)

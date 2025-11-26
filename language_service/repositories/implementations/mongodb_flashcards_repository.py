from typing import List, Any

from bson import ObjectId
from fastapi.encoders import jsonable_encoder
from pymongo.results import UpdateResult, InsertOneResult

from language_service.repositories.flashcard_repository import IFlashcardsRepository
from shared.schema.flashcards import Flashcard, FlashCardSet, FlashCardRead


class MongoDbFlashcardsRepository(IFlashcardsRepository):

    def get_user_flashcards(self, user_id: str):
        cursor = self.collection.find({'user_id': user_id})
        res = []
        for doc in cursor:
            if 'flashcards' in doc:
                flashcards = doc['flashcards']
                for f in flashcards:
                    res.append(FlashCardRead.model_validate(f))
        return res

    def create_flashcards(self, user_id: str, set_name: str, new_flashcards: List[Flashcard]) -> UpdateResult:
        flashcards_payload = jsonable_encoder(new_flashcards)

        return self.collection.update_one(
            {'name': set_name, 'user_id': user_id},
            {'$set': {'flashcards': flashcards_payload}},
            upsert=True
        )

    def get_set(self, set_id: ObjectId):
        return self.collection.find_one({'_id': set_id})

    def create_new_set(self, name: str, user_id: str, flashcards: Any = None) -> InsertOneResult:
        if flashcards is None:
            flashcards = []

        return self.collection.insert_one({'name': name, 'user_id': user_id, 'flashcards': flashcards})

    def get_user_sets(self, user_id: str):
        cursor = self.collection.find({'user_id': user_id})
        sets = []
        for doc in cursor:
            fc = FlashCardSet(**doc)
            sets.append(fc)
        return sets

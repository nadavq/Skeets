from typing import List, Any

from bson import ObjectId
from fastapi.encoders import jsonable_encoder
from pymongo.results import UpdateResult, InsertOneResult

from repositories.flashcard_repository import IFlashcardsRepository
from shared.schema.flashcards.enums import FlashcardStatus
from shared.schema.flashcards.flashcards import Flashcard, FlashCardSet


class MongoDbFlashcardsRepository(IFlashcardsRepository):

    def get_user_flashcards(self, user_id: str, set_id: str) -> List[Flashcard]:
        cursor = self.collection.find({'user_id': user_id, '_id': ObjectId(set_id)})
        res = []
        for doc in cursor:
            if 'flashcards' in doc:
                flashcards = doc['flashcards']
                for f in flashcards:
                    res.append(Flashcard.model_validate(f))
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

    def get_user_sets(self, user_id: str) -> List[FlashCardSet]:
        cursor = self.collection.find({'user_id': user_id})
        sets = []
        for doc in cursor:
            fc = FlashCardSet(**doc)
            sets.append(fc)
        return sets

    def update_flashcard(self, user_id: str, flash_card_id: str, set_id: str, status: FlashcardStatus):
        status_to_increment = 'num_of_remembers' if status == FlashcardStatus.Remember else 'num_of_learning'
        result = self.collection.update_one(
            {'_id': ObjectId(set_id), 'flashcards._id': flash_card_id},
            {
                '$set': {'flashcards.$.status': status},
                "$inc": {f"flashcards.$.{status_to_increment}": 1}
            }
        )

        print("matched:", result.matched_count, "modified:", result.modified_count)

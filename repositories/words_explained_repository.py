from bson import ObjectId

from schema.words_explained import WordExplained, WordExplainedCreate


class WordsExplainedRepository:

    def __init__(self, db):
        self.db = db
        self.collection = db['words_explained']

    def get_all_words_explained(self) -> list[WordExplained]:
        return self.collection.find()

    def add_word_explained(self, word_explained: WordExplainedCreate):
        self.collection.insert_one(word_explained.model_dump())

    def delete_word_explained(self, word_id: str):
        self.collection.delete_one({'_id': ObjectId(word_id)})
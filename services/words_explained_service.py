from typing import List

from repositories.words_explained_repository import WordsExplainedRepository
from schema.words_explained import WordExplained, WordExplainedCreate
from services.ai_service import AiService


class WordsExplainedService:

    def __init__(self, db):
        self.words_explained_repository = WordsExplainedRepository(db)
        self.ai_service = AiService(db)

    def get_all_words_explained(self) -> List[WordExplained]:
        return self.words_explained_repository.get_all_words_explained()

    def add_word_explained(self, word_explained: WordExplainedCreate):
        if not word_explained.description:
            word_explained.description = self.ai_service.generate_word_description(word_explained.name)
        return self.words_explained_repository.add_word_explained(word_explained)

    def delete_word_explained(self, word_id: str):
        self.words_explained_repository.delete_word_explained(word_id)
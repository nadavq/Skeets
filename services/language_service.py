import base64
from typing import List
from services.file_service import FileService
from services.ai_service import AiService
from services.sets_service import SetsService
from schema.flashcards import UpdateFlashCard, FlashCardCreate, FlashCardSetRead, \
    FlashCardRead, FlashCardsSetFromWordsCreate, FlashCardsSetFromTextCreate, AssetRead, SentenceInSet, AddTextToSet


class LanguageService:

    def __init__(self, db):
        self.db = db
        self.sets_service = SetsService(db)
        self.ai_service = AiService(db)
        self.file_service = FileService(db)

    def get_flashcards(self, user_id: str, set_id: str, is_sentences_game) -> List[FlashCardRead]:
        return self.sets_service.get_flashcards(user_id, set_id, is_sentences_game)

    def create_flashcards(self, user_id: str, set_id: str, flashcards: List[FlashCardCreate]):
        return self.sets_service.create_flashcards(user_id, set_id, flashcards)

    def create_new_set(self, user_id: str, name: str):
        return self.sets_service.create_new_set(name, user_id)

    def get_sets(self, user_id: str) -> List[FlashCardSetRead]:
        sets = self.sets_service.get_sets(user_id)
        sets.sort(key=lambda set: set.id, reverse=True)
        return sets

    def update_flashcard_status(self, user_id: str, update_flashcard: UpdateFlashCard):
        self.sets_service.update_flashcard(user_id, update_flashcard)

    def delete_set(self, set_id: str, user_id: str):
        self.sets_service.delete_set(set_id, user_id)

    def edit_set(self, user_id: str, set_to_edit: FlashCardSetRead):
        self.sets_service.edit_set(user_id, set_to_edit)

    def create_set_from_words(self, user_id: str, set_from_words_create: FlashCardsSetFromWordsCreate):
        return self.sets_service.create_set_from_words(user_id, set_from_words_create)

    def create_asset_set_from_text(self, user_id: str, set_from_text_create: FlashCardsSetFromTextCreate):
        words_in_set = set_from_text_create.text.split('\n')
        for word_pair in words_in_set:
            word_pair_split = word_pair.split(set_from_text_create.separator)
            word_in_russian = word_pair_split[0]
            word_in_english = word_pair_split[1]
            asset = self.ai_service.create_asset_from_word(word_in_english)

            if asset is not None:
                self.file_service.save_asset_to_db(asset, word_in_english, word_in_russian)

        return self.sets_service.create_set_from_text(user_id, set_from_text_create)

    def get_assets(self, user_id: str, set_id: str):
        flashcards: List[FlashCardRead] = self.sets_service.get_flashcards(user_id, set_id, False)
        keywords = list(map(lambda f: f.front, flashcards))
        assets_from_db = self.file_service.get_assets_by_keywords(keywords)
        assets = []

        for asset in assets_from_db:
            assets.append(AssetRead(word_in_english=asset['asset_name_english'], word_in_russian=asset['asset_name_russian'], asset=base64.b64encode(asset["asset_in_bytes"]).decode("utf-8")))

        return assets

    def generate_sentences_from_set(self, user_id: str, set_id: str) -> List[SentenceInSet]:
        set_from_db = self.sets_service.get_set(user_id, set_id)
        words = list(map(lambda f: f.back, set_from_db.flashcards))
        sentences = self.ai_service.generate_sentences(words)

        sentences_to_persist = []
        for sentence in sentences:
            sentence_and_translation = sentence.split(" - ")
            sentence_in_russian = sentence_and_translation[0]
            sentence_in_english = sentence_and_translation[1]
            sentences_to_persist.append(SentenceInSet(sentence_in_english=sentence_in_english, sentence_in_russian=sentence_in_russian))

        self.sets_service.save_sentences(user_id, set_id, sentences_to_persist)
        return sentences_to_persist

    def delete_card(self, set_id: str, card_id: str):
        self.sets_service.delete_card(set_id, card_id)

    def add_text_to_set(self, user_id: str, add_text_to_set: AddTextToSet):
        self.sets_service.add_text_to_set(user_id, add_text_to_set)
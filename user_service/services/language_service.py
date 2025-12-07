from typing import List

from shared.schema.flashcards.flashcards import UpdateFlashCard, FlashCardCreate, FlashCardSetRead, \
    FlashCardsSetFromTextCreate
from user_service.remote.remote_language_service import RemoteLanguageService


class LanguageService:

    async def get_flashcards(self, user_id: str, set_id: str):
        flashcards = await RemoteLanguageService().fetch_flashcards(user_id, set_id)
        return flashcards

    async def create_flashcards(self, user_id: str, set_name: str, flashcards: List[FlashCardCreate]):
        return await RemoteLanguageService().create_flashcards(user_id, set_name, flashcards)

    async def create_new_set(self, user_id: str, name: str):
        return await RemoteLanguageService().create_new_set(name, user_id)

    async def get_sets(self, user_id: str) -> List[FlashCardSetRead]:
        return await RemoteLanguageService().get_sets(user_id)

    async def create_set_from_text(self, user_id: str, set_from_text_create: FlashCardsSetFromTextCreate):
        return await RemoteLanguageService().create_set_from_text(user_id, set_from_text_create)

    async def update_flashcard_status(self, user_id: str, update_flashcard: UpdateFlashCard):
        return await RemoteLanguageService().update_flashcard_status(user_id, update_flashcard)

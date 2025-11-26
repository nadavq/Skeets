from abc import ABC

from language_service.repositories.flashcard_repository import IFlashcardsRepository


class MySqlFlashcardsRepository(IFlashcardsRepository, ABC):
    pass

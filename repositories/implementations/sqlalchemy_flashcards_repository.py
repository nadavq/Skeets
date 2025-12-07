from abc import ABC

from repositories.flashcard_repository import IFlashcardsRepository


class MySqlFlashcardsRepository(IFlashcardsRepository, ABC):
    pass

from enum import Enum

from language_service.repositories.flashcard_repository import IFlashcardsRepository
from language_service.repositories.implementations.mongodb_flashcards_repository import MongoDbFlashcardsRepository
from language_service.repositories.implementations.sqlalchemy_flashcards_repository import MySqlFlashcardsRepository


class DbType(Enum):
    MYSQL = 1
    MONGODB = 2


curr_db_type = DbType.MONGODB


def get_flashcards_repository(db) -> IFlashcardsRepository:
    if curr_db_type == DbType.MONGODB:
        return MongoDbFlashcardsRepository(db)
    else:
        return MySqlFlashcardsRepository(db)


from enum import Enum
from repositories.implementations.mongodb_user_repository import MongoDbUserRepository
from repositories.implementations.mysql_user_repository import MySqlUserRepository
from repositories.user_repository import IUserRepository
from repositories.flashcard_repository import IFlashcardsRepository
from repositories.implementations.mongodb_flashcards_repository import MongoDbFlashcardsRepository
from repositories.implementations.sqlalchemy_flashcards_repository import MySqlFlashcardsRepository

class DbType(Enum):
    MYSQL = 1
    MONGODB = 2


curr_db_type = DbType.MONGODB


def get_user_repository(db) -> IUserRepository:
    if curr_db_type == DbType.MONGODB:
        return MongoDbUserRepository(db)
    else:
        return MySqlUserRepository(db)


def get_flashcards_repository(db) -> IFlashcardsRepository:
    if curr_db_type == DbType.MONGODB:
        return MongoDbFlashcardsRepository(db)
    else:
        return MySqlFlashcardsRepository(db)
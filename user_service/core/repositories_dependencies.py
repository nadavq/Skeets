from enum import Enum
from user_service.repositories.implementations.mongodb_user_repository import MongoDbUserRepository
from user_service.repositories.implementations.mysql_user_repository import MySqlUserRepository
from user_service.repositories.user_repository import IUserRepository


class DbType(Enum):
    MYSQL = 1
    MONGODB = 2


curr_db_type = DbType.MONGODB


def get_user_repository(db) -> IUserRepository:
    if curr_db_type == DbType.MONGODB:
        return MongoDbUserRepository(db)
    else:
        return MySqlUserRepository(db)


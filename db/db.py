import os
from typing import Annotated, Mapping, Any

from dotenv import load_dotenv
from fastapi import Depends
from pymongo.synchronous.database import Database
from sqlalchemy.orm import Session

from pymongo import MongoClient

load_dotenv()
# sqlalchemy_database_url = os.getenv("SQLALCHEMY_DATABASE_URL")
# engine = create_engine(sqlalchemy_database_url, echo=True)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
connection_string = os.getenv("MONGO_URI")
client = MongoClient(connection_string)


def get_db():
    # if curr_db_type == DbType.MONGODB:
    db: Database[Mapping[str, Any]] = client["skeets"]
    yield db
    # else:
    #     db = SessionLocal()
    #     try:
    #         yield db
    #     finally:
    #         db.close()


db_dep = Annotated[Session, Depends(get_db)]

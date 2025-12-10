import os
from typing import Annotated, Mapping, Any

from dotenv import load_dotenv
from fastapi import Depends
from pymongo.synchronous.database import Database
from sqlalchemy.orm import Session

from pymongo import MongoClient

load_dotenv()
connection_string = os.getenv("MONGO_URI")
client = MongoClient(connection_string)


def get_db():
    db: Database[Mapping[str, Any]] = client["skeets"]
    yield db


db_dep = Annotated[Session, Depends(get_db)]

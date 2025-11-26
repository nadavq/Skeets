import os
from typing import Annotated

from dotenv import load_dotenv
from fastapi import Depends
from pymongo import MongoClient
from sqlalchemy.orm import Session

load_dotenv()
connection_string = os.getenv("MONGO_URI")
client = MongoClient(connection_string)


def get_db():
    db = client["skeets_language_service"]
    yield db


db_dep = Annotated[Session, Depends(get_db)]

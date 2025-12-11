from bson import ObjectId
from pymongo.results import InsertOneResult

from schema.file import FileDataCreate


class FileRepository:

    def __init__(self, db):
        self.db = db
        self.collection = db["files"]

    def save_image_to_db(self, file_data: FileDataCreate) -> InsertOneResult:
        return self.collection.insert_one(file_data.model_dump())

    def get_file_by_id(self, file_id: str):
        return self.collection.find_one({"_id": ObjectId(file_id)})

from typing import List

from bson import ObjectId, Binary
from pymongo.results import InsertOneResult

from schema.file import FileDataCreate, AssetDataCreate


class FileRepository:

    def __init__(self, db):
        self.db = db
        self.collection = db["files"]
        self.assets_collection = db["assets"]

    def save_image_to_db(self, file_data: FileDataCreate) -> InsertOneResult:
        return self.collection.insert_one(file_data.model_dump())

    def get_file_by_id(self, file_id: str):
        return self.collection.find_one({"_id": ObjectId(file_id)})

    def save_asset_to_db(self, asset_data_create: AssetDataCreate):
        mongo_doc = {
            "asset_in_bytes": Binary(asset_data_create.asset_in_bytes),
            "asset_name_english": asset_data_create.asset_name_english,
            "asset_name_russian": asset_data_create.asset_name_russian,
        }
        return self.assets_collection.insert_one(mongo_doc)

    def get_assets_by_keywords(self, keywords: List[str]):
        return self.assets_collection.find({"asset_name_english": {"$in": keywords}})

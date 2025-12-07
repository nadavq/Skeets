from bson import ObjectId
from pymongo.results import InsertOneResult

from shared.utils.copy_utils import merge
from user_service.model.user import User
from user_service.repositories.user_repository import IUserRepository


class MongoDbUserRepository(IUserRepository):

    def __init__(self, db):
        super().__init__(db)
        self.collection = db["users"]

    def get_user_from_doc(self, doc):
        user: User = merge(doc, User())
        user.id = str(doc["_id"])
        return user

    def create_user(self, user: User) -> User:
        data = {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "password": user.password,
            "creation_time": user.creation_time,
            "last_update_time": user.last_update_time,
        }
        result: InsertOneResult = self.collection.insert_one(data)
        doc = self.collection.find_one({"_id": result.inserted_id})
        return self.get_user_from_doc(doc)

    def get_user_by_email(self, email: str) -> User | None:
        doc = self.collection.find_one({"email": email})
        if not doc:
            return None
        return self.get_user_from_doc(doc)

    def get_user(self, user_id: str) -> User:
        object_id = ObjectId(str(user_id))

        # Query the collection
        user_document = self.collection.find_one(
            {'_id': object_id}
        )
        # Note: This is a limitation - we can't easily look up by the hashed int ID
        # In a real implementation, you'd want to store the numeric ID in MongoDB
        # For now, this method won't work reliably with MongoDB
        # You'd need to search all documents and match by hash, which is inefficient
        # This is a design limitation when using MongoDB with an int ID requirement
        return self.get_user_from_doc(user_document)
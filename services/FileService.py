import base64

from repositories.file_repository import FileRepository
from schema.file import FileDataCreate, FileDataRead, SetFromImageCreate, FileData
from services.ai_service import AiService
from services.sets_service import SetsService
from services.language_service import LanguageService
from shared.schema.flashcards.flashcards import FlashCardsSetFromTextCreate, FlashCardSetRead


class FileService:

    def __init__(self, db):
        self.db = db
        self.ai_service = AiService(db)
        self.language_service = LanguageService(db)
        self.file_repo = FileRepository(db)
        self.flashcards_service = SetsService(db)

    def create_set_from_file(self, user_id, set_from_image_create: SetFromImageCreate):
        file_id = set_from_image_create.file_id
        file_from_db = self.file_repo.get_file_by_id(file_id)

        if file_from_db is None:
            raise Exception(
                f"File with id {file_id} was not found. Please make sure you uploaded the file first."
            )

        file = FileData(**file_from_db)
        set_comma_separated = self.ai_service.create_set_from_image(file.data_url)
        new_set: FlashCardSetRead = self.flashcards_service.create_set_from_text(user_id,
                                                                               FlashCardsSetFromTextCreate(
                                                                                   text=set_comma_separated,
                                                                                   set_name=set_from_image_create.set_name))
        return new_set

    async def upload_img(self, user_id: str, file):
        image_bytes = await file.read()
        base64_str = base64.b64encode(image_bytes).decode("utf-8")
        data_url = f"data:{file.content_type};base64,{base64_str}"

        saved_file = self.save_file_to_db(FileDataCreate(user_id=user_id, data_url=data_url))
        saved_file = self.file_repo.get_file_by_id(saved_file.inserted_id)
        return FileDataRead(**saved_file)

    def save_file_to_db(self, file_data: FileDataCreate):
        return self.file_repo.save_image_to_db(file_data)

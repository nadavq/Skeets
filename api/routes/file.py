from fastapi import APIRouter, File, UploadFile

from db.db import db_dep
from schema.file import FileDataRead, SetFromImageCreate
from services.FileService import FileService
from services.ai_service import AiService
from shared.common import user_dep

router = APIRouter(prefix="/file", tags=["File"])


@router.post("/upload-img", response_model=FileDataRead, response_model_by_alias=False)
async def upload_img(user_id: user_dep, db: db_dep, file: UploadFile = File(...)):
    return await FileService(db).upload_img(user_id, file)


@router.post("/create-set-from-image")
def create_set_from_file(user_id: user_dep, db: db_dep, file_data: SetFromImageCreate):
    return FileService(db).create_set_from_file(user_id, file_data)


@router.post("/test")
def test(db: db_dep, user_id: user_dep):
    AiService(db).a('wake up')

from pydantic import BaseModel, Field, field_validator

from utils.copy_utils import convert_object_id_to_str


class FileData(BaseModel):
    id: str = Field(..., alias="_id")
    user_id: str
    data_url: str

    model_config = {
        "populate_by_name": True
    }

    @field_validator("id", mode="before")
    def isolate_id(cls, v):
        return convert_object_id_to_str(v)


class FileDataCreate(BaseModel):
    user_id: str
    data_url: str


class AssetDataCreate(BaseModel):
    asset_in_bytes: bytes
    asset_name_english: str
    asset_name_russian: str


class FileDataRead(BaseModel):
    id: str = Field(..., alias="_id")
    user_id: str

    model_config = {
        "populate_by_name": True
    }

    @field_validator("id", mode="before")
    def isolate_id(cls, v):
        return convert_object_id_to_str(v)


class SetFromImageCreate(BaseModel):
    file_id: str = Field(...)
    set_name: str = Field(...)

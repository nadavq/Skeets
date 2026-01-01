from pydantic import BaseModel, field_validator, Field

from utils.copy_utils import convert_object_id_to_str


class WordExplained(BaseModel):
    id: str = Field(alias="_id")
    name: str
    description: str

    @field_validator("id", mode="before")
    def isolate_id(cls, v):
        return convert_object_id_to_str(v)

class WordExplainedCreate(BaseModel):
    name: str
    description: str = Field(default=None)

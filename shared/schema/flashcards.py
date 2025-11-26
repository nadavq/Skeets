from typing import List

from pydantic import BaseModel, Field, field_validator

from shared.utils.copy_utils import convert_object_id_to_str


class Flashcard(BaseModel):
    front: str
    back: str


class FlashCardCreate(BaseModel):
    front: str
    back: str


class FlashCardRead(BaseModel):
    # id: str
    front: str
    back: str

    class Config:
        from_attributes = True


class FlashCardSetCreate(BaseModel):
    name: str
    user_id: str


class FlashCardSet(BaseModel):
    id: str = Field(alias="_id")
    name: str
    user_id: str
    flashcards: List[Flashcard] | None = None

    model_config = {
        "populate_by_alias": True
    }

    @field_validator("id", mode="before")
    def isolate_id(cls, v):
        return convert_object_id_to_str(v)


class FlashCardSetRead(BaseModel):
    id: str = Field(alias="_id")
    name: str
    flashcards: List[FlashCardRead] | None = None

    model_config = {
        "from_attributes": True,
        "populate_by_name": True
    }


class FlashCardsSetFromTextCreate(BaseModel):
    text: str
    set_name: str

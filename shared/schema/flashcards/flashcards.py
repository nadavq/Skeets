from typing import List

from bson import ObjectId
from pydantic import BaseModel, Field, field_validator

from shared.schema.flashcards.enums import FlashcardStatus
from shared.utils.copy_utils import convert_object_id_to_str


class Flashcard(BaseModel):
    id: str = Field(alias="_id", default_factory=lambda: str(ObjectId()))
    front: str
    back: str
    status: FlashcardStatus = Field(default=FlashcardStatus.StillLearning)
    num_of_remembers: int = Field(default=0)
    num_of_learning: int = Field(default=0)
    is_sentence: bool = Field(default=False)

    model_config = {
        "populate_by_name": True
    }


class FlashCardCreate(BaseModel):
    front: str
    back: str


class FlashCardRead(BaseModel):
    id: str = Field(alias="_id")
    front: str
    back: str
    status: FlashcardStatus
    num_of_remembers: int
    num_of_learning: int

    model_config = {
        "from_attributes": True,
        "populate_by_name": True
    }

    @field_validator("id", mode="before")
    def isolate_id(cls, v):
        return convert_object_id_to_str(v)


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

    @field_validator("id", mode="before")
    def isolate_id(cls, v):
        return convert_object_id_to_str(v)


class FlashCardsSetFromTextCreate(BaseModel):
    text: str
    set_name: str
    separator: str = Field(default=",", min_length=1, max_length=1, description="Separator between words in text")


class FlashCardsSetFromWordsCreate(BaseModel):
    words: str
    set_name: str


class UpdateFlashCard(BaseModel):
    id: str
    status: FlashcardStatus
    set_id: str


class AssetRead(BaseModel):
    word_in_english: str
    word_in_russian: str
    asset: str


class SentenceInSet(BaseModel):
    sentence_in_english: str
    sentence_in_russian: str

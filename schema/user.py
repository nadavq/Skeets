from pydantic import BaseModel, Field, EmailStr

from schema.enums import FlashcardSide


class UserCreate(BaseModel):
    first_name: str = Field(..., min_length=2, max_length=16, description="First name of user")
    last_name: str = Field(..., min_length=2, max_length=16, description="Last name of user")
    password: str = Field(..., min_length=8, max_length=32, description="Password of user")
    email: EmailStr = Field(..., description="Email of user")


class UserRead(BaseModel):
    id: str
    first_name: str
    last_name: str
    email: str
    flashcard_side: str = Field(default=FlashcardSide.Regular)

    class Config:
        from_attributes = True


class UserEdit(BaseModel):
    flashcards_side: str = Field(default=FlashcardSide.Regular)
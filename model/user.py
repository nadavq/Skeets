import datetime

from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from base import Base
from schema.enums import FlashcardSide


class User(Base):
    __tablename__ = 'users'

    id: Mapped[str] = mapped_column(String, primary_key=True)
    creation_time: Mapped[DateTime] = mapped_column(DateTime, nullable=False, default=datetime.datetime.now)
    last_update_time: Mapped[DateTime] = mapped_column(DateTime, nullable=False, default=datetime.datetime.now,
                                                       onupdate=datetime.datetime.now)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String, nullable=False)
    flashcards_side: Mapped[str] = mapped_column(String, default=FlashcardSide.Regular)

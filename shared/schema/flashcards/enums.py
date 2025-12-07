from enum import Enum


class FlashcardStatus(str, Enum):
    Remember = "Remember"
    StillLearning = "StillLearning"

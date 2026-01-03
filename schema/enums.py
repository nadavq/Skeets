from enum import Enum


class FlashcardStatus(str, Enum):
    Remember = "Remember"
    StillLearning = "StillLearning"


class FlashcardSide(str, Enum):
    Regular = "Regular"
    Reversed = "Reversed"
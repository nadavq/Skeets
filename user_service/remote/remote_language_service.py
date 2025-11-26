import os
from typing import List
import httpx
from dotenv import load_dotenv
from pydantic import TypeAdapter
from fastapi.encoders import jsonable_encoder

from shared.schema.flashcards import FlashCardCreate, FlashCardSet, FlashCardSetRead, FlashCardRead, \
    FlashCardsSetFromTextCreate

load_dotenv()
LANGUAGE_SERVICE_BASE_URL = os.environ.get("LANGUAGE_SERVICE_BASE_URL")


class RemoteLanguageService:

    def __init__(self):
        self.base_url = LANGUAGE_SERVICE_BASE_URL

    async def fetch_flashcards(self, user_id) -> List[FlashCardRead]:
        async with httpx.AsyncClient(timeout=30.0) as client:
            flashcards = await client.get(f"{LANGUAGE_SERVICE_BASE_URL}/flashcards/{user_id}")
            flashcards.raise_for_status()
            flashcards = flashcards.json()

            adapter = TypeAdapter(List[FlashCardRead])
            return adapter.validate_python(flashcards)

    async def create_flashcards(self, user_id: str, set_name: str, flashcards: List[FlashCardCreate]):
        payload = jsonable_encoder(flashcards)

        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                flashcards = await client.post(f"{LANGUAGE_SERVICE_BASE_URL}/flashcards/{user_id}/{set_name}",
                                               json=payload)
                print(flashcards)
            except Exception as e:
                print(e)

    async def create_new_set(self, name: str, user_id: str):
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                await client.post(f"{LANGUAGE_SERVICE_BASE_URL}/flashcards/new-set/{user_id}/{name}")
            except Exception as e:
                print(e)
        pass

    async def get_sets(self, user_id: str) -> List[FlashCardSetRead]:
        async with httpx.AsyncClient(timeout=30.0) as client:
            sets = await client.get(f"{LANGUAGE_SERVICE_BASE_URL}/flashcards/sets/{user_id}")
            sets.raise_for_status()

            sets_read = []

            for s in sets.json():
                sets_read.append(FlashCardSetRead.model_validate(s))

            return sets_read

    async def create_set_from_text(self, user_id: str,
                                   set_from_text_create: FlashCardsSetFromTextCreate) -> FlashCardSet:
        async with httpx.AsyncClient(timeout=30.0) as client:
            new_set = await client.post(f"{LANGUAGE_SERVICE_BASE_URL}/flashcards/set/from-text/{user_id}",
                                        json=set_from_text_create.model_dump())
            new_set.raise_for_status()

            d = FlashCardSet.model_validate(new_set.json())
            return d

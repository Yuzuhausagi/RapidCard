from pydantic import BaseModel, Field


class FlashCard(BaseModel):
    word: str
    definition: str


class Difficulty(BaseModel):
    difficulty: str = Field(...)

from pydantic import BaseModel


class FlashCard(BaseModel):
    word: str
    definition: str

from dataclasses import dataclass


@dataclass
class FlashCard:
    display_word: str
    answer: str

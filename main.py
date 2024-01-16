from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from models import FlashCard
import random


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

simple_words = [
    "apple",
    "ball",
    "cat",
    "dog",
    "egg",
    "fish",
    "goat",
    "hat",
    "ice",
    "juice",
    "kite",
    "lion",
    "mouse",
    "nut",
    "orange",
    "pig",
    "queen",
    "rose",
    "sun",
    "tree",
    "umbrella",
    "vase",
    "water",
    "x-ray",
    "yarn",
    "zebra",
]

db = {
    "車": "car",
    "上": "up",
    "下": "down",
    "侍": "samurai",
    "家族": "family",
    "右": "right",
    "左": "left",
    "恋人": "lover",
    "炎": "flame",
    "銀行": "bank",
}


@app.get("/")
async def root():
    random_word = random.choice(list(db.keys()))
    return RedirectResponse(f"/{random_word}")


@app.get("/healthcheck/{test_param_example}")
def health(request: Request, test_param_example: str):
    return {"example": test_param_example}


@app.get("/{test_word}", response_class=HTMLResponse)
async def test_word(request: Request, test_word: str):
    random_falseword = random.choice(simple_words)
    random_falseword2 = random.choice(simple_words)

    answer = db[test_word]
    guess_options = [random_falseword, random_falseword2, answer]
    random.shuffle(guess_options)

    return templates.TemplateResponse(
        request=request,
        name="item.html",
        context={"test_word": test_word, "guess_options": guess_options},
    )

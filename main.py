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

correct_answers = 0
wrong_answers = 0


wrong_counter = {}


@app.post("/api/word/")
async def addword(request: Request, formData: FlashCard):
    db[formData.word] = formData.definition
    print(db)


@app.get("/newpage")
async def add_word_page(request: Request, reponse_class=HTMLResponse):
    return templates.TemplateResponse(
        request=request,
        name="newpage.html",
    )


@app.get("/api/reset")
def resetSession(request: Request):
    global correct_answers
    global wrong_answers
    correct_answers = 0
    wrong_answers = 0


@app.get("/api/guess/{current_word}/{guess}")
def checker(request: Request, guess: str, current_word):
    global correct_answers
    global wrong_answers

    answer = db[current_word]

    for key in db.keys():
        wrong_counter[key] = 0

    if guess == answer:
        print(f"{current_word} {guess}")
        correct_answers += 1
    else:
        wrong_answers += 1

    return {
        "isCorrect": guess == answer,
        "wrong_answers": wrong_answers,
        "correct_answers": correct_answers,
    }


@app.get("/")
async def root():
    # multiple_occurrences = False
    # for occurrences in wrong_counter.values():
    #     if occurrences > 1:
    #         failed_word = random.choice(list(wrong_counter.keys()))
    #         multiple_occurrences = True
    #         break
    #     else:
    #         random_word = random.choice(list(db.keys()))
    #
    # if multiple_occurrences:
    #     failed_word = random.choice(list(wrong_counter.keys()))
    # else:
    #     random_word = random.choice(list(db.keys()))
    #
    # selected_word = failed_word if multiple_occurrences else random_word
    random_word = random.choice(list(db.keys()))
    return RedirectResponse(f"/{random_word}")


@app.get("/healthcheck/{test_param_example}")
def health(request: Request, test_param_example: str):
    return {"example": test_param_example}


# http://127.0.0.1:1337/favicon.ico
@app.get("/{test_word}", response_class=HTMLResponse)
async def test_word(request: Request, test_word: str):
    if test_word == "favicon.ico":
        return None

    print(test_word)
    random_falseword = random.choice(simple_words)
    random_falseword2 = random.choice(simple_words)

    answer = db[test_word]
    guess_options = [random_falseword, random_falseword2, answer]
    random.shuffle(guess_options)
    print(correct_answers, wrong_answers)
    return templates.TemplateResponse(
        request=request,
        name="item.html",
        context={
            "test_word": test_word,
            "guess_options": guess_options,
            "correct_answers": correct_answers,
            "wrong_answers": wrong_answers,
        },
    )

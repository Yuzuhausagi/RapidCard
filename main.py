from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from models import FlashCard, Difficulty
import random


# TODO: implement difficulty, hard mode = button locked on wrong or right. Easy  mode = no locks
# TODO: Do some testing next time

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
current_difficulty = "easy"

wrong_counter = {}

for key in db.keys():
    wrong_counter[key] = 0


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


@app.post("/api/setDifficulty")
def setDifficulty(formData: Difficulty):
    global current_difficulty
    current_difficulty = formData.difficulty
    print(formData.difficulty)


@app.get("/api/guess/{current_word}/{guess}")
def checker(request: Request, guess: str, current_word):
    global correct_answers
    global wrong_answers

    answer = db[current_word]

    if guess == answer:
        correct_answers += 1
        wrong_counter[current_word] -= 1
    else:
        wrong_answers += 1
        wrong_counter[current_word] += 1

    return {
        "isCorrect": guess == answer,
        "wrong_answers": wrong_answers,
        "correct_answers": correct_answers,
        "current_difficulty": current_difficulty,
    }


@app.get("/healthcheck/{test_param_example}")
def health(request: Request, test_param_example: str):
    return {"example": test_param_example}


# http://127.0.0.1:1337/favicon.ico
@app.get("/", response_class=HTMLResponse)
async def test_word(request: Request):
    resulting_word = "ERROR"

    max_wrong_count = max(wrong_counter.values()) if wrong_counter else 0
    print(wrong_counter)
    print(max_wrong_count)
    for word, count in wrong_counter.items():
        if count == max_wrong_count:
            resulting_word = word
            print(f"Word with most wrong guesses: {word}, guessed wrong {count} times")

    random_falseword = random.choice(simple_words)
    random_falseword2 = random.choice(simple_words)
    random_falseword3 = random.choice(simple_words)
    random_falseword4 = random.choice(simple_words)
    random_falseword5 = random.choice(simple_words)
    random_falseword6 = random.choice(simple_words)
    random_falseword7 = random.choice(simple_words)
    random_falseword8 = random.choice(simple_words)
    random_falseword9 = random.choice(simple_words)
    x = random.randint(0, 1)

    print(resulting_word)

    if x == 0:
        other_word = random.choice(list(db.keys()))
        resulting_word = other_word

    guess_options = []
    answer = db[resulting_word]
    if current_difficulty == "hard":
        guess_options = [
            random_falseword,
            random_falseword2,
            random_falseword3,
            random_falseword4,
            random_falseword5,
            random_falseword6,
            random_falseword7,
            random_falseword8,
            random_falseword9,
            answer,
        ]
        random.shuffle(guess_options)
    elif current_difficulty == "medium":
        guess_options = [
            random_falseword,
            random_falseword2,
            random_falseword3,
            random_falseword4,
            random_falseword5,
            random_falseword6,
            answer,
        ]
        random.shuffle(guess_options)
    else:
        guess_options = [random_falseword, random_falseword2, random_falseword3, answer]
        random.shuffle(guess_options)

    print(f' "correct"{correct_answers},"Wrong" {wrong_answers}')
    return templates.TemplateResponse(
        request=request,
        name="item.html",
        context={
            "test_word": resulting_word,
            "guess_options": guess_options,
            "correct_answers": correct_answers,
            "wrong_answers": wrong_answers,
            "current_difficulty": current_difficulty,
        },
    )

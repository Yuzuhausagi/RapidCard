from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from models import FlashCard, Difficulty
import random
import pymongo


# TODO: Put everything stored in the backend to a database. Work on user sessions
# TODO: Styling happens in the end.


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

client = pymongo.MongoClient("localhost", 27017)
zxc = client.words
collection = zxc["false_words"]
data = collection.find()
simple_words = []
for i, v in enumerate(data):
    simple_words.append(v[str(i)])

collection1 = zxc["Japanese_Answer"]

jpwords = {}
data1 = collection1.find()
for d in data1:
    keys = d.keys()
    char = list(keys)[1]
    v = d[char]
    jpwords[char] = v


correct_answers = 0
wrong_answers = 0
current_difficulty = "easy"

wrong_counter = {}

for key in jpwords.keys():
    wrong_counter[key] = 0


@app.post("/api/word/")
async def addword(request: Request, formData: FlashCard):
    jpwords[formData.word] = formData.definition
    print(jpwords)


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

    answer = jpwords[current_word]

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
        "answer": answer,
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

    x = random.randint(0, 1)

    print(resulting_word)

    if x == 0:
        other_word = random.choice(list(jpwords.keys()))
        resulting_word = other_word

    guess_options = []
    answer = jpwords[resulting_word]
    random.shuffle(simple_words)

    if current_difficulty == "hard":
        for i in range(10):
            guess_options.append(simple_words[i])

    elif current_difficulty == "medium":
        for i in range(6):
            guess_options.append(simple_words[i])

    else:
        for i in range(3):
            guess_options.append(simple_words[i])
    guess_options.append(answer)
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

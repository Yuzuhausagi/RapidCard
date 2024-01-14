from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/healthcheck/{test_param_example}")
def health(request: Request, test_param_example: str):
    return {"example": test_param_example}

@dataclasses
class GuessWord:
    word: str
    answer: str
    guesses: list

@app.get("/items/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str):
    print(id)
    guess_word = "example word"
    # car, up, down, samurai, family, right, left, lover/girlfriend/boyfriend/sweetheart,flame,
    japanese_words = ["車", "上", "下", "侍", "家族", "右", "左", "恋人", "炎", "銀行"]
    dict = {}
    guess_options = [dict[id], ]
    return templates.TemplateResponse(
        request=request, name="item.html", context={"id": id, "guess_options": guess_options}
    )
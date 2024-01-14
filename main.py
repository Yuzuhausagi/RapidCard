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


@app.get("/test", response_class=HTMLResponse)
async def read_item(request: Request):
    my_list = ["apple", "pear", "please work?"]
    return {"example": "asdasdasd"}
    # return templates.TemplateResponse(
    #     request=request, name="test.html", context={"myList": my_list}
    # )


@app.get("/items/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str):
    print(id)
    my_list = ["apple", "pear", "please work?"]
    return templates.TemplateResponse(
        request=request, name="item.html", context={"id": id, "my": my_list}
    )
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseSettings

app = FastAPI()
templates = Jinja2Templates(directory="fastapi_blog/templates")
app.mount("/static/css", StaticFiles(directory="fastapi_blog/static/css"), name="css")
app.mount("/static/js", StaticFiles(directory="fastapi_blog/static/js"), name="js")
app.mount("/static/img", StaticFiles(directory="fastapi_blog/static/img"), name="img")
app.mount(
    "/static/webfonts",
    StaticFiles(directory="fastapi_blog/static/webfonts"),
    name="webfonts",
)


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/index", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})


@app.get("/contact", response_class=HTMLResponse)
def contact(request: Request):
    return templates.TemplateResponse("contact.html", {"request": request})


@app.get("/post", response_class=HTMLResponse)
def post(request: Request):
    return templates.TemplateResponse("post.html", {"request": request})


if __name__ == "__main__":
    uvicorn.run("fastapi_blog:app")

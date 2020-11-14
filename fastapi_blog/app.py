import os

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from fastapi_blog.models import database, fetch_post, posts
from fastapi_blog.utils import init_db

templates = Jinja2Templates(directory="fastapi_blog/templates")


def get_app() -> FastAPI:
    app = FastAPI()
    app.mount("/static", StaticFiles(directory="fastapi_blog/static"), name="static")
    return app


app = get_app()


@app.on_event("startup")
async def startup():
    await database.connect()
    if os.environ.get("INIT_DB"):
        await init_db()


@app.on_event("shutdown")
async def shutdown():
    query = posts.delete()
    await database.execute(query)
    await database.disconnect()


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/index", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})


@app.get("/post", response_class=HTMLResponse)
async def post(request: Request):
    post = await fetch_post(1)
    print(post)
    return templates.TemplateResponse("post.html", {"request": request, "post": post})


@app.get("/post/{post_id}", response_class=HTMLResponse)
async def post_by_id(request: Request, post_id: int):
    post = await fetch_post(post_id)
    return templates.TemplateResponse("post.html", {"request": request, "post": post})


if __name__ == "__main__":
    uvicorn.run("fastapi_blog.app:app")

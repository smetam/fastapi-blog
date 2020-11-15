import os

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from fastapi_blog.models import database  # fetch_tags, fetch_tags
from fastapi_blog.models import fetch_post, fetch_posts
from fastapi_blog.utils import get_context, init_db, teardown_db

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
        await teardown_db()
        await init_db()


@app.on_event("shutdown")
async def shutdown():
    if os.environ.get("TEARDOWN_DB"):
        await teardown_db()
    await database.disconnect()


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    context = get_context(request)
    return templates.TemplateResponse("index.html", context)


@app.get("/index", response_class=HTMLResponse)
async def index(request: Request):
    posts = await fetch_posts()
    context = get_context(request, posts=posts)
    return templates.TemplateResponse("index.html", context)


@app.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    context = get_context(request)
    return templates.TemplateResponse("about.html", context)


@app.get("/post", response_class=HTMLResponse)
async def post(request: Request):
    post = await fetch_post()
    context = get_context(request, post=post)
    return templates.TemplateResponse("post.html", context)


@app.get("/post/{post_id:int}", response_class=HTMLResponse)
async def post(request: Request, post_id: int):
    post = await fetch_post(post_id)
    context = get_context(request, post=post)
    return templates.TemplateResponse("post.html", context)


# @app.get("/tag/{tag_id:int}", response_class=HTMLResponse)
# async def tag(request: Request, tag_id: int):
#     post = await fetch_tag(tag_id)
#     return templates.TemplateResponse("post.html", {"request": request, "post": post})


if __name__ == "__main__":
    uvicorn.run("fastapi_blog.app:app")

import os

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from fastapi_blog.core import get_context, init_db, teardown_db
from fastapi_blog.models import (
    database,
    fetch_last_post_id,
    fetch_post,
    fetch_posts,
    fetch_posts_by_tag,
    fetch_tag,
    fetch_tags,
)

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


@app.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    context = get_context(request)
    return templates.TemplateResponse("about.html", context)


@app.get("/contact", response_class=HTMLResponse)
async def contact(request: Request):
    context = get_context(request)
    return templates.TemplateResponse("contact.html", context)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    context = get_context(request, page=-1)
    return templates.TemplateResponse("home.html", context)


@app.get("/index", response_class=HTMLResponse)
async def index(request: Request):
    context = get_context(request, page=-1)
    return templates.TemplateResponse("home.html", context)


@app.get("/posts/{page:int}", response_class=HTMLResponse)
async def posts(request: Request, page: int = 0):
    items_per_page = 3
    posts = await fetch_posts(offset=page * items_per_page, limit=items_per_page)
    context = get_context(request, posts=posts, page=page)
    return templates.TemplateResponse("posts.html", context)


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


@app.get("/tags", response_class=HTMLResponse)
async def tags(request: Request):
    # TODO: tags page
    tags = await fetch_tags()
    return templates.TemplateResponse("tags.html", get_context(request, tags=tags))


@app.get("/tag/{tag_id:int}", response_class=HTMLResponse)
async def tag(request: Request, tag_id: int):
    tag = await fetch_tag(tag_id)
    return templates.TemplateResponse(
        "tag.html", get_context(request, tag=tag, page=-1)
    )


@app.get("/tag/{tag_id:int}/{page:int}", response_class=HTMLResponse)
async def tag(request: Request, tag_id: int, page: int = 0):
    items_per_page = 3
    posts = await fetch_posts_by_tag(
        tag_id, offset=page * items_per_page, limit=items_per_page
    )
    return templates.TemplateResponse(
        "tag_posts.html", get_context(request, tag_id=tag_id, posts=posts, page=page)
    )


if __name__ == "__main__":
    uvicorn.run("fastapi_blog.app:app")

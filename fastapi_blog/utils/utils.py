import datetime
import json
from collections import namedtuple
from typing import Any, Dict, Union

from fastapi import Request
from fastapi.templating import Jinja2Templates

from fastapi_blog import INIT_DATA_PATH
from fastapi_blog.models import database, post_tags, posts, tags

reusable_templates = Jinja2Templates(directory="fastapi_blog/templates/reusable")
Reusable = namedtuple("Reusable", ("head", "navbar", "footer", "scripts"))


def parse_date(date_str):
    try:
        return datetime.datetime.fromisoformat(date_str)
    except ValueError:
        return datetime.datetime.now()


def datetime_parser(dct: Dict[Union[str, int], Any]) -> Dict[Union[str, int], Any]:
    for key, val in dct.items():
        if isinstance(val, dict):
            dct[key] = datetime_parser(val)
        elif key in ["date", "datetime"]:
            dct[key] = parse_date(val)
    return dct


async def init_db():
    with open(INIT_DATA_PATH) as f:
        init_data = json.load(f, object_hook=datetime_parser)
    table_by_name = {"posts": posts, "tags": tags, "post_tags": post_tags}
    for table_name, inserts in init_data.items():
        table = table_by_name[table_name]
        query = table.insert().values(inserts)
        await database.execute(query)


async def teardown_db():
    for table in [posts, tags, post_tags]:
        query = table.delete()
        await database.execute(query)


def get_reusable(request: Request) -> Reusable:
    head = reusable_templates.TemplateResponse("head.html", {"request": request})
    footer = reusable_templates.TemplateResponse("footer.html", {"request": request})
    navbar = reusable_templates.TemplateResponse("navbar.html", {"request": request})
    scripts = reusable_templates.TemplateResponse("scripts.html", {"request": request})
    return Reusable(
        *[item.body.decode("utf-8") for item in (head, navbar, footer, scripts)]
    )


def get_context(request: Request, **kwargs) -> Dict[str, Any]:
    reusable = get_reusable(request)
    context = {"request": request, "reusable": reusable, **kwargs}
    return context

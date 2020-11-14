import datetime
import json
from typing import Any, Dict, Union

from fastapi_blog import CONFIG
from fastapi_blog.models import database, posts


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
    with open(CONFIG) as f:
        init_posts = json.load(f, object_hook=datetime_parser)["init_posts"]

    query = posts.insert().values(init_posts)
    await database.execute(query)

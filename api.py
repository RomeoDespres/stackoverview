from contextlib import closing
import functools
import json
from typing import Any, Callable, Dict, List

from typing import TypedDict

import db


class Response(TypedDict):
    statusCode: int
    body: str


def get(f: Callable) -> Callable:
    @functools.wraps(f)
    def wrapped(event: dict = {}, context: Any = None) -> Response:
        result = f()
        return {
            "statusCode": 200,
            "body": json.dumps(result),
        }

    return wrapped


@get
def tag_reputation() -> Dict[str, List]:
    with closing(db.get_connection()) as connection:
        with connection.cursor() as cursor:
            cursor.execute(db.get_sql("get_tags_reputation"))
            columns = [description[0] for description in cursor.description]
            rows = cursor.fetchall()
    return {
        "tags": [
            {column: value for column, value in zip(columns, row)}
            for row in rows
        ]
    }

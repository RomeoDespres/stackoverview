from contextlib import closing
import functools
import json
from typing import Any, Callable, Dict, List, Union

import humps

import db


def get(f: Callable) -> Callable:
    @functools.wraps(f)
    def wrapped(event: dict = {}, context: Any = None) -> Dict[str, Any]:
        result = f()
        return {
            "statusCode": 200,
            "body": json.dumps(humps.camelize(result)),
        }

    return wrapped


@get
def tag_reputation() -> Dict[str, Union[List, float]]:
    params = {"limit": 20, "offset": 0}
    sql = "select * from tag_reputation limit %(limit)s offset %(offset)s"
    with closing(db.get_connection()) as connection:
        with connection.cursor() as cursor:
            cursor.execute(sql, params)
            columns = [description[0] for description in cursor.description]
            rows = cursor.fetchall()
            cursor.execute("select * from avg_answer_reputation")
            avg_reputation = cursor.fetchone()[0]
    return {
        "tags": [
            {column: value for column, value in zip(columns, row)}
            for row in rows
        ],
        "avg_reputation": avg_reputation,
    }

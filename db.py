import os
from pathlib import Path
from typing import Iterable, TypedDict

import psycopg2
from psycopg2.extensions import connection as PostgresConnection


class PostgreSQLCredentials(TypedDict):
    host: str
    port: int
    database: str
    user: str
    password: str


def create_tables(connection: PostgresConnection) -> None:
    """Create empty tables in database."""
    with connection.cursor() as cursor:
        for sql in get_sql_script("create_tables"):
            cursor.execute(sql)
    connection.commit()


def get_connection() -> PostgresConnection:
    """Return database connection."""
    return psycopg2.connect(**get_credentials())


def get_credentials() -> PostgreSQLCredentials:
    """Return database credentials."""
    return {
        "host": os.environ["POSTGRES_HOST"],
        "port": int(os.environ["POSTGRES_PORT"]),
        "database": os.environ["POSTGRES_DB"],
        "user": os.environ["POSTGRES_USER"],
        "password": os.environ["POSTGRES_PASSWORD"],
    }


def get_sql(name: str) -> str:
    name += ".sql"
    sql_dir = Path(__file__).absolute().parent / "sql"
    return (sql_dir / name).read_text()


def get_sql_script(name: str) -> Iterable[str]:
    script = get_sql(name)
    yield from filter(bool, map(str.strip, script.split(";")))

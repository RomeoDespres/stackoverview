import datetime as dt
from typing import Any, Iterable, Tuple

from psycopg2.extensions import cursor as PostgresCursor
from psycopg2.extras import execute_batch

from client import APIClient, Answers, User, Questions
import db
import log


def fetch_last_30_days() -> Tuple[Questions, Answers]:
    end = dt.datetime.now()
    start = end - dt.timedelta(seconds=30 * 24 * 60 * 60)
    api_client = APIClient()
    questions = api_client.questions(start=start, end=end)
    answers = api_client.answers(questions)
    return questions, answers


def run(event: Any = None, context: Any = None) -> None:
    logger = log.get_logger()

    logger.info("Running ETL")
    questions, answers = fetch_last_30_days()
    upload_data(questions, answers)
    logger.info("ETL ran successfully")


def upload_accepted_answers(
    questions: Questions, cursor: PostgresCursor
) -> None:
    logger = log.get_logger()
    logger.info("Uploading accepted answers")

    def iter_answers() -> Iterable[dict]:
        for question in questions["items"]:
            if question.get("accepted_answer_id") is not None:
                yield {
                    "question_id": question["question_id"],
                    "answer_id": question["accepted_answer_id"],
                }

    execute_batch(cursor, db.get_sql("upsert_accepted_answer"), iter_answers())


def upload_answers(answers: Answers, cursor: PostgresCursor) -> None:
    logger = log.get_logger()
    logger.info("Uploading answers")

    def iter_answers() -> Iterable[dict]:
        for answer in answers["items"]:
            yield {**answer, "owner_id": answer["owner"].get("user_id")}

    execute_batch(cursor, db.get_sql("upsert_answer"), iter_answers(), 1000)


def upload_data(questions: Questions, answers: Answers) -> None:
    with db.get_connection() as connection:
        with connection.cursor() as cursor:
            upload_users(questions, answers, cursor)
            upload_questions(questions, cursor)
            upload_answers(answers, cursor)
            upload_accepted_answers(questions, cursor)


def upload_questions(questions: Questions, cursor: PostgresCursor) -> None:
    logger = log.get_logger()
    logger.info("Uploading questions")
    items = questions["items"]

    def iter_questions() -> Iterable[dict]:
        for question in items:
            yield {**question, "owner_id": question["owner"].get("user_id")}

    execute_batch(
        cursor, db.get_sql("upsert_question"), iter_questions(), 1000
    )

    logger.info("Uploading tags")
    tags = {(tag,) for question in items for tag in question["tags"]}
    execute_batch(cursor, db.get_sql("upsert_tag"), tags)

    def iter_question_tags() -> Iterable[dict]:
        for question in items:
            question_id = question["question_id"]
            for tag in question["tags"]:
                yield {"question_id": question_id, "tag_id": tag}

    logger.info("Uploading question tags")
    delete, insert = db.get_sql_script("upsert_question_tag")
    question_ids = tuple({question["question_id"] for question in items})
    cursor.execute(delete, (question_ids,))
    execute_batch(cursor, insert, iter_question_tags(), 10000)


def upload_users(
    questions: Questions, answers: Answers, cursor: PostgresCursor
) -> None:
    logger = log.get_logger()
    logger.info("Uploading users")

    def iter_users() -> Iterable[User]:
        for question in questions["items"]:
            if question["owner"].get("user_id") is not None:
                yield question["owner"]
        for answer in answers["items"]:
            if answer["owner"].get("user_id") is not None:
                yield answer["owner"]

    execute_batch(cursor, db.get_sql("upsert_account"), iter_users(), 1000)

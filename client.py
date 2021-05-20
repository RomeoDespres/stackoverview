from __future__ import annotations

from contextlib import contextmanager
import datetime as dt
import logging
import os
from queue import Queue
import time
from typing import Any, Dict, List, Literal, Iterator, Optional, TypedDict

import requests
from requests.exceptions import ConnectionError
from requests_toolbelt.sessions import BaseUrlSession


class Answer(TypedDict):
    owner: User
    is_accepted: bool
    score: int
    last_activity_date: int
    creation_date: int
    answer_id: int
    question_id: int
    content_license: str


class Answers(TypedDict):
    has_more: bool
    quota_max: int
    quota_remaining: int
    items: List[Answer]


class Question(TypedDict):
    tags: List[str]
    owner: User
    is_answered: bool
    accepted_answer_id: Optional[int]
    view_count: int
    answer_count: int
    score: int
    last_activity_date: int
    creation_date: int
    last_edit_date: int
    question_id: int
    content_license: str
    link: str
    title: str


class Questions(TypedDict):
    has_more: bool
    quota_max: int
    quota_remaining: int
    items: List[Question]


class User(TypedDict):
    account_id: int
    reputation: int
    user_id: int
    user_type: Literal["anonymous", "registered", "unregistered", "moderator"]
    profile_image: str
    display_name: str
    link: str


class APIClientSession(BaseUrlSession):

    throttling_window = 10

    def __init__(self, base_url: str = None) -> None:
        self.backoff_until: Optional[dt.datetime] = None
        self.request_queue: Queue[dt.datetime] = Queue(30)

        if base_url is None:
            base_url = "https://api.stackexchange.com/"
        super().__init__(base_url)

    def maybe_backoff(self) -> None:
        if self.backoff_until is not None:
            delta = (self.backoff_until - dt.datetime.now()).total_seconds()
            delta += 0.1  # Just for safety
            if delta >= 0:
                logging.info(f"Backoff for {delta:.1f} seconds")
                time.sleep(delta)
            self.backoff_until = None

    def maybe_throttle(self) -> None:
        if self.request_queue.full():
            now = dt.datetime.now()
            delta = (now - self.request_queue.get()).total_seconds()
            if delta <= self.throttling_window:
                wait_time = self.throttling_window - delta
                logging.info(f"Throttle for {wait_time:.1f} seconds")
                time.sleep(wait_time)

    def request(
        self,
        method: str,
        url: str,
        params: dict = {},
        *args: Any,
        **kwargs: Any,
    ) -> requests.Response:
        self.maybe_backoff()
        self.maybe_throttle()

        params["key"] = os.environ["STACKOVERFLOW_API_KEY"]
        params["site"] = "stackoverflow"
        params["pagesize"] = 100

        response = super().request(method, url, params, *args, **kwargs)

        payload = response.json()
        if "backoff" in payload:
            backoff = dt.timedelta(seconds=payload["backoff"])
            self.backoff_until = dt.datetime.now() + backoff

        self.request_queue.put(dt.datetime.now())

        return response


class APIClient:
    def __init__(self) -> None:
        self.session = APIClientSession()

    def answers(self, questions: Questions) -> Answers:
        batch_size = 100

        answers: Answers = {
            "has_more": True,
            "items": [],
            "quota_max": -1,
            "quota_remaining": -1,
        }
        items: List[Answer] = []

        for i in range(0, len(questions["items"]), batch_size):
            batch = questions["items"][i : i + batch_size]
            ids = (question["question_id"] for question in batch)
            url = f"questions/{';'.join(map(str, ids))}/answers"
            page = 0
            params = {}
            answers["has_more"] = True
            while answers["has_more"]:
                page += 1
                params["page"] = page
                logging.info(
                    f"Answers: fetching page {params['page']} "
                    f"of batch {i // 100}"
                )
                with self.handle_connection_error() as result:
                    answers = self.session.get(url, params=params).json()
                if not result["success"]:
                    answers = self.session.get(url, params=params).json()
                items += answers["items"]
        answers["items"] = items
        return answers

    @contextmanager
    def handle_connection_error(self) -> Iterator[Dict[str, bool]]:
        result = {"success": False}
        try:
            yield result
            result["success"] = True
        except ConnectionError:
            logging.error("Too many requests. Retrying in 2 minutes.")
            time.sleep(120)
            self.session = APIClientSession()
            result["success"] = False

    def questions(self, start: dt.datetime, end: dt.datetime) -> Questions:
        page = 0
        params = {
            "tagged": "python",
            "fromdate": int(start.timestamp()),
            "todate": int(end.timestamp()),
        }
        items: List[Question] = []
        questions: Questions = {
            "has_more": True,
            "items": [],
            "quota_max": -1,
            "quota_remaining": -1,
        }
        while questions["has_more"]:
            page += 1
            params["page"] = page
            logging.info(f"Questions: fetching page {params['page']}")
            with self.handle_connection_error() as result:
                questions = self.session.get("questions", params=params).json()
            if not result["success"]:
                questions = self.session.get("questions", params=params).json()
            items += questions["items"]
        questions["items"] = items
        return questions

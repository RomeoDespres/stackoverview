import json
from typing import Any, Union

import api


def check_types(o: Any, t: Union[type, list, dict]) -> None:
    if isinstance(t, type):
        assert isinstance(o, t)
    elif isinstance(t, list):
        assert isinstance(o, list)
        for child in o:
            check_types(child, t[0])
    else:
        assert isinstance(o, dict)
        assert set(o) == set(t)
        for key, child in o.items():
            check_types(child, t[key])


def test_tag_reputation() -> None:
    body = json.loads(api.tag_reputation()["body"])
    types = {
        "tags": [{"tag": str, "reputation": float}],
        "avgReputation": float,
    }
    check_types(body, types)
    reputations = [tag["reputation"] for tag in body["tags"]]
    assert reputations == sorted(reputations)[::-1]

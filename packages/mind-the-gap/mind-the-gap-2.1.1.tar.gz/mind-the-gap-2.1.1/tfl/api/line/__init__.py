from typing import List, Tuple

from tfl.api import get_tfl_json
from tfl.api.factory import from_json
from tfl.api.presentation.entities.line import Line

ENDPOINT = "Line"


def by_id(*ids: Tuple[str, ...], status=False, detail=False) -> List[Line]:
    line_ids = ",".join(ids)
    endpoint = f"{ENDPOINT}/{line_ids}" + ("/Status" if status else "")
    params = {"detail": status and detail}
    json = get_tfl_json(f"{endpoint}", params=params)
    return from_json(json)


def by_mode(mode: str, status=False) -> List[Line]:
    endpoint = f"{ENDPOINT}/Mode/{mode}" + ("/Status" if status else "")
    json = get_tfl_json(endpoint)
    return from_json(json)

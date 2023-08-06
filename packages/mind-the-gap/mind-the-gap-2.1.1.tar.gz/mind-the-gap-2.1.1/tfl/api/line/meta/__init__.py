from typing import List

from tfl.api import get_tfl_json
from tfl.api.factory import from_json
from tfl.api.presentation.entities.mode import Mode
from tfl.api.presentation.entities.status_severity import StatusSeverity

ENDPOINT = "Line/Meta"


def modes() -> List[Mode]:
    json = get_tfl_json(f"{ENDPOINT}/Modes")
    return from_json(json)


def severity() -> List[StatusSeverity]:
    json = get_tfl_json(f"{ENDPOINT}/Severity")
    return from_json(json)


def disruption_categories() -> List[str]:
    json = get_tfl_json(f"{ENDPOINT}/DisruptionCategories")
    return json


def service_types() -> List[str]:
    json = get_tfl_json(f"{ENDPOINT}/ServiceTypes")
    return json

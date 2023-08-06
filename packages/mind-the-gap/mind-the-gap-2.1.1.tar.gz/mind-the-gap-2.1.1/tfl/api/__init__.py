from typing import Dict, Optional

import requests

from tfl import APP_KEY, BASE_URL


def get_tfl_json(endpoint: str, params: Optional[Dict] = None) -> Dict:
    params = params if params is not None else dict()
    if APP_KEY is not None:
        params["app_key"] = APP_KEY

    query_endpoint = f"{BASE_URL}/{endpoint}"

    return requests.get(query_endpoint, params=params).json()

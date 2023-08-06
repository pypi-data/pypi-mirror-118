__version__ = "2.1.1"

import os

BASE_URL = "https://api.tfl.gov.uk"
APP_KEY = os.getenv("TFL_APP_KEY", None)

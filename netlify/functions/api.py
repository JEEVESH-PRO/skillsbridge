import sys
import os

_CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
_ROOT_DIR = os.path.abspath(os.path.join(_CURRENT_DIR, "..", ".."))

for _p in (_CURRENT_DIR, _ROOT_DIR):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import serverless_wsgi
from app import app


def handler(event, context):
    return serverless_wsgi.handle_request(app, event, context)
import time
from database import sqlite_db
from werkzeug.exceptions import NotFound

# Cache
_QUERY_CACHE = {}
_CACHE_TTL = 120


def _get_cache(key):
    if key in _QUERY_CACHE:
        val, ts = _QUERY_CACHE[key]
        if time.time() - ts < _CACHE_TTL:
            return val
        del _QUERY_CACHE[key]
    return None


def _set_cache(key, val):
    _QUERY_CACHE[key] = (val, time.time())


def clear_query_cache():
    global _QUERY_CACHE
    _QUERY_CACHE = {}


class Query(sqlite_db.Query):
    pass


class _Query(sqlite_db._Query):
    pass


class _Session(sqlite_db._Session):
    pass


class Session:
    def __init__(self):
        self._session = sqlite_db._Session()

    @property
    def session(self):
        return self._session

    def init_app(self, app):
        pass

    def create_all(self):
        pass


class QueryDescriptor:
    def __init__(self):
        self._col_name = None

    def __get__(self, obj, objtype=None):
        if objtype is None:
            return self
        if not self._col_name:
            self._col_name = objtype._COLLECTION
        return sqlite_db.Query(objtype, self._col_name)


db = Session()
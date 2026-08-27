from database.firestore_db import get_db
from werkzeug.exceptions import NotFound
from firebase_admin import firestore as _fs


class _Query:
    def __init__(self, col, model_cls, wheres=None, order=None, limit_n=None):
        self._col = col
        self._model = model_cls
        self._wheres = list(wheres or [])
        self._order = order
        self._limit_n = limit_n

    def _clone(self, **kw):
        return _Query(self._col, self._model,
                      wheres=kw.get('wheres', self._wheres),
                      order=kw.get('order', self._order),
                      limit_n=kw.get('limit_n', self._limit_n))

    def filter_by(self, **kw):
        w = self._wheres + [(k, '==', v) for k, v in kw.items()]
        return self._clone(wheres=w)

    def filter(self, *args):
        return self._clone()

    def ilike(self, pattern):
        return self._clone()

    def order_by(self, field, direction=None):
        name = getattr(field, 'name', str(field))
        d = 'desc' if direction and str(direction).lower().startswith('desc') else 'asc'
        return self._clone(order=(name, d))

    def limit(self, n):
        return self._clone(limit_n=n)

    def _run(self):
        q = self._col
        for f, op, v in self._wheres:
            q = q.where(f, op, v)
        if self._order:
            name, d = self._order
            q = q.order_by(name, _fs.Query.DESCENDING if d == 'desc' else _fs.Query.ASCENDING)
        if self._limit_n is not None:
            q = q.limit(self._limit_n)
        return [self._model.from_dict(d.to_dict(), doc_id=d.id) for d in q.stream()]

    def first(self):
        r = self._clone(limit_n=1)._run()
        return r[0] if r else None

    def all(self):
        return self._run()

    def count(self):
        return len(self._run())

    def __iter__(self):
        return iter(self._run())

    def __len__(self):
        return len(self._run())

    def __getitem__(self, key):
        rows = self._run()
        return rows[key]


class Query:
    def __init__(self, model_cls, col_name):
        self._model = model_cls
        self._col_name = col_name

    def _colref(self):
        return get_db().collection(self._col_name)

    def get(self, obj_id):
        doc = self._colref().document(str(obj_id)).get()
        if doc.exists:
            return self._model.from_dict(doc.to_dict(), doc_id=doc.id)
        return None

    def get_or_404(self, obj_id):
        obj = self.get(obj_id)
        if not obj:
            raise NotFound()
        return obj

    def filter_by(self, **kw):
        return _Query(self._colref(), self._model).filter_by(**kw)

    def filter(self, *args):
        return _Query(self._colref(), self._model)

    def join(self, model):
        return _Query(self._colref(), self._model)

    def order_by(self, field, direction=None):
        return _Query(self._colref(), self._model).order_by(field, direction)

    def limit(self, n):
        return _Query(self._colref(), self._model).limit(n)

    def first(self):
        return _Query(self._colref(), self._model).first()

    def all(self):
        return _Query(self._colref(), self._model).all()


class _Session:
    def __init__(self):
        self._pending = []

    def add(self, obj):
        self._pending.append(obj)

    def delete(self, obj):
        self._pending.append(('delete', obj))

    def commit(self):
        db = get_db()
        for item in self._pending:
            if isinstance(item, tuple) and item[0] == 'delete':
                obj = item[1]
                if obj and getattr(obj, 'id', None):
                    db.collection(obj._COLLECTION).document(str(obj.id)).delete()
            else:
                obj = item
                if obj:
                    db.collection(obj._COLLECTION).document(str(obj.id)).set(obj.to_dict(), merge=True)
        self._pending = []


class QueryDescriptor:
    def __init__(self):
        self._col_name = None

    def __get__(self, obj, objtype=None):
        if objtype is None:
            return self
        if not self._col_name:
            self._col_name = objtype._COLLECTION
        return Query(objtype, self._col_name)


class Session:
    def __init__(self):
        self._session = _Session()

    @property
    def session(self):
        return self._session

    def init_app(self, app):
        pass

    def create_all(self):
        pass


db = Session()

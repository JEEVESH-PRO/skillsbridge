from firebase_admin import firestore


class QueryWrapper:
    def __init__(self, query, model_class):
        self._query = query
        self._model_class = model_class

    def filter_by(self, **kwargs):
        q = self._query
        for key, value in kwargs.items():
            q = query_where(q, key, '==', value)
        return QueryWrapper(q, self._model_class)

    def ilike(self, pattern):
        return QueryWrapper(self._query, self._model_class)

    def filter(self, *conditions):
        return QueryWrapper(self._query, self._model_class)

    def order_by(self, field, direction=None):
        if direction is None:
            field_name = getattr(field, 'name', str(field))
            direction = 'desc'
        else:
            field_name = getattr(field, 'name', str(field))
        q = self._query.order_by(field_name, firestore.Query.DESCENDING if direction == 'desc' else firestore.Query.ASCENDING)
        return QueryWrapper(q, self._model_class)

    def limit(self, n):
        return QueryWrapper(self._query.limit(n), self._model_class)

    def first(self):
        docs = self._query.limit(1).stream()
        for doc in docs:
            return self._model_class.from_dict(doc.to_dict(), doc_id=doc.id)
        return None

    def all(self):
        docs = self._query.stream()
        return [self._model_class.from_dict(d.to_dict(), doc_id=d.id) for d in docs]

    def count(self):
        return len(self.all())

    def __iter__(self):
        return iter(self.all())

    def __len__(self):
        return len(self.all())


def query_where(q, field, op, value):
    return q.where(field, op, value)

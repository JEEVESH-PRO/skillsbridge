import os
import sqlite3
from contextlib import closing
from datetime import datetime
from werkzeug.exceptions import NotFound

_env_db_path = os.environ.get('DB_PATH')
if _env_db_path:
    DB_PATH = _env_db_path
elif os.environ.get('AWS_LAMBDA_FUNCTION_NAME') or os.environ.get('NETLIFY') or os.environ.get('LAMBDA_TASK_ROOT'):
    # Serverless hosts (Netlify/AWS Lambda) have a read-only bundle dir; use /tmp.
    DB_PATH = '/tmp/skillsbridge.db'
else:
    DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'skillsbridge.db')


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize SQLite database and create tables if they don't exist"""
    with closing(get_db_connection()) as conn:
        cur = conn.cursor()
        
        # Users
        cur.execute('''CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            name TEXT,
            email TEXT UNIQUE,
            password_hash TEXT,
            role TEXT DEFAULT 'candidate',
            headline TEXT,
            bio TEXT,
            company_id TEXT,
            created_at TEXT
        )''')
        
        # Companies
        cur.execute('''CREATE TABLE IF NOT EXISTS companies (
            id TEXT PRIMARY KEY,
            name TEXT,
            industry TEXT,
            location TEXT,
            website TEXT,
            logo_url TEXT,
            description TEXT,
            founded_year TEXT,
            employee_count TEXT
        )''')
        
        # Skills
        cur.execute('''CREATE TABLE IF NOT EXISTS skills (
            id TEXT PRIMARY KEY,
            name TEXT,
            category TEXT DEFAULT 'General'
        )''')
        
        # Candidate Skills
        cur.execute('''CREATE TABLE IF NOT EXISTS candidate_skills (
            id TEXT PRIMARY KEY,
            user_id TEXT,
            skill_id TEXT,
            proficiency TEXT DEFAULT 'Intermediate'
        )''')
        
        # Job Postings
        cur.execute('''CREATE TABLE IF NOT EXISTS job_postings (
            id TEXT PRIMARY KEY,
            company_id TEXT,
            title TEXT,
            domain TEXT,
            experience_required TEXT,
            location TEXT DEFAULT 'Remote',
            salary_range TEXT,
            description TEXT,
            created_at TEXT,
            employer_id TEXT
        )''')
        
        # Job Skill Requirements
        cur.execute('''CREATE TABLE IF NOT EXISTS job_skill_requirements (
            id TEXT PRIMARY KEY,
            job_id TEXT,
            skill_id TEXT,
            required_level TEXT DEFAULT 'Intermediate'
        )''')
        
        # Courses
        cur.execute('''CREATE TABLE IF NOT EXISTS courses (
            id TEXT PRIMARY KEY,
            skill_id TEXT,
            title TEXT,
            provider TEXT DEFAULT 'Coursera',
            source_type TEXT,
            url TEXT,
            duration TEXT DEFAULT '4 Weeks',
            difficulty TEXT DEFAULT 'Intermediate',
            employer_id TEXT,
            created_at TEXT
        )''')
        
        # Interview Resources
        cur.execute('''CREATE TABLE IF NOT EXISTS interview_resources (
            id TEXT PRIMARY KEY,
            company_id TEXT,
            job_id TEXT,
            title TEXT,
            url TEXT,
            resource_type TEXT,
            description TEXT
        )''')
        
        # Applications
        cur.execute('''CREATE TABLE IF NOT EXISTS applications (
            id TEXT PRIMARY KEY,
            user_id TEXT,
            job_id TEXT,
            status TEXT DEFAULT 'Applied',
            match_score INTEGER DEFAULT 0,
            applied_at TEXT,
            cover_letter TEXT
        )''')
        
        conn.commit()
        return conn


def db_exists():
    return os.path.exists(DB_PATH)


def row_to_dict(row):
    if row is None:
        return None
    return dict(row)


# Query implementations
class _Query:
    def __init__(self, col_name, model_cls, wheres=None, order=None, limit_n=None):
        self._col_name = col_name
        self._model = model_cls
        self._wheres = list(wheres or [])
        self._order = order
        self._limit_n = limit_n

    def _clone(self, **kw):
        return _Query(self._col_name, self._model,
                      wheres=kw.get('wheres', self._wheres),
                      order=kw.get('order', self._order),
                      limit_n=kw.get('limit_n', self._limit_n))

    def filter_by(self, **kw):
        w = self._wheres + [(k, '==', v) for k, v in kw.items()]
        return self._clone(wheres=w)

    def filter(self, *args):
        # Keep signature compatible; for simple cases use filter_by
        return self._clone()

    def ilike(self, pattern):
        return self._clone()

    def order_by(self, field, direction=None):
        name = getattr(field, 'name', str(field))
        d = 'desc' if direction and str(direction).lower().startswith('desc') else 'asc'
        return self._clone(order=(name, d))

    def limit(self, n):
        return self._clone(limit_n=n)

    def _build_sql(self):
        cols = ['*']
        sql = f"SELECT {', '.join(cols)} FROM {self._col_name}"
        params = []
        if self._wheres:
            clauses = []
            for f, op, v in self._wheres:
                if op == '==':
                    clauses.append(f"{f} = ?")
                    params.append(v)
                elif op == '!=':
                    clauses.append(f"{f} != ?")
                    params.append(v)
                else:
                    clauses.append(f"{f} {op} ?")
                    params.append(v)
            sql += " WHERE " + " AND ".join(clauses)
        if self._order:
            name, d = self._order
            sql += f" ORDER BY {name} {d.upper()}"
        if self._limit_n is not None:
            sql += " LIMIT ?"
            params.append(int(self._limit_n))
        return sql, params

    def _run(self):
        with closing(get_db_connection()) as conn:
            cur = conn.cursor()
            sql, params = self._build_sql()
            cur.execute(sql, params)
            rows = cur.fetchall()
        results = []
        for r in rows:
            d = row_to_dict(r)
            results.append(self._model.from_dict(d, doc_id=d.get('id')))
        return results

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

    def get(self, obj_id):
        if not obj_id:
            return None
        with closing(get_db_connection()) as conn:
            cur = conn.cursor()
            cur.execute(f"SELECT * FROM {self._col_name} WHERE id = ?", (str(obj_id),))
            row = cur.fetchone()
        if not row:
            return None
        d = row_to_dict(row)
        return self._model.from_dict(d, doc_id=d.get('id'))

    def get_or_404(self, obj_id):
        obj = self.get(obj_id)
        if not obj:
            raise NotFound()
        return obj

    def filter_by(self, **kw):
        return _Query(self._col_name, self._model).filter_by(**kw)

    def filter(self, *args):
        return _Query(self._col_name, self._model)

    def join(self, model):
        return _Query(self._col_name, self._model)

    def order_by(self, field, direction=None):
        return _Query(self._col_name, self._model).order_by(field, direction)

    def limit(self, n):
        return _Query(self._col_name, self._model).limit(n)

    def first(self):
        return _Query(self._col_name, self._model).first()

    def all(self):
        return _Query(self._col_name, self._model).all()


class _Session:
    def __init__(self):
        self._pending = []

    def add(self, obj):
        self._pending.append(obj)

    def delete(self, obj):
        self._pending.append(('delete', obj))

    def commit(self):
        for item in self._pending:
            if isinstance(item, tuple) and item[0] == 'delete':
                obj = item[1]
                if obj and getattr(obj, 'id', None):
                    with closing(get_db_connection()) as conn:
                        cur = conn.cursor()
                        cur.execute(f"DELETE FROM {obj._COLLECTION} WHERE id = ?", (str(obj.id),))
                        conn.commit()
            else:
                obj = item
                if obj:
                    d = obj.to_dict()
                    # build insert/update (upsert by id)
                    cols = list(d.keys())
                    placeholders = ', '.join(['?'] * len(cols))
                    colstr = ', '.join(cols)
                    updates = ', '.join([f"{c}=excluded.{c}" for c in cols])
                    with closing(get_db_connection()) as conn:
                        cur = conn.cursor()
                        sql = f"INSERT OR REPLACE INTO {obj._COLLECTION} ({colstr}) VALUES ({placeholders})"
                        # sqlite doesn't support "excluded" in older forms; use insert or replace simpler
                        sql = f"INSERT OR REPLACE INTO {obj._COLLECTION} ({colstr}) VALUES ({placeholders})"
                        cur.execute(sql, [d.get(c) for c in cols])
                        conn.commit()
        self._pending = []
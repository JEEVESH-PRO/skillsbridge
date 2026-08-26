import sys
import types
import re
import apsw

def extract_select_columns(sql):
    try:
        parts = re.split(r'\s+FROM\s+', sql, flags=re.IGNORECASE)
        if len(parts) >= 2:
            select_part = parts[0]
            sel_idx = select_part.upper().find("SELECT ")
            if sel_idx != -1:
                cols_part = select_part[sel_idx + 7 :].strip()
                cols = []
                for raw_col in cols_part.split(','):
                    raw_col = raw_col.strip()
                    if not raw_col:
                        continue
                    tokens = raw_col.split()
                    if len(tokens) >= 3 and tokens[-2].upper() == 'AS':
                        cols.append(tokens[-1].strip(' "`[]'))
                    elif '.' in raw_col:
                        cols.append(raw_col.split('.')[-1].strip(' "`[]'))
                    else:
                        cols.append(raw_col.strip(' "`[]'))
                return cols
    except Exception:
        pass
    return []

class Cursor:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.conn.cursor()
        self.description = None
        self._rows = []
        self._idx = 0
        self._rowcount = -1

    @property
    def rowcount(self):
        return self._rowcount

    @property
    def lastrowid(self):
        try:
            return self.connection.conn.last_insert_rowid()
        except Exception:
            return None

    def execute(self, statements, bindings=None):
        if bindings is None:
            bindings = ()
        self.cursor.execute(statements, bindings)
        self.description = None
        self._rows = []

        try:
            row_iter = iter(self.cursor)
            try:
                desc = self.cursor.getdescription()
                if desc:
                    self.description = tuple(
                        (col[0], col[1] if len(col) > 1 and col[1] else 'TEXT', None, None, None, None, True)
                        for col in desc
                    )
            except Exception:
                self.description = None

            self._rows = list(row_iter)
        except Exception:
            self.description = None
            self._rows = []

        # Fallback column description extraction for SELECT queries returning 0 rows in APSW
        if self.description is None and statements.strip().upper().startswith("SELECT"):
            parsed_cols = extract_select_columns(statements)
            if parsed_cols:
                self.description = tuple(
                    (c, 'TEXT', None, None, None, None, True)
                    for c in parsed_cols
                )

        self._idx = 0
        try:
            self._rowcount = self.connection.conn.changes()
        except Exception:
            self._rowcount = -1
        return self

    def executemany(self, statements, seq_of_parameters):
        for params in seq_of_parameters:
            self.execute(statements, params)
        return self

    def fetchone(self):
        if self._idx < len(self._rows):
            row = self._rows[self._idx]
            self._idx += 1
            return row
        return None

    def fetchall(self):
        rows = self._rows[self._idx:]
        self._idx = len(self._rows)
        return rows

    def fetchmany(self, size=None):
        return self.fetchall()

    def __iter__(self):
        return iter(self._rows)

    def close(self):
        try:
            self.cursor.close()
        except Exception:
            pass

class Connection:
    def __init__(self, database, **kwargs):
        self.conn = apsw.Connection(database)
        
    def cursor(self):
        return Cursor(self)

    def create_function(self, name, num_params, func, *args, **kwargs):
        try:
            self.conn.createscalarfunction(name, func, num_params)
        except Exception:
            pass

    def commit(self):
        pass

    def rollback(self):
        pass

    def close(self):
        self.conn.close()

def connect(database, **kwargs):
    return Connection(database, **kwargs)

sqlite3_module = types.ModuleType('sqlite3')
sqlite3_module.connect = connect
sqlite3_module.sqlite_version = apsw.sqlite_lib_version()
sqlite3_module.sqlite_version_info = (3, 53, 4)
sqlite3_module.paramstyle = 'qmark'
sqlite3_module.threadsafety = 1

# DBAPI 2.0 Exceptions
sqlite3_module.Error = apsw.Error
sqlite3_module.DatabaseError = apsw.Error
sqlite3_module.OperationalError = apsw.SQLError
sqlite3_module.IntegrityError = apsw.ConstraintError
sqlite3_module.ProgrammingError = apsw.SQLError
sqlite3_module.Warning = apsw.Error
sqlite3_module.InterfaceError = apsw.Error
sqlite3_module.DataError = apsw.Error
sqlite3_module.InternalError = apsw.Error
sqlite3_module.NotSupportedError = apsw.Error

sqlite3_module.Binary = bytes
sqlite3_module.dbapi2 = sqlite3_module

sys.modules['sqlite3'] = sqlite3_module
sys.modules['sqlite3.dbapi2'] = sqlite3_module

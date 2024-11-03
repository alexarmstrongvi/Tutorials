import sqlite3
from contextlib import contextmanager
 
def main():
    with open_sqlite_db() as (_, cur):
        test_sqlite3(cur)
        test_basics(cur)

def test_sqlite3(cur: sqlite3.Cursor):
    res = cur.execute('SELECT "Hello World"')
    assert res is cur

    rows = res.fetchall()
    assert isinstance(rows, list) and isinstance(rows[0], tuple)

    assert rows[0][0] == "Hello World"

def test_basics(cur: sqlite3.Cursor):
    # Create a table
    cur.execute('''
    CREATE TABLE tbl (
        col_null   NULL,
        col_int    INTEGER,
        col_float  REAL,
        col_string TEXT
    );
    ''')
    assert cur.fetchall() == []
    # Insert row into table
    cur.execute('''
    INSERT into tbl(col_null, col_int, col_float, col_string)
    VALUES (NULL, 1, 1.5, 'A'),
           (NULL, 2, 2.5, 'B'),
           (NULL, 3, 3.5, 'B'),
           (NULL, 4, 3.5, 'C'),
           (NULL, 5, 4.5, 'C');
    ''')
    assert cur.fetchall() == []

    cur.execute('''
    SELECT * FROM tbl;
    ''')
    assert cur.fetchmany(2) == [
        (None, 1, 1.5, 'A'),
        (None, 2, 2.5, 'B'),
    ]


################################################################################
@contextmanager
def open_sqlite_db(database = ':memory:', **kwargs):
    con = sqlite3.connect(database, **kwargs)
    cur = con.cursor()
    try:
        yield con, cur
    finally:
        cur.close()
        con.close()


if __name__ == '__main__':
    main()

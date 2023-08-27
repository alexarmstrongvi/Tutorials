#!/usr/bin/env python

# Standard library
import os
from pathlib import Path
import logging

# 3rd party
import sqlite3

log = logging.getLogger(Path(__file__).stem)
logging.basicConfig(
    level  = logging.DEBUG,
    format = '%(levelname)s :: %(message)s',
)

################################################################################
def main():
    pass

def connection_basics(con: sqlite3.Connection) -> None:
    # Attributes
    print(f'''Connection attributes:
    {con.in_transaction = }
    {con.isolation_level = }
    {con.row_factory = }
    {con.text_factory = }
    {con.total_changes = }
    ''')

    # con.backup
    # con.blobopen
    # con.commit
    # con.create_aggregate
    # con.create_collation
    # con.create_function
    # con.create_window_function
    # con.cursor
    # con.deserialize
    # con.enable_load_extension
    # con.execute
    # con.executemany
    # con.executescript
    # con.getlimit
    # con.interrupt
    # con.iterdump
    # con.load_extension
    # con.rollback
    # con.serialize
    # con.set_authorizer
    # con.set_progress_handler
    # con.set_trace_callback
    # con.setlimit
    
    # con.close

def cursor_basics(cur: sqlite3.Cursor) -> None:
    # Attributes
    print(f'''Cursor attributes:
    {cur.arraysize = }
    {cur.connection = }
    {cur.description = }
    {cur.lastrowid = }
    {cur.rowcount = }
    {cur.row_factory = }
    ''')

    # Execution
    # cur.execute
    # cur.executemany
    # cur.executescript

    # Fetching
    # cur.fetchone
    # cur.fetchmany
    # cur.fetchall

    # Configuration
    # cur.setinputsizes
    # cur.setoutputsize

    # Closing
    # cur.close

if __name__ == '__main__':
    main()

    db_path = Path('./tmp/my_sqlite3_database.db')
    if db_path.is_file():
        log.info('Deleting previous database: %s', db_path)
        os.remove(db_path)

    # Create "connection" to database, creating if necessary
    con = sqlite3.connect(db_path)
    connection_basics(con)

    # Get "cursor" from database connection
    cur = con.cursor()
    cursor_basics(cur)

    # Create Table in database
    cmd = "CREATE TABLE mytable(colA, colB)"
    cur2 = cur.execute(cmd)
    assert cur == cur2

    cmd = "SELECT name FROM sqlite_master"
    cur.execute(cmd)
    assert cur.fetchall() == [('mytable',)]
    assert cur.execute(cmd).fetchone() == ('mytable',)

    # Transactions and committing
    cur.execute('''
        INSERT INTO mytable VALUES
            ('ValX', 1),
            ('ValY', 2)
    ''')
    result = cur.execute('SELECT colA FROM mytable').fetchall()
    assert result == [('ValX',), ('ValY',)]

    # TODO: Placeholders (instead of string formatting)

    # TODO: Transaction control, isolation_level, and con.commit()
    
    # TODO: Converting to/from Pandas
    
    # Close database connection (allowing it to be deleted if desired)
    con.close()

    try:
        con.cursor()
    except sqlite3.ProgrammingError as err:
        assert str(err) == 'Cannot operate on a closed database.'


/*******************************************************************************
* Global variables defined by SQLite
* 
*  - See https://sqlite.org/schematab.html
*******************************************************************************/

-- Create a database
ATTACH DATABASE 'test.db' AS db1;

-- Create a table
CREATE TABLE Tbl (
    col_null   NULL,
    col_int    INTEGER,
    col_float  REAL,
    col_string TEXT
);

-- sqlite_schema (as of 3.33) and sqlite_master 
SELECT * FROM sqlite_schema;

-- sqlite_temp_schema and sqlite_temp_master

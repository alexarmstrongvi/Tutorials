/*******************************************************************************
* Deleting rows from a table
* see [DELETE Statement](https://dev.mysql.com/doc/refman/8.0/en/delete.html)
*******************************************************************************/

SELECT '------------------------------------------' AS '';
SELECT 'Running tutorial on DELETE Statment' AS '';
SELECT '------------------------------------------' AS '';

/*******************************************************************************
* Setup test area
*******************************************************************************/
DROP DATABASE IF EXISTS tmp_database;
CREATE DATABASE tmp_database;
USE tmp_database;

CREATE TABLE tbl (
    col_int    INTEGER,
    col_float  REAL,
    col_string TEXT
);

INSERT INTO tbl (col_int, col_float, col_string)
VALUES (1, 1.5, 'A'),
       (2, 2.5, 'B'),
       (3, 3.5, 'B'),
       (4, 3.5, 'C'),
       (5, 4.5, 'C');

CREATE TABLE tbl2 (
    col_int    INTEGER,
    col_float  REAL,
    col_string TEXT
);

INSERT INTO tbl2 (col_int, col_string)
VALUES (5, 'Z'),
       (9, 'A');
/*******************************************************************************
* Single table
*******************************************************************************/

-- Simple delete rows
SELECT "Delete a row" AS '';
DELETE FROM tbl
WHERE col_int = 3;
SELECT * FROM tbl;

-- Limit the number of rows that get deleted and in what order: LIMIT and ORDER BY

-- Determine number of rows deleted: ROW_COUNT()

-- Restrict delete to a predifined parition: PARTITION

/*******************************************************************************
* Multiple table
*******************************************************************************/
SELECT "Delete a row using info from other table" AS '';
DELETE
    t1
FROM
    tbl t1,
    tbl2 t2
WHERE
    t1.col_int = t2.col_int;

DELETE FROM
    t1
USING
    tbl t1,
    tbl2 t2
WHERE
    t1.col_string = t2.col_string;

SELECT * FROM tbl;

/*******************************************************************************
* Safety - permissions, table locks, transactions, modifiers
*******************************************************************************/


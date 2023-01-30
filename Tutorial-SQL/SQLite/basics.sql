/*******************************************************************************
All the basics of SQL
*******************************************************************************/

SELECT '----------------------------------------';
SELECT 'Running basic SQLite script';
SELECT '----------------------------------------';
SELECT '';

/*******************************************************************************
* Creating (ATTACH DATABASE, CREATE TABLE, INSERT INTO)
*******************************************************************************/
-- Create a database
ATTACH DATABASE 'test.db' AS db1;

-- Create a table
CREATE TABLE tbl (
    col_null   NULL,
    col_int    INTEGER,
    col_float  REAL,
    col_string TEXT
);

-- Insert row into table
INSERT into tbl(col_null, col_int, col_float, col_string)
VALUES (NULL, 1, 1.5, 'A'),
       (NULL, 2, 2.5, 'B'),
       (NULL, 3, 3.5, 'B'),
       (NULL, 4, 3.5, 'C'),
       (NULL, 5, 4.5, 'C');

/*******************************************************************************
* Viewing (SELECT, FROM, WHERE)
*  - Comparison Operators : BETWEEN
*  - Logical Operators : AND, OR, NOT
*******************************************************************************/
-- Read a entire table
SELECT 'Printing Table';
SELECT * FROM tbl;
SELECT '';

-- Read a table column
SELECT 'Printing float column';
SELECT col_float FROM tbl;
SELECT '';

-- Read a table row
SELECT 'Printing row(s)';
SELECT ' <1>';
SELECT * FROM tbl WHERE col_int = 1;

-- Limit output
SELECT ' <2>';
SELECT * FROM tbl LIMIT 2;
SELECT ' <3>';
SELECT * FROM tbl LIMIT 2 OFFSET 2;

-- Sort the output
SELECT ' <4>';
SELECT * FROM tbl ORDER BY col_string DESC;

-- Remove duplicate output
SELECT ' <5>';
SELECT DISTINCT col_string FROM tbl;

/*******************************************************************************
* Aggregating (COUNT, GROUP BY, HAVING)
*******************************************************************************/
SELECT '';
SELECT 'Aggregating columns';
SELECT COUNT(col_float), col_string FROM tbl; -- will select first row of col_string
SELECT '';
SELECT COUNT(col_float), col_string FROM tbl
GROUP BY col_string
HAVING COUNT(col_float) > 1;
SELECT '';

/*******************************************************************************
* Modifying (UPDATE, SET, DELETE, DROP)
*******************************************************************************/
-- Update column in specifc row in table
UPDATE tbl 
SET col_int = -1 
WHERE col_string = 'A';

SELECT 'Printing updated table';
SELECT * FROM tbl;
SELECT '';

-- Delete column from table
SELECT 'Deleting all rows from table';
DELETE FROM tbl;
SELECT * FROM tbl;
SELECT 'Deleting table';
DROP TABLE tbl;


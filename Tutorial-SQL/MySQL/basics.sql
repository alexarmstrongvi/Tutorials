/*******************************************************************************
All the basics of MySQL
*******************************************************************************/

SELECT '----------------------------------------' AS '';
SELECT 'Running basic MySQL script' AS '';
SELECT '----------------------------------------' AS '';

/*******************************************************************************
* Setup test area
*******************************************************************************/
-- Create a database
DROP DATABASE IF EXISTS tmp_database;
CREATE DATABASE tmp_database;
USE tmp_database;

/*******************************************************************************
* Creating (ATTACH DATABASE, CREATE TABLE, INSERT INTO)
*******************************************************************************/

-- Create a table
CREATE TABLE tbl (
    col_int    INTEGER,
    col_float  REAL,
    col_string TEXT
);

-- Insert row into table
INSERT INTO tbl(col_int, col_float, col_string)
VALUES (1, 1.5, 'A'),
       (2, 2.5, 'B'),
       (3, 3.5, 'B'),
       (4, 3.5, 'C'),
       (5, 4.5, 'C');

/*******************************************************************************
* Viewing (SELECT, FROM, WHERE, LIMIT, OFFSET, ORDER BY, DISTINCT)
*******************************************************************************/
-- Read a entire table
SELECT 'Printing Table' AS '';
SELECT * FROM tbl;
SELECT '';

-- Read a table column
SELECT 'Printing float column' AS '';
SELECT col_float FROM tbl;

-- Read a table row
SELECT 'Printing row(s)' AS '';
SELECT ' <1>' AS '';
SELECT * FROM tbl WHERE col_int = 1;

-- Limit output
SELECT ' <2>' AS '';
SELECT * FROM tbl LIMIT 2;
SELECT ' <3>' AS '';
SELECT * FROM tbl LIMIT 2 OFFSET 2;

-- Sort the output
SELECT ' <4>' AS '';
SELECT * FROM tbl ORDER BY col_string DESC;

-- Remove duplicate output
SELECT ' <5>' AS '';
SELECT DISTINCT col_string FROM tbl;

/*******************************************************************************
* Aggregating (COUNT, GROUP BY, HAVING)
*******************************************************************************/
SELECT 'Aggregating columns' AS '';
-- SELECT COUNT(col_float), col_string FROM tbl; -- will cause error
SELECT COUNT(col_float), col_string FROM tbl
GROUP BY col_string
HAVING COUNT(col_float) > 1;

/*******************************************************************************
* Modifying (UPDATE, SET, DELETE, DROP)
*******************************************************************************/
-- Update column in specifc row in table
UPDATE tbl
SET col_int = -1 
WHERE col_string = 'A';

SELECT 'Printing updated table' AS '';
SELECT * FROM tbl;

SELECT 'Removing a row and column' AS '';
-- Delete row from table
DELETE FROM tbl
WHERE col_int = 3;
-- Delete column from table
ALTER TABLE tbl
DROP COLUMN col_float;
SELECT * FROM tbl;

-- Clear the table 
SELECT 'Deleting all rows from table' AS '';
DELETE FROM tbl;
SELECT * FROM tbl;

-- Delete the table
SELECT 'Deleting table' AS '';
DROP TABLE tbl;

/*******************************************************************************
* Clean up test area
*******************************************************************************/
DROP DATABASE tmp_database;

/*******************************************************************************
* WHERE
*******************************************************************************/

SELECT '----------------------------------------';
SELECT 'Running WHERE SQLite script';
SELECT '----------------------------------------';
SELECT '';

/*******************************************************************************
* Setup
*******************************************************************************/
-- Create a database
ATTACH DATABASE 'test.db' AS db1;

/*******************************************************************************
* Comparison operators
*******************************************************************************/
-- Create a table
CREATE TABLE tbl (
    col_int    INTEGER
);

-- Insert row into table
INSERT into tbl(col_int) VALUES (1);
INSERT into tbl VALUES (2);
INSERT into tbl VALUES (3);

-- Use operators
SELECT ' <1>';
SELECT * FROM tbl WHERE col_int =  2;
SELECT * FROM tbl WHERE col_int == 2;
SELECT * FROM tbl WHERE col_int IS 2;
SELECT ' <2>';
SELECT * FROM tbl WHERE col_int != 2;
SELECT * FROM tbl WHERE col_int <> 2;
SELECT * FROM tbl WHERE col_int IS NOT 2;
SELECT ' <3>';
SELECT * FROM tbl WHERE col_int <= 2;
-- SELECT * FROM tbl WHERE col_int !> 2;
SELECT ' <4>';
SELECT * FROM tbl WHERE col_int <  2;
SELECT ' <5>';
SELECT * FROM tbl WHERE col_int >= 2;
-- SELECT * FROM tbl WHERE col_int !< 2;
SELECT ' <6>';
SELECT * FROM tbl WHERE col_int >  2;
SELECT '';

/*******************************************************************************
* Logical operators ()
*******************************************************************************/
DROP TABLE tbl;
CREATE TABLE tbl (
    col_int   INTEGER,
    col_float REAL,
    col_text  TEXT
);

-- Insert row into table
INSERT into tbl(col_int, col_float, col_text) VALUES (1, 1.5, "A");
INSERT into tbl VALUES (2, 2.5, "AB");
INSERT into tbl VALUES (2, 10/3.0, "AC");
INSERT into tbl VALUES (3, 3.5, "B");
INSERT into tbl VALUES (NULL, 3.5, "BA");

-- Use operators
SELECT ' <7>';
SELECT * FROM tbl WHERE col_int IS NULL;
SELECT ' <8>';
SELECT * FROM tbl WHERE col_int IS NOT NULL;
SELECT ' <9>';
SELECT * FROM tbl WHERE col_int = 2 AND col_float = 10/3.0;
SELECT ' <10>';
SELECT * FROM tbl WHERE col_int = 2 OR col_float = 10/3.0;
SELECT ' <11>';
SELECT * FROM tbl WHERE col_float BETWEEN 3.2 AND 3.4;
SELECT ' <12>';
SELECT * FROM tbl WHERE col_int IN (1, 3);
SELECT ' <13>';
SELECT * FROM tbl WHERE col_text LIKE "B%";
SELECT ' <14>';
SELECT * FROM tbl WHERE col_text LIKE "B_";

-- SELECT * FROM tbl WHERE EXISTS ()

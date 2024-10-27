/*******************************************************************************
* Creating (CREATE TABLE, INSERT INTO)
*  - CREATE (TEMP / TEMPORARY) TABLE (IF NOT EXISTS)
*******************************************************************************/
-- Create a table
CREATE TABLE datatypes (
    c_null NULL,
    c_int  INTEGER, -- i8, i16, i24, i32, i48, or i64
    c_real REAL,    -- f64
    c_text TEXT,    -- UTF8, UTF16BE, or UTF16LE string
    c_blob BLOB    -- hexidecimal
);

INSERT INTO datatypes(c_null, c_int, c_real, c_text, c_blob)
VALUES (NULL, 1,    1.5,  'a',  x'00'),
       (NULL, TRUE, 2.56, 'AB', x'aF'), -- TRUE and FALSE are aliases for 1 and 0
       (NULL, NULL, NULL, NULL, NULL ); -- All columns are nullable

DROP TABLE datatypes;

/*******************************************************************************
* Querying:
*  Viewing
*  - SELECT: DISTINCT, ALL
*  - FROM
*  - WHERE
*  - ORDER BY
*  - LIMIT, OFFSET
*  Aggregating
*  - GROUP BY, HAVING
*  - WINDOW, AS

*******************************************************************************/
CREATE TABLE tbl (
    c_int INTEGER,
    c_str TEXT
);

-- Insert row into table
INSERT into tbl(c_int, c_str)
VALUES (1, 'A'),
       (2, 'B'),
       (3, 'B'),
       (4, 'C'),
       (5, 'C');

-- Read a entire table
SELECT * FROM tbl; -- Implicit SELECT ALL
-- EQUALS
-- [
--     (1, 'A'),
--     (2, 'B'),
--     (3, 'B'),
--     (4, 'C'),
--     (5, 'C'),
-- ]

-- Read a table column
SELECT c_int FROM tbl;
-- EQUALS [(1,), (2,), (3,), (4,), (5,)]

-- Read a table row
SELECT * FROM tbl WHERE c_int = 3;
-- EQUALS [(3, 'B')]

-- Limit output
SELECT c_int FROM tbl LIMIT 2;
-- EQUALS [(1,), (2,)]

SELECT c_int FROM tbl LIMIT 2 OFFSET 2;
-- EQUALS [(3,), (4,)]

-- Sort the output
SELECT c_int FROM tbl ORDER BY c_str DESC;
-- EQUALS [(4,), (5,), (2,), (3,), (1,)]

-- Remove duplicate output
SELECT DISTINCT c_str FROM tbl;
-- EQUALS [('A',), ('B',), ('C',)]

DROP TABLE tbl;

/*******************************************************************************
* Operators
*   - Equality   : =  ==  IS ISNULL
*   - Inequality : !=  <>  IS NOT NOTNULL NOT NULL
*   - Comparison : <=  <  >  >=  BETWEEN
*   - Logical    : NOT  AND  OR
*   - Binary     : &  |  <<  >>  ~
*   - Existential: EXISTS
*
* Arithmatic: +  -  *   /   %
*
* Strings
*   - LIKE   : %  _
*       - LIKE (expr) ESCAPE '\'
*   - GLOB   : *  ?
*   - REGEXP : Reserved but not part of default sqlite3. Requires extension
*   - MATCH  : Reserved but not part of default sqlite3. Requires extension
*   - ||
*   - [expr] COLLATE (collation-name)
*
* Other
* IN
*
* Unary
* + [expr] - No Op
* - [expr]
*
* JSON
* ->   ->>
*******************************************************************************/

CREATE TABLE tbl (col INTEGER);

INSERT into tbl(col)
VALUES (1), (NULL), (3), (4);

SELECT col FROM tbl WHERE col =  3;
-- EQUALS [(3,)]
SELECT col FROM tbl WHERE col == 3;
-- EQUALS [(3,)]
SELECT col FROM tbl WHERE col IS 3;
-- EQUALS [(3,)]
SELECT col FROM tbl WHERE col IS NOT DISTINCT FROM 3;
-- EQUALS [(3,)]
SELECT col FROM tbl WHERE col ISNULL;
-- EQUALS [(NULL,)]

SELECT col FROM tbl WHERE col != 3;
-- EQUALS [(1,), (4,)]
SELECT col FROM tbl WHERE col <> 3;
-- EQUALS [(1,), (4,)]
SELECT col FROM tbl WHERE col IS NOT 3;
-- EQUALS [(1,), (NULL,), (4,)]
SELECT col FROM tbl WHERE col IS DISTINCT FROM 3;
-- EQUALS [(1,), (NULL,), (4,)]
SELECT col FROM tbl WHERE col NOTNULL;
-- EQUALS [(1,), (3,), (4,)]
SELECT col FROM tbl WHERE col NOT NULL;
-- EQUALS [(1,), (3,), (4,)]

SELECT col FROM tbl WHERE col <= 3;
-- EQUALS [(1,), (3,)]
SELECT col FROM tbl WHERE col < 3;
-- EQUALS [(1,)]
SELECT col FROM tbl WHERE col >= 3;
-- EQUALS [(3,), (4,)]
SELECT col FROM tbl WHERE col > 3;
-- EQUALS [(4,)]
SELECT col FROM tbl WHERE col BETWEEN 1.5 AND 4;
-- EQUALS [(3,), (4,)]

-- SELECT * FROM tbl WHERE col !> 2;
-- SELECT * FROM tbl WHERE col <! 2;

SELECT col AS col1 FROM tbl WHERE EXISTS (
    SELECT col AS col2 FROM tbl WHERE col2 < col1
)
-- EQUALS [(3,), (4,)]

DROP TABLE tbl

/****************************************
* Strings
****************************************/
-- LIKE vs GLOB:
--   % -> *
--   _ -> ?
--  ASCII case-insensitive
-- === LIKE === --
WITH t(col) AS (VALUES ('A'), ('a'))
SELECT col FROM t WHERE col == 'A';
-- EQUALS [('A',)]
WITH t(col) AS (VALUES ('A'), ('a'), (NULL))
SELECT col FROM t WHERE col LIKE 'A';
-- EQUALS [('A',), ('a', )]
WITH t(col) AS (VALUES ('A'), ('AB'), ('%'), (''), (NULL))
SELECT col FROM t WHERE col LIKE '%';
-- EQUALS [('A',), ('AB',), ('%', ), ('', )]
WITH t(col) AS (VALUES ('A'), ('AB'), ('_'), (''), (NULL))
SELECT col FROM t WHERE col LIKE '_';
-- EQUALS [('A',), ('_',)]
WITH t(col) AS (VALUES ('A'), ('AB'), ('%'), (''), (NULL))
SELECT col FROM t WHERE col LIKE '\%' ESCAPE '\';
-- EQUALS [('%', )]
WITH t(col) AS (VALUES ('A'), ('AB'), ('_'), (''), (NULL))
SELECT col FROM t WHERE col LIKE '\_' ESCAPE '\';
-- EQUALS [('_', )]

-- === GLOB === --
WITH t(col) AS (VALUES ('A'), ('a'), (NULL))
SELECT col FROM t WHERE col GLOB 'A'; -- GLOB is case sensative unlike LIKE
-- EQUALS [('A',)]
WITH t(col) AS (VALUES ('A'), ('AB'), ('*'), (''), (NULL))
SELECT col FROM t WHERE col GLOB '*';
-- EQUALS [('A',), ('AB',), ('*', ), ('', )]
WITH t(col) AS (VALUES ('A'), ('AB'), ('?'), (''), (NULL))
SELECT col FROM t WHERE col GLOB '?';
-- EQUALS [('A',), ('?',)]
WITH t(col) AS (VALUES ('F'), ('f'), (NULL))
SELECT col FROM t WHERE col GLOB '[A-Z]';
-- EQUALS [('F',), ]

-- === COLLATE === --
WITH t(col) AS (VALUES ('A'), ('a'), ('A '))
SELECT col FROM t WHERE col == 'A' COLLATE BINARY;
-- EQUALS [('A',)]
WITH t(col) AS (VALUES ('A'), ('a'), ('A '))
SELECT col FROM t WHERE col == 'A' COLLATE NOCASE;
-- EQUALS [('A',), ('a',)]
WITH t(col) AS (VALUES ('A'), ('a'), ('A '))
SELECT col FROM t WHERE col == 'A' COLLATE RTRIM;
-- EQUALS [('A',), ('A ', )]

-- === || === --
SELECT 'A' || 'BC'
-- EQUALS [('ABC',)]

-- === IN === --
WITH t(col) AS (VALUES ('A'), ('B'), ('C'))
SELECT col FROM t WHERE col IN ('A', 'C', 'D')
-- EQUALS [('A',), ('C', )]


/*******************************************************************************
* CASE (expr) WHEN (expr) THEN (expr) ELSE (expr) END
*******************************************************************************/
WITH t(col) AS (VALUES (1), (2), (3), (NULL))
SELECT
    CASE col % 2
        WHEN 0 THEN 'even'
        WHEN 1 THEN 'odd'
        ELSE 'NaN'
    END
FROM t
-- EQUALS [('odd',), ('even',), ('odd',), ('NaN',)]

/*******************************************************************************
* ordering-term: ORDER BY
*******************************************************************************/
-- ASC, DESC
-- NULLS {FIRST, LAST}
-- COLLATE

/*******************************************************************************
* Aggregating (COUNT, GROUP BY, HAVING)
*******************************************************************************/
CREATE TABLE tbl (
    c_int    INTEGER,
    c_float  REAL,
    c_string TEXT
    -- TODO: DATE, TIME, DATETIME
);
INSERT into tbl(c_int, c_float, c_string)
VALUES (1, 1.5, 'A'),
       (2, 2.5, 'B'),
       (3, 3.5, 'B'),
       (4, 3.5, 'C'),
       (5, 4.5, 'C');

SELECT COUNT(c_float), c_string FROM tbl
GROUP BY c_string
HAVING COUNT(c_float) > 1;
-- EQUALS
-- [(2, 'B'), (2, 'C')]

-- 'bare' columns return undefined result
SELECT COUNT(c_float), c_string FROM tbl;
-- EQUALS
-- [(5, 'A'),]

/*******************************************************************************
* UNSORTED
*******************************************************************************/
-- common-table-expression: RECURSIVE, AS, MATERIALIZED 
-- type casting: CAST
-- functions: arguments, "FILTER ( WHERE expr )", OVER window PARTITION BY
-- raising: RAISE ({IGNORE, ROLLBACK, ABORT, FAIL}, error-message)

/*******************************************************************************
* Modifying (UPDATE, SET, DELETE, DROP)
*******************************************************************************/
-- Update column in specifc row in table
UPDATE tbl
   SET c_int = -1
 WHERE c_string = 'A';

SELECT * FROM tbl;
-- EQUALS
-- [
--     (-1, 1.5, 'A'),
--     (2, 2.5, 'B'),
--     (3, 3.5, 'B'),
--     (4, 3.5, 'C'),
--     (5, 4.5, 'C'),
-- ]

-- TODO: Delete column from table

-- Delet all rows from table
DELETE FROM tbl;

SELECT * FROM tbl;
-- EQUALS
-- []

DROP TABLE tbl;

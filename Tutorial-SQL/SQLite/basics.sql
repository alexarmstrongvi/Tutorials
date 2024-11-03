/*******************************************************************************
* Basic table creation/dropping and datatypes {{{
*******************************************************************************/
CREATE TABLE datatypes (
    c_null NULL,
    c_int  INTEGER, -- i8, i16, i24, i32, i48, or i64
    c_real REAL,    -- f64
    c_text TEXT,    -- UTF8, UTF16BE, or UTF16LE string
    c_blob BLOB     -- hexidecimal
);

INSERT INTO datatypes(c_null, c_int, c_real, c_text, c_blob)
VALUES (NULL, 1,    1.5,  'a',  x'00'),
       (NULL, TRUE, 2.56, 'AB', x'aF'), -- TRUE and FALSE are aliases for 1 and 0
       (NULL, NULL, NULL, NULL, NULL ); -- All columns are nullable

DROP TABLE datatypes;
-- }}}
/*******************************************************************************
* select-core: {{{
*  - SELECT {-, ALL, DISTINCT}
*    - FROM
*    - WHERE
*    - GROUP BY, HAVING
*    - WINDOW, AS (see window-defn)
*  - VALUES
*  - ORDER BY
*  - LIMIT, OFFSET
*
*******************************************************************************/
CREATE TABLE tbl (
    c_int INTEGER,
    c_str TEXT
);
INSERT INTO tbl(c_int, c_str)
VALUES (1, 'A'),
       (2, 'B'),
       (3, 'B'),
       (4, 'C'),
       (5, 'C');


-- Read entire table
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

-- Remove duplicate output
SELECT DISTINCT c_str FROM tbl;
-- EQUALS [('A',), ('B',), ('C',)]

-- Read a table row
SELECT * FROM tbl WHERE c_int = 3;
-- EQUALS [(3, 'B')]

-- Groupby and aggregate
SELECT c_str, sum(c_int) FROM tbl GROUP BY c_str;
-- EQUALS [('A', 1), ('B', 5), ('C', 9)]

-- Sort the output
SELECT c_int FROM tbl ORDER BY c_str DESC;
-- EQUALS [(4,), (5,), (2,), (3,), (1,)]

-- Limit output
SELECT c_int FROM tbl LIMIT 2;
-- EQUALS [(1,), (2,)]
SELECT c_int FROM tbl LIMIT 2 OFFSET 1;
-- EQUALS [(2,), (3,)]
SELECT c_int FROM tbl LIMIT 1, 2; -- Discouraged usage
-- EQUALS [(2,), (3,)]

-- Group and aggegate
SELECT SUM(c_int), COUNT(c_str) FROM tbl;
-- EQUALS [(15, 5),]
SELECT c_str, sum(c_int) FROM tbl GROUP BY c_str HAVING COUNT(c_str) > 1;
-- EQUALS [('B', 5,), ('C', 9,)]

-- 'bare' columns return undefined result
-- SQLite tends to return the first result
SELECT c_str, COUNT(c_int) FROM tbl;
-- EQUALS [('A', 5),]

-- VALUES clause outside of insertion (use case?)
VALUES (1,2), (3,4);
-- EQUALS [(1, 2), (3, 4)]
VALUES (1,2), (3,4,5);
-- RAISES (OperationalError, "all VALUES must have the same number of terms")
SELECT * FROM (VALUES (1, 2), (3, 4)) LIMIT 1;
-- EQUALS [(1, 2)]

DROP TABLE tbl;
-- }}}
/*******************************************************************************
* Operators {{{
*   - Equality    : =  ==  IS ISNULL
*   - Inequality  : !=  <>  IS NOT NOTNULL NOT NULL
*   - Comparison  : <=  <  >  >=  BETWEEN
*   - Logical     : NOT  AND  OR
*   - Binary      : &  |  <<  >>  ~
*   - Existential : EXISTS
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
* Collections: IN
*
* Unary
* + [expr] - No Op
* - [expr]
*
* JSON: ->  ->>
*******************************************************************************/

CREATE TABLE tbl (col INTEGER);

INSERT INTO tbl(col)
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

WITH t(col) AS (VALUES ('A'), ('B'), ('C'))
SELECT col FROM t WHERE col IN ('A', 'C', 'D');
-- EQUALS [('A',), ('C', )]

SELECT col AS col1 FROM tbl WHERE EXISTS (
    SELECT col AS col2 FROM tbl WHERE col2 < col1
);
-- EQUALS [(3,), (4,)]

DROP TABLE tbl;

/****************************************
* Strings
****************************************/
CREATE TABLE tbl (col TEXT);
INSERT INTO tbl
VALUES ('A'), ('a'), ('AB'), ('%'), (''), (NULL);

-- === LIKE and GLOB === --
-- % -> *
-- _ -> ?
-- ASCII case-insensitive -> case-sensative
SELECT col FROM tbl WHERE col == 'A';
-- EQUALS [('A',)]
SELECT col FROM tbl WHERE col LIKE 'A';
-- EQUALS [('A',), ('a', )]
SELECT col FROM tbl WHERE col LIKE '%';
-- EQUALS [('A',), ('a',), ('AB',), ('%', ), ('', )]
SELECT col FROM tbl WHERE col LIKE '_';
-- EQUALS [('A',), ('a',), ('%',)]
SELECT col FROM tbl WHERE col LIKE '\%' ESCAPE '\';
-- EQUALS [('%', )]

SELECT col FROM tbl WHERE col GLOB 'A'; -- GLOB is case sensitive unlike LIKE
-- EQUALS [('A',)]
SELECT col FROM tbl WHERE col GLOB '*';
-- EQUALS [('A',), ('a',), ('AB',), ('%', ), ('', )]
SELECT col FROM tbl WHERE col GLOB '?';
-- EQUALS [('A',), ('a',), ('%',)]
SELECT col FROM tbl WHERE col GLOB '[A-Z]';
-- EQUALS [('A',), ]

DROP TABLE tbl;

-- === COLLATE === --
CREATE TABLE tbl (col TEXT);
INSERT INTO tbl
VALUES ('A'), ('a'), ('A '), (NULL);

SELECT col FROM tbl WHERE col == 'A' COLLATE BINARY;
-- EQUALS [('A',)]
SELECT col FROM tbl WHERE col == 'A' COLLATE NOCASE;
-- EQUALS [('A',), ('a',)]
SELECT col FROM tbl WHERE col == 'A' COLLATE RTRIM;
-- EQUALS [('A',), ('A ', )]

DROP TABLE tbl;

-- === || === --
SELECT 'A' || 'BC';
-- EQUALS [('ABC',)]

-- }}}
/*******************************************************************************
* ordering-term: ORDER BY {{{
*******************************************************************************/
CREATE TABLE tbl (col TEXT);

INSERT INTO tbl(col)
VALUES ('ac'), (NULL), ('Ac'), ('ab');

SELECT col FROM tbl ORDER BY col; -- implicit ASC NULLS FIRST
-- EQUALS [(NULL,), ('Ac',), ('ab',), ('ac',)]
SELECT col FROM tbl ORDER BY col ASC NULLS FIRST;
-- EQUALS [(NULL,), ('Ac',), ('ab',), ('ac',)]
SELECT col FROM tbl ORDER BY col DESC NULLS LAST;
-- EQUALS [('ac',), ('ab',), ('Ac',), (NULL,)]
SELECT col FROM tbl ORDER BY col COLLATE NOCASE;
-- EQUALS [(NULL,), ('ab',), ('ac',), ('Ac',)]

DROP TABLE tbl;
-- }}}
/*******************************************************************************
* CASE (expr) WHEN (expr) THEN (expr) ELSE (expr) END {{{
*******************************************************************************/
WITH t(col) AS (VALUES (1), (2), (3), (NULL))
SELECT
    CASE col % 2
        WHEN 0 THEN 'even'
        WHEN 1 THEN 'odd'
        ELSE 'NaN'
    END
FROM t;
-- EQUALS [('odd',), ('even',), ('odd',), ('NaN',)]

-- }}}
/*******************************************************************************
* compound-operator, compound-select-stmt: UNION, UNION ALL, INTERSECT, EXCEPT {{{
*******************************************************************************/
-- Concatenate tables
-- ALL keeps duplicate rows
VALUES (1, 1), (2, 2)
UNION
VALUES (3, 3), (4, 4);
-- EQUALS [(1,1), (2,2), (3,3), (4,4)]

-- Duplicate rows removed by default. UNION -> set union
VALUES (1, 1), (2, 2)
UNION
VALUES (2, 2), (3, 3);
-- EQUALS [(1,1), (2,2), (3,3)]

-- NULL is equal to NULL when considering duplicate rows
VALUES (NULL)
UNION
VALUES (NULL);
-- EQUALS [(NULL,)]

-- ALL keeps duplicate rows
VALUES (1, 1), (2, 2)
UNION ALL
VALUES (2, 2), (3, 3);
-- EQUALS [(1,1), (2,2), (2,2), (3,3)]

VALUES (1, 1), (2, 2)
INTERSECT
VALUES (2, 2), (3, 3);
-- EQUALS [(2,2)]

VALUES (1, 1), (2, 2)
EXCEPT
VALUES (2, 2), (3, 3);
-- EQUALS [(1,1)]

-- }}}
/*******************************************************************************
* join-clause, join-constraint {{{
* - INNER JOIN vs {LEFT, RIGHT, FULL} OUTER JOIN
* - NATURAL JOIN
* - USING vs AS
* - CROSS JOIN
*******************************************************************************/
CREATE TABLE left (
    c_left INTEGER,
    val    INTEGER
);
CREATE TABLE right (
    c_right TEXT,
    val     INTEGER
);
INSERT INTO left(c_left, val)
VALUES (1, 11),
       (2, 22), (3, 22),
       (4, 33),
       (5, 44);

INSERT INTO right(val, c_right)
VALUES (11, "A"),
       (22, "B"),
       (33, "B"), (33, "C"),
       (55, "D");

-- INNER JOIN (a.k.a. JOIN)
SELECT * FROM left JOIN right USING (val);
-- EQUALS [
--     (1, 11, 'A'),               #  one-to-one
--     (2, 22, 'B'), (3, 22, 'B'), # many-to-one
--     (4, 33, 'B'), (4, 33, 'C'), #  one-to-many
-- ]
SELECT * FROM left INNER JOIN right USING (val)
EXCEPT -- JOIN defaults to INNER JOIN
SELECT * FROM left JOIN right USING (val);
-- EQUALS []

-- FULL OUTER JOIN (a.k.a. FULL JOIN)
SELECT * FROM left FULL JOIN right USING (val)
EXCEPT -- only show columns not part of inner join
SELECT * FROM left JOIN right USING (val);
-- EQUALS [
--     (NULL, 55, 'D'),  # none-to-one
--     (5,    44, NULL), #  one-to-none
-- ]

-- LEFT OUTER JOIN (a.k.a. LEFT JOIN)
SELECT * FROM left LEFT JOIN right USING (val)
EXCEPT -- only show columns not part of inner join
SELECT * FROM left JOIN right USING (val);
-- EQUALS [
--     (5,    44, NULL), #  one-to-none
-- ]

-- RIGHT OUTER JOIN (a.k.a. RIGHT JOIN)
SELECT * FROM left RIGHT JOIN right USING (val)
EXCEPT -- only show columns not part of inner join
SELECT * FROM left JOIN right USING (val);
-- EQUALS [
--     (NULL, 55, 'D'),  # none-to-one
-- ]

-- OUTER JOIN has not default so LEFT, RIGHT, or FULL must be specified
SELECT * FROM left OUTER JOIN right USING (val);
-- RAISES (OperationalError, "unknown join type: OUTER")

-- catersian product when no USING/ON specified. JOIN type is ignored and so
-- a comma can be used.
SELECT COUNT(*) FROM left, right;
-- EQUALS [(25,)]
SELECT COUNT(*) FROM left INNER JOIN right;
-- EQUALS [(25,)]
SELECT COUNT(*) FROM left FULL JOIN right;
-- EQUALS [(25,)]

SELECT * FROM left, right LIMIT 7;
-- EQUALS [
--   (1, 11, 'A', 11),
--   (1, 11, 'B', 22),
--   (1, 11, 'B', 33),
--   (1, 11, 'C', 33),
--   (1, 11, 'D', 55),
--   (2, 22, 'A', 11),
--   (2, 22, 'B', 22),
--   # ... all possible pairs
-- ]

-- NATURAL JOIN: join using shared columns. usable with all join types
SELECT * FROM left NATURAL JOIN right;
-- EQUALS [
--     (1, 11, 'A'),               #  one-to-one
--     (2, 22, 'B'), (3, 22, 'B'), # many-to-one
--     (4, 33, 'B'), (4, 33, 'C'), #  one-to-many
-- ]

-- AS vs USING
SELECT * FROM left JOIN right ON left.val == right.val;

-- Selecting columns
SELECT left.c_left, right.c_right FROM left JOIN right USING (val);
-- EQUALS [
--     (1, 'A'),           #  one-to-one
--     (2, 'B'), (3, 'B'), # many-to-one
--     (4, 'B'), (4, 'C'), #  one-to-many
-- ]

-- CROSS JOIN: different implementation of INNER JOIN that is more efficient in
-- particular cases. Docs discourage premature use of CROSS JOIN
SELECT * FROM left CROSS JOIN right
EXCEPT
SELECT * FROM left, right;
-- EQUALS []
SELECT * FROM left CROSS JOIN right USING (val)
EXCEPT
SELECT * FROM left INNER JOIN right USING (val);
-- EQUALS []

-- }}}
/*******************************************************************************
* TODO common-table-expression: RECURSIVE, AS, MATERIALIZED {{{
*******************************************************************************/
-- }}}
/*******************************************************************************
* Modifying (UPDATE, SET, DELETE, DROP) {{{
*******************************************************************************/
CREATE TABLE tbl (
    c_int    INTEGER,
    c_float  REAL,
    c_string TEXT
);
INSERT INTO tbl(c_int, c_float, c_string)
VALUES (1, 1.5, 'A'),
       (2, 2.5, 'B'),
       (3, 3.5, 'B'),
       (4, 3.5, 'C'),
       (5, 4.5, 'C');

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
-- }}}
/*******************************************************************************
* TODO
*******************************************************************************/
-- type casting: CAST
-- functions: arguments, "FILTER ( WHERE expr )", OVER window PARTITION BY
-- raising: RAISE ({IGNORE, ROLLBACK, ABORT, FAIL}, error-message)
-- result-column (AS)
-- table-or-subquery (AS, INDEXED BY, NOT INDEXED, schema-name)
-- EXPLAIN, EXPLAIN QUERY PLAN

/*******************************************************************************
{{{
vim: set foldmethod=marker: set foldlevel=0
}}}
*******************************************************************************/

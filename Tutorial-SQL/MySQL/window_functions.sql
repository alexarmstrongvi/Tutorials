/*******************************************************************************
* Window functions
* 
* References
*   - MySQL documentation
        - [Window Functions](https://dev.mysql.com/doc/refman/8.0/en/window-functions.html)
*******************************************************************************/

DROP DATABASE IF EXISTS tmp_database;
CREATE DATABASE tmp_database;
USE tmp_database;

CREATE TABLE tbl (
    category TEXT,
    value INTEGER
);

INSERT INTO tbl (category, value)
VALUES ('A', 1),
       ('A', 2),
       ('A', 3),
       ('A', 4),
       ('B', 9),
       ('B', 6),
       ('B', 6),
       ('B', 5);

-- Basics
SELECT
    category,
    value,
    RANK()         OVER(PARTITION BY category ORDER BY value) AS 'RANK',
    DENSE_RANK()   OVER(PARTITION BY category ORDER BY value) AS 'DENSE_RANK',
    PERCENT_RANK() OVER(PARTITION BY category ORDER BY value) AS 'PERCENT_RANK',
    CUME_DIST()    OVER(PARTITION BY category ORDER BY value) AS 'CUME_DIST'
FROM tbl

/*
RANK()	Rank of current row within its partition, with gaps
DENSE_RANK()	Rank of current row within its partition, without gaps
PERCENT_RANK()	Percentage rank value
CUME_DIST()	Cumulative distribution value

-- Within window frame
FIRST_VALUE()	Value of argument from first row of window frame
LAST_VALUE()	Value of argument from last row of window frame
NTH_VALUE()	Value of argument from N-th row of window frame

-- Within partition
ROW_NUMBER()	Number of current row within its partition
LAG()	Value of argument from row lagging current row within partition
LEAD()	Value of argument from row leading current row within partition
NTILE()	Bucket number of current row within its partition.
*/


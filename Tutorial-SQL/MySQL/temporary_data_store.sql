/*******************************************************************************
* Storing table and query results
*  - Derived tables
*  - Subqueries: correlated and uncorrelated
*  - Common table expressions (CTEs): Recursive and non-recursive
*  - Views
*  - Temporary variable
*  - Temporary table: local and global
*  - Permanent table
* 
* See table at bottom of [MSSQLTips.com](https://www.mssqltips.com/sqlservertip/6021/differences-between-sql-server-temp-tables-table-variables-subqueries-derived-tables-ctes-and-physical-tables/)
*******************************************************************************/

SELECT '------------------------------------------' AS '';
SELECT 'Running tutorial on temporary data storage' AS '';
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

/*******************************************************************************
* Derived tables
*******************************************************************************/
SELECT 'Derived Table' AS '';
SELECT *
FROM ( -- derived table
    SELECT col_int, col_string
    FROM tbl
) derived_tbl
WHERE derived_tbl.col_int > 2;

/*******************************************************************************
* Subqueries: correlated and uncorrelated
*******************************************************************************/
SELECT 'Subquery Table' AS '';
SELECT col_int, col_string
FROM tbl
WHERE (col_int, col_string) IN ( -- subquery
    SELECT col_int, col_string
    FROM tbl
    WHERE col_int > 2
);

/*******************************************************************************
* Common table expression 
*
* Use case(s):
*   - Recursive CTE
*   - Temp data needed in multiple parts of following statement
*   - Derived table or subquery would look unreadable
*
* Basic Syntax:
*    WITH cte_name (column_list) AS (
*        query
*    ) 
*    SELECT * FROM cte_name;
*******************************************************************************/
SELECT 'CTE Table' AS '';
WITH -- CTE
    cte_name AS (
        SELECT col_int, col_string
        FROM tbl
        WHERE col_int > 2
    )
SELECT * FROM cte_name;

/*******************************************************************************
* View
*******************************************************************************/

/*******************************************************************************
* Temporary variable
*******************************************************************************/

/*******************************************************************************
* Temporary tables
*******************************************************************************/

/*******************************************************************************
* Permanent table
*******************************************************************************/

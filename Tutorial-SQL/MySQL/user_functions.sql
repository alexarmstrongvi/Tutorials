/*******************************************************************************
* User defined functions
* 
* References
*   - MySQL documentation
        - [CREATE PROCEDURE and CREATE FUNCTION Statements](https://dev.mysql.com/doc/refman/8.0/en/create-procedure.html)
    - mysqltutorial.org
        - [Stored Function](https://www.mysqltutorial.org/mysql-stored-function/)
*******************************************************************************/

DROP DATABASE IF EXISTS tmp_database;
CREATE DATABASE tmp_database;
USE tmp_database;

/*******************************************************************************
* User defined functions
*******************************************************************************/
-- Basics
CREATE FUNCTION hello_world ()
RETURNS TEXT
DETERMINISTIC
    RETURN 'Hello World';

SELECT hello_world ();

SELECT '';
CREATE FUNCTION adder (
    x INT,
    y INT
)
RETURNS INT
DETERMINISTIC
    RETURN x+y;

SELECT adder (1, 2);

-- BEGIN/END, IN/OUT/INOUT, NOT DETERMINISTIC 

/*******************************************************************************
* User defined variables
* 
* References
*   - MySQL documentation
*       - [User-Defined Variables](https://dev.mysql.com/doc/refman/8.0/en/user-variables.html)
*******************************************************************************/

/*******************************************************************************
* Setup test area
*******************************************************************************/
DROP DATABASE IF EXISTS tmp_database;
CREATE DATABASE tmp_database;
USE tmp_database;

CREATE TABLE tbl (
    v INT
);
INSERT INTO tbl (v)
VALUES (4),(4),(5),(20),(11);

SELECT * FROM tbl;

/*******************************************************************************
* Basics
*******************************************************************************/
SET @var1 := 1; 
SELECT @var1;

SET @var2 := @var1 + 1; 
SELECT @var1, @var2;

-- Alternative assignment operators
SET @var1 =  2;
SET @var1 := 2;

-- Allowable names
SET @varname1 := 0;
SET @var_name := 1;
SET @var.name := 2;
SET @var$name := 3;
SET @'var@var!@#$%^&*()_+name' := 4;

SELECT @varname1,
       @var_name,
       @var.name,
       @var$name,
       @'var@var!@#$%^&*()_+name';


-- Create and update variable within SELECT statement (not advised)
SELECT '' AS '';
SET @increment = 0;
SELECT
    @increment := @increment + 1
FROM
    tbl;

-- Data types (CAST)

-- Statements (PREPARE, EXECUTE, DEALLOCATE PREPARE)

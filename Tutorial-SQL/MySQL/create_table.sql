/*******************************************************************************
* Creating tables
* Syntax
    * CREATE TABLE
        CREATE TABLE [IF NOT EXISTS] table_name(
           column_1_definition,
           column_2_definition,
           ...,
           table_constraints
        ) ENGINE=storage_engine;
    * Column definition
        column_name data_type(length) [NOT NULL] [DEFAULT value] [AUTO_INCREMENT] column_constraint;
    * Column constraint
        UNIQUE, CHECK, and PRIMARY KEY
    * Table_constraints
        PRIMARY KEY and FOREIGN KEY
    * Foreign Key
        [CONSTRAINT constraint_name]
        FOREIGN KEY [foreign_key_name] (column_name, ...)
        REFERENCES parent_table(colunm_name,...)
        [ON DELETE reference_option]
        [ON UPDATE reference_option]


* References
*   - MySQL documentation
*******************************************************************************/

DROP DATABASE IF EXISTS tmp_database;
CREATE DATABASE tmp_database;
USE tmp_database;

-- Simplest case for all basic data types
-- nothing is specific unless it has to be
CREATE TABLE tbl_of_all_types (
    -- Exact Numeric types
    c_integer   INTEGER, -- INT
    c_decimal   DECIMAL, -- DEC, FIXED, NUMERIC
    -- Approximate numeric types
    c_float     FLOAT,
    c_double    DOUBLE PRECISION, -- DOUBLE, 
    c_real      REAL, -- DOUBLE or FLOAT depending on REAL_AS_FLOAT mode
    -- Data and time
    c_date      DATE,
    c_time      TIME,
    c_datetime  DATETIME,
    c_timestamp TIMESTAMP,
    c_year      YEAR,
    -- String
    c_char      CHAR,
    c_varchar   VARCHAR(1000),
    c_binary    BINARY,
    c_varbinary VARBINARY(1000),
    -- c_blob      BLOB,
    c_text      TEXT,
    c_enum      ENUM('enum1','enum2'),
    c_set       SET('a','b','c')
);

INSERT INTO tbl_of_all_types
VALUES (1, 1,
        1.0, 1.0, 1.0,
        '2020-01-31', '12:59:59.999', '2020-01-31 12:59:59.999', '2020-01-31 12:59:59.999', '2020',
        '', 'Hello', '', 'Hello', 'Hello', 'enum1', 'a,c,b,b');

SELECT * FROM tbl_of_all_types;

CREATE TABLE tbl_with_options (
    c_primarykey INT AUTO_INCREMENT PRIMARY KEY,
    -- FOREIGN KEY (c_primarykey) REFERENCES tbl_with_options (c_primarykey),
    c_check      INT CHECK (c_check > 0),
    c_unique     INT UNIQUE,
    c_no_null    INT NOT NULL,
    c_default    INT DEFAULT 10
);

SELECT * FROM tbl_with_options;

-- Primary Key


-- Foreign Key

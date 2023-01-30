/*******************************************************************************
* Date and time data types and functionality
* 
* References
*   - MySQL documentation
        - [Date and Time Functions](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html)
        - [Date and Time Literals](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-literals.html)
        - [Temporal Intervals](https://dev.mysql.com/doc/refman/8.0/en/expressions.html#temporal-intervals)
    - mysqltutorial.org
        - []()
*******************************************************************************/

DROP DATABASE IF EXISTS tmp_database;
CREATE DATABASE tmp_database;
USE tmp_database;

-- Data Type (literals)
SELECT
    DATE('2019-12-31'),
    DATE(20191231),
    TIME('23:59:59.1234567'),
    TIME(235959),
    TIMESTAMP('2019-12-31 23:59:59');

-- Extract
-- EXTRACT()	Extract part of a date
SELECT
    YEAR        (NOW()) AS 'Y',
    MONTH       (NOW()) AS 'M',
    DAY         (NOW()) AS 'D', -- DAYOFMONTH
    HOUR        (NOW()) AS 'h',
    MINUTE      (NOW()) AS 'm',
    SECOND      (NOW()) AS 's',
    NOW();

SELECT '';
SELECT
    YEARWEEK   (NOW()) AS 'Y-W',
    WEEKOFYEAR (NOW()) AS 'W of Y',
    WEEK       (NOW()) AS 'W of Y',
    DAYOFYEAR  (NOW()) AS 'D of Y',
    DAYOFWEEK  (NOW()) AS 'D of W', -- [1 = Sunday]
    WEEKDAY    (NOW()) AS 'D of W', -- [0 = Monday]
    DAYNAME    (NOW()) AS 'D',
    NOW();

-- MONTHNAME()	Return the name of the month
-- QUARTER()	Return the quarter from a date argument
-- MICROSECOND (NOW()) AS 'ms',

/*
-- Data Types (non-literals)
DATETIME()

-- Arithmatic
ADDDATE(), DATE_ADD()
ADDTIME()
SUBDATE(), DATE_SUB()	Subtract a time value (interval) from a date
SUBTIME()	Subtract times
DATEDIFF()	Subtract two dates
PERIOD_ADD()	Add a period to a year-month
PERIOD_DIFF()	Return the number of months between periods
TIMEDIFF()	Subtract time
TIMESTAMPADD()	Add an interval to a datetime expression
TIMESTAMPDIFF()	Subtract an interval from a datetime expression

-- Convert and reformat
CONVERT_TZ()	Convert from one time zone to another
FROM_DAYS()	Convert a day number to a date
FROM_UNIXTIME()	Format Unix timestamp as a date
DATE_FORMAT()	Format date as specified
GET_FORMAT()	Return a date format string
MAKEDATE()	Create a date from the year and day of year
MAKETIME()	Create time from hour, minute, second
SEC_TO_TIME()	Converts seconds to 'hh:mm:ss' format
STR_TO_DATE()	Convert a string to a date
TIME_FORMAT()	Format as time
TIME_TO_SEC()	Return the argument converted to seconds
TO_DAYS()	Return the date argument converted to days
TO_SECONDS()	Return the date or datetime argument converted to seconds since Year 0

-- Current time
NOW(), LOCALTIME(), LOCALTIMESTAMP(), CURRENT_TIMESTAMP()
CURRENT_DATE(), CURDATE()
CURRENT_TIME(), CURTIME() 
SYSDATE()	Return the time at which the function executes
UNIX_TIMESTAMP()	Return a Unix timestamp
UTC_TIMESTAMP()	Return the current UTC date and time
UTC_DATE()	Return the current UTC date
UTC_TIME()	Return the current UTC time

-- Lookup
LAST_DAY()	Return the last day of the month for the argument
 */

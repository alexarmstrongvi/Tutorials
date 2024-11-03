/*******************************************************************************
Window functions

Window functions are related to aggregation functions but instead of calculating 
a single value for the entire group, they calculate a value for each entry in 
the group, usually dependent on the other values in the group:
    - AGG_FUNC(grp) -> val for whole group
    - WINDOW_FUNC(x, grp) -> val for each entry in group

I simple example would be normalizing a column by the mean and stddev but doing
so separately for each group.

Given that window functions depend on entries and their corresponding group, 
there are many more ways to specify that group compared to aggregate functions.
While groups for aggregate functions must partition a table, window functions
can be defined relative to each entry considered. A common example would be finding
the difference between each line and the preceding line. In this case the
"group" would be the entry and the preceding entry. This leads to groups that
overlap but that is not a problem.
*******************************************************************************/

/*******************************************************************************
* Basics {{{
*******************************************************************************/
CREATE TABLE tbl (
    grp TEXT,
    val INTEGER
);
INSERT INTO tbl(grp, val)
VALUES ('A', 1),
       ('A', 2),
       ('B', 3),
       ('B', 4),
       ('B', 5);

-- Default window leads to aggregation function over all rows
SELECT SUM(val) OVER () FROM tbl;
-- EQUALS [
--    (15,),
--    (15,),
--    (15,),
--    (15,),
--    (15,),
-- ]

-- Specifiying grouping via PARTITION BY causes window functions to be applied
-- separately to each group.
SELECT grp, SUM(val) OVER (PARTITION BY grp) FROM tbl;
-- EQUALS [
--    ('A', 3,),
--    ('A', 3,),
--    ('B', 12,),
--    ('B', 12,),
--    ('B', 12,),
-- ]

-- Using only PARTITION BY reduces to GROUP BY though the result is duplicated
-- for each row
SELECT grp, SUM(val) OVER (PARTITION BY grp) FROM tbl
EXCEPT
SELECT grp, SUM(val) FROM tbl GROUP BY grp;
-- EQUALS []

-- Specifiying order changes window for aggregation functions to be current row 
-- and all previous rows
SELECT 
    FIRST_VALUE(val) OVER win, 
    LAST_VALUE(val)  OVER win, 
    SUM(val)         OVER win,
    LAG(val)         OVER win,
    LEAD(val)        OVER win
FROM tbl
WINDOW win AS (ORDER BY val); -- assigns window name for reuse above
-- EQUALS [
--    (1, 1, 1,  NULL, 2),
--    (1, 2, 3,  1,    3),
--    (1, 3, 6,  2,    4),
--    (1, 4, 10, 3,    5),
--    (1, 5, 15, 4,    NULL),
-- ]

-- Combining partitioning and ordering
SELECT 
    grp,
    FIRST_VALUE(val) OVER win, 
    LAST_VALUE(val)  OVER win, 
    SUM(val)         OVER win,
    LAG(val)         OVER win,
    LEAD(val)        OVER win
FROM tbl
WINDOW win AS (PARTITION BY grp ORDER BY val);
-- EQUALS [
--    ('A', 1, 1, 1,  NULL, 2),
--    ('A', 1, 2, 3,  1,    NULL),
--    ('B', 3, 3, 3,  NULL, 4),
--    ('B', 3, 4, 7,  3,    5),
--    ('B', 3, 5, 12, 4,    NULL),
-- ]


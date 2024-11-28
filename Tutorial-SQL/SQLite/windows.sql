/*******************************************************************************
Window frames and functions

Window functions are related to aggregation functions but instead of calculating
a single value for the entire group, they calculate a value for each entry in
the group, usually dependent on the other values in the group:
    - AGG_FUNC(grp) -> val for whole group
    - WINDOW_FUNC(x, grp) -> val for each entry in group

A simple example would be normalizing a column by the mean and stddev but doing
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
* Basics: OVER (PARTITION BY expr ORDER BY ordering-term) {{{
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

-- Default window includes all rows for each input row
SELECT SUM(val) OVER () FROM tbl;
-- EQUALS [
--    (15,),
--    (15,),
--    (15,),
--    (15,),
--    (15,),
-- ]

-- Grouping via PARTITION BY makes the window include all rows in
-- same partition as the input row
SELECT grp, SUM(val) OVER (PARTITION BY grp) FROM tbl;
-- EQUALS [
--    ('A', 3,),
--    ('A', 3,),
--    ('B', 12,),
--    ('B', 12,),
--    ('B', 12,),
-- ]

-- In this way, using only PARTITION BY reduces to GROUP BY though the result is
-- duplicated for each row
SELECT grp, SUM(val) OVER (PARTITION BY grp) FROM tbl
EXCEPT
SELECT grp, SUM(val) FROM tbl GROUP BY grp;
-- EQUALS []

-- Specifiying order makes the window include all rows up to and including the
-- input row.
-- Ordering is required for many of the window functions to make sense (i.e. not
-- involve undefined behavior).
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

-- Combining partitioning and ordering restricts the ordering behavior to the
-- partitions.
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

DROP TABLE tbl;

-- }}}
/*******************************************************************************
* filter-clause {{{
*******************************************************************************/
CREATE TABLE tbl (
    col INTEGER
);
INSERT INTO tbl(col)
VALUES (1), (4), (5), (2), (3);

SELECT
    group_concat(col,'') FILTER (WHERE mod(col,2) != 0) OVER win
FROM tbl
WINDOW win AS (ORDER BY col);
-- EQUALS [('1',), ('1',), ('13',), ('13',), ('135',)]


DROP TABLE tbl;
-- }}}
/*******************************************************************************
* frame-spec {{{
* - The frame-spec controls for each input row which rows from the corresponding
*   partition are included in the window frame
*******************************************************************************/
CREATE TABLE tbl (
    grp TEXT,
    a INTEGER,
    b INTEGER
);
INSERT INTO tbl(grp, a, b)
VALUES ('A', 1, 1),
       ('A', 2, 1),
       ('B', 3, 3),
       ('B', 4, 3),
       ('B', 5, 6),
       ('C', 6, 6);

-- The default frame-spec is
--      RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW EXCLUDE NO OTHERS
-- which, as demoed before, means a frame includes the range of rows up to and
-- include the current row with no exclusions
SELECT group_concat(a,'') OVER win FROM tbl
WINDOW win AS (ORDER BY a RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW EXCLUDE NO OTHERS)

UNION -- drop EXCLUDE NO OTHERS
SELECT group_concat(a,'') OVER win FROM tbl
WINDOW win AS (ORDER BY a RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)

UNION -- drop RANGE * AND CURRENT ROW
SELECT group_concat(a,'') OVER win FROM tbl
WINDOW win AS (ORDER BY a RANGE UNBOUNDED PRECEDING)

EXCEPT -- drop frame-spec
SELECT group_concat(a,'') OVER win FROM tbl
WINDOW win AS (ORDER BY a);
-- EQUALS []

-- CURRENT ROW
-- {N, UNBOUNDED} {PRECEDING, FOLLOWING}
-- BETWEEN ... AND ..
SELECT group_concat(a,'') OVER win FROM tbl
WINDOW win AS (ORDER BY a RANGE UNBOUNDED PRECEDING);
-- EQUALS [('1',),('12',),('123',),('1234',), ('12345',), ('123456',)]
SELECT group_concat(a,'') OVER win FROM tbl
WINDOW win AS (ORDER BY a RANGE 1 PRECEDING);
-- EQUALS [('1',),('12',),('23',),('34',),('45',),('56',)]
SELECT group_concat(a,'') OVER win FROM tbl
WINDOW win AS (ORDER BY a RANGE CURRENT ROW);
-- EQUALS [('1',),('2',),('3',),('4',),('5',),('6',)]

SELECT group_concat(a,'') OVER win FROM tbl
WINDOW win AS (ORDER BY a RANGE BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING);
-- EQUALS [('123456',),('23456',),('3456',),('456',), ('56',), ('6',)]
SELECT group_concat(a,'') OVER win FROM tbl
WINDOW win AS (ORDER BY a RANGE BETWEEN 1 FOLLOWING AND 2 FOLLOWING);
-- EQUALS [('23',),('34',),('45',),('56',), ('6',), (NULL,)]


-- ROWS vs GROUPS vs RANGE
SELECT group_concat(a,'') over win, group_concat(b,'') OVER win FROM tbl
WINDOW win AS (ORDER BY b RANGE 2 PRECEDING); -- b in [b-2, b]
-- EQUALS [
--    ('12',   '11'),
--    ('12',   '11'),
--    ('1234', '1133'),
--    ('1234', '1133'),
--    ('56',   '66'),
--    ('56',   '66'),
-- ]
SELECT group_concat(a,'') over win, group_concat(b,'') OVER win FROM tbl
WINDOW win AS (ORDER BY b ROWS 2 PRECEDING); -- row_num in [row_num-2, row_num]
-- EQUALS [
--    ('1',   '1'),
--    ('12',  '11'),
--    ('123', '113'),
--    ('234', '133'),
--    ('345', '336'),
--    ('456', '366'),
-- ]
SELECT group_concat(a,'') over win, group_concat(b,'') OVER win FROM tbl
WINDOW win AS (ORDER BY b GROUPS 2 PRECEDING); -- grp_num in [grp_num-2, grp_num]
-- EQUALS [
--    ('12',     '11'),
--    ('12',     '11'),
--    ('1234',   '1133'),
--    ('1234',   '1133'),
--    ('123456', '113366'),
--    ('123456', '113366'),
-- ]

-- EXCLUDE {NO OTHERS, CURRENT ROW, GROUP, TIES}
SELECT group_concat(a,'') over win, group_concat(b,'') OVER win FROM tbl
WINDOW win AS (ORDER BY b RANGE 2 PRECEDING EXCLUDE NO OTHERS);
-- EQUALS [
--    ('12',   '11'),
--    ('12',   '11'),
--    ('1234', '1133'),
--    ('1234', '1133'),
--    ('56',   '66'),
--    ('56',   '66'),
-- ]
SELECT group_concat(a,'') over win, group_concat(b,'') OVER win FROM tbl
WINDOW win AS (ORDER BY b RANGE 2 PRECEDING EXCLUDE CURRENT ROW);
-- EQUALS [
--    ('2',   '1'),
--    ('1',   '1'),
--    ('124', '113'),
--    ('123', '113'),
--    ('6',   '6'),
--    ('5',   '6'),
-- ]
SELECT group_concat(a,'') over win, group_concat(b,'') OVER win FROM tbl
WINDOW win AS (ORDER BY b RANGE 2 PRECEDING EXCLUDE GROUP);
-- EQUALS [
--    (NULL, NULL),
--    (NULL, NULL),
--    ('12', '11'),
--    ('12', '11'),
--    (NULL, NULL),
--    (NULL, NULL),
-- ]
SELECT group_concat(a,'') over win, group_concat(b,'') OVER win FROM tbl
WINDOW win AS (ORDER BY b RANGE 2 PRECEDING EXCLUDE TIES);
-- EQUALS [
--    ('1',   '1'),
--    ('2',   '1'),
--    ('123', '113'),
--    ('124', '113'),
--    ('5',   '6'),
--    ('6',   '6'),
-- ]
DROP TABLE tbl;


-- }}}
/*******************************************************************************
* Window functions {{{
*******************************************************************************/
-- functions

-- row_number(), rank(), dense_rank(), percent_rank() and cume_dist()

-- ntile(N)

-- lag(expr, offset, default)
-- lead(expr, offset, default)
-- first_value(expr)
-- last_value(expr)
-- nth_value(expr, N)

-- }}}
/*******************************************************************************
{{{
vim: set foldmethod=marker: set foldlevel=0
}}}
*******************************************************************************/

